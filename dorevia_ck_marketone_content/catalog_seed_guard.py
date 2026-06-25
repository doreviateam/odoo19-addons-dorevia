# -*- coding: utf-8 -*-
"""Garde-fou catalogue seed MOA — état de référence PROTOCOLE_QA_AXE_C (2026-06-24)."""

# Jeu commercial seed sandbox CK — 7 produits publiés de référence.
MOA_SEED_PUBLISHED_PRODUCT_NAMES = (
    'Chapeau Panama',
    'Confiture de goyave',
    'Jus Mont-Pelé',
    'Manio Crackers',
    'Pâte de manioc',
    'Savon vétiver',
    'Galettes de manioc',
)

MOA_SEED_MIN_PUBLISHED_COUNT = len(MOA_SEED_PUBLISHED_PRODUCT_NAMES)


def count_moa_seed_published_products(env):
    """Produits seed MOA effectivement publiés sur le site."""
    Template = env['product.template'].sudo()
    return Template.search_count([
        ('name', 'in', list(MOA_SEED_PUBLISHED_PRODUCT_NAMES)),
        ('is_published', '=', True),
        ('website_published', '=', True),
        ('sale_ok', '=', True),
    ])


def ensure_moa_seed_catalog_published(env):
    """Réaligne la publication des produits seed MOA (idempotent · sans dépublication)."""
    Template = env['product.template'].sudo()
    restored = 0
    for name in MOA_SEED_PUBLISHED_PRODUCT_NAMES:
        product = Template.search([('name', '=', name)], limit=1)
        if not product:
            continue
        vals = {}
        if not product.sale_ok:
            vals['sale_ok'] = True
        if not product.is_published:
            vals['is_published'] = True
        if not product.website_published:
            vals['website_published'] = True
        if vals:
            product.write(vals)
            restored += 1
    return restored
