# -*- coding: utf-8 -*-


def migrate(cr, version):
    from odoo import SUPERUSER_ID, api

    env = api.Environment(cr, SUPERUSER_ID, {})
    from odoo.addons.dorevia_membership_adhesions.hooks import sync_root_app_menu_name

    sync_root_app_menu_name(env)
