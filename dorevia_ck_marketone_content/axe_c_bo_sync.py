# -*- coding: utf-8 -*-
"""Axe C — corrections BO catalogue scriptables (migration 19.0.1.43.0).

Périmètre :
- Bloc E : UOM card (g / kg) + prix de référence pour 4 produits masse.
- Bloc E : Chapeau Panama — pas de prix de référence, UOM card vidées.
- Bloc D : traductions fr_FR catégories publiques exposées, Galettes de manioc,
  attribut Origine et valeur Guadeloupe.

Hors périmètre (autres migrations / tickets) :
- Jus Mont-Pelé, Pâte de manioc (MOA-2 → ``apply_moa2_bo_corrections`` · 19.0.1.44.0).
- Catégorie « Coups de cœur » (ticket XML data séparé).
- Action 6 — origine sur les 6 produits sans attribut (données MOA).
"""

import logging

_logger = logging.getLogger(__name__)

FR_LANG = 'fr_FR'

# Sous-catégories catalogue — libellé identique en fr_FR (noms déjà français).
PUBLIC_CATEGORY_FR_LABELS = (
    'Biscuits',
    'Confitures',
    'Épices',
    'Farines & manioc',
    'Huiles',
    'Jus de fruits',
    'Alcools',
    'Liqueurs',
    'Savons',
)

GALETTES_PRODUCT_NAME = 'Galettes de manioc'

# (nom produit en_US, afficher prix réf., vider UOM card)
_PRODUCT_UOM_TARGETS = (
    ('Confiture de goyave', True, False),
    ('Manio Crackers', True, False),
    ('Galettes de manioc', True, False),
    ('Savon vétiver', True, False),
    ('Chapeau Panama', False, True),
)

# MOA-2 — arbitrage contenance / prix de référence (migration 19.0.1.44.0).
# (nom produit, code UOM nette, code UOM prix réf., afficher prix réf.)
_MOA2_PRODUCT_UOM_TARGETS = (
    ('Jus Mont-Pelé', 'l', 'l', True),
    ('Pâte de manioc', 'kg', 'kg', True),
)


def _card_uom(env, xmlid_suffix):
    return env.ref(
        f'dorevia_ck_marketone_content.ck_card_uom_{xmlid_suffix}',
        raise_if_not_found=False,
    )


def _raw_field_translation(env, record, field, lang):
    """Valeur jsonb brute — sans repli automatique sur en_US.

    ``field`` et ``record._table`` sont des littéraux internes (name, _table) ;
    ne pas réutiliser avec des noms dynamiques non contrôlés.
    """
    env.cr.execute(
        f"SELECT COALESCE({field}->>%s, '') FROM {record._table} WHERE id = %s",
        (lang, record.id),
    )
    row = env.cr.fetchone()
    return (row[0] if row else '').strip()


def _ensure_field_translation(env, record, field, lang, label):
    """Écrit une traduction si absente ou différente (idempotent)."""
    if not record or not label:
        return False
    expected = label.strip()
    if _raw_field_translation(env, record, field, lang) == expected:
        return False
    if hasattr(record, 'update_field_translations'):
        record.update_field_translations(field, {lang: expected})
    else:
        record.with_context(lang=lang).write({field: expected})
    return True


def _ensure_public_category_fr_translations(env):
    Category = env['product.public.category'].sudo()
    updated = 0
    for label in PUBLIC_CATEGORY_FR_LABELS:
        category = Category.search([('name', '=', label)], limit=1)
        if not category:
            _logger.warning(
                'Axe C BO sync : catégorie publique « %s » introuvable — ignorée.',
                label,
            )
            continue
        if _ensure_field_translation(env, category, 'name', FR_LANG, label):
            updated += 1
    return updated


def _ensure_galettes_product_fr(env):
    Product = env['product.template'].sudo()
    product = Product.search([('name', '=', GALETTES_PRODUCT_NAME)], limit=1)
    if not product:
        _logger.warning(
            'Axe C BO sync : produit « %s » introuvable — fr_FR ignoré.',
            GALETTES_PRODUCT_NAME,
        )
        return False
    return _ensure_field_translation(env, product, 'name', FR_LANG, GALETTES_PRODUCT_NAME)


def _find_origin_attribute(env):
    return env['product.attribute'].sudo().search([
        ('name', 'ilike', 'origine'),
    ], limit=1)


def _ensure_origin_attribute_fr(env):
    attribute = _find_origin_attribute(env)
    if not attribute:
        _logger.warning('Axe C BO sync : attribut Origine introuvable — ignoré.')
        return 0
    updated = 0
    source = (attribute.name or '').strip() or 'Origine'
    if _ensure_field_translation(env, attribute, 'name', FR_LANG, source):
        updated += 1
    value = env['product.attribute.value'].sudo().search([
        ('attribute_id', '=', attribute.id),
        ('name', 'ilike', 'guadeloupe'),
    ], limit=1)
    if not value:
        _logger.warning(
            'Axe C BO sync : valeur Guadeloupe introuvable sur attribut %s.',
            attribute.id,
        )
        return updated
    value_label = (value.name or '').strip() or 'Guadeloupe'
    if _ensure_field_translation(env, value, 'name', FR_LANG, value_label):
        updated += 1
    return updated


def _many2one_target_id(value):
    if not value:
        return False
    return value.id if hasattr(value, 'id') else value


def _product_field_differs(product, field, target):
    current = product[field]
    if field.endswith('_id'):
        return _many2one_target_id(current) != _many2one_target_id(target)
    return current != target


def _ensure_product_card_uom(env, uom_g, uom_kg):
    Product = env['product.template'].sudo()
    updated = 0
    for product_name, show_ref, clear_uom in _PRODUCT_UOM_TARGETS:
        product = Product.search([('name', '=', product_name)], limit=1)
        if not product:
            _logger.warning(
                'Axe C BO sync : produit « %s » introuvable — UOM ignoré.',
                product_name,
            )
            continue
        if clear_uom:
            vals = {
                'ck_net_quantity_uom_id': False,
                'ck_reference_price_uom_id': False,
                'ck_show_reference_price': False,
            }
        else:
            vals = {
                'ck_net_quantity_uom_id': uom_g.id,
                'ck_reference_price_uom_id': uom_kg.id,
                'ck_show_reference_price': show_ref,
            }
        changes = {
            key: val
            for key, val in vals.items()
            if _product_field_differs(product, key, val)
        }
        if not changes:
            continue
        product.write(changes)
        updated += 1
    return updated


def _write_product_card_uom_if_differs(product, vals):
    changes = {
        key: val
        for key, val in vals.items()
        if _product_field_differs(product, key, val)
    }
    if not changes:
        return False
    product.write(changes)
    return True


def _ensure_moa2_product_card_uom(env):
    """UOM card MOA-2 — Jus Mont-Pelé (l/l) et Pâte de manioc (kg/kg) uniquement."""
    Product = env['product.template'].sudo()
    updated = 0
    for product_name, net_code, ref_code, show_ref in _MOA2_PRODUCT_UOM_TARGETS:
        product = Product.search([('name', '=', product_name)], limit=1)
        if not product:
            _logger.warning(
                'MOA-2 BO sync : produit « %s » introuvable — ignoré.',
                product_name,
            )
            continue
        uom_net = _card_uom(env, net_code)
        uom_ref = _card_uom(env, ref_code)
        if not uom_net or not uom_ref:
            _logger.error(
                'MOA-2 BO sync : UOM card %s/%s absentes — « %s » ignoré.',
                net_code,
                ref_code,
                product_name,
            )
            continue
        if _write_product_card_uom_if_differs(product, {
            'ck_net_quantity_uom_id': uom_net.id,
            'ck_reference_price_uom_id': uom_ref.id,
            'ck_show_reference_price': show_ref,
        }):
            updated += 1
    return updated


def apply_moa2_bo_corrections(env):
    """Applique l'arbitrage MOA-2 (migration 19.0.1.44.0, idempotent)."""
    stats = {
        'moa2_products_uom': _ensure_moa2_product_card_uom(env),
    }
    _logger.info('MOA-2 BO sync 19.0.1.44.0 appliqué : %s', stats)
    return stats


def apply_axe_c_bo_corrections(env):
    """Applique les corrections BO Axe C scriptables (idempotent)."""
    uom_g = _card_uom(env, 'g')
    uom_kg = _card_uom(env, 'kg')
    if not uom_g or not uom_kg:
        _logger.error(
            'Axe C BO sync : UOM card g/kg absentes — bloc E ignoré.',
        )
        uom_products = 0
    else:
        uom_products = _ensure_product_card_uom(env, uom_g, uom_kg)

    stats = {
        'public_categories_fr': _ensure_public_category_fr_translations(env),
        'galettes_fr': int(_ensure_galettes_product_fr(env)),
        'origin_fr': _ensure_origin_attribute_fr(env),
        'products_uom': uom_products,
    }
    _logger.info('Axe C BO sync 19.0.1.43.0 appliqué : %s', stats)
    return stats
