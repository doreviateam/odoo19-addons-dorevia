# -*- coding: utf-8 -*-
"""Filtre catalogue — facettes collections commerciales (Lot B)."""

from odoo import models

_MARKETONE_EMPTY_DOMAIN = [("id", "=", 0)]


class ProductTemplate(models.Model):
    _inherit = "product.template"

    def _search_get_detail(self, website, order, options):
        detail = super()._search_get_detail(website, order, options)
        base_domain = list(detail.get("base_domain") or [])

        if collection_ids := options.get("marketone_collection_ids"):
            collections = (
                self.env["marketone.shop.collection"]
                .sudo()
                .browse(list(collection_ids))
            )
            product_ids = list(set(collections.mapped("product_ids").ids))
            if product_ids:
                base_domain.append([("id", "in", product_ids)])
            else:
                base_domain.append(_MARKETONE_EMPTY_DOMAIN)

        detail["base_domain"] = base_domain
        return detail
