# -*- coding: utf-8 -*-
from odoo import models

from odoo.addons.dorevia_ck_marketone_content.home_featured import (
    FEATURED_CATEGORY_XMLID,
    refresh_home_featured_products,
)


class ProductPublicCategory(models.Model):
    _inherit = 'product.public.category'

    def write(self, vals):
        result = super().write(vals)
        if 'product_tmpl_ids' not in vals:
            return result
        featured = self.env.ref(FEATURED_CATEGORY_XMLID, raise_if_not_found=False)
        if featured and featured in self:
            refresh_home_featured_products(self.env)
        return result
