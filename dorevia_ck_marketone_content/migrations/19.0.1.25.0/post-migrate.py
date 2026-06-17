# -*- coding: utf-8 -*-
"""Section 3 — CTA « Ajouter au panier » sur les cards vedettes home."""


def migrate(cr, version):
    from odoo import SUPERUSER_ID, api
    from odoo.addons.dorevia_ck_marketone_content.home_featured import (
        _featured_arch_missing_cart_cta,
        bootstrap_home_featured_products,
        get_curated_featured_variants,
    )

    env = api.Environment(cr, SUPERUSER_ID, {})
    if not bootstrap_home_featured_products(env):
        raise RuntimeError('CK featured migration 25.0: bootstrap_home_featured_products a échoué')

    page = env['website.page'].sudo().search([('url', '=', '/')], limit=1)
    arch = page.view_id.arch_db or '' if page and page.view_id else ''
    website = env['website'].search([], limit=1)
    variants = get_curated_featured_variants(env)
    if website and _featured_arch_missing_cart_cta(env, website, arch, variants):
        raise RuntimeError(
            'CK featured migration 25.0: CTA panier absent des cards vedettes home'
        )
    cr.commit()
