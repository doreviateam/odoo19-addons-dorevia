# -*- coding: utf-8 -*-
"""Seed recette Nav-Shop — arborescence niveau 2 (ticket §14)."""

NAV_SHOP_L2_SEED = (
    ('Épicerie', (
        ('Biscuits', 10),
        ('Confitures', 20),
        ('Épices', 30),
    )),
    ('Boissons', (
        ('Jus de fruits', 10),
        ('Alcools', 20),
        ('Liqueurs', 30),
    )),
    ('Maison & bien-être', (
        ('Savons', 10),
        ('Huiles', 20),
    )),
)

# Produit témoin ticket §14 · §10
NAV_SHOP_L2_PRODUCT_HINTS = (
    ('Jus Mont-Pelé', 'Boissons', 'Jus de fruits'),
    ('Mont-Pelé', 'Boissons', 'Jus de fruits'),
)


def seed_nav_shop_l2_categories(env):
    """Crée les sous-catégories L2 recette si absentes · rattache un produit témoin si trouvé."""
    Category = env['product.public.category'].sudo()
    Product = env['product.template'].sudo()
    created = 0

    for root_name, children in NAV_SHOP_L2_SEED:
        root = Category.search([
            ('name', '=', root_name),
            ('parent_id', '=', False),
        ], limit=1)
        if not root:
            continue
        child_by_name = {}
        for child_name, sequence in children:
            child = Category.search([
                ('name', '=', child_name),
                ('parent_id', '=', root.id),
            ], limit=1)
            if not child:
                child = Category.create({
                    'name': child_name,
                    'parent_id': root.id,
                    'sequence': sequence,
                })
                created += 1
            child_by_name[child_name] = child

        for product_hint, root_name_hint, child_name_hint in NAV_SHOP_L2_PRODUCT_HINTS:
            if root_name_hint != root_name:
                continue
            child = child_by_name.get(child_name_hint)
            if not child:
                continue
            product = Product.search([
                ('name', 'ilike', product_hint),
                ('sale_ok', '=', True),
            ], limit=1)
            if product and child not in product.public_categ_ids:
                product.write({'public_categ_ids': [(4, child.id)]})

    return created
