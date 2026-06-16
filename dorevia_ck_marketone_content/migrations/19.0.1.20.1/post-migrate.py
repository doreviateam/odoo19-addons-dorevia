# -*- coding: utf-8 -*-
"""Section 3 — reconstruction home si étiquettes produit absentes des cards SSR."""


def migrate(cr, version):
    from odoo import api, SUPERUSER_ID
    from odoo.addons.dorevia_ck_marketone_content.home_featured import (
        _featured_arch_missing_product_labels,
        bootstrap_home_featured_products,
        get_curated_featured_variants,
    )

    env = api.Environment(cr, SUPERUSER_ID, {})
    page = env['website.page'].sudo().search([('url', '=', '/')], limit=1)
    if not page or not page.view_id:
        return

    arch = page.view_id.arch_db or ''
    variants = get_curated_featured_variants(env)
    if not variants:
        variants = env['product.product'].browse()

    if _featured_arch_missing_product_labels(env, arch, variants):
        bootstrap_home_featured_products(env)
        arch = page.view_id.arch_db or ''
        if _featured_arch_missing_product_labels(env, arch, variants):
            raise RuntimeError(
                'CK featured migration 20.1: étiquettes produit toujours absentes de la home'
            )
    cr.commit()
