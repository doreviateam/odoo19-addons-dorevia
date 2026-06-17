# -*- coding: utf-8 -*-
"""Helpers Lot2 — mode auto sélection vedettes (ticket lot2 option B).

En mode curation peuplée, ``get_ready_featured_variants`` et le seuil
``MIN_FEATURED_PRODUCTS`` ne s'appliquent plus. Les tests lot2 neutralisent
temporairement la catégorie « Coups de cœur » pour exercer le chemin auto.
"""

from odoo.addons.dorevia_ck_marketone_content.home_featured import (
    FEATURED_CATEGORY_XMLID,
    MIN_FEATURED_PRODUCTS,
)

_TINY_PNG = (
    b'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAADElEQVR4nGP4z8AAAAMBAQDJ/pLvAAAAAElFTkSuQmCC'
)


def detach_featured_curation(env):
    """Retire les produits de la catégorie curation — retourne l'état pour restauration."""
    category = env.ref(FEATURED_CATEGORY_XMLID, raise_if_not_found=False)
    if not category:
        return []
    category = category.sudo()
    templates = env['product.template'].sudo().search([
        ('public_categ_ids', 'in', category.ids),
    ])
    saved = [(template.id, list(template.public_categ_ids.ids)) for template in templates]
    if templates:
        templates.write({'public_categ_ids': [(3, category.id)]})
    return saved


def restore_featured_curation(env, saved):
    """Restaure la curation BO après un test lot2."""
    if not saved:
        return
    Template = env['product.template'].sudo()
    for template_id, categ_ids in saved:
        Template.browse(template_id).write({'public_categ_ids': [(6, 0, categ_ids)]})


def ensure_auto_featured_catalog(env, min_count=MIN_FEATURED_PRODUCTS):
    """Assure assez de produits publiés avec image pour le seuil auto lot2."""
    from odoo.addons.dorevia_ck_marketone_content.home_featured import get_ready_featured_variants

    Template = env['product.template'].sudo()
    published = Template.search([
        ('is_published', '=', True),
        ('website_published', '=', True),
        ('sale_ok', '=', True),
    ], order='website_sequence asc, id asc')
    for template in published:
        if not template.image_1920:
            template.image_1920 = _TINY_PNG
    index = 0
    while len(get_ready_featured_variants(env)) < min_count and index < min_count + 3:
        Template.create({
            'name': f'CK Lot2 Vedette Auto {index}',
            'is_published': True,
            'website_published': True,
            'sale_ok': True,
            'list_price': 1.0,
            'image_1920': _TINY_PNG,
        })
        index += 1
