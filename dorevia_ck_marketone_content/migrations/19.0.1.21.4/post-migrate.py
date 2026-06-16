# -*- coding: utf-8 -*-
"""Migration 21.4 — visuels MOA officiels S4 (épicerie, soin, artisanat)."""


def migrate(cr, version):
    from odoo import api, SUPERUSER_ID

    env = api.Environment(cr, SUPERUSER_ID, {})
    from odoo.addons.dorevia_ck_marketone_content.home_univers import (
        UNIVERS_IMAGES_VERSION,
        bootstrap_home_univers,
    )

    if not bootstrap_home_univers(env):
        raise RuntimeError('CK univers migration 21.4: bootstrap_home_univers a échoué')
    page = env['website.page'].search([('url', '=', '/')], limit=1)
    arch = page.view_id.arch_db if page and page.view_id else ''
    if isinstance(arch, dict):
        arch = next(iter(arch.values()), '')
    if f'?v={UNIVERS_IMAGES_VERSION}' not in arch:
        raise RuntimeError('CK univers migration 21.4: cache-bust visuels MOA absent')
