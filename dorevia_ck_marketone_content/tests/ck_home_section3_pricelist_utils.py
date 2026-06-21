# -*- coding: utf-8 -*-
"""Helpers recette Section 3 — prix vedettes avec pricelist active (cible CK)."""

from odoo.addons.dorevia_ck_marketone_content.catalog_manioc_variants import (
    MANIO_CRACKERS_PARENT_NAME,
)


def enable_website_pricelists(env):
    """Active le groupe Odoo pricelist (prérequis MOA B2C/B2B)."""
    if not env.user.has_group('product.group_product_pricelist'):
        env['res.config.settings'].create({
            'group_product_pricelist': True,
        }).execute()


def ensure_ck_b2c_pricelist(env, website, *, name='CK B2C Recette'):
    """Liste de prix publique sélectionnable, rattachée au site."""
    Pricelist = env['product.pricelist'].sudo()
    pl = Pricelist.search([
        ('name', '=', name),
        ('website_id', '=', website.id),
    ], limit=1)
    if not pl:
        pl = Pricelist.create({
            'name': name,
            'currency_id': website.company_id.currency_id.id,
            'selectable': True,
            'website_id': website.id,
        })
    website.invalidate_recordset(['pricelist_ids'])
    return pl


def set_variant_fixed_price(env, pricelist, variant, amount):
    """Règle variante — n'affecte pas les autres variantes du template."""
    Item = env['product.pricelist.item'].sudo()
    item = Item.search([
        ('pricelist_id', '=', pricelist.id),
        ('applied_on', '=', '0_product_variant'),
        ('product_id', '=', variant.id),
    ], limit=1)
    vals = {
        'pricelist_id': pricelist.id,
        'applied_on': '0_product_variant',
        'product_id': variant.id,
        'compute_price': 'fixed',
        'fixed_price': amount,
    }
    if item:
        item.write(vals)
    else:
        Item.create(vals)


def get_manioc_cracker_variants(env):
    parent = env['product.template'].sudo().search([
        ('name', '=', MANIO_CRACKERS_PARENT_NAME),
    ], limit=1)
    if not parent:
        return parent, env['product.product'].browse(), env['product.product'].browse()
    sale = parent.product_variant_ids.filtered(
        lambda v: 'sal' in (v.display_name or '').lower()
    )[:1]
    sweet = parent.product_variant_ids.filtered(
        lambda v: 'sucr' in (v.display_name or '').lower()
    )[:1]
    return parent, sale, sweet


def format_ck_price(env, website, amount):
    return env['ir.qweb.field.monetary'].value_to_html(
        amount,
        {'display_currency': website.currency_id},
    ).replace('\xa0', ' ').strip()
