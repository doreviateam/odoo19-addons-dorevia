# -*- coding: utf-8 -*-
"""Migration 21.11 — markup éditeur S4 (sans cover link, data-href, img dans p)."""


def migrate(cr, version):
    from odoo import api, SUPERUSER_ID

    env = api.Environment(cr, SUPERUSER_ID, {})
    from odoo.addons.dorevia_ck_marketone_content.home_univers import (
        bootstrap_home_univers,
        univers_arch_is_valid,
    )

    if not bootstrap_home_univers(env):
        raise RuntimeError('CK univers migration 21.11: bootstrap_home_univers a échoué')
    page = env['website.page'].search([('url', '=', '/')], limit=1)
    arch = page.view_id.arch_db if page and page.view_id else ''
    if isinstance(arch, dict):
        arch = next(iter(arch.values()), '')
    if not univers_arch_is_valid(arch):
        raise RuntimeError('CK univers migration 21.11: arch S4 invalide après bootstrap')
    if 'ck-univers-card__cover' in arch:
        raise RuntimeError('CK univers migration 21.11: cover link encore présent')
