# -*- coding: utf-8 -*-
from odoo import models

_VARIANT_FEATURED_REFRESH_FIELDS = {
    'additional_product_tag_ids',
    'is_published',
    'sale_ok',
    'lst_price',
}


class ProductProduct(models.Model):
    _inherit = 'product.product'

    def write(self, vals):
        result = super().write(vals)
        if _VARIANT_FEATURED_REFRESH_FIELDS.intersection(vals):
            templates = self.mapped('product_tmpl_id')
            # QA D3 — cohérence avec M1 (product.template) : ne reconstruire la home
            # que si un template concerné appartient aux vedettes (curation peuplée) ;
            # sinon (mode repli auto) comportement large conservé. Évite N rebuilds
            # lors d'un import/màj de masse de lst_price hors « Coups de cœur ».
            if templates and templates._ck_touches_featured():
                templates._ck_refresh_home_featured_products()
        return result
