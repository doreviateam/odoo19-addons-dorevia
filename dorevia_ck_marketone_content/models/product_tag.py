# -*- coding: utf-8 -*-
from odoo import models

_TAG_REFRESH_FIELDS = {'name', 'sequence', 'active', 'visible_to_customers'}


class ProductTag(models.Model):
    _inherit = 'product.tag'

    def _ck_featured_templates_for_tags(self):
        return self.env['product.template'].sudo().search([
            '|',
            ('product_tag_ids', 'in', self.ids),
            ('product_variant_ids.additional_product_tag_ids', 'in', self.ids),
        ])

    def _ck_refresh_home_featured_for_tagged_products(self):
        templates = self._ck_featured_templates_for_tags()
        if templates:
            templates._ck_refresh_home_featured_products()

    def write(self, vals):
        templates = self._ck_featured_templates_for_tags() if _TAG_REFRESH_FIELDS.intersection(vals) else None
        result = super().write(vals)
        if templates:
            templates._ck_refresh_home_featured_products()
        return result

    def unlink(self):
        templates = self._ck_featured_templates_for_tags()
        result = super().unlink()
        if templates:
            templates._ck_refresh_home_featured_products()
        return result
