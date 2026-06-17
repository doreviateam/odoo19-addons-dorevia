# -*- coding: utf-8 -*-
"""Migration 21.3 — refresh home S4 (cache-bust visuels univers)."""


def migrate(cr, version):
    from odoo import api, SUPERUSER_ID

    env = api.Environment(cr, SUPERUSER_ID, {})
    from odoo.addons.dorevia_ck_marketone_content.home_univers import (
        UNIVERS_IMAGES_VERSION,
        bootstrap_home_univers,
    )

    if not bootstrap_home_univers(env):
        raise RuntimeError('CK univers migration 21.3: bootstrap_home_univers a échoué')
    page = env['website.page'].search([('url', '=', '/')], limit=1)
    arch = page.view_id.arch_db if page and page.view_id else ''
    if isinstance(arch, dict):
        arch = next(iter(arch.values()), '')
    token = f'?v={UNIVERS_IMAGES_VERSION}'
    if token not in arch:
        raise RuntimeError('CK univers migration 21.3: cache-bust visuels absent')
