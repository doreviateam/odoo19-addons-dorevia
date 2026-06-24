# -*- coding: utf-8 -*-
"""Pages rayon éditorialisées P2B — contenu validé MOA, par rayon.

P2B est recentré sur Épicerie seul (cf. BRIEF_CONTENU_SHOP_RAYONS_CK_P2B.md
§2.1, arbitrage MOA 2026-06-23). Boissons / Soin & Bien-être / Artisanat
n'ont qu'un seul produit publié chacun — ils ne sont volontairement pas
inscrits dans RAYON_EDITORIAL tant que leur catalogue ne justifie pas un
traitement éditorial complet (brief §6).

Le contenu ci-dessous reprend mot pour mot la proposition V0 validée
(brief §9.2). Les sous-familles et mises en avant restent gatées sur les
mêmes données réelles que le mega-menu header (nav_mega_menu._resolve_families)
— si le catalogue Épicerie redescend sous le seuil, ce bloc se masque tout
seul, sans intervention Dev.
"""
from .nav_mega_menu import _find_root_category, _match_family_category, _resolve_families
from .nav_v22_config import EPICERIE_FAMILIES

RAYON_EDITORIAL_MIN_FAMILIES = 3
RAYON_EDITORIAL_MIN_PRODUCTS = 4

RAYON_EDITORIAL = {
    'Épicerie': {
        'title': 'Épicerie créole',
        'phrase': (
            'Confitures, manioc, condiments, cacao, cafés et douceurs créoles '
            'sélectionnés pour leur goût, leur origine et leur usage au quotidien.'
        ),
        'family_specs': EPICERIE_FAMILIES,
        'highlights': (
            {
                'title': "Le manioc à l'honneur",
                'text': "Farines, galettes, crackers et produits autour d'un essentiel créole.",
                'family_slug': 'farines-manioc',
            },
            {
                'title': 'Douceurs des îles',
                'text': 'Confitures, cacao, café et notes sucrées pour le petit-déjeuner ou le cadeau.',
                'family_slug': 'confitures-douceurs',
            },
            {
                'title': 'Pour relever la cuisine',
                'text': 'Sauces, condiments et saveurs pour retrouver les gestes créoles.',
                'family_slug': 'sauces-condiments',
            },
        ),
        'proof': (
            'Origines identifiées — chaque produit est rattaché à une origine, un '
            'producteur ou un partenaire connu lorsque l’information est disponible.'
        ),
    },
}


def get_rayon_editorial(env, category):
    """Contenu éditorial de rayon pour `category`, ou None si non publiable.

    `category` doit être une catégorie racine inscrite dans RAYON_EDITORIAL,
    avec au moins RAYON_EDITORIAL_MIN_FAMILIES familles réelles et
    RAYON_EDITORIAL_MIN_PRODUCTS produits publiés (règle §6 du brief P2B).
    """
    if not category or category.parent_id:
        return None
    spec = RAYON_EDITORIAL.get(category.name)
    if not spec:
        return None

    families = _resolve_families(env, category.name, spec['family_specs'])
    if len(families) < RAYON_EDITORIAL_MIN_FAMILIES:
        return None

    Category = env['product.public.category'].sudo()
    Product = env['product.template'].sudo()
    all_children = Category.search([('id', 'child_of', category.id)])
    published_count = Product.search_count([
        ('public_categ_ids', 'in', all_children.ids),
        ('website_published', '=', True),
    ])
    if published_count < RAYON_EDITORIAL_MIN_PRODUCTS:
        return None

    slug_by_label = {label: slug for label, slug, *_rest in spec['family_specs']}
    url_by_slug = {
        slug_by_label[fam['label']]: fam['url']
        for fam in families
        if fam['label'] in slug_by_label
    }

    # Image de famille = photo du premier produit publié de la sous-catégorie
    # (vraie photo produit, jamais d'image générique inventée — si aucune
    # photo n'est disponible, le template affiche "Aucune image disponible",
    # même principe que le repère Sept-Fons fourni par MOA).
    root = _find_root_category(env, category.name)
    aliases_by_slug = {slug: aliases for _label, slug, aliases, *_rest in spec['family_specs']}
    for fam in families:
        slug = slug_by_label.get(fam['label'])
        aliases = aliases_by_slug.get(slug, (fam['label'],))
        fam_category = _match_family_category(env, root, aliases)
        product = Product.browse()
        if fam_category:
            product = Product.search([
                ('public_categ_ids', 'in', fam_category.id),
                ('website_published', '=', True),
            ], limit=1, order='id')
        fam['image_url'] = (
            f'/web/image/product.template/{product.id}/image_256' if product else None
        )

    highlights = []
    for highlight in spec['highlights']:
        url = url_by_slug.get(highlight['family_slug'])
        if not url:
            continue
        highlights.append({'title': highlight['title'], 'text': highlight['text'], 'url': url})

    return {
        'title': spec['title'],
        'phrase': spec['phrase'],
        'families': families,
        'highlights': highlights,
        'proof': spec['proof'],
    }
