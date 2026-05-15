# -*- coding: utf-8 -*-
"""Migration 19.0.1.10.67 : menu Communauté + sous-menus."""

from odoo.api import Environment, SUPERUSER_ID

from odoo.addons.dorevia_ckreyol_marketplace.hooks import _sync_ckr_menus


def migrate(cr, version):
    env = Environment(cr, SUPERUSER_ID, {})
    _sync_ckr_menus(env)
