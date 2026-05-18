# -*- coding: utf-8 -*-
"""Extension ``website_sale`` — filtre porte Incontournables via ``_search_get_detail``."""

from odoo import models

_MARKETONE_EMPTY_DOMAIN = [("id", "=", 0)]


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def _search_get_detail(self, website, order, options):
        detail = super()._search_get_detail(website, order, options)
        if not options.get("marketone_featured_only"):
            return detail
        base_domain = list(detail.get("base_domain") or [])
        if options.get("marketone_featured_category_invalid"):
            base_domain.append(_MARKETONE_EMPTY_DOMAIN)
        elif category_id := options.get("marketone_featured_category_id"):
            base_domain.append([("public_categ_ids", "in", [category_id])])
        else:
            base_domain.append(_MARKETONE_EMPTY_DOMAIN)
        detail["base_domain"] = base_domain
        return detail
