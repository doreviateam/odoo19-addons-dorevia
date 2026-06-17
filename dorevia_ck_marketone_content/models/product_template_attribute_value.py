# -*- coding: utf-8 -*-
from odoo import models


class ProductTemplateAttributeValue(models.Model):
    _inherit = 'product.template.attribute.value'

    def write(self, vals):
        res = super().write(vals)
        if 'price_extra' in vals:
            templates = self.mapped('ptav_product_variant_ids.product_tmpl_id')
            if templates and templates._ck_touches_featured():
                templates._ck_refresh_home_featured_products()
        return res
