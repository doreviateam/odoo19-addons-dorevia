# -*- coding: utf-8 -*-
"""Extension ``website_sale`` — portes catalogue via ``_search_get_detail``."""

from odoo import models

_MARKETONE_EMPTY_DOMAIN = [("id", "=", 0)]


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def _marketone_origin_attribute(self):
        return self.env.ref(
            "dorevia_ckreyol_marketone.marketone_product_attribute_origin",
            raise_if_not_found=False,
        )

    def _marketone_get_origin_shop_lines(self, website=None):
        """Lignes origine pour la fiche produit : label + URL porte (retail-first)."""
        self.ensure_one()
        attribute = self._marketone_origin_attribute()
        if not attribute:
            return []
        website = website or self.env["website"].get_current_website()
        value_ids = self.attribute_line_ids.filtered(
            lambda line: line.attribute_id == attribute
        ).value_ids
        if not value_ids:
            return []
        Origin = self.env["marketone.shop.origin"].sudo()
        profiles = Origin.search(
            [
                ("attribute_value_id", "in", value_ids.ids),
                ("website_published", "=", True),
                ("website_id", "in", [False, website.id]),
            ]
        )
        by_value = {}
        for profile in profiles:
            vid = profile.attribute_value_id.id
            if vid not in by_value or (
                profile.website_id
                and profile.website_id.id == website.id
            ):
                by_value[vid] = profile
        lines = []
        for value in value_ids:
            profile = by_value.get(value.id)
            label = (
                profile.display_name_visitor
                if profile
                else value.name
            )
            if profile:
                url = (
                    f"/shop?marketone_mode=origin"
                    f"&marketone_origin={profile.slug}"
                )
            else:
                url = None
            lines.append({"label": label, "url": url})
        return lines

    def _search_get_detail(self, website, order, options):
        detail = super()._search_get_detail(website, order, options)
        base_domain = list(detail.get("base_domain") or [])

        if options.get("marketone_featured_only"):
            if options.get("marketone_featured_category_invalid"):
                base_domain.append(_MARKETONE_EMPTY_DOMAIN)
            elif category_id := options.get("marketone_featured_category_id"):
                base_domain.append([("public_categ_ids", "in", [category_id])])
            else:
                base_domain.append(_MARKETONE_EMPTY_DOMAIN)

        if options.get("marketone_origin_mode"):
            if options.get("marketone_origin_invalid"):
                base_domain.append(_MARKETONE_EMPTY_DOMAIN)
            elif value_ids := options.get("marketone_origin_attribute_value_ids"):
                base_domain.append(
                    [("attribute_line_ids.value_ids", "in", list(value_ids))]
                )

        detail["base_domain"] = base_domain
        return detail
