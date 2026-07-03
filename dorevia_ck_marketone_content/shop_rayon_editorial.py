# -*- coding: utf-8 -*-
"""Bannière univers shop — contenu éditorial V1 validé MOA (note V1.1 · 27/06/2026).

Chaque univers CK dispose d'une bannière (titre + phrase).  Épicerie bénéficie
en outre de familles visuelles et de mises en avant lorsque le catalogue atteint
les seuils définis en §6 du brief P2B.  En deçà des seuils, Épicerie affiche
la bannière simple (titre + phrase) — dégradé gracieux validé MOA §3.1.

Boissons / Soin & bien-être / Artisanat n'ont qu'un contenu simple en V1 ;
les familles et highlights sont réservés à une V2 éditoriale.

L'identification de l'univers passe désormais par le champ technique
`ck_universe` sur `product.public.category` (Option A — robuste aux renommages,
lisible BO, héritage parent/enfant via `_get_ck_universe()`).
"""
from .nav_mega_menu import _find_root_category, _match_family_category, _resolve_families
from .nav_v22_config import EPICERIE_FAMILIES

RAYON_EDITORIAL_MIN_FAMILIES = 3
RAYON_EDITORIAL_MIN_PRODUCTS = 4

# Clé = valeur de ck_universe (code technique).  'boutique' est un fallback
# interne uniquement — il n'apparaît pas dans la sélection BO (MOA §4.1).
RAYON_EDITORIAL = {
    'boutique': {
        'title': 'Boutique C-Kréyòl',
        'phrase': (
            'Produits créoles sélectionnés, aux origines identifiées, pour découvrir '
            'des saveurs, des soins et des savoir-faire issus des territoires.'
        ),
    },
    'epicerie': {
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
    'boissons': {
        'title': 'Boissons des îles',
        'phrase': (
            'Jus, nectars, infusions, sirops et boissons traditionnelles '
            'inspirées des territoires créoles.'
        ),
    },
    'soin': {
        'title': 'Soin & bien-être créole',
        'phrase': (
            'Savons, huiles et gestes de soin inspirés des plantes, matières '
            'et savoir-faire des territoires créoles.'
        ),
    },
    'artisanat': {
        'title': 'Artisanat & culture',
        'phrase': (
            'Objets, matières, créations et symboles qui racontent une culture '
            'vivante, entre maison, usage et transmission.'
        ),
    },
}


def get_rayon_editorial(env, category=None):
    """Bannière shop pour `category` (ou fallback boutique si None).

    Retourne toujours un dict {title, phrase, subtitle, image_url} non None
    (subtitle/image_url valent None si non renseignés — fallback géré côté template).
    Pour Épicerie avec catalogue suffisant, ajoute {families, highlights, proof}.
    """
    universe = category._get_ck_universe() if category else None
    spec = RAYON_EDITORIAL.get(universe or 'boutique', RAYON_EDITORIAL['boutique'])

    # Banner Univers (CK-UNIVERSE-BANNER-001 Lot A) — accroche + image native,
    # calculés une seule fois et fusionnés dans chaque dict retourné ci-dessous.
    banner_extra = {
        'subtitle': category.ck_subtitle or None if category else None,
        'image_url': (
            f'/web/image/product.public.category/{category.id}/image_1024'
            if category and category.image_1920 else None
        ),
    }

    # Univers simples : bannière titre + phrase, aucune condition catalogue
    if universe != 'epicerie':
        return {'title': spec['title'], 'phrase': spec['phrase'], **banner_extra}

    # Épicerie : familles + highlights si seuils atteints, dégradé gracieux sinon
    families = _resolve_families(env, category.name, spec['family_specs'])
    if len(families) < RAYON_EDITORIAL_MIN_FAMILIES:
        return {'title': spec['title'], 'phrase': spec['phrase'], **banner_extra}

    Category = env['product.public.category'].sudo()
    Product = env['product.template'].sudo()
    all_children = Category.search([('id', 'child_of', category.id)])
    published_count = Product.search_count([
        ('public_categ_ids', 'in', all_children.ids),
        ('website_published', '=', True),
    ])
    if published_count < RAYON_EDITORIAL_MIN_PRODUCTS:
        return {'title': spec['title'], 'phrase': spec['phrase'], **banner_extra}

    slug_by_label = {label: slug for label, slug, *_rest in spec['family_specs']}
    url_by_slug = {
        slug_by_label[fam['label']]: fam['url']
        for fam in families
        if fam['label'] in slug_by_label
    }

    # Image de famille = photo du premier produit publié de la sous-catégorie
    # (vraie photo produit, jamais d'image générique inventée — si aucune
    # photo n'est disponible, le template affiche "Aucune image disponible").
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
        **banner_extra,
    }
