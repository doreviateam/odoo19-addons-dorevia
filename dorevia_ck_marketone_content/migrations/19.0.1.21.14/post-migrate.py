# -*- coding: utf-8 -*-
"""Hero carrousel — slides éditables individuellement (o_editable_media)."""


def migrate(cr, version):
    from odoo import api, SUPERUSER_ID

    env = api.Environment(cr, SUPERUSER_ID, {})
    from odoo.addons.dorevia_ck_marketone_content.home_hero import (
        bootstrap_home_hero,
        hero_home_arch_is_valid,
    )

    if not bootstrap_home_hero(env):
        raise RuntimeError('CK hero migration 21.14: bootstrap_home_hero a échoué')
    page = env['website.page'].search([('url', '=', '/')], limit=1)
    arch = page.view_id.arch_db if page and page.view_id else ''
    if isinstance(arch, dict):
        arch = next(iter(arch.values()), '')
    if not hero_home_arch_is_valid(arch):
        raise RuntimeError('CK hero migration 21.14: arch hero invalide après bootstrap')
    if 'ck-hero__slide-media o_editable' not in arch:
        raise RuntimeError('CK hero migration 21.14: zone slide o_editable absente')
