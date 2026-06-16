# -*- coding: utf-8 -*-
"""Reconstruction home — étiquettes produit sur les cards."""

def migrate(cr, version):
    from odoo import api, SUPERUSER_ID
    from odoo.addons.dorevia_ck_marketone_content.home_featured import (
        bootstrap_home_featured_products,
    )

    env = api.Environment(cr, SUPERUSER_ID, {})
    if not bootstrap_home_featured_products(env):
        return
    page = env['website.page'].sudo().search([
        ('url', '=', '/'),
        ('website_id', '=', env['website'].search([], limit=1).id),
    ], limit=1)
    if page and 'product-card-labels' not in (page.view_id.arch_db or ''):
        bootstrap_home_featured_products(env)
