# -*- coding: utf-8 -*-
"""Nav-U2 — applique la classe racine boutique sur l'entrée /shop existante."""
from odoo.addons.dorevia_ck_marketone_content.nav_sync import sync_shop_root_icon_header


def migrate(cr, version):
    from odoo import api, SUPERUSER_ID

    env = api.Environment(cr, SUPERUSER_ID, {})
    sync_shop_root_icon_header(env)
