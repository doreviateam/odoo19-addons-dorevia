# -*- coding: utf-8 -*-

from odoo.addons.dorevia_ck_theme.hooks import is_marketone_content_installed


def migrate(cr, version):
    from odoo import api, SUPERUSER_ID

    env = api.Environment(cr, SUPERUSER_ID, {})
    if not is_marketone_content_installed(env):
        return
    from odoo.addons.dorevia_ck_marketone_content.hooks import bootstrap_all_marketone_content

    bootstrap_all_marketone_content(env)
