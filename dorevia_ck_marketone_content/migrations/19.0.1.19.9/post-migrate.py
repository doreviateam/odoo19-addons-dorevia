# -*- coding: utf-8 -*-
"""Reconstruction home — étiquettes produit sur les cards pré-rendues."""


def migrate(cr, version):
    from odoo import api, SUPERUSER_ID
    from odoo.addons.dorevia_ck_marketone_content.home_featured import (
        _get_featured_labels_line,
        bootstrap_home_featured_products,
        get_curated_featured_variants,
    )

    env = api.Environment(cr, SUPERUSER_ID, {})
    bootstrap_home_featured_products(env)

    page = env['website.page'].sudo().search([
        ('url', '=', '/'),
        ('website_id', '=', env['website'].search([], limit=1).id),
    ], limit=1)
    arch = page.view_id.arch_db or ''
    for variant in get_curated_featured_variants(env):
        labels = _get_featured_labels_line(variant.product_tmpl_id)
        if labels and labels not in arch:
            raise RuntimeError(
                f'CK featured migration: étiquettes manquantes pour {variant.display_name!r}'
            )

    cr.commit()
