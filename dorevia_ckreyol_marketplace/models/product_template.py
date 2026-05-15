# -*- coding: utf-8 -*-
"""Extension de ``product.template`` pour les portes Explorer → ``/shop``.

Consomme les options injectées par ``controllers/website_sale_ckr.py``
dans les options passées à ``website._search_with_fuzzy`` :

* ``ckr_pack_only`` → porte **Kits/Pack** (voir
  ``docs/mvp_01/CONTRAT_URL_PACKS.md`` §12). Restriction aux produits
  dont ``pack_ok = True`` (module OCA ``product_pack``).
* ``ckr_promo_only`` → porte **Promotions** (voir
  ``docs/mvp_01/CONTRAT_URL_PROMOTIONS.md`` §12). Restriction aux
  ``product.template.id`` retournés par
  ``product.pricelist._ckr_get_promo_template_ids`` (source de vérité
  A2 : pricelist datée avec remise).
* ``ckr_origin_only`` + ``ckr_origin_attribute_value_ids`` → porte
  **Origines** (voir ``docs/mvp_01/SPEC_IMPL_ORIGINES.md`` §5).
  Restriction aux ``product.template`` qui portent **au moins une**
  des valeurs d'attribut cibles (logique **OU**) dans leurs lignes
  d'attribut standard. Si ``ckr_origin_only`` est vrai sans ids de
  valeurs (``ckr_mode=origin`` seul) : **aucune** restriction — le
  catalogue complet est affiché (§3.2).
* ``ckr_public_category_ids`` / ``ckr_category_invalid`` → facette
  **Catégories** (``/shop?ckr_category=…``), alignée sur
  ``WebsiteSaleCKR._get_shop_domain`` (min-max prix, compteur, grille).

Cette extension ne touche qu'à la couche *recherche* (``base_domain``
du moteur Odoo). Aucune logique métier parallèle n'est introduite —
chaque porte reste entièrement adossée à sa source de vérité standard /
OCA.

Champ **``ckr_origin_value_ids``** : raccourci éditeur sur l'attribut
catalogue « Origine » (``data/ckr_product_attribute_origin.xml``),
synchronisé avec ``attribute_line_ids`` — évite de chercher l'onglet
« Attributs & variantes » réservé au groupe Variantes.
"""
import re

from odoo import api, fields, models
from odoo.fields import Command, Domain
from odoo.http import request
from odoo.tools import float_compare, html2plaintext


# Sentinel : ``id = 0`` est la manière canonique Odoo de forcer
# « aucun résultat » dans un domaine sans déclencher d'exception.
_CKR_EMPTY_DOMAIN = [("id", "=", 0)]


def _ckr_strip_list_price_constraints(base_domain_fragments):
    """Retire les feuilles ``list_price`` du domaine recherche boutique.

    Odoo filtre alors sur ``list_price`` ; sur config. pricelist + ``list_price`` nul
    en base, la grille reflète pourtant ``price_reduce``. On remplace par un filtre
    sur ces montants lorsque ``request`` est disponible.
    """
    return [
        clause
        for clause in base_domain_fragments
        if not (
            isinstance(clause, (list, tuple))
            and len(clause) == 3
            and clause[0] == "list_price"
            and clause[1] in (">=", "<=")
        )
    ]


# Libellés e-commerce trop génériques — exclus de la ligne méta tuile /shop (Lot 1 carte CK).
_CKR_SHOP_TILE_META_WEAK_NAMES = frozenset(
    name.strip().lower()
    for name in (
        "goods",
        "good",
        "all",
        "miscellaneous",
        "misc",
        "other",
        "default",
        "general",
        "non classé",
        "non classe",
        "divers",
        "produits",
        "articles",
        "saleable",
        "vente",
        "collection",
        "collections",
        "promotion",
        "promotions",
        "incontournable",
        "incontournables",
        "boutique",
        "selection",
        "sélection",
    )
)

# Séparateur méta tuile : espace insécable + point médian (évite césure ; lisible vs un simple tiret).
_CKR_SHOP_TILE_META_SEP = "\u00a0·\u00a0"

_CKR_SHOP_TILE_WEAK_UOM = frozenset(
    name.strip().lower()
    for name in (
        "units",
        "unit",
        "unit(s)",
        "unité",
        "unité(s)",
        "unités",
        "unite",
        "unite(s)",
        "unites",
        "pcs",
        "pc",
        "pièce",
        "pièces",
        "piece",
        "pieces",
        "udm",
        "un",
        "u",
    )
)

_CKR_SHOP_TILE_FORMAT_RE = re.compile(
    r"(?i)\b(?:\d+\s?[xX]\s?\d+(?:[.,]\d+)?\s?(?:kg|g|mg|l|cl|ml)|"
    r"\d+(?:[.,]\d+)?\s?(?:kg|g|mg|l|cl|ml)|"
    r"\d+\s?(?:pi[eè]ces?|pcs?))\b"
)


class ProductTemplate(models.Model):
    _inherit = "product.template"

    ck_product_name = fields.Char(
        string="Nom CK",
        help=(
            "Nom commercial affiché en priorité sur la tuile boutique /shop. "
            "Si vide, le nom produit Odoo (name) est utilisé. Ne remplace pas "
            "le champ name pour les documents internes."
        ),
    )

    ckr_origin_value_ids = fields.Many2many(
        comodel_name="product.attribute.value",
        string="Origines",
        compute="_compute_ckr_origin_value_ids",
        inverse="_inverse_ckr_origin_value_ids",
        store=False,
        help=(
            "Valeurs de l'attribut catalogue « Origine » pour ce produit. "
            "Équivalent à une ligne « Origine » dans Attributs & variantes."
        ),
    )

    # ------------------------------------------------------------------
    # Porte Collections — rattachement M2M (SPEC_IMPL_COLLECTIONS §2.1)
    # ------------------------------------------------------------------
    # Inverse stocké du M2M déclaré côté ``ckr.shop.collection``. Le
    # ``relation`` (et l'ordre ``column1``/``column2``) doivent **refléter**
    # exactement la déclaration d'origine (colonnes **inversées** par
    # rapport au forward) pour que les deux côtés partagent bien la même
    # table de liaison.
    ckr_collection_ids = fields.Many2many(
        comodel_name="ckr.shop.collection",
        relation="ckr_shop_collection_product_template_rel",
        column1="product_template_id",
        column2="collection_id",
        string="Collections",
        help=(
            "Collections éditoriales C-Kreyol auxquelles ce produit est "
            "rattaché. Source de vérité de la porte /collections (voir "
            "docs/mvp_01/SPEC_IMPL_COLLECTIONS.md §2.1). Un produit "
            "peut appartenir à plusieurs collections (RC-02) : la vue "
            "/collections/<slug> filtre par appartenance, "
            "/collections/union/<a>/<b>/… applique le OU."
        ),
    )

    @api.model
    def _ckr_origin_attribute(self):
        return self.env.ref(
            "dorevia_ckreyol_marketplace.ckr_product_attribute_origin",
            raise_if_not_found=False,
        )

    @api.depends(
        "attribute_line_ids",
        "attribute_line_ids.attribute_id",
        "attribute_line_ids.value_ids",
    )
    def _compute_ckr_origin_value_ids(self):
        attr = self._ckr_origin_attribute()
        Value = self.env["product.attribute.value"]
        if not attr:
            for tmpl in self:
                tmpl.ckr_origin_value_ids = Value.browse()
            return
        for tmpl in self:
            line = tmpl.attribute_line_ids.filtered(lambda l: l.attribute_id == attr)[:1]
            tmpl.ckr_origin_value_ids = line.value_ids

    def _inverse_ckr_origin_value_ids(self):
        attr = self._ckr_origin_attribute()
        if not attr:
            return
        Line = self.env["product.template.attribute.line"]
        for tmpl in self:
            line = tmpl.attribute_line_ids.filtered(lambda l: l.attribute_id == attr)[:1]
            if tmpl.ckr_origin_value_ids:
                if line:
                    line.value_ids = tmpl.ckr_origin_value_ids
                else:
                    Line.create(
                        {
                            "product_tmpl_id": tmpl.id,
                            "attribute_id": attr.id,
                            "value_ids": [Command.set(tmpl.ckr_origin_value_ids.ids)],
                        }
                    )
            elif line:
                # Pas de ligne vide : contrainte Odoo sur
                # product.template.attribute.line (valeurs requises si actif).
                line.unlink()

    def _search_get_detail(self, website, order, options):
        """Ajoute le filtre de porte au ``base_domain`` selon les options CK.

        Se greffe sur le ``base_domain`` (liste de domaines AND-és par le
        moteur de recherche) au lieu d'introduire un mécanisme parallèle :
        garantit que les facettes / pagination / calcul min-max prix
        convergent vers le même périmètre produit.

        Les portes sont traitées en séquence (indépendantes) ; une
        éventuelle combinaison hypothétique ``ckr_mode=pack`` + promo
        (qui ne peut pas se produire côté HTTP, whitelist exclusive du
        contrôleur, mais qui pourrait se produire côté appel direct
        Python) serait interprétée comme **intersection** des
        restrictions, ce qui est la sémantique AND naturelle du
        ``base_domain`` Odoo.
        """
        detail = super()._search_get_detail(website, order, options)
        base_domain = list(detail.get("base_domain") or [])

        if options.get("ckr_category_invalid"):
            base_domain.append(_CKR_EMPTY_DOMAIN)
        elif options.get("ckr_public_category_ids"):
            base_domain.append(
                [
                    (
                        "public_categ_ids",
                        "in",
                        list(options["ckr_public_category_ids"]),
                    )
                ]
            )

        if options.get("ckr_pack_only"):
            base_domain.append([("pack_ok", "=", True)])

        if options.get("ckr_promo_only"):
            promo_ids = (
                self.env["product.pricelist"]
                .sudo()
                ._ckr_get_promo_template_ids(website=website)
            )
            if promo_ids is None:
                # Cas « global promo » : aucun filtre supplémentaire
                # (toute la boutique est légitimement en promotion).
                pass
            elif not promo_ids:
                # État vide : aucune promo active → on garantit un
                # résultat vide via le sentinel. Le bandeau dédié
                # (ckr_shop_promo_banner, flag ckr_promo_empty) prend le
                # relais côté vue.
                base_domain.append(_CKR_EMPTY_DOMAIN)
            else:
                base_domain.append([("id", "in", list(promo_ids))])

        if options.get("ckr_origin_only"):
            # SPEC_IMPL §3.2 / §5 :
            # - sans value_ids : `ckr_mode=origin` seul → pas de
            #   restriction (catalogue complet + bandeau) ;
            # - avec value_ids : filtre OU sur les lignes d'attribut
            #   standard du template (`attribute_line_ids.value_ids`).
            value_ids = options.get("ckr_origin_attribute_value_ids") or []
            if value_ids:
                base_domain.append(
                    [("attribute_line_ids.value_ids", "in", list(value_ids))]
                )

        if options.get("ckr_collection_only"):
            # Porte **Collections** — SPEC_IMPL_COLLECTIONS §3.2 / §5.2.
            # L'option est toujours posée en paire avec
            # ``ckr_collection_template_ids`` par le contrôleur
            # (`controllers/website_sale_ckr.py` — `_get_search_options`).
            # La sémantique est **stricte** : aucun template_id résolu
            # (collection unique sans produit, union vide au sens des
            # rattachements, vue générale sans collection visible…) →
            # résultat catalogue **vide**. C'est exactement l'état vide
            # §12 A rendu par ``ckr_shop_collection_banner`` ; éviter
            # un domaine vide (``[]``) qui autoriserait l'ensemble du
            # catalogue est **impératif**.
            template_ids = options.get("ckr_collection_template_ids") or []
            if template_ids:
                base_domain.append([("id", "in", list(template_ids))])
            else:
                base_domain.append(_CKR_EMPTY_DOMAIN)

        detail["base_domain"] = (
            self._ckr_substitute_shop_price_reduce_filter(domain=base_domain, website=website, options=options)
        )
        return detail

    # ------------------------------------------------------------------

    def _ckr_substitute_shop_price_reduce_filter(self, *, domain, website, options):
        """Aligne la recherche sur le même prix boutique que les tuiles (pricelist)."""
        if not request:
            return domain

        min_p = float(options.get("min_price") or 0.0)
        max_p = float(options.get("max_price") or 0.0)
        # Même seuil truthy que le standard : pas de recherche prix si tout à 0.
        if min_p <= 0.0 and max_p <= 0.0:
            return domain

        fragments = list(domain or [])
        stripped = _ckr_strip_list_price_constraints(fragments)
        if not stripped:
            return fragments

        try:
            combined = Domain(stripped[0])
            for part in stripped[1:]:
                combined &= Domain(part)
        except (TypeError, ValueError):
            return domain

        Product = self.with_context(bin_size=True)
        candidates = Product.search(combined)
        if not candidates:
            return [_CKR_EMPTY_DOMAIN]

        by_tmpl = candidates._get_sales_prices(website)
        round_cur = website.currency_id.rounding or 0.01
        keep_ids = []
        for tmpl in candidates:
            entry = by_tmpl.get(tmpl.id)
            if not isinstance(entry, dict):
                continue
            pr = entry.get("price_reduce")
            if pr is None:
                continue
            amount = float(pr)
            if min_p > 0.0:
                if float_compare(amount, min_p, precision_rounding=round_cur) < 0:
                    continue
            if max_p > 0.0:
                if float_compare(amount, max_p, precision_rounding=round_cur) > 0:
                    continue
            keep_ids.append(tmpl.id)

        stripped.append([("id", "in", keep_ids)] if keep_ids else _CKR_EMPTY_DOMAIN)
        return stripped

    # ------------------------------------------------------------------
    # Helper fiche produit (SPEC_IMPL §7)
    # ------------------------------------------------------------------
    def _ckr_get_origin_profiles(self, website=None):
        """Profils ``ckr.shop.origin`` publiés pour ce template.

        Utilisé depuis la fiche produit (héritage
        ``website_sale.product``) pour afficher les libellés visiteur
        des origines attachées au produit. Résolution côté standard :
        on lit les ``product.attribute.value`` du template via les
        lignes d'attribut, puis on filtre sur les profils CK publiés.

        :returns: recordset ``ckr.shop.origin`` (ordre `_order` du
            modèle) ; vide si le produit n'a aucune origine associée.
        """
        self.ensure_one()
        value_ids = self.attribute_line_ids.value_ids.ids
        if not value_ids:
            return self.env["ckr.shop.origin"].browse()
        domain = [
            ("attribute_value_id", "in", value_ids),
            ("website_published", "=", True),
        ]
        if website is not None:
            domain.append(("website_id", "in", [False, website.id]))
        return self.env["ckr.shop.origin"].sudo().search(domain)

    def _ckr_get_product_origin_labels(self, website=None):
        """Libellés d'origine pour la fiche produit (mode informatif MVP2.3).

        Priorité :
        1) profils `ckr.shop.origin` publiés (libellé visiteur),
        2) repli sur les valeurs brutes de l'attribut catalogue Origine.
        """
        self.ensure_one()
        profiles = self._ckr_get_origin_profiles(website=website)
        if profiles:
            labels = [(p.display_name_visitor or "").strip() for p in profiles]
            return [lbl for lbl in labels if lbl]

        attr = self._ckr_origin_attribute()
        if not attr:
            return []
        line = self.attribute_line_ids.filtered(lambda l: l.attribute_id == attr)[:1]
        if not line:
            return []
        vals = line.value_ids.sorted(key=lambda v: ((v.name or "").lower(), v.id))
        return [(v.name or "").strip() for v in vals if (v.name or "").strip()]

    def _ckr_get_product_specs_single_values(self):
        """Valeurs simples pour `Spécifications`, sans l'attribut Origine.

        L'origine est déjà rendue en haut de fiche dans un bloc éditorial.
        On évite le doublon en bas.
        """
        self.ensure_one()
        values = self.valid_product_template_attribute_line_ids._prepare_single_value_for_display()
        origin_attr = self._ckr_origin_attribute()
        if not origin_attr:
            return values
        return {
            attribute: line_values
            for attribute, line_values in (values or {}).items()
            if attribute.id != origin_attr.id
        }

    def _ckr_product_text_plain(self, value):
        """Texte éditorial nettoyé pour les blocs bas de fiche."""
        text = html2plaintext(value or "")
        text = re.sub(r"\s+", " ", text or "").strip()
        return text

    def _ckr_get_product_long_description(self):
        """Description utile pour le bloc bas de fiche produit.

        Priorité aux champs éditoriaux e-commerce existants. On ne génère pas
        de texte si la fiche ne contient qu'une promesse courte.
        """
        self.ensure_one()
        promise = self._ckr_shop_tile_compact_text(
            self._ckr_get_product_promise_line()
        )
        for raw in (
            self.description_ecommerce,
            self.website_description,
            self.description_sale,
        ):
            text = self._ckr_product_text_plain(raw)
            if not text:
                continue
            if self._ckr_shop_tile_compact_text(text) == promise:
                continue
            if len(text) > 900:
                text = text[:897].rstrip() + "..."
            return text
        return ""

    def _ckr_get_product_specs_lines(self, website=None):
        """Lignes factuelles pour `Spécifications techniques`.

        Source uniquement des données Odoo déjà présentes : référence, origine,
        familles publiques, collections et format détecté.
        """
        self.ensure_one()
        lines = []
        seen = set()

        def add(label, value):
            text = str(value or "").strip()
            key = (label, text)
            if text and key not in seen:
                seen.add(key)
                lines.append({"label": label, "value": text})

        variant = self.product_variant_ids[:1]
        if variant and variant.default_code:
            add("Référence", variant.default_code)

        origins = self._ckr_get_product_origin_labels(website=website)
        add("Origine", ", ".join(origins))

        public_categories = [
            cat.name
            for cat in self.public_categ_ids.sorted("sequence")
            if self._ckr_shop_tile_meta_label_is_useful(cat.name)
        ]
        add("Famille", ", ".join(public_categories))

        collections = [
            collection.name
            for collection in self._ckr_get_visible_collections(website=website)
            if self._ckr_shop_tile_meta_label_is_useful(collection.name)
        ]
        add("Collection", ", ".join(collections))

        add("Format", self._ckr_get_shop_tile_format_segment())
        return lines

    def _ckr_get_product_detail_sections(self, website=None):
        """Sections bas de fiche rendues uniquement quand elles sont alimentées."""
        self.ensure_one()
        sections = []
        long_description = self._ckr_get_product_long_description()
        if long_description:
            sections.append(
                {
                    "key": "description",
                    "title": "Description",
                    "body": long_description,
                    "open": True,
                }
            )

        specs = self._ckr_get_product_specs_lines(website=website)
        if specs:
            sections.append(
                {
                    "key": "specs",
                    "title": "Spécifications techniques",
                    "lines": specs,
                    "open": not sections,
                }
            )
        return sections

    def _ckr_is_product_recommendable(self, website=None):
        """Vrai si le produit peut être proposé en recommandation publique."""
        self.ensure_one()
        if not self.active or not self.sale_ok:
            return False
        if "is_published" in self._fields and not self.is_published:
            return False
        if "website_published" in self._fields and not self.website_published:
            return False
        if website and "website_id" in self._fields and self.website_id:
            return self.website_id == website
        return True

    def _ckr_get_product_recommendation_templates(self, website=None, limit=4):
        """Recommandations simples et fiables pour `Vous aimerez aussi`.

        Ordre : relations alternatives Odoo, même famille publique, même
        origine, même collection. Aucun produit aléatoire n'est injecté.
        """
        self.ensure_one()
        candidates = self.env["product.template"].browse()

        def append(recordset):
            nonlocal candidates
            for tmpl in recordset:
                if tmpl.id == self.id or tmpl in candidates:
                    continue
                if tmpl._ckr_is_product_recommendable(website=website):
                    candidates |= tmpl
                if len(candidates) >= limit:
                    return True
            return False

        if append(self.alternative_product_ids):
            return candidates[:limit]

        domain = [
            ("id", "!=", self.id),
            ("sale_ok", "=", True),
            ("active", "=", True),
        ]
        if "is_published" in self._fields:
            domain.append(("is_published", "=", True))
        if "website_published" in self._fields:
            domain.append(("website_published", "=", True))

        if self.public_categ_ids:
            same_family = self.search(
                domain + [("public_categ_ids", "in", self.public_categ_ids.ids)],
                limit=limit,
            )
            if append(same_family):
                return candidates[:limit]

        origin_attr = self._ckr_origin_attribute()
        if origin_attr:
            origin_line = self.attribute_line_ids.filtered(
                lambda line: line.attribute_id == origin_attr
            )[:1]
            if origin_line and origin_line.value_ids:
                same_origin = self.search(
                    domain
                    + [
                        (
                            "attribute_line_ids.value_ids",
                            "in",
                            origin_line.value_ids.ids,
                        )
                    ],
                    limit=limit,
                )
                if append(same_origin):
                    return candidates[:limit]

        collections = self._ckr_get_visible_collections(website=website)
        if collections:
            collection_products = collections.mapped("product_template_ids")
            append(collection_products)
        return candidates[:limit]

    # ------------------------------------------------------------------
    # Helper fiche produit — porte Collections
    # (SPEC_IMPL_COLLECTIONS §10, CONTRAT §11 — MOA 2026-04-22)
    # ------------------------------------------------------------------
    def _ckr_get_visible_collections(self, website=None):
        """Collections **visibles** auxquelles ce template est rattaché.

        Utilisé depuis la fiche produit (héritage
        ``website_sale.product`` — cf. ``views/pages/ckr_product.xml``)
        pour afficher un bloc de liens uniquement vers
        ``/collections/<slug>`` (CONTRAT §11 : pas d'union depuis
        fiche en V1).

        Filtrage :

        * M2M ``ckr_collection_ids`` (inverse du forward porté par
          ``ckr.shop.collection.product_template_ids``) ;
        * visibilité navigation publique via
          ``ckr.shop.collection._ckr_is_visible`` — ``active`` +
          fenêtre de validité + site courant.

        :param website: ``website.website`` ou ``None`` (aucune
            restriction site).

        :returns: recordset ``ckr.shop.collection`` trié par
            ``_order`` (``sequence, name, id``). Vide si le produit
            n'est rattaché à aucune collection visible.
        """
        self.ensure_one()
        if not self.ckr_collection_ids:
            return self.env["ckr.shop.collection"].browse()
        # On lit en sudo côté fiche produit publique : ACL masquerait
        # les collections au visiteur non authentifié sinon.
        collections = self.ckr_collection_ids.sudo()
        return collections.filtered(lambda c: c._ckr_is_visible(website=website))

    def _ckr_get_product_promise_line(self):
        """Retourne une phrase courte exploitable pour la fiche produit.

        Source MVP2.3 : première ligne utile de ``description_sale``.
        Garde-fou : si aucune source éditoriale propre n'est disponible,
        le bloc doit rester masqué côté template (pas de génération artificielle).
        """
        self.ensure_one()
        desc = html2plaintext(self.description_sale or "")
        for raw in desc.splitlines():
            line = (raw or "").strip()
            if not line:
                continue
            # Évite de répéter le titre produit comme fausse "promesse".
            if self._ckr_shop_tile_compact_text(line) == self._ckr_shop_tile_compact_text(self.name):
                continue
            if len(line) > 180:
                line = line[:177].rstrip() + "..."
            return line
        return ""

    # ------------------------------------------------------------------
    # Homepage — sélection produits MVP2.1 (DECISION_PRODUITS_HOMEPAGE_MVP21)
    # ------------------------------------------------------------------

    def _ckr_get_homepage_origin_short_label(self, website):
        """Libellé court pour carte accueil (profil CK ou valeur attribut)."""
        self.ensure_one()
        profiles = self._ckr_get_origin_profiles(website=website)
        if not profiles:
            return ""
        p0 = profiles[0]
        return (p0.name_visitor or p0.attribute_value_id.name or "").strip()

    def _ckr_get_homepage_combination_info(self):
        """Prix catalogue / pricelist courant pour la grille (sans panier)."""
        self.ensure_one()
        if not request:
            return {}
        return self.sudo()._get_combination_info(
            only_template=True,
            add_qty=1.0,
        )

    def _ckr_has_homepage_listing_image(self):
        """Vrai si un binaire visuel exploitable (fiche / une variante) pour la grille."""
        self.ensure_one()
        p = self.sudo()
        if p.image_1920:
            return True
        for v in p.product_variant_ids:
            if v.image_1920:
                return True
        return False

    def _ckr_get_homepage_listing_image_url(self):
        """URL `web/image` 512 (modèle d’abord, sinon une variante avec binaire)."""
        self.ensure_one()
        p = self.sudo()
        if p.image_1920:
            return f"/web/image/product.template/{p.id}/image_512"
        for v in p.product_variant_ids:
            if v.image_1920:
                return f"/web/image/product.product/{v.id}/image_512"
        return None

    def _ckr_get_homepage_listing_image_fallback_url(self):
        """Visuel CK servi en statique si la fiche n’a aucun binaire image (repli recette)."""
        return "/dorevia_ckreyol_marketplace/static/src/img/selection/ckr_selection_card_fallback.png"

    # ------------------------------------------------------------------
    # Tuile /shop — méta + sous-titre (Lot 1 positioning C-Kreyol)
    # ------------------------------------------------------------------

    def _ckr_shop_tile_has_more_block(self, website=None):
        """True si le panneau sous le bouton info (``fa-info``, corps ``ckr-product-card__details-body``) a du contenu utile.

        (méta catalogue, ligne desc. / sous-titre, ou écart nom commercial vs nom Odoo — voir QWeb.)

        Sert surtout à décider d’afficher le **coin média** sur **/shop/wishlist** (pas de bouton wishlist).
        Sur la grille **/shop**, le bouton **info** est **toujours** rendu dans le rail ; ce flag n’y masque plus l’icône.
        Voir ``docs/mvp_02/SPEC_CK_NOM_CK_TUILE_PRODUIT.md`` et ``NOTE_TECH_TUILE_CORNER_ACTIONS.md``.
        """
        self.ensure_one()
        meta = (self._ckr_get_shop_tile_meta_line(website=website) or "").strip()
        desc = (self._ckr_get_shop_tile_description_line() or "").strip()
        sub = (self._ckr_get_shop_tile_subtitle(website=website) or "").strip()
        extra = desc or sub
        commercial = (self.ck_product_name or "").strip() or (self.name or "").strip()
        odoo_name = (self.name or "").strip()
        if meta or extra:
            return True
        return odoo_name != commercial

    def _ckr_shop_tile_meta_label_is_useful(self, label):
        """True si le libellé vaut une méta « achat » (hors taxonomie générique type *Goods*)."""
        if label is None:
            return False
        text = str(label).strip()
        if not text:
            return False
        return text.lower() not in _CKR_SHOP_TILE_META_WEAK_NAMES

    @api.model
    def _ckr_shop_tile_pretty_format(self, value):
        """Normalise un segment format pour l'affichage visiteur (`100g` -> `100 g`)."""
        text = str(value or "").strip()
        if not text:
            return ""
        text = re.sub(r"\s+", " ", text)
        text = re.sub(r"(?i)(\d)\s*([a-zéè]+)\b", r"\1 \2", text)
        text = re.sub(r"(?i)(\d)\s*[xX]\s*(\d)", r"\1 x \2", text)
        return text.strip()

    @api.model
    def _ckr_shop_tile_extract_format(self, *values):
        """Extrait un format court depuis le nom ou une description si l'UdM est trop faible."""
        for raw in values:
            text = str(raw or "").strip()
            if not text:
                continue
            match = _CKR_SHOP_TILE_FORMAT_RE.search(text)
            if match:
                pretty = self._ckr_shop_tile_pretty_format(match.group(0))
                if pretty:
                    return pretty
        return ""

    @api.model
    def _ckr_shop_tile_compact_text(self, value):
        """Normalisation souple pour comparer deux libellés sans dépendre de la ponctuation."""
        text = str(value or "").lower()
        text = re.sub(r"[^a-z0-9àâçéèêëîïôûùüÿñæœ]+", " ", text)
        return " ".join(text.split())

    def _ckr_shop_tile_first_useful_category_name(self, category_root):
        """Remonte la hiérarchie (``product.public.category`` ou ``product.category``) pour le 1er nom utile.

        Souvent la feuille BO est un regroupement générique (« Tous », « Vente ») alors qu’un parent
        porte un libellé exploitable (« Boissons », « Épicerie »).
        """
        self.ensure_one()
        if not category_root:
            return ""
        seen = set()
        current = category_root
        while current and current.id not in seen:
            seen.add(current.id)
            name = (current.name or "").strip()
            if name and self._ckr_shop_tile_meta_label_is_useful(name):
                return name
            current = current.parent_id
        return ""

    def _ckr_get_shop_tile_family_segment(self):
        """Segment « famille » : 1re catégorie e-commerce utile (avec remontée parents), puis interne."""
        self.ensure_one()
        for cat in self.public_categ_ids.sorted("sequence"):
            hit = self._ckr_shop_tile_first_useful_category_name(cat)
            if hit:
                return hit
        if self.categ_id:
            return self._ckr_shop_tile_first_useful_category_name(self.categ_id)
        return ""

    def _ckr_get_shop_tile_format_segment(self):
        """Segment « format » : UdM produit si elle apporte de l’information (pas *Units* générique)."""
        self.ensure_one()
        uom = self.uom_id
        if not uom:
            return self._ckr_shop_tile_extract_format(
                self.name,
                html2plaintext(self.description_sale or ""),
            )
        name = (uom.name or "").strip()
        if not name:
            return self._ckr_shop_tile_extract_format(
                self.name,
                html2plaintext(self.description_sale or ""),
            )
        key = name.lower().replace(" ", "")
        weak_compact = {w.replace(" ", "") for w in _CKR_SHOP_TILE_WEAK_UOM}
        if key in weak_compact or name.lower() in _CKR_SHOP_TILE_WEAK_UOM:
            return self._ckr_shop_tile_extract_format(
                self.name,
                html2plaintext(self.description_sale or ""),
            )
        return self._ckr_shop_tile_pretty_format(name)

    def _ckr_get_shop_tile_origin_segment(self, website=None):
        """Segment « origine » : profil CK publié si dispo, sinon valeur brute de l’attribut Origine.

        Sur /shop, beaucoup de fiches n’ont pas encore de ``ckr.shop.origin`` publié alors que
        l’attribut catalogue est renseigné : sans ce repli, la méta se réduit à *Unité(s)*.
        """
        self.ensure_one()
        if website is not None:
            short = (self._ckr_get_homepage_origin_short_label(website) or "").strip()
            if short:
                return short
        attr = self._ckr_origin_attribute()
        if not attr:
            return ""
        line = self.attribute_line_ids.filtered(lambda l: l.attribute_id == attr)[:1]
        if not line or not line.value_ids:
            return ""
        vals = line.value_ids.sorted(key=lambda v: ((v.name or "").lower(), v.id))
        name = (vals[0].name or "").strip()
        if not name or not self._ckr_shop_tile_meta_label_is_useful(name):
            return ""
        return name

    def _ckr_get_shop_tile_collection_segment(self, website=None):
        """Segment « collection » de repli si aucune famille produit utile n'est disponible."""
        self.ensure_one()
        collections = self._ckr_get_visible_collections(website=website)
        for collection in collections:
            name = (collection.name or "").strip()
            if name and self._ckr_shop_tile_meta_label_is_useful(name):
                return name
        return ""

    def _ckr_get_shop_tile_description_line(self):
        """Première ligne utile de `description_sale`, nettoyée pour la tuile boutique."""
        self.ensure_one()
        desc = html2plaintext(self.description_sale or "")
        for raw in desc.splitlines():
            line = raw.strip()
            if line:
                return line
        return ""

    def _ckr_get_shop_tile_meta_segments(self, website=None):
        """Segments méta tuile : origine → famille/collection → format, limités à 2 items lisibles."""
        self.ensure_one()
        parts = []
        origin = (self._ckr_get_shop_tile_origin_segment(website=website) or "").strip()
        if origin:
            parts.append(origin)
        family = (self._ckr_get_shop_tile_family_segment() or "").strip()
        if family and family not in parts:
            parts.append(family)
        elif len(parts) < 2:
            collection = (self._ckr_get_shop_tile_collection_segment(website=website) or "").strip()
            if collection and collection not in parts:
                parts.append(collection)
        fmt = (self._ckr_get_shop_tile_format_segment() or "").strip()
        if fmt and fmt not in parts and len(parts) < 2:
            parts.append(fmt)
        return parts

    def _ckr_get_shop_tile_meta_line(self, website=None):
        """Ligne méta affichée au-dessus du titre (ex. « Guadeloupe · 100 g »)."""
        self.ensure_one()
        segs = self._ckr_get_shop_tile_meta_segments(website=website)
        return _CKR_SHOP_TILE_META_SEP.join(segs) if segs else ""

    def _ckr_get_shop_tile_subtitle(self, website=None):
        """Sous-titre court sous le titre : extrait éditorial ou repli catégorie utile.

        Lot 1 : pas de champ dédié — ``description_sale`` en texte brut tronqué, sinon famille
        si elle n’est pas déjà entièrement portée par la méta (évite doublon total).
        """
        self.ensure_one()
        line = self._ckr_get_shop_tile_description_line()
        if line:
            compact_title = self._ckr_shop_tile_compact_text(self.name)
            compact_line = self._ckr_shop_tile_compact_text(line)
            if compact_line and compact_line != compact_title:
                if len(line) > 88:
                    line = line[:85].rstrip() + "…"
                return line
        meta_set = set(self._ckr_get_shop_tile_meta_segments(website=website))
        fmt = (self._ckr_get_shop_tile_format_segment() or "").strip()
        if fmt and fmt not in meta_set:
            return fmt
        collection = (self._ckr_get_shop_tile_collection_segment(website=website) or "").strip()
        if collection and collection not in meta_set:
            return collection
        for cat in self.public_categ_ids.sorted("sequence"):
            cand = self._ckr_shop_tile_first_useful_category_name(cat)
            if cand and cand not in meta_set:
                return cand
        if self.categ_id:
            cand = self._ckr_shop_tile_first_useful_category_name(self.categ_id)
            if cand and cand not in meta_set:
                return cand
        return ""
