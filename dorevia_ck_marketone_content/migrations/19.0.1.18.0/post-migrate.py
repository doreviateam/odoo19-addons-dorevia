# -*- coding: utf-8 -*-
"""Section 3 — curation BO : catégorie 'Coups de cœur' + amorçage set MOA + réinjection."""


def migrate(cr, version):
    from odoo import api, SUPERUSER_ID
    from odoo.addons.dorevia_ck_marketone_content.home_featured import (
        _ensure_featured_category,
        bootstrap_home_featured_products,
    )

    env = api.Environment(cr, SUPERUSER_ID, {})
    category = _ensure_featured_category(env)

    # Amorçage : ranger le set vedettes MOA dans la catégorie (idempotent).
    seed_names = (
        'Confiture de goyave',
        'Manio Crackers',
        'Galettes de manioc',
        'Savon vétiver',
    )
    Template = env['product.template'].sudo()
    for name in seed_names:
        tmpl = Template.search([('name', '=', name)], limit=1)
        if tmpl and category not in tmpl.public_categ_ids:
            tmpl.write({'public_categ_ids': [(4, category.id)]})

    bootstrap_home_featured_products(env)
