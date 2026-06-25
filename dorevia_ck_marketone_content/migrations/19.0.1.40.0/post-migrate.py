# -*- coding: utf-8 -*-
"""Correctif QA Communauté — restauration catalogue seed + menus rayons.

Répare les instances ayant subi la migration 39.0 initiale (bootstrap seul
sur catalogue partiellement dépublié).
"""
from odoo.addons.dorevia_ck_marketone_content.catalog_seed_guard import (
    ensure_moa_seed_catalog_published,
)
from odoo.addons.dorevia_ck_marketone_content.nav_sync import (
    bootstrap_ck_navigation,
    sync_communaute_header,
)


def migrate(cr, version):
    from odoo import api, SUPERUSER_ID

    env = api.Environment(cr, SUPERUSER_ID, {})
    ensure_moa_seed_catalog_published(env)
    sync_communaute_header(env)
    bootstrap_ck_navigation(env)
