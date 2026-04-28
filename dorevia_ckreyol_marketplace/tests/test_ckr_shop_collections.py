# -*- coding: utf-8 -*-
"""Tests automatisés — Porte **Collections** V1 (PV + spec).

Référence : **RC-01 … RC-14** dans ``docs/mvp_01/PV_RECETTE_COLLECTIONS_V1.md``,
``SPEC_IMPL_COLLECTIONS.md`` (§12), ``CONTRAT_URL_COLLECTIONS.md``.

Chaque méthode correspond à la colonne *Couverture auto associée* du PV
(**noms verrouillés** : ``TestCkrCollectionsPVModel.*`` /
``TestCkrCollectionsPVHttp.*`` — renommer uniquement avec mise à jour
du PV).

État courant (module **19.0.1.6.0** — étape 3 checklist §13 livrée) :

* ``TestCkrCollectionsPVModel`` : **RC-01**, **RC-02**, **RC-03** (×4,
  dont **visibilité Active + période**) et **RC-14 priorité** :
  **tous implémentés** (``_ckr_effective_mode`` désormais câblé dans
  ``controllers/website_sale_ckr.py``).
* ``TestCkrCollectionsPVHttp`` : **tous implémentés** — vues générale /
  unitaire / union (S1), 301 de normalisation, 302 de repli (A), flash
  session one-shot sans ``ckr_notice`` en query, canonical self, état
  vide §12 A, fiche produit, non-régression portes livrées.

Tests de **support logique** (non rattachés au PV) :

* normalisation / résolution des slugs par ``_ckr_resolve_visible_slugs``
  (ordre d'apparition, déduplication, filtrage visibilité) ;
* contrainte de bornes de dates (``date_start <= date_end``).

Exécution ciblée (exemple) ::

    odoo -d <base> --test-enable --stop-after-init \\
        --test-tags=dorevia_ckr_collections

Tag ``post_install`` : dépend de ``website_sale``, du modèle CK
``ckr.shop.collection`` (étape 1) et du contrôleur public Collections
(étape 3 — routes ``/collections[/…]``, hooks, bandeaux).
"""
import html
import re
from datetime import date, timedelta
from urllib.parse import urlparse, parse_qs

from psycopg2 import IntegrityError

from odoo.addons.dorevia_ckreyol_marketplace.controllers.website_sale_ckr import (
    CKR_COLLECTION_FLASH_SESSION_KEY,
    CKR_MODE_COLLECTION,
    CKR_MODE_FEATURED,
    CKR_MODE_ORIGIN,
    CKR_MODE_PACK,
    CKR_MODE_PARAM,
    CKR_MODE_PRIORITY,
    CKR_MODE_PROMO,
    _ckr_effective_mode,
)
from odoo.exceptions import ValidationError
from odoo.tests import tagged
from odoo.tests.common import HttpCase, TransactionCase


@tagged("post_install", "-at_install", "dorevia_ckr_collections")
class TestCkrCollectionsPVModel(TransactionCase):
    """RC-01, RC-02, RC-03 (slug, unicité, menus, visibilité Active + période), RC-14.

    Contraintes **model-level** figées par le cadrage et la spec :

    * slug unique par site (SQL) ;
    * slug ``union`` réservé (Python, [CONTRAT §4.6]) ;
    * visibilité navigation = ``active`` ∧ fenêtre ``date_start`` /
      ``date_end`` inclusivement (``at_date`` paramétrable sur les
      helpers ``_ckr_visible_domain`` / ``_ckr_is_visible`` /
      ``_ckr_resolve_visible_slugs``) ;
    * cohérence des bornes ``date_start <= date_end`` ;
    * priorité ``_ckr_effective_mode()`` figée (SPEC §5.1).
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.website = cls.env.ref("website.default_website")
        cls.Collection = cls.env["ckr.shop.collection"]
        # Date de référence fixée pour la déterminisme des tests
        # de fenêtre de validité (RC-03). On choisit un jour « au
        # milieu de l'année » pour laisser de la marge de +/- 30 j.
        cls.today = date(2026, 6, 15)

    # ------------------------------------------------------------------
    # RC-01 — fiche produit BO (champ collections)
    # ------------------------------------------------------------------
    def test_ckr_col_rc01_form_view_contains_collection_field(self):
        """RC-01 : la vue formulaire produit expose ``ckr_collection_ids``."""
        view = self.env.ref(
            "dorevia_ckreyol_marketplace.product_template_form_view_ckr_collection"
        )
        self.assertIn("ckr_collection_ids", view.arch)

    # ------------------------------------------------------------------
    # RC-02 — multi-collections sur produit (inverse M2M persisté)
    # ------------------------------------------------------------------
    def test_ckr_col_rc02_product_template_multi_collections(self):
        """RC-02 : un produit peut appartenir à **plusieurs** collections.

        Écriture via le champ **inverse** ``product.template.ckr_collection_ids``
        puis relecture : la table de liaison partagée doit rendre la
        relation symétriquement côté ``ckr.shop.collection``.
        """
        col_a = self.Collection.create(
            {
                "name": "RC-02 Collection A",
                "slug": "rc02-col-a",
                "website_id": self.website.id,
            }
        )
        col_b = self.Collection.create(
            {
                "name": "RC-02 Collection B",
                "slug": "rc02-col-b",
                "website_id": self.website.id,
            }
        )
        tmpl = self.env["product.template"].create(
            {
                "name": "CKR RC-02 Produit multi-collections",
                "type": "consu",
                "sale_ok": True,
                "website_published": True,
            }
        )
        tmpl.ckr_collection_ids = [(6, 0, [col_a.id, col_b.id])]
        tmpl.invalidate_recordset()
        self.assertEqual(
            set(tmpl.ckr_collection_ids.ids),
            {col_a.id, col_b.id},
            "L'inverse M2M ckr_collection_ids doit contenir les 2 collections.",
        )
        self.assertIn(
            tmpl,
            col_a.product_template_ids,
            "Le forward M2M côté ckr.shop.collection doit voir le produit.",
        )
        self.assertIn(
            tmpl,
            col_b.product_template_ids,
            "Le forward M2M côté ckr.shop.collection doit voir le produit.",
        )
        self.assertEqual(col_a.product_template_count, 1)
        self.assertEqual(col_b.product_template_count, 1)

    # ------------------------------------------------------------------
    # RC-03 — ``ckr.shop.collection`` : slug, union, unicité, menus, visibilité
    # ------------------------------------------------------------------
    def test_ckr_col_rc03_slug_reserved_union(self):
        """RC-03 : ``slug='union'`` est **réservé** (contrat §4.6).

        Couvre aussi les slugs invalides (format / vide) : une seule
        méthode suffit pour verrouiller la contrainte de normalisation
        côté Python (regex + set réservé).
        """
        # Slug réservé « union »
        with self.assertRaises(ValidationError):
            self.Collection.create(
                {
                    "name": "RC-03 Union interdit",
                    "slug": "union",
                    "website_id": self.website.id,
                }
            )
        # Slug majuscule → regex rejette
        with self.assertRaises(ValidationError):
            self.Collection.create(
                {
                    "name": "RC-03 Majuscules",
                    "slug": "MAJUSCULE",
                    "website_id": self.website.id,
                }
            )
        # Slug vide → regex rejette (chaîne stripée)
        with self.assertRaises(ValidationError):
            self.Collection.create(
                {
                    "name": "RC-03 Vide",
                    "slug": "   ",
                    "website_id": self.website.id,
                }
            )
        # Slug correct → création accepte
        rec = self.Collection.create(
            {
                "name": "RC-03 OK",
                "slug": "rc03-ok",
                "website_id": self.website.id,
            }
        )
        self.assertTrue(rec.exists())

    def test_ckr_col_rc03_slug_unique_per_website(self):
        """RC-03 : unicité SQL ``(website_id, slug)``."""
        self.Collection.create(
            {
                "name": "RC-03 Uniq A",
                "slug": "rc03-uniq-slug",
                "website_id": self.website.id,
            }
        )
        with self.cr.savepoint(), self.assertRaises(IntegrityError):
            self.Collection.create(
                {
                    "name": "RC-03 Uniq B",
                    "slug": "rc03-uniq-slug",
                    "website_id": self.website.id,
                }
            )

    def test_ckr_col_rc03_menus_and_action_exist(self):
        """RC-03 : menus back-office et action window présents (deux branches)."""
        self.env.ref(
            "dorevia_ckreyol_marketplace.menu_ckreyol_configuration_collections"
        )
        self.env.ref(
            "dorevia_ckreyol_marketplace.menu_ckreyol_catalog_collections"
        )
        self.env.ref(
            "dorevia_ckreyol_marketplace.action_ckr_shop_collection"
        )

    def test_ckr_col_rc03_visibility_active_and_period(self):
        """RC-03 / SPEC §12.2 T3 : visible ssi **Active** ∧ fenêtre date.

        **Bornes inclusives** (MOA 2026-04-22) :

        * sans ``date_start`` / ``date_end`` : toujours visible (si actif) ;
        * ``date_start = today`` : **visible** (borne incluse) ;
        * ``date_end = today`` : **visible** (borne incluse) ;
        * ``date_start > today`` : **non visible** (à venir) ;
        * ``date_end < today`` : **non visible** (expirée) ;
        * ``active = False`` : **non visible** quelle que soit la fenêtre.
        """
        today = self.today
        j_minus_30 = today - timedelta(days=30)
        j_plus_30 = today + timedelta(days=30)

        # Cas de référence : aucune borne → visible si actif.
        col_always = self.Collection.create(
            {
                "name": "RC-03 Always",
                "slug": "rc03-vis-always",
                "website_id": self.website.id,
            }
        )
        self.assertTrue(col_always._ckr_is_visible(self.website, today))

        # Fenêtre encadrante → visible.
        col_in = self.Collection.create(
            {
                "name": "RC-03 In period",
                "slug": "rc03-vis-in",
                "website_id": self.website.id,
                "date_start": j_minus_30,
                "date_end": j_plus_30,
            }
        )
        self.assertTrue(col_in._ckr_is_visible(self.website, today))

        # Bornes inclusives (start = today, end = today).
        col_boundary = self.Collection.create(
            {
                "name": "RC-03 Boundary",
                "slug": "rc03-vis-boundary",
                "website_id": self.website.id,
                "date_start": today,
                "date_end": today,
            }
        )
        self.assertTrue(col_boundary._ckr_is_visible(self.website, today))

        # Fenêtre future → non visible.
        col_upcoming = self.Collection.create(
            {
                "name": "RC-03 Upcoming",
                "slug": "rc03-vis-upcoming",
                "website_id": self.website.id,
                "date_start": j_plus_30,
            }
        )
        self.assertFalse(col_upcoming._ckr_is_visible(self.website, today))

        # Fenêtre expirée → non visible.
        col_expired = self.Collection.create(
            {
                "name": "RC-03 Expired",
                "slug": "rc03-vis-expired",
                "website_id": self.website.id,
                "date_end": j_minus_30,
            }
        )
        self.assertFalse(col_expired._ckr_is_visible(self.website, today))

        # Archivée → non visible quelle que soit la fenêtre.
        col_archived = self.Collection.create(
            {
                "name": "RC-03 Archived",
                "slug": "rc03-vis-archived",
                "website_id": self.website.id,
                "active": False,
            }
        )
        self.assertFalse(col_archived._ckr_is_visible(self.website, today))

        # Cohérence avec le domaine ORM ``_ckr_visible_domain`` : la
        # recherche doit retourner exactement les enregistrements
        # jugés visibles record-wise.
        domain = self.Collection._ckr_visible_domain(
            website=self.website, at_date=today
        )
        # Filtrer sur nos slugs RC-03 pour ne pas dépendre d'autres
        # collections hypothétiques chargées par d'autres tests.
        domain = [("slug", "like", "rc03-vis-")] + domain
        visible = self.Collection.search(domain)
        expected = {col_always, col_in, col_boundary}
        self.assertEqual(
            set(visible),
            expected,
            "Le domaine ORM doit renvoyer exactement les collections "
            "actives et dans la fenêtre, bornes incluses.",
        )

    # ------------------------------------------------------------------
    # RC-14 — priorité ``_ckr_effective_mode()`` (sans HTTP, SPEC §5.1)
    # ------------------------------------------------------------------
    def test_ckr_col_rc14_effective_mode_priority(self):
        """RC-14 modèle : ``pack > promo > featured > origin > collection`` figée.

        Vérification triple :

        1. la constante ``CKR_MODE_PRIORITY`` expose l'ordre figé
           (``collection`` **en dernier** — non-régression absolue) ;
        2. ``_ckr_effective_mode`` sur multi-valeurs respecte la
           priorité (pack > promo > featured > origin > collection) ;
        3. ``collection`` est bien lu quand il est seul — confirme
           son ajout à ``CKR_MODES_ALLOWED``.
        """
        self.assertEqual(
            CKR_MODE_PRIORITY,
            (
                CKR_MODE_PACK,
                CKR_MODE_PROMO,
                CKR_MODE_FEATURED,
                CKR_MODE_ORIGIN,
                CKR_MODE_COLLECTION,
            ),
            "L'ordre CKR_MODE_PRIORITY doit être figé pack > promo > "
            "featured > origin > collection (SPEC_IMPL §5.1 / SPEC §4.6).",
        )
        # Multi-modes → la priorité figée s'applique
        self.assertEqual(
            _ckr_effective_mode(
                {CKR_MODE_PARAM: [CKR_MODE_COLLECTION, CKR_MODE_ORIGIN]}
            ),
            CKR_MODE_ORIGIN,
            "origin doit l'emporter sur collection (collection en dernier).",
        )
        self.assertEqual(
            _ckr_effective_mode(
                {CKR_MODE_PARAM: [CKR_MODE_COLLECTION, CKR_MODE_PACK]}
            ),
            CKR_MODE_PACK,
            "pack l'emporte sur tous les autres modes.",
        )
        self.assertEqual(
            _ckr_effective_mode(
                {CKR_MODE_PARAM: [CKR_MODE_COLLECTION, CKR_MODE_PROMO]}
            ),
            CKR_MODE_PROMO,
            "promo l'emporte sur collection.",
        )
        self.assertEqual(
            _ckr_effective_mode(
                {CKR_MODE_PARAM: [CKR_MODE_COLLECTION, CKR_MODE_FEATURED]}
            ),
            CKR_MODE_FEATURED,
            "featured doit l'emporter sur collection.",
        )
        self.assertEqual(
            _ckr_effective_mode(
                {CKR_MODE_PARAM: [CKR_MODE_FEATURED, CKR_MODE_ORIGIN]}
            ),
            CKR_MODE_FEATURED,
            "featured doit l'emporter sur origin.",
        )
        self.assertEqual(
            _ckr_effective_mode(
                {CKR_MODE_PARAM: [CKR_MODE_PROMO, CKR_MODE_FEATURED]}
            ),
            CKR_MODE_PROMO,
            "promo l'emporte sur featured.",
        )
        self.assertEqual(
            _ckr_effective_mode(
                {
                    CKR_MODE_PARAM: [
                        CKR_MODE_COLLECTION,
                        CKR_MODE_ORIGIN,
                        CKR_MODE_FEATURED,
                        CKR_MODE_PROMO,
                        CKR_MODE_PACK,
                    ]
                }
            ),
            CKR_MODE_PACK,
            "pack l'emporte en cas de cumul complet des modes whitelistés.",
        )
        # collection seule → reconnue (ajoutée à CKR_MODES_ALLOWED)
        self.assertEqual(
            _ckr_effective_mode({CKR_MODE_PARAM: CKR_MODE_COLLECTION}),
            CKR_MODE_COLLECTION,
            "collection doit être lisible quand aucun autre mode "
            "whitelisté n'est présent.",
        )

    # ------------------------------------------------------------------
    # Tests logique support (hors PV — défense helpers modèle)
    # ------------------------------------------------------------------
    def test_resolve_visible_slugs_order_and_filter(self):
        """``_ckr_resolve_visible_slugs`` : ordre d'apparition + visibilité.

        Préserve l'ordre d'apparition des slugs d'entrée (après
        déduplication) — nécessaire pour que le contrôleur compare
        l'URL reçue à la forme canonique triée et décide du 301
        (SPEC_IMPL §3.3). Les slugs inconnus / non visibles sont
        **ignorés** silencieusement — le repli 302 (option A) est à
        la charge du contrôleur.
        """
        today = self.today
        col_z = self.Collection.create(
            {
                "name": "Resolve Z",
                "slug": "resolve-z",
                "website_id": self.website.id,
            }
        )
        col_a = self.Collection.create(
            {
                "name": "Resolve A",
                "slug": "resolve-a",
                "website_id": self.website.id,
            }
        )
        # Collection expirée : doit être filtrée par visibilité.
        self.Collection.create(
            {
                "name": "Resolve Expired",
                "slug": "resolve-expired",
                "website_id": self.website.id,
                "date_end": today - timedelta(days=1),
            }
        )
        ordered = self.Collection._ckr_resolve_visible_slugs(
            # doublons + inconnus + expirée mélangés
            ["resolve-z", "resolve-a", "resolve-z", "inconnu", "resolve-expired"],
            website=self.website,
            at_date=today,
        )
        self.assertEqual(
            [c.id for c in ordered],
            [col_z.id, col_a.id],
            "Ordre d'apparition préservé, doublons et invalides filtrés.",
        )

    def test_date_range_consistency_constraint(self):
        """``date_start > date_end`` → ``ValidationError`` (défense modèle)."""
        with self.assertRaises(ValidationError):
            self.Collection.create(
                {
                    "name": "Range invalide",
                    "slug": "range-invalid",
                    "website_id": self.website.id,
                    "date_start": date(2026, 12, 31),
                    "date_end": date(2026, 1, 1),
                }
            )


@tagged("post_install", "-at_install", "dorevia_ckr_collections")
class TestCkrCollectionsPVHttp(HttpCase):
    """RC-04 … RC-13 + RC-14 HTTP (requêtes HTTP / non-régression portes).

    **Patron de données** (setUpClass) :

    * **A** (``http-col-a``) — visible, 1 produit rattaché exclusif ;
    * **B** (``http-col-b``) — visible, 1 produit rattaché exclusif ;
    * **C** (``http-col-c``) — visible, 0 produit rattaché (état
      vide §12 A pour RC-11) ;
    * **D** (``http-col-d``) — archivée (active=False), 1 produit ;
    * **E** (``http-col-e``) — expirée, 1 produit.

    Tous les produits sont publiés. Le produit non rattaché
    (``http-col-lonely``) sert de témoin d'exclusion sur la vue
    générale (« exclusion des produits hors collections »).
    """

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.website = cls.env.ref("website.default_website")
        Collection = cls.env["ckr.shop.collection"]
        Template = cls.env["product.template"]
        today = date.today()
        j_minus_30 = today - timedelta(days=30)

        cls.product_a = Template.create(
            {
                "name": "CKR HTTP Collection A Produit",
                "type": "consu",
                "sale_ok": True,
                "website_published": True,
            }
        )
        cls.product_b = Template.create(
            {
                "name": "CKR HTTP Collection B Produit",
                "type": "consu",
                "sale_ok": True,
                "website_published": True,
            }
        )
        cls.product_d = Template.create(
            {
                "name": "CKR HTTP Collection D Produit",
                "type": "consu",
                "sale_ok": True,
                "website_published": True,
            }
        )
        cls.product_e = Template.create(
            {
                "name": "CKR HTTP Collection E Produit",
                "type": "consu",
                "sale_ok": True,
                "website_published": True,
            }
        )
        cls.product_lonely = Template.create(
            {
                "name": "CKR HTTP Produit sans collection",
                "type": "consu",
                "sale_ok": True,
                "website_published": True,
            }
        )

        cls.col_a = Collection.create(
            {
                "name": "Sélection A HTTP",
                "slug": "http-col-a",
                "website_id": cls.website.id,
                "product_template_ids": [(6, 0, [cls.product_a.id])],
            }
        )
        cls.col_b = Collection.create(
            {
                "name": "Sélection B HTTP",
                "slug": "http-col-b",
                "website_id": cls.website.id,
                "product_template_ids": [(6, 0, [cls.product_b.id])],
            }
        )
        cls.col_c_empty = Collection.create(
            {
                "name": "Sélection vide HTTP",
                "slug": "http-col-c",
                "website_id": cls.website.id,
            }
        )
        cls.col_d_archived = Collection.create(
            {
                "name": "Sélection archivée HTTP",
                "slug": "http-col-d",
                "website_id": cls.website.id,
                "active": False,
                "product_template_ids": [(6, 0, [cls.product_d.id])],
            }
        )
        cls.col_e_expired = Collection.create(
            {
                "name": "Sélection expirée HTTP",
                "slug": "http-col-e",
                "website_id": cls.website.id,
                "date_end": j_minus_30,
                "product_template_ids": [(6, 0, [cls.product_e.id])],
            }
        )

    # ------------------------------------------------------------------
    # Helpers HTTP (inspirés de test_ckr_shop_origins — parité patron)
    # ------------------------------------------------------------------
    def _assert_redirect(self, path, expected_code, location_substr=None):
        resp = self.url_open(path, allow_redirects=False, timeout=60)
        self.assertEqual(
            resp.status_code,
            expected_code,
            "%s → attendu %s, obtenu %s" % (path, expected_code, resp.status_code),
        )
        if location_substr is not None:
            loc = resp.headers.get("Location", "")
            self.assertIn(
                location_substr,
                loc,
                "Location inattendue pour %s : %r" % (path, loc),
            )
        return resp

    def _canonical_href(self, html_text):
        m = re.search(
            r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']+)["\']',
            html_text,
            re.I,
        )
        self.assertTrue(m, "Balise canonical absente du HTML.")
        return html.unescape(m.group(1))

    # --- RC-04 — ``GET /collections`` ---

    def test_ckr_col_rc04_general_view_200_and_copy(self):
        """RC-04 : vue générale 200 + copy bandeau §8 + exclusion lonely.

        La vue générale doit inclure les produits rattachés à **au moins
        une** collection **visible** (A et B) et **exclure** les produits
        sans collection (``product_lonely``) ou rattachés uniquement à
        des collections non visibles (archivée D, expirée E).
        """
        resp = self.url_open("/collections", timeout=60)
        self.assertEqual(resp.status_code, 200)
        text = resp.text
        # Copy §8 figée MOA 2026-04-22
        self.assertIn("Découvrez les collections actuellement disponibles.", text)
        # Les produits des collections visibles apparaissent
        self.assertIn(self.product_a.name, text)
        self.assertIn(self.product_b.name, text)
        # Le produit sans collection n'apparaît pas
        self.assertNotIn(self.product_lonely.name, text)
        # Les produits des collections non visibles (D archivée, E expirée)
        # n'apparaissent pas non plus
        self.assertNotIn(self.product_d.name, text)
        self.assertNotIn(self.product_e.name, text)

    # --- RC-05 — vue unitaire ---

    def test_ckr_col_rc05_single_collection_view_title_and_fallback(self):
        """RC-05 : ``/collections/<slug_A>`` 200 + titre + fallback §8.

        En l'absence de phrase métier dédiée (V1, pas de champ enrichi),
        le bandeau doit afficher la copy §8 « Parcourez les produits
        rattachés à cette collection. » Le titre affiché est le
        ``name`` de la collection.
        """
        resp = self.url_open("/collections/http-col-a", timeout=60)
        self.assertEqual(resp.status_code, 200)
        text = resp.text
        self.assertIn(self.col_a.name, text)
        self.assertIn("Parcourez les produits rattachés à cette collection.", text)
        self.assertIn(self.product_a.name, text)
        # Filtre strict : pas de produit d'une autre collection visible
        self.assertNotIn(self.product_b.name, text)

    # --- RC-06 — union S1 + OU ---

    def test_ckr_col_rc06_union_or_filter_and_copy(self):
        """RC-06 : ``/collections/union/<a>/<b>`` canonique → OU + copy §8.

        Chemin déjà trié (``http-col-a`` < ``http-col-b`` en ordre
        lexicographique strict) : 200 direct sans 301. La liste est
        l'**union** des produits (OU) et le bandeau porte le titre
        figé « Collections sélectionnées » + sous-texte §8.
        """
        resp = self.url_open(
            "/collections/union/http-col-a/http-col-b", timeout=60
        )
        self.assertEqual(resp.status_code, 200)
        text = resp.text
        self.assertIn("Collections sélectionnées", text)
        self.assertIn(
            "Voici les produits appartenant à au moins une des collections combinées.",
            text,
        )
        self.assertIn(self.product_a.name, text)
        self.assertIn(self.product_b.name, text)
        # Produit hors des deux collections visibles
        self.assertNotIn(self.product_lonely.name, text)

    # --- RC-07 — 301 normalisation ---

    def test_ckr_col_rc07_union_order_dupes_301(self):
        """RC-07 : ordre non canonique → 301 vers ``/shop`` (slugs triés)."""
        resp = self._assert_redirect(
            "/collections/union/http-col-b/http-col-a",
            301,
            "/shop",
        )
        loc = resp.headers.get("Location", "")
        self.assertIn("http-col-a", loc)
        self.assertIn("http-col-b", loc)

    def test_ckr_col_rc07_union_collapses_to_single_301(self):
        """RC-07 : doublon union → 301 ``/shop?ckr_collection=…`` (vue unitaire)."""
        resp = self._assert_redirect(
            "/collections/union/http-col-a/http-col-a",
            301,
            "/shop",
        )
        loc = resp.headers.get("Location", "")
        self.assertIn("ckr_collection=http-col-a", loc)

    # --- RC-08 — 302 replis ---

    def test_ckr_col_rc08_unknown_slug_302(self):
        """RC-08 : ``/collections/<slug_inconnu>`` → 302 ``/collections``.

        Vérifie aussi que la Location **ne contient pas** ``ckr_notice=``
        (CONTRAT §8 — flash session one-shot, pas de query visible).
        """
        resp = self._assert_redirect(
            "/collections/slug-inconnu-pv",
            302,
            "/shop",
        )
        loc = resp.headers.get("Location", "")
        self.assertNotIn("ckr_notice", loc)
        parsed = urlparse(loc)
        self.assertEqual(parsed.path.rstrip("/") or "/", "/shop")
        self.assertFalse(parse_qs(parsed.query))

    def test_ckr_col_rc08_union_incomplete_302(self):
        """RC-08 : ``/collections/union/<un_seul>`` → 302 (n ≥ 2 exigé).

        Cas distinct du collapse RC-07 : un seul segment (raw_count=1)
        **même valide** n'est pas une union (n ≥ 2) — on replie sur la
        vue générale avec message. Le contrat §7 autorise l'exception
        « normalisation vers /collections/<slug> » *uniquement* après
        dédup (raw_count > 1) — cf. patron d'implémentation SPEC §3.4.
        """
        resp = self._assert_redirect(
            "/collections/union/http-col-a",
            302,
            "/shop",
        )
        loc = resp.headers.get("Location", "")
        self.assertNotIn("ckr_notice", loc)

    def test_ckr_col_rc08_union_invalid_slug_repli_a_302(self):
        """RC-08 : union avec au moins un slug invalide → **repli A** 302.

        Pas de recomposition partielle (V1 — SPEC §6) : même si
        ``http-col-a`` est valide et ``slug-inconnu`` ne l'est pas, on
        replie sur ``/collections`` (302) **sans** 301 résiduel vers
        ``/collections/http-col-a``.
        """
        resp = self._assert_redirect(
            "/collections/union/http-col-a/slug-inconnu-pv",
            302,
            "/shop",
        )
        loc = resp.headers.get("Location", "")
        self.assertNotIn("ckr_notice", loc)

    # --- RC-09 — flash / pas ``ckr_notice`` sur Location ---

    def test_ckr_col_rc09_flash_no_query_on_location(self):
        """RC-09 : message flash one-shot en session, jamais en query.

        Deux invariants à vérifier :

        1. le **302** n'expose **pas** ``?ckr_notice=…`` sur Location
           (alignement strict CONTRAT §8) ;
        2. après avoir suivi le 302 (requête suivante sur
           ``/collections``), le message figé SPEC §7 doit apparaître
           dans la page puis être **consommé** (seconde requête :
           message absent).
        """
        # Étape 1 : Location du 302 ne contient pas ckr_notice
        resp = self.url_open(
            "/collections/slug-rc09-inconnu",
            allow_redirects=False,
            timeout=60,
        )
        self.assertEqual(resp.status_code, 302)
        loc = resp.headers.get("Location", "")
        self.assertNotIn("ckr_notice", loc)
        self.assertFalse(parse_qs(urlparse(loc).query))
        # Étape 2 : suivi du 302 (session conservée par self.opener
        # dans HttpCase) → la page /collections contient le message.
        resp2 = self.url_open("/collections/slug-rc09-inconnu", timeout=60)
        self.assertEqual(resp2.status_code, 200)
        # Fragment sans apostrophe pour éviter les divergences
        # d'encodage typographique entre le code et le HTML rendu.
        self.assertIn("pas retrouvé exactement la collection demandée", resp2.text)
        # Étape 3 : consommation one-shot — le rechargement de /collections
        # ne doit plus afficher le message.
        resp3 = self.url_open("/collections", timeout=60)
        self.assertEqual(resp3.status_code, 200)
        self.assertNotIn(
            "pas retrouvé exactement la collection demandée",
            resp3.text,
        )

    # --- RC-10 — copies §8 smoke ---

    def test_ckr_col_rc10_fixed_copies_smoke(self):
        """RC-10 : les 4 copies §8 figées sont présentes sur leurs pages."""
        # Générale
        r1 = self.url_open("/collections", timeout=60)
        self.assertIn(
            "Découvrez les collections actuellement disponibles.", r1.text
        )
        # Unitaire fallback
        r2 = self.url_open("/collections/http-col-a", timeout=60)
        self.assertIn(
            "Parcourez les produits rattachés à cette collection.", r2.text
        )
        # Union titre + sous-texte
        r3 = self.url_open(
            "/collections/union/http-col-a/http-col-b", timeout=60
        )
        self.assertIn("Collections sélectionnées", r3.text)
        self.assertIn(
            "Voici les produits appartenant à au moins une des collections combinées.",
            r3.text,
        )
        # État vide §12 A
        r4 = self.url_open("/collections/http-col-c", timeout=60)
        self.assertIn(
            "Aucun produit", r4.text,
            "La copy §12 A doit apparaître sur une collection sans produit.",
        )

    # --- RC-11 — état vide collection valide sans produit ---

    def test_ckr_col_rc11_empty_state_valid_collection(self):
        """RC-11 : collection valide, 0 produit → 200 + empty §12 A.

        Vérifications :

        * 200 (**pas** de 302 — la collection est valide au sens
          visibilité) ;
        * copy §12 A : *Aucun produit n'est affiché pour cette collection
          pour le moment.* ;
        * lien **« Retour aux collections »** pointant vers
          ``/collections``.
        """
        resp = self.url_open("/collections/http-col-c", timeout=60)
        self.assertEqual(resp.status_code, 200)
        text = resp.text
        # Copy corps §12 A (fragment sans apostrophe typographique)
        self.assertIn("Aucun produit", text)
        self.assertIn("affiché pour cette collection pour le moment", text)
        # Lien Retour aux collections → conteneur /shop
        self.assertIn("Retour aux collections", text)
        self.assertIn("ckr_collection_scope=all", text)

    # --- RC-12 — canonical ---

    def test_ckr_col_rc12_canonical_self_paths(self):
        """RC-12 : canonical self, aucune référence ``/shop?ckr_mode=collection``.

        Vérifié sur les 3 cibles publiques nobles : générale, unitaire,
        union canonique.
        """
        expectations = [
            ("/collections", ("ckr_collection_scope=all",)),
            ("/collections/http-col-a", ("ckr_collection=http-col-a",)),
            (
                "/collections/union/http-col-a/http-col-b",
                ("ckr_collection=http-col-a", "ckr_collection=http-col-b"),
            ),
        ]
        for path, subs in expectations:
            resp = self.url_open(path, timeout=60)
            self.assertEqual(
                resp.status_code, 200,
                "%s doit renvoyer 200 (chemin canonique attendu)." % path,
            )
            canon = self._canonical_href(resp.text)
            self.assertIn("/shop", canon, "Canonical shop attendu pour %s" % path)
            for s in subs:
                self.assertIn(s, canon, "Canonical %r manquant dans %r" % (s, canon))
            self.assertNotIn("ckr_mode=collection", canon)

    # --- RC-13 — fiche produit liens ``/collections/<slug>`` ---

    def test_ckr_col_rc13_product_page_collection_links(self):
        """RC-13 : fiche produit — liens ``/shop?ckr_collection=<slug>`` uniquement.

        Le produit A est rattaché à la collection A uniquement. Sa fiche
        affiche le bloc Collections avec un lien conteneur ``/shop`` — et
        **aucun** lien union ni ``/shop?ckr_mode=collection``.
        """
        url = self.product_a.website_url
        self.assertTrue(url.startswith("/"))
        resp = self.url_open(url, timeout=60)
        self.assertEqual(resp.status_code, 200)
        text = resp.text
        self.assertIn("ckr-product-collections", text)
        self.assertIn('href="/shop?ckr_collection=http-col-a"', text)
        # Interdits V1 depuis la fiche
        self.assertNotIn("/collections/union/", text)
        self.assertNotIn("ckr_mode=collection", text)

    # --- RC-14 — non-régression autres portes ---

    def test_ckr_col_rc14_regression_other_gates(self):
        """RC-14 HTTP : les portes déjà livrées restent inchangées.

        Invariants contrôlés (alignement ``test_pv_rc13_regression_
        other_gates`` Origines) :

        * ``/kits`` → 301 ``/shop?ckr_mode=pack`` ;
        * ``/promotions`` → 301 ``/shop?ckr_mode=promo`` ;
        * ``/origines`` → 301 ``/shop?ckr_mode=origin`` ;
        * ``/categories`` → 301 vers ``/shop?ckr_category=…`` (pas ``/shop/category/``) ;
        * ``/shop`` nu → 200.

        Garantit que l'introduction de ``CKR_MODE_COLLECTION`` et des
        routes ``/collections[/…]`` n'altère **aucune** porte déjà
        livrée (§5.1 : ``collection`` ajouté **en fin** de
        ``CKR_MODE_PRIORITY``).
        """
        self._assert_redirect("/kits", 301, "ckr_mode=pack")
        self._assert_redirect("/promotions", 301, "ckr_mode=promo")
        self._assert_redirect("/incontournables", 301, "ckr_mode=featured")
        self._assert_redirect("/origines", 301, "ckr_mode=origin")
        r_cat = self.url_open("/categories", allow_redirects=False, timeout=60)
        self.assertEqual(r_cat.status_code, 301)
        loc_cat = r_cat.headers.get("Location", "")
        self.assertIn("/shop", loc_cat)
        self.assertNotIn("/shop/category/", loc_cat)
        r_shop = self.url_open("/shop", timeout=60)
        self.assertEqual(r_shop.status_code, 200)

    # --- Porte Incontournables (featured) — SPEC §4.6 ---

    def test_ckr_featured_shop_filters_configured_collection(self):
        """``featured_collection_id`` valide → 200, périmètre = produits de la collection."""
        ICP = self.env["ir.config_parameter"].sudo()
        ICP.set_param(
            "dorevia_ckreyol_marketplace.featured_collection_id",
            str(self.col_a.id),
        )
        r = self.url_open("/shop?ckr_mode=featured", timeout=60)
        self.assertEqual(r.status_code, 200)
        self.assertIn(self.product_a.name, r.text)
        self.assertNotIn(self.product_b.name, r.text)
        self.assertNotIn(self.product_lonely.name, r.text)

    def test_ckr_featured_invalid_or_unconfigured_302(self):
        """Paramètre absent / 0 → ``/shop?ckr_mode=featured`` → 302 ``/shop`` nu."""
        ICP = self.env["ir.config_parameter"].sudo()
        ICP.set_param(
            "dorevia_ckreyol_marketplace.featured_collection_id",
            "0",
        )
        self._assert_redirect("/shop?ckr_mode=featured", 302, "/shop")

    def test_ckr_featured_non_visible_collection_302(self):
        """Collection archivée configurée → 302 /shop nu."""
        ICP = self.env["ir.config_parameter"].sudo()
        ICP.set_param(
            "dorevia_ckreyol_marketplace.featured_collection_id",
            str(self.col_d_archived.id),
        )
        self._assert_redirect("/shop?ckr_mode=featured", 302, "/shop")

    def test_ckr_featured_canonical_has_mode(self):
        """Canonical /shop inclut ``ckr_mode=featured`` lorsque le paramètre est valide."""
        ICP = self.env["ir.config_parameter"].sudo()
        ICP.set_param(
            "dorevia_ckreyol_marketplace.featured_collection_id",
            str(self.col_a.id),
        )
        r = self.url_open("/shop?ckr_mode=featured", timeout=60)
        self.assertEqual(r.status_code, 200)
        canon = self._canonical_href(r.text)
        self.assertIn("ckr_mode=featured", canon)
