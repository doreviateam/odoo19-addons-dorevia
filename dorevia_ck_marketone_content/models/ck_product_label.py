# -*- coding: utf-8 -*-
from odoo import fields, models


class DoreviaCkProductLabel(models.Model):
    _name = 'dorevia.ck.product.label'
    _description = 'Étiquette card home CK'
    _order = 'sequence, name'

    name = fields.Char(required=True, translate=True)
    sequence = fields.Integer(default=10)
    active = fields.Boolean(default=True)
