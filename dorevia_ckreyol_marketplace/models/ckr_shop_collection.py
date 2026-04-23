# -*- coding: utf-8 -*-
"""Modèle CK « collection éditoriale » — porte Collections (``/collections``).

Objet **éditorial propre à CK** : contrairement à ``ckr.shop.origin``
qui **décore** une valeur d'attribut catalogue (source de vérité
standard), ``ckr.shop.collection`` **porte lui-même** la source de
vérité du rattachement produit via un M2M direct
``product_template_ids`` (cf. [CADRAGE_FONCTIONNEL_COLLECTIONS.md]
§9.2 et [SPEC_IMPL_COLLECTIONS.md] §2.1 — MOA 2026-04-22) :

* pas d'attribut catalogue « Collection » imposé côté produit (une
  collection est une **curation éditoriale / saisonnière / thématique**,
  pas un axe taxonomique stable) ;
* la liste visiteur ``/collections/<slug>`` lit directement
  ``collection.product_template_ids`` (et ``/collections/union/…``
  applique l'union des ensembles — filtre OU — SPEC_IMPL §3.3).

Contraintes verrouillées (**SPEC_IMPL §2.2**, [CONTRAT_URL_COLLECTIONS.md]
§4.6 — MOA 2026-04-22) :

* ``unique(website_id, slug)`` → unicité logique du slug par site ;
* ``slug != "union"`` → le segment ``union`` est **réservé** à la
  syntaxe combinée ``/collections/union/<s1>/…/<sn>`` (S1 actée) ;
* slug normalisé : minuscules ASCII + chiffres + tirets simples
  (même règle que ``ckr.shop.origin`` — cohérence maintenance).

Visibilité **navigation publique** (SPEC_IMPL §2.2 T3, RC-03 PV) :

* ``active`` **ET** fenêtre ``date_start`` / ``date_end`` couvrant la
  date courante **ET** site courant (ou ``website_id`` non renseigné).

Priorité ``ckr_mode`` en cas de conflit multi-modes dans la requête
(cohérence portes livrées, SPEC_IMPL §5.1) : ``pack > promo > origin
> collection`` — ``collection`` est **en dernier** pour garantir
**zéro régression** sur les portes déjà déployées. La décision est
figée dans ``CKR_MODE_PRIORITY`` du contrôleur (ajout à venir à
l'étape suivante de la checklist §13) ; le présent modèle n'en
dépend pas directement.

Droits (**SPEC_IMPL §2.3** + ``security/ir.model.access.csv``) :

* employés (``base.group_user``) : lecture seule ;
* éditeurs site (``website.group_website_designer``) : CRUD ;
* aucun accès public — le futur contrôleur lira en ``sudo()``.
"""
import re

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


# Même règle de normalisation que ``ckr.shop.origin`` (minuscules ASCII
# + chiffres + tirets simples, pas de tiret en début/fin). Volontairement
# stricte : évite toute collision avec les séparateurs de chemin
# ``/collections/union/<s1>/<s2>/…`` et les encodages visuels équivoques.
_CKR_COLLECTION_SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")

# Segment réservé à la syntaxe combinée S1 (``/collections/union/…``).
# Interdit comme slug de collection pour écarter toute ambiguïté de
# routage ([CONTRAT_URL_COLLECTIONS.md] §4.6).
_CKR_COLLECTION_SLUG_RESERVED = frozenset({"union"})


class CkrShopCollection(models.Model):
    _name = "ckr.shop.collection"
    _description = "C-Kreyol — Collection éditoriale (porte /collections)"
    _order = "sequence, name, id"

    # ------------------------------------------------------------------
    # Identité visiteur / BO (SPEC_IMPL §2.1)
    # ------------------------------------------------------------------
    name = fields.Char(
        string="Titre affiché",
        required=True,
        translate=True,
        help=(
            "Titre affiché au visiteur (bandeau, fiche produit, navigation). "
            "Traduit — alimente aussi les copies §8 lorsqu'une collection "
            "unitaire est résolue."
        ),
    )
    slug = fields.Char(
        string="Slug",
        required=True,
        index=True,
        help=(
            "Identifiant stable utilisé dans l'URL publique "
            "(``/collections/<slug>`` et segments de "
            "``/collections/union/<s1>/…/<sn>``). Minuscules ASCII, "
            "chiffres et tirets uniquement ; ``union`` est réservé "
            "à la syntaxe combinée et interdit ici."
        ),
    )
    sequence = fields.Integer(
        string="Ordre d'affichage",
        default=10,
        help=(
            "Ordre d'affichage dans la navigation visible "
            "(ex. sous-menu horizontal) et la vue générale "
            "``/collections``."
        ),
    )

    # ------------------------------------------------------------------
    # Visibilité navigation (CADRAGE §2, SPEC_IMPL §2.2 / §2.3)
    # ------------------------------------------------------------------
    active = fields.Boolean(
        string="Active",
        default=True,
        help=(
            "Si décochée, la collection est ignorée par les contrôleurs "
            "front (vue générale, unitaire, union) et ses slugs ne "
            "résolvent plus côté visiteur (repli 302 au routage)."
        ),
    )
    date_start = fields.Date(
        string="Début de validité",
        help=(
            "Si renseignée, la collection n'est visible qu'à partir de "
            "cette date (inclusivement). Sinon, pas de borne basse."
        ),
    )
    date_end = fields.Date(
        string="Fin de validité",
        help=(
            "Si renseignée, la collection n'est plus visible après "
            "cette date (inclusivement). Sinon, pas de borne haute."
        ),
    )

    # ------------------------------------------------------------------
    # Rattachement produit — source de vérité CK (SPEC_IMPL §2.1)
    # ------------------------------------------------------------------
    product_template_ids = fields.Many2many(
        comodel_name="product.template",
        relation="ckr_shop_collection_product_template_rel",
        column1="collection_id",
        column2="product_template_id",
        string="Produits rattachés",
        help=(
            "Produits inclus dans la collection. Source de vérité CK "
            "du filtre visiteur (``/collections/<slug>`` = M2M ∋ ; "
            "``/collections/union/<a>/<b>/…`` = union des M2M — OU)."
        ),
    )
    product_template_count = fields.Integer(
        string="Nombre de produits",
        compute="_compute_product_template_count",
        help="Nombre de produits rattachés à la collection (toutes publications).",
    )

    # ------------------------------------------------------------------
    # Site (multi-site — aligné sur ``ckr.shop.origin``)
    # ------------------------------------------------------------------
    website_id = fields.Many2one(
        comodel_name="website",
        string="Site web",
        ondelete="cascade",
        index=True,
        help=(
            "Site web sur lequel la collection est exposée. Laisser "
            "vide pour une collection non scopée (disponible sur tous "
            "les sites — utile en mono-site)."
        ),
    )

    # ------------------------------------------------------------------
    # Contraintes SQL (SPEC_IMPL §2.2) — API ``models.Constraint`` Odoo 19
    # ------------------------------------------------------------------
    _ckr_shop_collection_slug_website_uniq = models.Constraint(
        "unique(website_id, slug)",
        "Le slug d'une collection doit être unique par site.",
    )

    # ------------------------------------------------------------------
    # Validations Python
    # ------------------------------------------------------------------
    @api.constrains("slug")
    def _check_slug_format(self):
        """Normalisation (regex) + interdiction du segment réservé ``union``.

        Alignement [CONTRAT_URL_COLLECTIONS.md] §4.6 (S1) : le segment
        ``union`` n'est pas un slug de collection, il désigne la
        combinaison ; autoriser un tel slug ouvrirait une ambiguïté
        irréversible côté routage (``/collections/union`` ↔ collection
        nommée « union »).
        """
        for record in self:
            slug = (record.slug or "").strip()
            if not slug:
                raise ValidationError(
                    _("Le slug d'une collection ne peut pas être vide.")
                )
            if slug in _CKR_COLLECTION_SLUG_RESERVED:
                raise ValidationError(
                    _(
                        "Le slug « %s » est réservé à la syntaxe de "
                        "combinaison ``/collections/union/…`` et ne peut "
                        "pas être utilisé comme slug de collection."
                    )
                    % slug
                )
            if not _CKR_COLLECTION_SLUG_RE.match(slug):
                raise ValidationError(
                    _(
                        "Le slug de collection « %s » n'est pas valide : "
                        "minuscules ASCII, chiffres et tirets uniquement, "
                        "pas de tiret en début/fin."
                    )
                    % slug
                )

    @api.constrains("date_start", "date_end")
    def _check_date_range(self):
        """Bornes cohérentes : ``date_start <= date_end`` si toutes deux fournies."""
        for record in self:
            if record.date_start and record.date_end and record.date_start > record.date_end:
                raise ValidationError(
                    _(
                        "Période de validité invalide pour la collection "
                        "« %(name)s » : la date de début (%(start)s) est "
                        "postérieure à la date de fin (%(end)s)."
                    )
                    % {
                        "name": record.name or record.slug or "",
                        "start": record.date_start,
                        "end": record.date_end,
                    }
                )

    # ------------------------------------------------------------------
    # Champs calculés
    # ------------------------------------------------------------------
    @api.depends("product_template_ids")
    def _compute_product_template_count(self):
        for record in self:
            record.product_template_count = len(record.product_template_ids)

    # ------------------------------------------------------------------
    # Visibilité navigation (RC-03 PV / SPEC_IMPL §2.2 T3)
    # ------------------------------------------------------------------
    @api.model
    def _ckr_visible_domain(self, website=None, at_date=None):
        """Domaine « collection **visible** pour la navigation publique ».

        Construit un domaine ORM réutilisable par les contrôleurs
        (routes ``/collections``, ``/collections/<slug>``,
        ``/collections/union/…``) et par les résolveurs internes.

        Critères (MOA 2026-04-22) :

        * ``active = True`` (archive standard Odoo) ;
        * ``date_start`` **non renseignée** ou **<= at_date** ;
        * ``date_end`` **non renseignée** ou **>= at_date** ;
        * ``website_id`` non renseigné (collection non scopée) ou égal
          au site courant.

        :param website: ``website.website`` ou ``None`` (aucune
            restriction site — utile pour le BO / les imports).
        :param at_date: ``date`` de référence ; défaut = ``fields.Date.
            context_today(self)`` (fuseau / utilisateur courant).

        :returns: liste de tuples (domaine ORM).
        """
        today = at_date or fields.Date.context_today(self)
        domain = [
            ("active", "=", True),
            "|",
            ("date_start", "=", False),
            ("date_start", "<=", today),
            "|",
            ("date_end", "=", False),
            ("date_end", ">=", today),
        ]
        if website is not None:
            domain.append(("website_id", "in", [False, website.id]))
        return domain

    def _ckr_is_visible(self, website=None, at_date=None):
        """True si la collection est visible pour la navigation publique.

        Variante *record-wise* de :meth:`_ckr_visible_domain`. Réalise
        les vérifications **en mémoire** (pas de requête ORM) — utile
        pour décider d'un ``302`` sur un enregistrement déjà résolu.
        """
        self.ensure_one()
        if not self.active:
            return False
        today = at_date or fields.Date.context_today(self)
        if self.date_start and self.date_start > today:
            return False
        if self.date_end and self.date_end < today:
            return False
        if website is not None and self.website_id and self.website_id.id != website.id:
            return False
        return True

    # ------------------------------------------------------------------
    # Résolution pour le contrôleur (SPEC_IMPL §3.2 / §3.3)
    # ------------------------------------------------------------------
    @api.model
    def _ckr_resolve_visible_slugs(self, slugs, website=None, at_date=None):
        """Résout un itérable de slugs en collections **visibles**.

        Mirroir logique de :func:`CkrShopOrigin._ckr_resolve_published_slugs`,
        adapté à la visibilité Collections (``active`` + fenêtre date).
        Les slugs en entrée sont **normalisés** (strip + lower) et
        **dédupliqués** en préservant l'ordre d'apparition — pour que
        le contrôleur puisse comparer l'URL reçue à la forme canonique
        (triée lexicographiquement) et décider du **301** éventuel
        ([SPEC_IMPL §3.3 / §3.4]).

        :param slugs: itérable de chaînes ``slug``.
        :param website: ``website.website`` ou ``None`` (pas de
            restriction site — les collections non scopées et celles
            scopées sont considérées).
        :param at_date: date de référence pour la fenêtre de validité.

        :returns: ``ckr.shop.collection`` (recordset) des collections
            **visibles** trouvées, dans l'ordre d'apparition des slugs
            (dédupliqué). Les slugs inconnus / non visibles / hors
            période sont **ignorés** — la gestion du repli HTTP 302
            (option A, [SPEC_IMPL §6]) est à la charge du contrôleur.
        """
        normalized = []
        seen = set()
        for raw in slugs or ():
            value = (raw or "").strip().lower()
            if not value or value in seen:
                continue
            seen.add(value)
            normalized.append(value)
        if not normalized:
            return self.browse()

        domain = self._ckr_visible_domain(website=website, at_date=at_date)
        domain = [("slug", "in", normalized)] + domain

        records = self.sudo().search(domain)
        if not records:
            return records

        by_slug = {rec.slug: rec for rec in records}
        ordered_ids = [by_slug[s].id for s in normalized if s in by_slug]
        return self.browse(ordered_ids)
