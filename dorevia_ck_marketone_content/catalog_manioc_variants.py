# -*- coding: utf-8 -*-
"""Catalogue CK — modèle MOA vedettes : Manio Crackers (variantes) + Galettes séparées."""

from .ck_product_placeholders import CK_CREAM_PLACEHOLDER_PNG_B64

MANIO_CRACKERS_PARENT_NAME = 'Manio Crackers'
GALETTES_TEMPLATE_NAME = 'Galettes de manioc'
FORMAT_ATTRIBUTE_NAME = 'Format'
CRACKER_FORMAT_VALUES = (
    'Manio Crackers salé',
    'Manio Crackers sucré',
)
GALETTES_WEBSITE_SEQUENCE = 10015

def _manio_crackers_parent(env):
    return env['product.template'].sudo().search([
        ('name', '=', MANIO_CRACKERS_PARENT_NAME),
    ], limit=1)


def _manio_crackers_variants_ready(parent):
    if not parent:
        return False
    line = parent.attribute_line_ids.filtered(
        lambda l: l.attribute_id.name == FORMAT_ATTRIBUTE_NAME
    )[:1]
    if not line:
        return False
    value_names = set(line.value_ids.mapped('name'))
    return (
        len(parent.product_variant_ids) == len(CRACKER_FORMAT_VALUES)
        and all(name in value_names for name in CRACKER_FORMAT_VALUES)
        and 'Galettes de manioc' not in value_names
    )


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
    return _manio_crackers_variants_ready(parent)


def _link_epicerie_category(env, template):
    category = env['product.public.category'].sudo().search([
        ('name', '=', 'Épicerie créole'),
    ], limit=1)
    if category and category not in template.public_categ_ids:
        template.write({'public_categ_ids': [(4, category.id)]})


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
        if not galettes.image_1920:
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
        'image_1920': CK_CREAM_PLACEHOLDER_PNG_B64,
    })
    _link_epicerie_category(env, galettes)
    return bool(galettes)


def bootstrap_catalog_vedettes_products(env):
    """Aligne le catalogue BO MOA : Manio Crackers (2 variantes) + Galettes séparées."""
    manio_ok = _ensure_manioc_crackers_parent(env)
    galettes_ok = _ensure_galettes_separate_product(env)
    return manio_ok and galettes_ok


# Alias rétro-compat migrations / hooks antérieurs
bootstrap_manioc_product_variants = bootstrap_catalog_vedettes_products

# Rétro-compat tests / imports historiques
MANIOC_PARENT_NAME = MANIO_CRACKERS_PARENT_NAME
MANIOC_VARIANT_ATTRIBUTE = FORMAT_ATTRIBUTE_NAME
MANIOC_VARIANT_VALUES = CRACKER_FORMAT_VALUES
