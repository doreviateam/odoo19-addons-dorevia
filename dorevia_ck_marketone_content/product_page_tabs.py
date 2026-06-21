# -*- coding: utf-8 -*-
"""Fiche produit CK — regroupement des sections parser en blocs verticaux + ancres."""

import re

from markupsafe import Markup

from odoo.addons.dorevia_ck_marketone_content.product_page_details import (
    build_ck_product_page_detail_sections,
)

_BLOCK_DISCOVER_KEYS = frozenset({'origin_usage', 'usage', 'origin_producer'})
_BLOCK_COMPOSITION_KEYS = frozenset({'ingredients', 'nutrition'})
_BLOCK_CONSERVATION_KEYS = frozenset({'conservation'})

_BLOCK_META = {
    'discover': {
        'title': 'Découvrir',
        'nav_label': 'Découvrir',
        'anchor_id': 'ck-section-discover',
    },
    'composition': {
        'title': 'Composition',
        'nav_label': 'Composition',
        'anchor_id': 'ck-section-composition',
    },
    'conservation': {
        'title': 'Conservation & livraison',
        'nav_label': 'Conservation',
        'anchor_id': 'ck-section-conservation',
    },
    'details': {
        'title': 'Détails produit',
        'nav_label': 'Détails',
        'anchor_id': 'ck-section-details',
    },
}

_MARKDOWN_EMPHASIS_RE = re.compile(r'\*([^*\n]+)\*')


def _sanitize_section_body(body):
    """Retire les artefacts Markdown simples (*Usage :*) sans parser Markdown."""
    if not body:
        return Markup('')
    text = str(body)
    text = _MARKDOWN_EMPHASIS_RE.sub(r'\1', text)
    return Markup(text)


def _copy_section(section):
    copied = dict(section)
    if copied.get('body'):
        copied['body'] = _sanitize_section_body(copied['body'])
    if copied.get('subtitles'):
        copied['subtitles'] = [
            {
                **sub,
                'body': _sanitize_section_body(sub.get('body')),
            }
            for sub in copied['subtitles']
        ]
    return copied


def _format_reference_price(env, website, product, variant):
    from odoo.addons.dorevia_ck_marketone_content.home_featured import (
        _format_featured_reference_price,
        _get_featured_price_amount,
    )

    if not product.ck_show_reference_price:
        return ''
    price = _get_featured_price_amount(env, website, variant)
    return _format_featured_reference_price(env, website, price, product)


def _format_net_quantity(product):
    from odoo.addons.dorevia_ck_marketone_content.home_featured import (
        _format_featured_net_quantity,
    )

    return _format_featured_net_quantity(
        product.ck_net_quantity,
        product.ck_net_quantity_uom_id,
    )


def _is_origin_attribute_line(line):
    attr_name = (line.attribute_id.name or '').lower()
    return 'origine' in attr_name or 'origin' in attr_name


def _build_details_specs(product, variant, env, website):
    """Lignes factuelles section Détails produit — champs existants uniquement."""
    from odoo.addons.dorevia_ck_marketone_content.ck_product_origin import (
        ck_origin_from_attribute,
    )

    rows = []
    origin = ck_origin_from_attribute(product)
    if origin:
        rows.append({'label': 'Origine', 'value': origin})

    categories = product.public_categ_ids.filtered(
        lambda c: (c.name or '').strip().lower() != 'coups de cœur'
    )
    if categories:
        rows.append({
            'label': 'Catégorie',
            'value': ', '.join(categories.mapped('name')),
        })

    net_qty = _format_net_quantity(product)
    if net_qty:
        rows.append({'label': 'Contenance', 'value': net_qty})

    ref_price = _format_reference_price(env, website, product, variant)
    if ref_price:
        rows.append({'label': 'Prix de référence', 'value': ref_price})

    if product.default_code:
        rows.append({'label': 'Référence', 'value': product.default_code})

    for line in product.attribute_line_ids:
        if _is_origin_attribute_line(line):
            continue
        values = line.value_ids.mapped('name')
        if not values:
            continue
        rows.append({
            'label': line.attribute_id.name,
            'value': ', '.join(values),
        })

    if variant and variant.default_code and variant.default_code != product.default_code:
        rows.append({'label': 'Référence variante', 'value': variant.default_code})

    return rows


def _append_block(blocks, key, **extra):
    meta = _BLOCK_META[key]
    blocks.append({
        'key': key,
        'title': meta['title'],
        'nav_label': meta['nav_label'],
        'anchor_id': meta['anchor_id'],
        **extra,
    })


def build_ck_product_page_tabs(product, variant=None):
    """Blocs complémentaires fiche produit — empilement vertical + ancres (API inchangée)."""
    product.ensure_one()
    variant = variant or product.product_variant_id
    website = product.env['website'].get_current_website()
    env = product.env

    sections = [_copy_section(section) for section in build_ck_product_page_detail_sections(product)]
    blocks = []

    discover = [s for s in sections if s.get('key') in _BLOCK_DISCOVER_KEYS]
    if discover:
        _append_block(blocks, 'discover', sections=discover)

    composition = [s for s in sections if s.get('key') in _BLOCK_COMPOSITION_KEYS]
    if composition:
        _append_block(blocks, 'composition', sections=composition)

    conservation = [s for s in sections if s.get('key') in _BLOCK_CONSERVATION_KEYS]
    if conservation:
        _append_block(blocks, 'conservation', sections=conservation)

    specs = _build_details_specs(product, variant, env, website)
    if specs:
        _append_block(blocks, 'details', specs=specs)

    return blocks
