# -*- coding: utf-8 -*-
from odoo import models

_VARIANT_FEATURED_REFRESH_FIELDS = {
    'additional_product_tag_ids',
    'is_published',
    'sale_ok',
}


class ProductProduct(models.Model):
    _inherit = 'product.product'

    def write(self, vals):
        result = super().write(vals)
        if _VARIANT_FEATURED_REFRESH_FIELDS.intersection(vals):
            self.mapped('product_tmpl_id')._ck_refresh_home_featured_products()
        return result
