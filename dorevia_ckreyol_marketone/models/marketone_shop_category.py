# -*- coding: utf-8 -*-
"""Catégories e-commerce principales — sidebar /shop (ADR-029)."""

from odoo import api, models

# Ordre MOA des rayons (liste cible ADR-029 / mapping recette).
# Résolution par libellé + website_id : choix transitoire documenté — voir
# ``_marketone_primary_public_category_ids`` (config) pour une évolution stable.
MARKETONE_PRIMARY_PUBLIC_CATEGORY_NAMES = (
    "Biscuits salés",
    "Biscuits sucrés",
    "Épices",
    "Assaisonnements",
    "Sauces",
    "Condiments",
    "Confitures",
    "Sirops",
    "Boissons",
    "Farines",
    "Fécules",
    "Kits & Coffrets",
    "Miels",
)

MARKETONE_SECONDARY_PUBLIC_CATEGORY_NAMES = frozenset(
    {
        "Incontournables",
        "Apéritif créole",
        "Cuisine du manioc",
        "Idées cadeaux",
    }
)

MARKETONE_PRIMARY_CATEGORY_IDS_PARAM = (
    "dorevia_ckreyol_marketone.primary_public_category_ids"
)


class ProductPublicCategory(models.Model):
    _inherit = "product.public.category"

    @api.model
    def _marketone_primary_public_category_ids_from_param(self, website):
        """IDs ordonnés depuis ir.config_parameter (résolution stable optionnelle)."""
        raw = (
            self.env["ir.config_parameter"]
            .sudo()
            .get_param(MARKETONE_PRIMARY_CATEGORY_IDS_PARAM, "")
            or ""
        )
        ids = []
        for part in raw.split(","):
            part = part.strip()
            if part.isdigit():
                ids.append(int(part))
        if not ids:
            return []
        records = self.sudo().browse(ids).exists()
        id_to_rec = {rec.id: rec for rec in records}
        return [id_to_rec[i].id for i in ids if i in id_to_rec]

    @api.model
    def _marketone_primary_public_categories(self, website=None):
        """Catégories principales pour la sidebar /shop (publiées, avec produits)."""
        website = website or self.env["website"].get_current_website()
        Category = self.sudo()
        param_ids = self._marketone_primary_public_category_ids_from_param(website)
        if param_ids:
            categories = Category.browse(param_ids).exists()
        else:
            all_on_site = Category.search([("website_id", "=", website.id)])
            by_name = {rec.name: rec for rec in all_on_site}
            categories = Category.browse()
            for name in MARKETONE_PRIMARY_PUBLIC_CATEGORY_NAMES:
                rec = by_name.get(name)
                if rec:
                    categories |= rec
        if not self.env.user._is_internal():
            categories = categories.filtered("has_published_products")
        return categories

    @api.model
    def _marketone_primary_public_categories_for_shop(
        self, search_product, active_category_ids=None, website=None
    ):
        """Principales visibles sidebar (C4) : allowlist ∩ produits du contexte ∪ actives.

        ``search_product`` doit refléter le périmètre boutique **sans** la facette
        ``marketone_category`` (multi OR) — voir le contrôleur.
        """
        website = website or self.env["website"].get_current_website()
        allowlist = self._marketone_primary_public_categories(website=website)
        allowlist_ids = set(allowlist.ids)
        active_ids = set(active_category_ids or [])
        if not search_product:
            return allowlist.filtered(lambda rec: rec.id in active_ids)
        grouped = self.env["product.template"]._read_group(
            domain=[("id", "in", search_product.ids)],
            groupby=["public_categ_ids"],
        )
        categ_ids_with_products = {
            group[0].id
            for group in grouped
            if group[0] and group[0].id in allowlist_ids
        }
        return allowlist.filtered(
            lambda rec: rec.id in categ_ids_with_products or rec.id in active_ids
        )

    @api.model
    def _marketone_resolve_primary_categories_from_slugs(self, slugs, website=None):
        """Résout les slugs vers des principales publiées (allowlist sidebar)."""
        website = website or self.env["website"].get_current_website()
        slugs = [s.strip() for s in (slugs or []) if (s or "").strip()]
        if not slugs:
            return self.browse()
        primaries = self._marketone_primary_public_categories(website=website)
        if not primaries:
            return self.browse()
        ir_http = self.env["ir.http"].sudo()
        want = set(slugs)
        return primaries.filtered(lambda rec: ir_http._slug(rec) in want)
