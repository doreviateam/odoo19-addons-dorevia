# -*- coding: utf-8 -*-
from odoo import fields, models

from odoo.addons.dorevia_ck_marketone_content.nav_v22_config import (
    MEGA_MENU_ARTISANAT,
    MEGA_MENU_BOISSONS,
    MEGA_MENU_EPICERIE,
    MEGA_MENU_MAISON,
    NAV_MAISON_LABEL,
)


class CkMegaMenuRayonVisual(models.Model):
    """Visuel éditorial permanent par rayon (identité), distinct de
    ck.mega.menu.visual.block qui porte les campagnes datées colonne 4.

    P4 — gouvernance : ce visuel illustre le RAYON (Épicerie, Boissons...),
    jamais un produit précis — le nom du produit éventuellement utilisé
    comme image ne doit pas apparaître dans title/subtitle.
    """

    _name = 'ck.mega.menu.rayon.visual'
    _description = 'Visuel éditorial permanent — rayon mega-menu header CK'
    _order = 'id'

    MENU_SELECTION = [
        (MEGA_MENU_EPICERIE, 'Épicerie'),
        (MEGA_MENU_BOISSONS, 'Boissons'),
        (MEGA_MENU_MAISON, NAV_MAISON_LABEL),
        (MEGA_MENU_ARTISANAT, 'Artisanat'),
    ]

    menu_key = fields.Selection(
        selection=MENU_SELECTION,
        string='Rayon',
        required=True,
        index=True,
    )
    image = fields.Image(string='Image', required=True, max_width=1920, max_height=1920)
    title = fields.Char(string='Titre éditorial', required=True, size=60)
    subtitle = fields.Char(string='Sous-titre éditorial', size=120)
    active = fields.Boolean(default=True)

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
