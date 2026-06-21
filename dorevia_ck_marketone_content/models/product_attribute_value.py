# -*- coding: utf-8 -*-
from odoo import models


class ProductAttributeValue(models.Model):
    _inherit = 'product.attribute.value'

    def _ck_featured_templates_for_values(self):
        """Templates dont une variante porte une de ces valeurs d'attribut."""
        ptavs = self.env['product.template.attribute.value'].sudo().search([
            ('product_attribute_value_id', 'in', self.ids),
        ])
        return ptavs.mapped('ptav_product_variant_ids.product_tmpl_id')

    def write(self, vals):
        # Le titre des cards multi-variantes vient du nom de la valeur d'attribut
        # (ex. « salé » / « sucré »). Capter le renommage AVANT super().
        templates = (
            self._ck_featured_templates_for_values()
            if 'name' in vals
            else None
        )
        result = super().write(vals)
        if templates and templates._ck_touches_featured():
            templates._ck_refresh_home_featured_products()
        return result
