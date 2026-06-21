# -*- coding: utf-8 -*-
from odoo import models

# Champs du ruban e-commerce visibles sur le badge de la carte vedette.
_RIBBON_REFRESH_FIELDS = {'name', 'bg_color', 'text_color'}


class ProductRibbon(models.Model):
    _inherit = 'product.ribbon'

    def _ck_featured_templates_for_ribbon(self):
        return self.env['product.template'].sudo().search([
            ('website_ribbon_id', 'in', self.ids),
        ])

    def write(self, vals):
        templates = (
            self._ck_featured_templates_for_ribbon()
            if _RIBBON_REFRESH_FIELDS.intersection(vals)
            else None
        )
        result = super().write(vals)
        # Scopé curation (cohérent M1/D3) : rebuild seulement si un produit en vedette
        # porte ce ruban.
        if templates and templates._ck_touches_featured():
            templates._ck_refresh_home_featured_products()
        return result
