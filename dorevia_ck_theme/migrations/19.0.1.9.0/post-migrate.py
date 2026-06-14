# -*- coding: utf-8 -*-
"""Split thème / contenu — le thème ne seed plus de pages métier (§4bis)."""

from odoo.addons.dorevia_ck_theme.hooks import remove_legacy_phase3_script_view


def migrate(cr, version):
    from odoo import api, SUPERUSER_ID

    env = api.Environment(cr, SUPERUSER_ID, {})
    remove_legacy_phase3_script_view(env)
