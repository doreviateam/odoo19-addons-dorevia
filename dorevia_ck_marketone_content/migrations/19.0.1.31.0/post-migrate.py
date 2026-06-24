# -*- coding: utf-8 -*-
"""P4 hybride — visuels rayon BO (identité) + re-sync navigation.

Seed de démonstration : réutilise une photo produit déjà publiée comme point
de départ éditable en BO, une seule fois à la migration — ce n'est PAS une
sélection automatique au rendu (cf. note de gouvernance P4). À remplacer par
un vrai visuel de territoire/ambiance lors de la validation MOA finale.
"""

from odoo.addons.dorevia_ck_marketone_content.nav_sync import bootstrap_ck_navigation


def _seed_rayon_visuals(env):
    Visual = env['ck.mega.menu.rayon.visual']
    Product = env['product.template']
    seeds = (
        ('epicerie', 3, 'Épicerie créole', 'Une sélection de saveurs et de producteurs identifiés.'),
        ('boissons', 2593, 'Boissons créoles', 'Jus et boissons locales, origine identifiée.'),
    )
    for menu_key, product_id, title, subtitle in seeds:
        if Visual.search([('menu_key', '=', menu_key)], limit=1):
            continue
        product = Product.browse(product_id)
        if not product.exists() or not product.image_1920:
            continue
        Visual.create({
            'menu_key': menu_key,
            'image': product.image_1920,
            'title': title,
            'subtitle': subtitle,
        })


def migrate(cr, version):
    from odoo import api, SUPERUSER_ID

    env = api.Environment(cr, SUPERUSER_ID, {})
    _seed_rayon_visuals(env)
    bootstrap_ck_navigation(env)
