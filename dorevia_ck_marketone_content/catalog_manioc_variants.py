# -*- coding: utf-8 -*-
"""Catalogue CK — modèle MOA vedettes : Manio Crackers (variantes) + Galettes séparées."""

import base64

from odoo.tools import file_open

from .ck_product_placeholders import (
    CK_CREAM_PLACEHOLDER_PNG_B64,
    is_tiny_product_image,
)

MANIO_CRACKERS_PARENT_NAME = 'Manio Crackers'
GALETTES_TEMPLATE_NAME = 'Galettes de manioc'
# Vraie photo Galettes (webp partagé avec le hero) — évite la zone beige MOA.
GALETTES_IMAGE_PATH = 'dorevia_ck_marketone_content/static/img/ck_hero_crepe_manioc.webp'
FORMAT_ATTRIBUTE_NAME = 'Format'
FORMAT_ATTRIBUTE_ALIASES = (FORMAT_ATTRIBUTE_NAME, 'Saveur')
CRACKER_FORMAT_VALUES = (
    'Manio Crackers salé',
    'Manio Crackers sucré',
)
MANIO_SALE_LST_PRICE = 3.6
MANIO_SWEET_LST_PRICE = 3.5
GALETTES_WEBSITE_SEQUENCE = 10015


def _normalize_cracker_token(value):
    """Compare libellés variantes sans casse ni accents (seed BO hétérogène)."""
    import unicodedata
    normalized = unicodedata.normalize('NFKD', (value or '').lower())
    return ''.join(ch for ch in normalized if not unicodedata.combining(ch))


def cracker_format_attribute_line(parent):
    """Ligne d'attribut Format/Saveur du parent Manio Crackers (vide si absente)."""
    if not parent:
        return parent.attribute_line_ids[:0]
    for line in parent.attribute_line_ids:
        if line.attribute_id.name in FORMAT_ATTRIBUTE_ALIASES:
            return line
    for line in parent.attribute_line_ids:
        tokens = {_normalize_cracker_token(name) for name in line.value_ids.mapped('name')}
        if any('sal' in token for token in tokens) and any('sucr' in token for token in tokens):
            return line
    return parent.attribute_line_ids[:0]


def _cracker_value_tokens(line):
    return {_normalize_cracker_token(name) for name in line.value_ids.mapped('name')}


def _manio_crackers_variants_ready(parent):
    if not parent:
        return False
    line = cracker_format_attribute_line(parent)
    if not line:
        return False
    tokens = _cracker_value_tokens(line)
    return (
        len(parent.product_variant_ids) == len(CRACKER_FORMAT_VALUES)
        and any('sal' in token for token in tokens)
        and any('sucr' in token for token in tokens)
        and not any('galette' in token for token in tokens)
    )


def _manio_crackers_parent(env):
    return env['product.template'].sudo().search([
        ('name', '=', MANIO_CRACKERS_PARENT_NAME),
    ], limit=1)


def _align_manioc_cracker_prices(parent):
    """Prix MOA recette — lst_price salé 3,6 € · sucré 3,5 € (via list_price + price_extra)."""
    sale = parent.product_variant_ids.filtered(
        lambda v: 'sucr' not in _normalize_cracker_token(v.display_name)
        and 'sal' in _normalize_cracker_token(v.display_name)
    )[:1]
    sweet = parent.product_variant_ids.filtered(
        lambda v: 'sucr' in _normalize_cracker_token(v.display_name)
    )[:1]
    parent.write({'list_price': MANIO_SALE_LST_PRICE})
    if sale:
        sale.write({'list_price': MANIO_SALE_LST_PRICE})
    if sweet:
        ptav = sweet.product_template_attribute_value_ids[:1]
        if ptav:
            ptav.write({'price_extra': MANIO_SWEET_LST_PRICE - MANIO_SALE_LST_PRICE})
        else:
            sweet.write({'list_price': MANIO_SWEET_LST_PRICE})


def _deprecate_duplicate_cracker_templates(env, parent):
    """Anciens templates crackers séparés — hors parent MOA."""
    Template = env['product.template'].sudo()
    for fragment in ('Manio Crackers sal', 'Manio Crackers sucr'):
        duplicate = Template.search([
            ('name', 'ilike', fragment),
            ('id', '!=', parent.id),
        ], limit=1)
        if duplicate:
            duplicate.write({
                'active': False,
                'is_published': False,
                'website_published': False,
                'sale_ok': False,
            })


def _ensure_manioc_crackers_parent(env):
    """Valide le parent Manio Crackers + 2 variantes Format (sans toucher au BO si déjà OK)."""
    parent = _manio_crackers_parent(env)
    if not parent:
        return False
    _deprecate_duplicate_cracker_templates(env, parent)
    parent.write({
        'is_published': True,
        'website_published': True,
        'sale_ok': True,
    })
    for variant in parent.product_variant_ids:
        variant.write({'is_published': True, 'sale_ok': True})
    _align_manioc_cracker_prices(parent)
    return _manio_crackers_variants_ready(parent)


def _link_epicerie_category(env, template):
    category = env['product.public.category'].sudo().search([
        ('name', '=', 'Épicerie créole'),
    ], limit=1)
    if category and category not in template.public_categ_ids:
        template.write({'public_categ_ids': [(4, category.id)]})


def _galettes_image_b64():
    """Vraie photo Galettes depuis l'asset statique (base64) ; None si absente."""
    try:
        with file_open(GALETTES_IMAGE_PATH, 'rb') as fh:
            return base64.b64encode(fh.read())
    except OSError:
        return None


def _ensure_galettes_separate_product(env):
    """Galettes de manioc = template distinct (MOA · pas variante Manio Crackers)."""
    Template = env['product.template'].sudo()
    galettes = Template.search([('name', '=', GALETTES_TEMPLATE_NAME)], limit=1)
    if galettes:
        if galettes.attribute_line_ids:
            return False
        galettes.write({
            'active': True,
            'is_published': True,
            'website_published': True,
            'sale_ok': True,
            'website_sequence': GALETTES_WEBSITE_SEQUENCE,
        })
        image = _galettes_image_b64()
        if image and is_tiny_product_image(galettes.image_1920):
            galettes.write({'image_1920': image})
        elif not galettes.image_1920:
            galettes.write({'image_1920': CK_CREAM_PLACEHOLDER_PNG_B64})
        _link_epicerie_category(env, galettes)
        return True

    galettes = Template.create({
        'name': GALETTES_TEMPLATE_NAME,
        'type': 'consu',
        'is_published': True,
        'website_published': True,
        'sale_ok': True,
        'list_price': 1.0,
        'website_sequence': GALETTES_WEBSITE_SEQUENCE,
        'image_1920': _galettes_image_b64() or CK_CREAM_PLACEHOLDER_PNG_B64,
    })
    _link_epicerie_category(env, galettes)
    return bool(galettes)


def bootstrap_catalog_vedettes_products(env):
    """Aligne le catalogue BO MOA : Manio Crackers (2 variantes) + Galettes séparées."""
    try:
        from .catalog_seed import _ensure_manio_crackers, catalog_seed_counts, MOA_SEED_PRODUCT_COUNT

        if catalog_seed_counts(env)['published'] >= MOA_SEED_PRODUCT_COUNT:
            galettes = env['product.template'].sudo().search([
                ('name', '=', GALETTES_TEMPLATE_NAME),
            ], limit=1)
            return _ensure_manio_crackers(env) and bool(galettes)
    except (ImportError, ValueError):
        pass
    manio_ok = _ensure_manioc_crackers_parent(env)
    galettes_ok = _ensure_galettes_separate_product(env)
    return manio_ok and galettes_ok


# Alias rétro-compat migrations / hooks antérieurs
bootstrap_manioc_product_variants = bootstrap_catalog_vedettes_products

# Rétro-compat tests / imports historiques
MANIOC_PARENT_NAME = MANIO_CRACKERS_PARENT_NAME
MANIOC_VARIANT_ATTRIBUTE = FORMAT_ATTRIBUTE_NAME
MANIOC_VARIANT_VALUES = CRACKER_FORMAT_VALUES
