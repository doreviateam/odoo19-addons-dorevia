# -*- coding: utf-8 -*-
from odoo import fields, models


class WebsiteMenu(models.Model):
    _inherit = 'website.menu'

    ck_nav_css_class = fields.Char(
        string='CK nav CSS class',
        help='Classe CSS optionnelle pour le rendu header Nav V2 (desktop/mobile).',
    )
