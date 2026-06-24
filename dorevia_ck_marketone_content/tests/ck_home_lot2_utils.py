# -*- coding: utf-8 -*-
"""Helpers Lot2 / Section 3 — sélection vedettes via ck_is_featured."""

from odoo.addons.dorevia_ck_marketone_content.ck_product_placeholders import (
    CK_CREAM_PLACEHOLDER_PNG_B64,
    ensure_test_product_image,
)
from odoo.addons.dorevia_ck_marketone_content.home_featured import (
    FEATURED_CURATED_MAX,
    get_curated_featured_variants,
)

# Ticket Dev — aligné sur FEATURED_CURATED_MAX (cap grille 4 colonnes) :
# au-delà, ces tests min-cards échoueraient puisque le cap empêche d'afficher
# plus que FEATURED_CURATED_MAX cartes, quel que soit le nombre saisi en BO.
FEATURED_TEST_MIN_CARDS = FEATURED_CURATED_MAX


def clear_ck_is_featured(env):
    """Désactive En vedette sur tous les produits — retourne les ids précédemment actifs."""
    Template = env['product.template'].sudo()
    featured = Template.search([('ck_is_featured', '=', True)])
    saved = featured.ids
    if featured:
        featured.write({'ck_is_featured': False})
    return saved


def restore_ck_is_featured(env, template_ids):
    if not template_ids:
        return
    env['product.template'].sudo().browse(template_ids).write({'ck_is_featured': True})


def ensure_featured_catalog(env, min_count=FEATURED_TEST_MIN_CARDS):
    """Assure assez de produits En vedette publiés avec image pour les tests lot2."""
    Template = env['product.template'].sudo()
    published = Template.search([
        ('is_published', '=', True),
        ('website_published', '=', True),
        ('sale_ok', '=', True),
    ], order='website_sequence asc, id asc')
    for template in published:
        ensure_test_product_image(template, 'image_1920')
    index = 0
    while len(get_curated_featured_variants(env)) < min_count and index < min_count + 3:
        Template.create({
            'name': f'CK Lot2 Vedette Featured {index}',
            'ck_is_featured': True,
            'is_published': True,
            'website_published': True,
            'sale_ok': True,
            'list_price': 1.0,
            'image_1920': CK_CREAM_PLACEHOLDER_PNG_B64,
        })
        index += 1


def mark_featured(env, template, *, featured=True):
    template.sudo().write({'ck_is_featured': featured})
