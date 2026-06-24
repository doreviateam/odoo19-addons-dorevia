# -*- coding: utf-8 -*-
"""P3 pilote — fallback éditorial CK colonne 4 mega-menu : re-sync navigation."""

from odoo.addons.dorevia_ck_marketone_content.nav_sync import bootstrap_ck_navigation


def migrate(cr, version):
    from odoo import api, SUPERUSER_ID

    env = api.Environment(cr, SUPERUSER_ID, {})
    bootstrap_ck_navigation(env)
