# -*- coding: utf-8 -*-
"""Navigation Communauté — sync chirurgical header (sans bootstrap complet).

La migration 39 initiale appelait bootstrap_ck_navigation : si le catalogue
était temporairement dépublié, les rayons Boissons / Maison / Artisanat étaient
supprimés. Ce script ne touche qu'à l'entrée Communauté.
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
