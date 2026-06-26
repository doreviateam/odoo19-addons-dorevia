# -*- coding: utf-8 -*-
"""Tuiles sous-catégories génériques (Note 07 Lot B).

Pour toute catégorie sans contenu éditorial P2B (hors RAYON_EDITORIAL),
affiche les enfants directs ayant au moins un produit publié, avec image
du premier produit (même pattern que shop_rayon_editorial.py).
"""


def _category_has_published_products(env, category):
    Category = env['product.public.category'].sudo()
    Product = env['product.template'].sudo()
    all_ids = Category.search([('id', 'child_of', category.id)]).ids
    return bool(Product.search([
        ('public_categ_ids', 'in', all_ids),
        ('website_published', '=', True),
    ], limit=1))


def _first_product_image_url(env, category):
    Category = env['product.public.category'].sudo()
    Product = env['product.template'].sudo()
    all_ids = Category.search([('id', 'child_of', category.id)]).ids
    product = Product.search([
        ('public_categ_ids', 'in', all_ids),
        ('website_published', '=', True),
    ], limit=1, order='id')
    return f'/web/image/product.template/{product.id}/image_256' if product else None


def get_ck_category_family_tiles(env, category):
    """Tuiles visuelles des enfants directs de `category` avec au moins un produit publié.

    Retourne [] si `category` est None, n'a aucun enfant éligible, ou si la
    catégorie dispose d'un contenu éditorial P2B (le rayon prend le dessus).
    """
    if not category:
        return []
    children = env['product.public.category'].sudo().search(
        [('parent_id', '=', category.id)],
        order='sequence, name',
    )
    tiles = []
    for child in children:
        if not _category_has_published_products(env, child):
            continue
        slug = env['ir.http']._slug(child)
        tiles.append({
            'label': child.name,
            'url': f'/shop/category/{slug}',
            'image_url': _first_product_image_url(env, child),
        })
    return tiles
