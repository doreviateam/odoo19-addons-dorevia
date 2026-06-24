# -*- coding: utf-8 -*-
from odoo import models


class ProductPublicCategory(models.Model):
    _inherit = 'product.public.category'

    # Homepage « Nos coups de cœur » pilotée par product.template.ck_is_featured
    # depuis 19.0.1.28.3 — plus de refresh sur write catégorie.

    def get_ck_rayon_editorial(self):
        """Contenu éditorial de rayon P2B (cf. shop_rayon_editorial.py), ou None."""
        self.ensure_one()
        from ..shop_rayon_editorial import get_rayon_editorial
        return get_rayon_editorial(self.env, self)
