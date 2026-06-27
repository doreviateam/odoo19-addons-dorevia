# -*- coding: utf-8 -*-
"""Fiche produit CK — regroupement sections V1.1 + repli parser website_description."""

import re

from markupsafe import Markup

from odoo.tools import html2plaintext

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
        'title': 'Conservation',
        'nav_label': 'Conservation',
        'anchor_id': 'ck-section-conservation',
    },
    'practical': {
        'title': 'Infos pratiques',
        'nav_label': 'Infos pratiques',
        'anchor_id': 'ck-section-practical',
    },
    'producer': {
        'title': 'Producteur',
        'nav_label': 'Producteur',
        'anchor_id': 'ck-section-producer',
    },
}

_MARKDOWN_EMPHASIS_RE = re.compile(r'\*([^*\n]+)\*')


def _plain_text(value):
    return re.sub(r'\s+', ' ', html2plaintext(value or '')).strip()


def _text_markup(value):
    text = (value or '').strip()
    if not text:
        return Markup('')
    return Markup(f'<p>{Markup.escape(text)}</p>')


def _sanitize_section_body(body):
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


def _visible_public_categories(product):
    return product.public_categ_ids.filtered(
        lambda category: (category.name or '').strip().lower() != 'coups de cœur'
    )


def _build_practical_specs(product, variant, env, website):
    """Lignes factuelles section Infos pratiques — champs MOA + standards utiles."""
    from odoo.addons.dorevia_ck_marketone_content.ck_product_origin import (
        ck_origin_from_attribute,
    )

    rows = []
    net_qty = _format_net_quantity(product)
    if net_qty:
        rows.append({'label': 'Contenance', 'value': net_qty})

    packaging = (product.ck_packaging_label or '').strip()
    if packaging:
        rows.append({'label': 'Conditionnement', 'value': packaging})

    if product.default_code:
        rows.append({'label': 'Référence', 'value': product.default_code})

    categories = _visible_public_categories(product)
    if categories:
        rows.append({
            'label': 'Catégorie',
            'value': ', '.join(categories.mapped('name')),
        })

    origin = ck_origin_from_attribute(product)
    if origin:
        rows.append({'label': 'Origine', 'value': origin})

    producer = product.ck_producer_id
    if producer and producer.ck_is_producer:
        rows.append({'label': 'Producteur', 'value': producer.name})

    ref_price = _format_reference_price(env, website, product, variant)
    if ref_price:
        rows.append({'label': 'Prix de référence', 'value': ref_price})

    if variant and variant.default_code and variant.default_code != product.default_code:
        rows.append({'label': 'Référence variante', 'value': variant.default_code})

    return rows


def _build_discover_sections(product):
    discover_html = (product.ck_discover_html or '').strip()
    if discover_html and _plain_text(discover_html):
        return [{
            'key': 'discover',
            'title': '',
            'body': Markup(discover_html),
            'subtitles': [],
        }]

    parsed = [
        _copy_section(section)
        for section in build_ck_product_page_detail_sections(product)
        if section.get('key') in _BLOCK_DISCOVER_KEYS
    ]
    return parsed


def _build_composition_sections(product):
    sections = []
    ingredients = (product.ck_ingredients or '').strip()
    allergens = (product.ck_allergens or '').strip()
    nutrition = (product.ck_nutrition_html or '').strip()

    if ingredients:
        sections.append({
            'key': 'ingredients',
            'title': 'Ingrédients',
            'body': _text_markup(ingredients),
            'subtitles': [],
        })
    if allergens:
        sections.append({
            'key': 'allergens',
            'title': 'Allergènes',
            'body': _text_markup(allergens),
            'subtitles': [],
        })
    if nutrition and _plain_text(nutrition):
        sections.append({
            'key': 'nutrition',
            'title': 'Valeurs nutritionnelles',
            'body': Markup(nutrition),
            'subtitles': [],
        })

    if sections:
        return sections

    return [
        _copy_section(section)
        for section in build_ck_product_page_detail_sections(product)
        if section.get('key') in _BLOCK_COMPOSITION_KEYS
    ]


def _build_conservation_sections(product):
    before = (product.ck_conservation_before or '').strip()
    after = (product.ck_conservation_after or '').strip()
    if before or after:
        subtitles = []
        if before:
            subtitles.append({
                'title': 'Avant ouverture',
                'body': _text_markup(before),
            })
        if after:
            subtitles.append({
                'title': 'Après ouverture',
                'body': _text_markup(after),
            })
        return [{
            'key': 'conservation',
            'title': 'Conservation',
            'body': Markup(''),
            'subtitles': subtitles,
        }]

    return [
        _copy_section(section)
        for section in build_ck_product_page_detail_sections(product)
        if section.get('key') in _BLOCK_CONSERVATION_KEYS
    ]


def _build_producer_block(product):
    partner = product.ck_producer_id
    if not partner or not partner.ck_is_producer:
        return None
    return {
        'name': partner.name,
        'short_description': (partner.ck_producer_short_description or '').strip(),
        'location_label': (partner.ck_producer_location_label or '').strip(),
        'image_url': f'/web/image/res.partner/{partner.id}/image_1920' if partner.image_1920 else '',
    }


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
    """Blocs complémentaires fiche produit — empilement vertical + ancres V1.1."""
    product.ensure_one()
    variant = variant or product.product_variant_id
    website = product.env['website'].get_current_website()
    env = product.env
    blocks = []

    discover = _build_discover_sections(product)
    if discover:
        _append_block(blocks, 'discover', sections=discover)

    composition = _build_composition_sections(product)
    if composition:
        _append_block(blocks, 'composition', sections=composition)

    conservation = _build_conservation_sections(product)
    if conservation:
        _append_block(blocks, 'conservation', sections=conservation)

    specs = _build_practical_specs(product, variant, env, website)
    if specs:
        _append_block(blocks, 'practical', specs=specs)

    producer = _build_producer_block(product)
    if producer:
        _append_block(blocks, 'producer', producer=producer)

    return blocks
