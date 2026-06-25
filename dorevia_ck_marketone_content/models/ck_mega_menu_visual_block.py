# -*- coding: utf-8 -*-
from odoo import fields, models

from odoo.addons.dorevia_ck_marketone_content.nav_v22_config import (
    MEGA_MENU_ARTISANAT,
    MEGA_MENU_BOISSONS,
    MEGA_MENU_EPICERIE,
    MEGA_MENU_MAISON,
    NAV_MAISON_LABEL,
)


class CkMegaMenuVisualBlock(models.Model):
    _name = 'ck.mega.menu.visual.block'
    _description = 'Bloc visuel mega-menu header CK'
    _order = 'sequence, id'

    MENU_SELECTION = [
        (MEGA_MENU_EPICERIE, 'Épicerie'),
        (MEGA_MENU_BOISSONS, 'Boissons'),
        (MEGA_MENU_MAISON, NAV_MAISON_LABEL),
        (MEGA_MENU_ARTISANAT, 'Artisanat'),
    ]

    name = fields.Char(string='Référence interne', required=True)
    menu_key = fields.Selection(
        selection=MENU_SELECTION,
        string='Menu concerné',
        required=True,
        index=True,
    )
    image = fields.Image(string='Image', required=True, max_width=1920, max_height=1920)
    title = fields.Char(string='Titre', required=True, size=60)
    subtitle = fields.Char(string='Sous-titre', size=120)
    target_url = fields.Char(string='Lien cible', required=True)
    cta_label = fields.Char(string='Libellé CTA', required=True, size=30, default='Découvrir')
    date_start = fields.Date(string='Date début')
    date_end = fields.Date(string='Date fin')
    active = fields.Boolean(default=True)
    sequence = fields.Integer(default=10)

    def _ck_refresh_navigation(self):
        from odoo.addons.dorevia_ck_marketone_content.nav_sync import bootstrap_ck_navigation
        bootstrap_ck_navigation(self.env)

    def create(self, vals_list):
        records = super().create(vals_list)
        records._ck_refresh_navigation()
        return records

    def write(self, vals):
        result = super().write(vals)
        self._ck_refresh_navigation()
        return result

    def unlink(self):
        result = super().unlink()
        self._ck_refresh_navigation()
        return result
