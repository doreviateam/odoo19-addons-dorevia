# -*- coding: utf-8 -*-
"""Reconstruction home — commit explicite pour persister les étiquettes produit."""


def migrate(cr, version):
    from odoo import api, SUPERUSER_ID
    from odoo.addons.dorevia_ck_marketone_content.home_featured import (
        bootstrap_home_featured_products,
        get_curated_featured_variants,
        render_ck_featured_cards,
    )

    env = api.Environment(cr, SUPERUSER_ID, {})
    website = env['website'].search([], limit=1)
    variants = get_curated_featured_variants(env)
    cards = render_ck_featured_cards(env, website, variants)
    if cards and 'product-card-labels' not in cards[0]:
        raise RuntimeError('CK featured migration: étiquettes produit absentes des cards SSR')

    if not bootstrap_home_featured_products(env):
        raise RuntimeError('CK featured migration: bootstrap_home_featured_products a échoué')

    page = env['website.page'].sudo().search([
        ('url', '=', '/'),
        ('website_id', '=', website.id),
    ], limit=1)
    arch = page.view_id.arch_db or ''
    if cards and 'product-card-labels' not in arch:
        raise RuntimeError('CK featured migration: arch home sans product-card-labels après bootstrap')

    cr.commit()
