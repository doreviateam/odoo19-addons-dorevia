# -*- coding: utf-8 -*-
"""Migration 21.8 — sélection éditeur par card (inner snippet + section sans data-snippet)."""


def migrate(cr, version):
    from odoo import api, SUPERUSER_ID

    env = api.Environment(cr, SUPERUSER_ID, {})
    from odoo.addons.dorevia_ck_marketone_content.home_univers import (
        UNIVERS_CARD_SNIPPET,
        UNIVERS_EDITABLE_MEDIA_MARKER,
        UNIVERS_SECTION_SNIPPET,
        bootstrap_home_univers,
    )

    if not bootstrap_home_univers(env):
        raise RuntimeError('CK univers migration 21.8: bootstrap_home_univers a échoué')
    page = env['website.page'].search([('url', '=', '/')], limit=1)
    arch = page.view_id.arch_db if page and page.view_id else ''
    if isinstance(arch, dict):
        arch = next(iter(arch.values()), '')
    if arch.count(f'data-snippet="{UNIVERS_CARD_SNIPPET}"') != 3:
        raise RuntimeError('CK univers migration 21.8: sous-snippets card absents')
    if arch.count(UNIVERS_EDITABLE_MEDIA_MARKER) != 3:
        raise RuntimeError('CK univers migration 21.8: o_editable_media absent')
    if 'ck-univers-card--epicerie o_editable' not in arch:
        raise RuntimeError('CK univers migration 21.8: cards o_editable absentes')
    head = arch.split('ck-univers-cards__grid')[0] if 'ck-univers-cards__grid' in arch else arch
    if f'data-snippet="{UNIVERS_SECTION_SNIPPET}"' in head:
        raise RuntimeError('CK univers migration 21.8: data-snippet section encore présent')
