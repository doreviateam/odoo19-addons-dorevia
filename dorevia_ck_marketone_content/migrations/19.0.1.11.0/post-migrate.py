# -*- coding: utf-8 -*-


def migrate(cr, version):
    from odoo import api, SUPERUSER_ID
    from odoo.addons.dorevia_ck_marketone_content.home_hero import (
        HERO_CAROUSEL_INTERVAL_MS,
        HERO_VARIANT_MARKER,
    )

    env = api.Environment(cr, SUPERUSER_ID, {})
    website = env['website'].search([], limit=1)
    if not website:
        return
    page = env['website.page'].sudo().search([
        ('url', '=', '/'),
        ('website_id', '=', website.id),
    ], limit=1)
    if not page or not page.view_id:
        return
    view = page.view_id.sudo()
    arch = view.arch_db
    if isinstance(arch, dict):
        arch = next(iter(arch.values()), '')
    arch = arch or ''
    if HERO_VARIANT_MARKER in arch and 'data-bs-interval="6000"' in arch:
        view.write({
            'arch_db': arch.replace(
                'data-bs-interval="6000"',
                f'data-bs-interval="{HERO_CAROUSEL_INTERVAL_MS}"',
                1,
            ),
        })
