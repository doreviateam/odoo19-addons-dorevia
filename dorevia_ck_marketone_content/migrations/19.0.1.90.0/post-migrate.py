# -*- coding: utf-8 -*-
"""Migration 19.0.1.90.0 — seed catalogue MOA (9 produits · images static)."""


def migrate(cr, version):
    from odoo import api, SUPERUSER_ID

    env = api.Environment(cr, SUPERUSER_ID, {})
    from odoo.addons.dorevia_ck_marketone_content.catalog_seed import ensure_catalog_seed
    from odoo.addons.dorevia_ck_marketone_content.hooks import bootstrap_all_marketone_content

    ensure_catalog_seed(env)
    bootstrap_all_marketone_content(env)
