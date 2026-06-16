# -*- coding: utf-8 -*-
"""Migration 19.0.1.21.1 — correctifs QA Section 4 (lien Épicerie + Coffrets)."""


def migrate(cr, version):
    from odoo import api, SUPERUSER_ID

    env = api.Environment(cr, SUPERUSER_ID, {})
    from odoo.addons.dorevia_ck_marketone_content.home_univers import bootstrap_home_univers
    from odoo.addons.dorevia_ck_marketone_content.home_discovery_pack import (
        bootstrap_home_discovery_pack,
        discovery_pack_arch_is_valid,
    )

    if not bootstrap_home_univers(env):
        raise RuntimeError('CK univers migration 21.1: bootstrap_home_univers a échoué')
    page = env['website.page'].search([('url', '=', '/')], limit=1)
    arch = page.view_id.arch_db if page and page.view_id else ''
    if isinstance(arch, dict):
        arch = next(iter(arch.values()), '')
    if '/shop/category/epicerie-1' not in arch and 'epicerie-1' not in arch:
        raise RuntimeError('CK univers migration 21.1: lien Épicerie créole absent')
    if not discovery_pack_arch_is_valid(arch):
        if not bootstrap_home_discovery_pack(env):
            raise RuntimeError('CK univers migration 21.1: Coffrets découverte absent')
