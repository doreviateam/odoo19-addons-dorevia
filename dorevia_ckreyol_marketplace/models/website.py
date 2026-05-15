# -*- coding: utf-8 -*-
"""Extension de ``website`` — canonical maîtrisé pour les portes CK.

Le canonical natif d'Odoo (``website._get_canonical_url``) passe par
``ir_http._url_localized`` qui **supprime systématiquement la query
string** (commentaire explicite dans le code natif : *« canonical URLs
should not have qs »*). Ce comportement est sain par défaut, mais entre
en conflit avec la configuration gelée des portes Hybride H1 :

* **Kits / Pack**   → canonical attendu : ``/shop?ckr_mode=pack``.
* **Promotions**    → canonical attendu : ``/shop?ckr_mode=promo``.
* **Incontournables** → canonical attendu : ``/shop?ckr_mode=featured``.
* **Origines**      → canonical attendu : ``/shop?ckr_mode=origin``
  (+ ``ckr_origin=<slug>`` éventuellement répété, avec
  **déduplication** et **tri lexicographique** SPEC_IMPL §3.4).

Décision : rétablir les paramètres CK dans le canonical **uniquement**
pour les requêtes ``/shop`` portant déjà un mode CK **whitelisté**.
Respecte la destination commerciale unique ``/shop`` (ADR-CKR-007)
tout en préservant le **contexte de lecture** qui fait la porte
(ADR-CKR-008).

Aucune autre URL n'est affectée : le comportement natif reste la règle
générale, l'extension se limite strictement au couple
(path=``/shop``, ckr_mode ∈ whitelist).
"""
import logging
from urllib.parse import urlencode as _ckr_urlencode_query

from odoo import api, fields, models
from odoo.http import request

# Import local pour éviter les dépendances circulaires / charger la
# whitelist et le paramètre une seule fois, au chargement du module. La
# source de vérité du nom du paramètre et des valeurs admises reste
# ``controllers/website_sale_ckr.py`` — ce modèle se limite à les
# consommer.
from odoo.addons.dorevia_ckreyol_marketplace.controllers.website_sale_ckr import (
    CKR_CANONICAL_PATH,
    CKR_CATEGORY_PARAM,
    CKR_COLLECTION_QUERY_PARAM,
    CKR_COLLECTION_SCOPE_ALL,
    CKR_COLLECTION_SCOPE_PARAM,
    CKR_MODE_PARAM,
    CKR_ORIGIN_PARAM,
    _ckr_canonical_category_slugs,
    _ckr_canonical_origin_slugs,
    _ckr_candidate_modes,
    _ckr_mode_sort_key,
)

_logger = logging.getLogger(__name__)


class Website(models.Model):
    _inherit = "website"

    ckr_homepage_featured_1 = fields.Many2one(
        "product.template",
        string="Accueil — Produit 1/4 (sélection)",
        ondelete="set null",
        domain="[('sale_ok', '=', True)]",
    )
    ckr_homepage_featured_2 = fields.Many2one(
        "product.template",
        string="Accueil — Produit 2/4 (sélection)",
        ondelete="set null",
        domain="[('sale_ok', '=', True)]",
    )
    ckr_homepage_featured_3 = fields.Many2one(
        "product.template",
        string="Accueil — Produit 3/4 (sélection)",
        ondelete="set null",
        domain="[('sale_ok', '=', True)]",
    )
    ckr_homepage_featured_4 = fields.Many2one(
        "product.template",
        string="Accueil — Produit 4/4 (sélection)",
        ondelete="set null",
        domain="[('sale_ok', '=', True)]",
    )

    @api.model
    def ckr_ensure_showcase_featured_on_empty_websites(self):
        """Remplit les 4 emplacements « Sélection accueil » si tous vides.

        S'appuie sur les fiches vitrine ``data/ckr_product_selection_showcase_data.xml``
        (Crêpes, Bière, Sucre de canne, Chips). Ne remplace **pas** une
        configuration partielle ou complète existante (choix MOA / recette).
        Idempotent : rejouable à l'upgrade (migration) et à l'install (hook).
        """
        xmlids = (
            "dorevia_ckreyol_marketplace.product_template_ckr_sel_crepes",
            "dorevia_ckreyol_marketplace.product_template_ckr_sel_biere",
            "dorevia_ckreyol_marketplace.product_template_ckr_sel_sucre",
            "dorevia_ckreyol_marketplace.product_template_ckr_sel_chips",
        )
        pids = []
        for x in xmlids:
            rec = self.env.ref(x, raise_if_not_found=False)
            if not rec:
                _logger.warning(
                    "[C-Kreyol] vitrine sélection : xmlid %s introuvable, abandon.",
                    x,
                )
                return
            pids.append(rec.id)
        Product = self.env["product.template"]
        for website in self.search([]):
            if any(
                (
                    website.ckr_homepage_featured_1,
                    website.ckr_homepage_featured_2,
                    website.ckr_homepage_featured_3,
                    website.ckr_homepage_featured_4,
                )
            ):
                continue
            if any(not Product.browse(pid).exists() for pid in pids):
                return
            website.sudo().write(
                {
                    "ckr_homepage_featured_1": pids[0],
                    "ckr_homepage_featured_2": pids[1],
                    "ckr_homepage_featured_3": pids[2],
                    "ckr_homepage_featured_4": pids[3],
                }
            )
            _logger.info(
                "[C-Kreyol] site %r : 4 fiches vitrine affectées (sélection accueil).",
                website.name,
            )

    def _get_ckr_homepage_resolved_featured_product_list(self, max_slots=4):
        """Jusqu'à 4 `product.template` **avec visuel** (ordre BO puis catalogue).

        Règles (recette visuelle NO-GO corrigée) : un emplacement BO sans
        image « exploitable » est **sauté** et remplacé par le prochain
        produit du site remplissant `website_sale` + image (pas de
        placeholder gris Odoo en grille).
        """
        self.ensure_one()
        website = self
        out = []
        used = set()

        def _eligible(tmpl):
            t = tmpl.sudo()
            if t.id in used:
                return False
            if not t.sale_ok or not t.active:
                return False
            if not t.website_published:
                return False
            if t.website_id and t.website_id != website:
                return False
            return t._ckr_has_homepage_listing_image()

        def _push(tmpl):
            if not tmpl or not _eligible(tmpl):
                return False
            out.append(tmpl.sudo())
            used.add(tmpl.sudo().id)
            return True

        for tmpl in (
            self.ckr_homepage_featured_1,
            self.ckr_homepage_featured_2,
            self.ckr_homepage_featured_3,
            self.ckr_homepage_featured_4,
        ):
            if len(out) >= max_slots:
                break
            if tmpl:
                _push(tmpl)

        if len(out) < max_slots:
            domain = [
                ("sale_ok", "=", True),
                ("active", "=", True),
                ("website_published", "=", True),
                "|",
                ("website_id", "=", False),
                ("website_id", "=", website.id),
            ]
            if used:
                domain.append(("id", "not in", list(used)))
            pool = (
                self.env["product.template"]
                .sudo()
                .search(
                    domain,
                    order="website_sequence asc, id desc",
                    limit=80,
                )
            )
            for tmpl in pool:
                if len(out) >= max_slots:
                    break
                _push(tmpl)
        return out[:max_slots]

    def _get_ckr_homepage_featured_product_list(self):
        return self._get_ckr_homepage_resolved_featured_product_list()

    def _get_ckr_homepage_selection_cards(self):
        """Données QWeb : prix dynamique, règle §9.4 sur l'affichage origine.
        (DECISION_PRODUITS_HOMEPAGE_MVP21, PROPOSITION_HOMEPAGE §9.4)
        """
        if not request:
            return []
        self.ensure_one()
        products = self._get_ckr_homepage_featured_product_list()
        if not products:
            return []
        n = len(products)
        with_l = sum(
            1 for p in products if p._ckr_get_homepage_origin_short_label(self)
        )
        show_origin_line = n > 0 and (with_l / n) >= 0.8
        out = []
        for p in products:
            img_url = p._ckr_get_homepage_listing_image_url()
            if not img_url:
                img_url = p._ckr_get_homepage_listing_image_fallback_url()
            out.append(
                {
                    "product": p,
                    "combination_info": p.sudo()._ckr_get_homepage_combination_info(),
                    "listing_image_url": img_url,
                    "show_origin": show_origin_line,
                    "origin": (
                        p._ckr_get_homepage_origin_short_label(self)
                        if show_origin_line
                        else ""
                    ),
                }
            )
        return out

    def _get_canonical_url(self):
        url = super()._get_canonical_url()
        if not request or not getattr(request, "httprequest", None):
            return url

        # Restreint à la page grille boutique + paramètres CK (modes cumulables,
        # facettes catégories, origines, collections).
        # ``path`` peut être ``/shop`` ou ``/<langue>/shop`` (routage website).
        path = request.httprequest.path or ""
        if not path.endswith(CKR_CANONICAL_PATH):
            return url

        modes = sorted(_ckr_candidate_modes(), key=_ckr_mode_sort_key)
        params = [(CKR_MODE_PARAM, m) for m in modes]
        for slug in _ckr_canonical_category_slugs():
            params.append((CKR_CATEGORY_PARAM, slug))
        for slug in _ckr_canonical_origin_slugs():
            params.append((CKR_ORIGIN_PARAM, slug))
        args = request.httprequest.args
        scope = (args.get(CKR_COLLECTION_SCOPE_PARAM) or "").strip().lower()
        cols_sorted = sorted(
            {
                (s or "").strip().lower()
                for s in args.getlist(CKR_COLLECTION_QUERY_PARAM)
                if (s or "").strip()
            }
        )
        if scope == CKR_COLLECTION_SCOPE_ALL:
            params.append(
                (CKR_COLLECTION_SCOPE_PARAM, CKR_COLLECTION_SCOPE_ALL)
            )
        for col in cols_sorted:
            params.append((CKR_COLLECTION_QUERY_PARAM, col))
        if not params:
            return url

        separator = "&" if "?" in url else "?"
        # ``urllib.parse.urlencode`` préserve les clés répétées (ex. plusieurs
        # ``ckr_mode``), contrairement à certains raccourcis werkzeug selon versions.
        return f"{url}{separator}{_ckr_urlencode_query(params)}"
