# -*- coding: utf-8 -*-
"""P2B prérequis — classement catalogue Épicerie (data hygiene, pas d'invention).

Constat (cf. BRIEF_CONTENU_SHOP_RAYONS_CK_P2B.md, échange MOA du 2026-06-23) :
les 4 produits Épicerie publiés étaient rattachés uniquement à la catégorie
racine "Épicerie", sans sous-catégorie — `_resolve_families` (nav_mega_menu.py)
résolvait donc 0 famille pour Épicerie, alors que 3 sous-catégories existent
déjà en base (Biscuits, Confitures, Épices) et que la règle de publication du
brief P2B exige 3 familles minimum.

Ce script ne fait QUE rattacher des produits réels à des catégories réelles
(ou créer la sous-catégorie "Farines & manioc", déjà prévue dans
nav_v22_config.py::EPICERIE_FAMILIES, alias "Manioc"/"Farines") — aucun
produit ni contenu n'est inventé. Effet de bord positif attendu : le
mega-menu Épicerie du header (jusqu'ici "partiel", cf. LIVRABLE_MOA_HEADER
§9.2) et la future page rayon P2B partagent la même taxonomie
(nav_v22_config.py) et bénéficient donc tous les deux de ce correctif.

Mapping retenu (évident, pas d'arbitrage caché) :
- Confiture de goyave -> Confitures (déjà existante)
- Manio Crackers       -> Biscuits (déjà existante, famille "Biscuits & crackers")
- Galettes de manioc   -> Farines & manioc (nouvelle, alias "Manioc"/"Farines")
- Pâte de manioc       -> Farines & manioc (idem)
"""


def migrate(cr, version):
    from odoo import api, SUPERUSER_ID

    env = api.Environment(cr, SUPERUSER_ID, {})
    _classify_epicerie_catalog(env)


def _classify_epicerie_catalog(env):
    Category = env['product.public.category'].sudo()
    Product = env['product.template'].sudo()

    epicerie = Category.search([
        ('name', '=ilike', 'Épicerie'),
        ('parent_id', '=', False),
    ], limit=1)
    if not epicerie:
        return

    def _get_or_create_child(name, sequence):
        child = Category.search([
            ('name', '=', name),
            ('parent_id', '=', epicerie.id),
        ], limit=1)
        if child:
            return child
        return Category.create({
            'name': name,
            'parent_id': epicerie.id,
            'sequence': sequence,
        })

    biscuits = Category.search([('name', '=', 'Biscuits'), ('parent_id', '=', epicerie.id)], limit=1)
    confitures = Category.search([('name', '=', 'Confitures'), ('parent_id', '=', epicerie.id)], limit=1)
    # Sequence 25 : entre Confitures (20) et Épices (30), ordre EPICERIE_FAMILIES.
    farines_manioc = _get_or_create_child('Farines & manioc', 25)

    mapping = (
        ('Confiture de goyave', confitures),
        ('Manio Crackers', biscuits),
        ('Galettes de manioc', farines_manioc),
        ('Pâte de manioc', farines_manioc),
    )
    for product_name, category in mapping:
        if not category:
            continue
        product = Product.search([('name', '=', product_name)], limit=1)
        if not product or category in product.public_categ_ids:
            continue
        product.write({'public_categ_ids': [(4, category.id)]})
