# -*- coding: utf-8 -*-
"""Migration 21.7 — cards univers éditables individuellement (o_editable_media + sous-snippet)."""


def migrate(cr, version):
    from odoo import api, SUPERUSER_ID

    env = api.Environment(cr, SUPERUSER_ID, {})
    from odoo.addons.dorevia_ck_marketone_content.home_univers import (
        UNIVERS_CARD_SNIPPET,
        UNIVERS_EDITABLE_MEDIA_MARKER,
        bootstrap_home_univers,
    )

    if not bootstrap_home_univers(env):
        raise RuntimeError('CK univers migration 21.7: bootstrap_home_univers a échoué')
    page = env['website.page'].search([('url', '=', '/')], limit=1)
    arch = page.view_id.arch_db if page and page.view_id else ''
    if isinstance(arch, dict):
        arch = next(iter(arch.values()), '')
    if arch.count(f'data-snippet="{UNIVERS_CARD_SNIPPET}"') != 3:
        raise RuntimeError('CK univers migration 21.7: sous-snippets card absents')
    if arch.count(UNIVERS_EDITABLE_MEDIA_MARKER) != 3:
        raise RuntimeError('CK univers migration 21.7: zones image o_editable_media absentes')
    if arch.count('ck-univers-card__cover') != 3:
        raise RuntimeError('CK univers migration 21.7: liens cover absents')
