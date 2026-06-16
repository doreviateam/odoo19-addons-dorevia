# -*- coding: utf-8 -*-
"""Section 3 — lecture SQL product_tag_ids + reconstruction home obligatoire."""


def migrate(cr, version):
    from odoo import api, SUPERUSER_ID
    from odoo.addons.dorevia_ck_marketone_content.home_featured import (
        _featured_arch_missing_product_labels,
        bootstrap_home_featured_products,
        get_curated_featured_variants,
    )

    env = api.Environment(cr, SUPERUSER_ID, {})
    if not bootstrap_home_featured_products(env):
        raise RuntimeError('CK featured migration 20.4: bootstrap_home_featured_products a échoué')

    page = env['website.page'].sudo().search([('url', '=', '/')], limit=1)
    arch = page.view_id.arch_db or '' if page and page.view_id else ''
    variants = get_curated_featured_variants(env)
    if _featured_arch_missing_product_labels(env, arch, variants):
        raise RuntimeError(
            'CK featured migration 20.4: product_tag_ids non rendus sur les cards home'
        )
    cr.commit()
