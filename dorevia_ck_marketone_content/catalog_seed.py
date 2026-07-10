# -*- coding: utf-8 -*-
"""Seed catalogue MOA — référence sandbox 18079 · install fraîche sans filestore.

Voir INVENTAIRE_CATALOGUE_SEED_18079.md et NOTE_MOA_CADRAGE_CK_DEPLOYABLE_SEED_CODE_FIRST_20260710.md.
"""
from __future__ import annotations

import base64
import logging

from odoo.tools import file_open

from .catalog_manioc_variants import (
    CRACKER_FORMAT_VALUES,
    FORMAT_ATTRIBUTE_ALIASES,
    FORMAT_ATTRIBUTE_NAME,
    MANIO_SALE_LST_PRICE,
    MANIO_SWEET_LST_PRICE,
    _align_manioc_cracker_prices,
    _cracker_value_tokens,
    _deprecate_duplicate_cracker_templates,
    _manio_crackers_variants_ready,
    _normalize_cracker_token,
)
from .ck_product_placeholders import is_tiny_product_image

_logger = logging.getLogger(__name__)

CATALOG_IMG_PREFIX = 'dorevia_ck_marketone_content/static/img/catalog/'
MOA_SEED_PRODUCT_COUNT = 9
MOA_SEED_FEATURED_TEMPLATE_COUNT = 6

# Racines L1 — noms exacts BO réf. 18079
CATALOG_ROOT_CATEGORIES = (
    ('Épicerie', 1),
    ('Boissons', 123),
    ('Soin & Bien-être', 2),
    ('Artisanat', 3),
)

CATALOG_L2_SEED = (
    ('Épicerie', (
        ('Biscuits', 10),
        ('Confitures', 20),
        ('Farines & manioc', 30),
        ('Épices', 40),
    )),
    ('Boissons', (
        ('Jus de fruits', 10),
        ('Alcools', 20),
        ('Liqueurs', 30),
    )),
    ('Soin & Bien-être', (
        ('Savons', 10),
        ('Huiles', 20),
    )),
    ('Artisanat', (
        ('Musique', 10),
    )),
)

# (name, list_price, website_sequence, ck_is_featured, image_file, (root, l2))
SIMPLE_PRODUCT_SEED = (
    (
        'Confiture de goyave',
        5.5,
        10005,
        True,
        'confiture_goyave.webp',
        ('Épicerie', 'Confitures'),
    ),
    (
        'Galettes de manioc',
        7.5,
        10015,
        False,
        'galettes_manioc.webp',
        ('Épicerie', 'Farines & manioc'),
    ),
    (
        'Savon vétiver',
        6.3,
        10025,
        True,
        'savon_vetiver.webp',
        ('Soin & Bien-être', 'Savons'),
    ),
    (
        'Chapeau Panama',
        17.6,
        10030,
        True,
        'chapeau_panama.webp',
        ('Artisanat', None),
    ),
    (
        'Pâte de manioc',
        3.95,
        10035,
        True,
        'pate_manioc.webp',
        ('Épicerie', 'Farines & manioc'),
    ),
    (
        'Jus Mont-Pelé',
        5.0,
        10040,
        False,
        'jus_mont_pele.webp',
        ('Boissons', 'Jus de fruits'),
    ),
    (
        'Tambour Gro Ka',
        435.0,
        10045,
        True,
        'tambour_gro_ka.webp',
        ('Artisanat', 'Musique'),
    ),
    (
        'Coffret découverte créole',
        29.9,
        10050,
        False,
        'coffret_decouverte.webp',
        ('Épicerie', 'Épices'),
    ),
)

MANIO_CRACKERS_NAME = 'Manio Crackers'
MANIO_VARIANT_IMAGES = (
    ('Manio Crackers salé', 'manio_crackers_sale.webp'),
    ('Manio Crackers sucré', 'manio_crackers_sweet.webp'),
)

# Origine géographique MOA — éligibilité coups de cœur (CATALOG-ARCHI-001 §7.1).
PRODUCT_ORIGIN_TAG_NAMES = {
    'Confiture de goyave': 'La Réunion',
    'Manio Crackers': 'Martinique',
    'Savon vétiver': 'La Réunion',
    'Chapeau Panama': 'Guadeloupe',
    'Pâte de manioc': 'La Réunion',
    'Tambour Gro Ka': 'Martinique',
    'Galettes de manioc': 'La Réunion',
    'Jus Mont-Pelé': 'Martinique',
    'Coffret découverte créole': 'Guadeloupe',
}


def _ensure_product_origin_tag(env, product, origin_name):
    if not origin_name:
        return
    Tag = env['product.tag'].sudo()
    tag = Tag.search([('name', '=', origin_name)], limit=1)
    if not tag:
        tag = Tag.create({'name': origin_name})
    if tag not in product.product_tag_ids:
        product.write({'product_tag_ids': [(4, tag.id)]})


def _ensure_product_seed_qualification(env, product):
    """Traçabilité + disponibilité — gate vedettes home install fraîche."""
    vals = {}
    if not product.ck_availability_mode:
        vals['ck_availability_mode'] = 'stock'
    if vals:
        product.write(vals)
    origin = PRODUCT_ORIGIN_TAG_NAMES.get(product.name)
    if origin:
        _ensure_product_origin_tag(env, product, origin)


def load_catalog_image_b64(filename):
    """Charge un webp catalogue en base64 pour ``image_1920``."""
    path = f'{CATALOG_IMG_PREFIX}{filename}'
    with file_open(path, 'rb') as fh:
        return base64.b64encode(fh.read())


def _category_by_names(env, root_name, child_name=None):
    Category = env['product.public.category'].sudo()
    root = Category.search([('name', '=', root_name), ('parent_id', '=', False)], limit=1)
    if not root:
        return Category.browse()
    if not child_name:
        return root
    child = Category.search([
        ('name', '=', child_name),
        ('parent_id', '=', root.id),
    ], limit=1)
    return child


def ensure_catalog_root_categories(env):
    """Crée les racines L1 MOA si absentes (Coups de cœur = XML data existant)."""
    Category = env['product.public.category'].sudo()
    for name, sequence in CATALOG_ROOT_CATEGORIES:
        cat = Category.search([('name', '=', name), ('parent_id', '=', False)], limit=1)
        if not cat:
            Category.create({'name': name, 'sequence': sequence})
        elif cat.sequence != sequence:
            cat.write({'sequence': sequence})
    return True


def ensure_catalog_l2_categories(env):
    """Sous-catégories L2 recette MOA."""
    Category = env['product.public.category'].sudo()
    for root_name, children in CATALOG_L2_SEED:
        root = Category.search([('name', '=', root_name), ('parent_id', '=', False)], limit=1)
        if not root:
            continue
        for child_name, sequence in children:
            child = Category.search([
                ('name', '=', child_name),
                ('parent_id', '=', root.id),
            ], limit=1)
            if not child:
                Category.create({
                    'name': child_name,
                    'parent_id': root.id,
                    'sequence': sequence,
                })
    return True


def _coups_de_coeur_category(env):
    return env.ref(
        'dorevia_ck_marketone_content.public_categ_coups_de_coeur',
        raise_if_not_found=False,
    )


def _write_product_image_if_needed(record, image_b64):
    if not image_b64:
        return False
    if is_tiny_product_image(record.image_1920):
        record.write({'image_1920': image_b64})
        return True
    return False


def _ensure_simple_product(env, spec):
    name, list_price, sequence, featured, image_file, categ = spec
    Template = env['product.template'].sudo()
    product = Template.search([('name', '=', name)], limit=1)
    image_b64 = load_catalog_image_b64(image_file)
    categ_ids = []
    cat = _category_by_names(env, categ[0], categ[1])
    if cat:
        categ_ids.append(cat.id)
    if featured:
        coups = _coups_de_coeur_category(env)
        if coups:
            categ_ids.append(coups.id)
    vals = {
        'type': 'consu',
        'is_published': True,
        'website_published': True,
        'sale_ok': True,
        'list_price': list_price,
        'website_sequence': sequence,
        'ck_is_featured': featured,
    }
    if categ_ids:
        vals['public_categ_ids'] = [(6, 0, list(set(categ_ids)))]
    if not product:
        vals.update({'name': name, 'image_1920': image_b64})
        product = Template.create(vals)
    else:
        product.write(vals)
        _write_product_image_if_needed(product, image_b64)
    _ensure_product_seed_qualification(env, product)
    return product


def _get_or_create_attribute(env, name):
    Attribute = env['product.attribute'].sudo()
    attr = Attribute.search([('name', '=', name)], limit=1)
    if not attr:
        attr = Attribute.create({
            'name': name,
            'create_variant': 'always',
            'display_type': 'radio',
        })
    return attr


def _ensure_manio_crackers(env):
    """Parent Manio + 2 variantes salé/sucré · images distinctes."""
    Template = env['product.template'].sudo()
    parent = Template.search([('name', '=', MANIO_CRACKERS_NAME)], limit=1)
    attr_name = FORMAT_ATTRIBUTE_NAME
    for alias in FORMAT_ATTRIBUTE_ALIASES:
        attr = _get_or_create_attribute(env, alias)
        if attr:
            attr_name = attr.name
            break
    attr = _get_or_create_attribute(env, attr_name)
    value_ids = []
    for value_name in CRACKER_FORMAT_VALUES:
        Value = env['product.attribute.value'].sudo()
        val = Value.search([
            ('name', '=', value_name),
            ('attribute_id', '=', attr.id),
        ], limit=1)
        if not val:
            val = Value.create({'name': value_name, 'attribute_id': attr.id})
        value_ids.append(val.id)

    coups = _coups_de_coeur_category(env)
    biscuits = _category_by_names(env, 'Épicerie', 'Biscuits')
    categ_ids = [c.id for c in (biscuits, coups) if c]

    base_vals = {
        'type': 'consu',
        'is_published': True,
        'website_published': True,
        'sale_ok': True,
        'list_price': MANIO_SALE_LST_PRICE,
        'website_sequence': 10010,
        'ck_is_featured': True,
    }
    if categ_ids:
        base_vals['public_categ_ids'] = [(6, 0, categ_ids)]

    if not parent:
        parent = Template.create({
            'name': MANIO_CRACKERS_NAME,
            'attribute_line_ids': [(0, 0, {
                'attribute_id': attr.id,
                'value_ids': [(6, 0, value_ids)],
            })],
            'image_1920': load_catalog_image_b64('manio_crackers_sale.webp'),
            **base_vals,
        })
    else:
        if not parent.attribute_line_ids:
            parent.write({
                'attribute_line_ids': [(0, 0, {
                    'attribute_id': attr.id,
                    'value_ids': [(6, 0, value_ids)],
                })],
            })
        parent.write(base_vals)
        _write_product_image_if_needed(
            parent,
            load_catalog_image_b64('manio_crackers_sale.webp'),
        )

    _deprecate_duplicate_cracker_templates(env, parent)
    for variant_name, image_file in MANIO_VARIANT_IMAGES:
        variant = parent.product_variant_ids.filtered(
            lambda v, n=variant_name: _normalize_cracker_token(n) in _normalize_cracker_token(v.display_name)
        )[:1]
        if variant:
            variant.write({'sale_ok': True})
            _write_product_image_if_needed(variant, load_catalog_image_b64(image_file))

    _align_manioc_cracker_prices(parent)
    _ensure_product_seed_qualification(env, parent)
    return _manio_crackers_variants_ready(parent)


def catalog_seed_counts(env):
    """Compteurs pour gate MOA / tests."""
    Template = env['product.template'].sudo()
    published = Template.search([
        ('is_published', '=', True),
        ('website_published', '=', True),
        ('sale_ok', '=', True),
    ])
    featured = published.filtered('ck_is_featured')
    with_image = published.filtered(
        lambda p: not is_tiny_product_image(p.image_1920)
        or any(
            not is_tiny_product_image(v.image_1920)
            for v in p.product_variant_ids
        )
    )
    return {
        'published': len(published),
        'featured_templates': len(featured),
        'with_image': len(with_image),
    }


def assert_catalog_seed_complete(env):
    """Lève ValueError si le seed MOA est incomplet (gate install fraîche)."""
    from .catalog_seed_guard import (
        MOA_SEED_MIN_FEATURED_COUNT,
        MOA_SEED_MIN_PUBLISHED_COUNT,
        MOA_SEED_PUBLISHED_PRODUCT_NAMES,
        count_moa_seed_featured_templates,
        count_moa_seed_published_products,
    )

    errors = []
    published = count_moa_seed_published_products(env)
    if published < MOA_SEED_MIN_PUBLISHED_COUNT:
        errors.append(f"produits seed publiés {published}/{MOA_SEED_MIN_PUBLISHED_COUNT}")
    featured = count_moa_seed_featured_templates(env)
    if featured < MOA_SEED_MIN_FEATURED_COUNT:
        errors.append(f"templates ck_is_featured {featured}/{MOA_SEED_MIN_FEATURED_COUNT}")

    Template = env['product.template'].sudo()
    missing_image = []
    for name in MOA_SEED_PUBLISHED_PRODUCT_NAMES:
        product = Template.search([('name', '=', name)], limit=1)
        if not product:
            errors.append(f"produit absent : {name}")
            continue
        has_image = not is_tiny_product_image(product.image_1920)
        if product.product_variant_ids:
            has_image = has_image or any(
                not is_tiny_product_image(variant.image_1920)
                for variant in product.product_variant_ids
            )
        if not has_image:
            missing_image.append(name)
    if missing_image:
        errors.append('images manquantes : ' + ', '.join(missing_image))

    if errors:
        raise ValueError('Catalogue seed MOA incomplet : ' + '; '.join(errors))


def ensure_catalog_seed(env):
    """Seed catalogue pilote MOA — idempotent · images depuis static/img/catalog/."""
    if not env.is_superuser():
        env = env(su=True)
    ensure_catalog_root_categories(env)
    ensure_catalog_l2_categories(env)
    _ensure_manio_crackers(env)
    for spec in SIMPLE_PRODUCT_SEED:
        _ensure_simple_product(env, spec)
    assert_catalog_seed_complete(env)
    _logger.info(
        'CK catalog seed MOA OK — %s publiés · %s featured',
        MOA_SEED_PRODUCT_COUNT,
        MOA_SEED_FEATURED_TEMPLATE_COUNT,
    )
    return True
