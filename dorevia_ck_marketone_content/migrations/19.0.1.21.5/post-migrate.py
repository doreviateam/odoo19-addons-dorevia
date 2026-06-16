# -*- coding: utf-8 -*-
"""Migration 21.5 — en-tête S4 aligné à gauche."""


def migrate(cr, version):
    from odoo import api, SUPERUSER_ID

    env = api.Environment(cr, SUPERUSER_ID, {})
    from odoo.addons.dorevia_ck_marketone_content.home_univers import bootstrap_home_univers

    if not bootstrap_home_univers(env):
        raise RuntimeError('CK univers migration 21.5: bootstrap_home_univers a échoué')
    page = env['website.page'].search([('url', '=', '/')], limit=1)
    arch = page.view_id.arch_db if page and page.view_id else ''
    if isinstance(arch, dict):
        arch = next(iter(arch.values()), '')
    if 'ck-univers-cards__head text-center' in arch:
        raise RuntimeError('CK univers migration 21.5: en-tête encore centré')
