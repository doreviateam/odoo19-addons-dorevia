# -*- coding: utf-8 -*-
from odoo import models


class ProductPublicCategory(models.Model):
    _inherit = 'product.public.category'

    # Homepage « Nos coups de cœur » pilotée par product.template.ck_is_featured
    # depuis 19.0.1.28.3 — plus de refresh sur write catégorie.
