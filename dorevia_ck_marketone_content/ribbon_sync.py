# -*- coding: utf-8 -*-
"""Rubans produit e-commerce — alignement libellés CK."""

NOUVEAU_RIBBON_LABEL = 'Nouveau !'
LEGACY_NEW_RIBBON_NAMES = ('New!', 'New')


def francize_new_product_ribbon(env):
    """Remplace le ruban natif Odoo « New! » par « Nouveau ! » (donnée BO)."""
    Ribbon = env['product.ribbon'].sudo()
    updated = 0
    for legacy_name in LEGACY_NEW_RIBBON_NAMES:
        for ribbon in Ribbon.search([('name', '=', legacy_name)]):
            ribbon.write({'name': NOUVEAU_RIBBON_LABEL})
            updated += 1
    return updated
