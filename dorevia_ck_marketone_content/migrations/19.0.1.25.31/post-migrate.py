# -*- coding: utf-8 -*-
"""Réinjecte la section Ingrédients sur la confiture goyave (onglet Composition)."""

from odoo.addons.dorevia_ck_marketone_content.hooks import PRODUCT_WEBSITE_DESCRIPTIONS


def migrate(cr, version):
    from odoo import api, SUPERUSER_ID

    env = api.Environment(cr, SUPERUSER_ID, {})
    product = env['product.template'].search([('name', '=', 'Confiture de goyave')], limit=1)
    if not product:
        return
    expected = PRODUCT_WEBSITE_DESCRIPTIONS.get('Confiture de goyave')
    if not expected:
        return
    current = product.website_description or ''
    if 'ingrédients' in current.lower() or 'ingredients' in current.lower():
        return
    product.write({'website_description': expected})
