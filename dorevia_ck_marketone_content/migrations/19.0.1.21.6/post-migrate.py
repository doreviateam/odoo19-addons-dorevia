# -*- coding: utf-8 -*-
"""Migration 21.6 — visuels univers éditables (o_editable) via Website Builder."""


def migrate(cr, version):
    from odoo import api, SUPERUSER_ID

    env = api.Environment(cr, SUPERUSER_ID, {})
    from odoo.addons.dorevia_ck_marketone_content.home_univers import (
        UNIVERS_EDITABLE_MEDIA_MARKER,
        bootstrap_home_univers,
    )

    if not bootstrap_home_univers(env):
        raise RuntimeError('CK univers migration 21.6: bootstrap_home_univers a échoué')
    page = env['website.page'].search([('url', '=', '/')], limit=1)
    arch = page.view_id.arch_db if page and page.view_id else ''
    if isinstance(arch, dict):
        arch = next(iter(arch.values()), '')
    if arch.count(UNIVERS_EDITABLE_MEDIA_MARKER) != 3:
        raise RuntimeError('CK univers migration 21.6: zones image éditables absentes')
