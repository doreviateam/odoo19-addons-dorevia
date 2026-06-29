# -*- coding: utf-8 -*-
from odoo import models

from odoo.addons.dorevia_ck_theme.product_card_ribbon import ck_product_ribbon_badge_class


class ProductRibbon(models.Model):
    _inherit = 'product.ribbon'

    def get_ck_card_badge_class(self):
        """Classe sémantique badge card grille — parité Home ``home_featured``."""
        if not self:
            return 'badge-ribbon'
        self.ensure_one()
        return ck_product_ribbon_badge_class(self)
