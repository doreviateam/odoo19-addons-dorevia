# -*- coding: utf-8 -*-
"""Fiche produit CK V1.1 — métadonnées zone haute et prix absolus variantes."""

from markupsafe import Markup

from odoo.tools import format_amount


def _join_metadata_markup(*parts):
    return Markup(' · ').join(part for part in parts if part)


def build_ck_product_page_metadata_line(env, product, variant):
    """Ligne métadonnées fiche produit : origine · producteur · poids net · prix réf."""
    from odoo.addons.dorevia_ck_marketone_content.ck_product_origin import (
        ck_origin_from_attribute,
    )
    from odoo.addons.dorevia_ck_marketone_content.home_featured import (
        _get_featured_format_and_reference_parts,
    )

    website = env['website'].get_current_website()
    if not website:
        return Markup('')

    parts = []
    origin = ck_origin_from_attribute(product)
    # Ne pas afficher l'origine en texte si un badge origine couvre déjà ce territoire.
    if origin and any(b.badge_type == 'origin' for b in product.ck_badge_ids):
        origin = ''
    if origin:
        parts.append(Markup.escape(origin))

    partner = product.ck_producer_id
    if partner and partner.ck_is_producer and (partner.name or '').strip():
        producer_name = Markup.escape(partner.name.strip())
        parts.append(Markup(
            f'<a href="#ck-section-producer" class="ck-product-purchase__meta-link">'
            f'{producer_name}</a>'
        ))

    qty_part, ref_part = _get_featured_format_and_reference_parts(env, website, variant)
    if qty_part:
        parts.append(Markup.escape(qty_part))
    if ref_part:
        parts.append(Markup.escape(ref_part))

    return _join_metadata_markup(*parts)


def build_ck_variant_value_prices(env, template, attribute_line):
    """Prix absolu website par valeur d'attribut — jamais de delta central."""
    website = env['website'].get_current_website()
    if not website or not attribute_line:
        return {}

    from odoo.addons.dorevia_ck_marketone_content.home_featured import (
        _get_featured_price_amount,
    )

    prices = {}
    for ptav in attribute_line.product_template_value_ids:
        variant = template.product_variant_ids.filtered(
            lambda variant: ptav in variant.product_template_attribute_value_ids
        )[:1]
        if not variant:
            continue
        amount = _get_featured_price_amount(env, website, variant)
        prices[ptav.id] = format_amount(env, amount, website.currency_id)
    return prices
