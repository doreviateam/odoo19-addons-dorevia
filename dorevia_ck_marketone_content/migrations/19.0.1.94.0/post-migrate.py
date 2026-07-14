# -*- coding: utf-8 -*-
"""CK-CHECKOUT-STOCK-001 — sync allow_out_of_stock_order depuis ck_availability_mode."""
import logging

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    from odoo import api, SUPERUSER_ID

    env = api.Environment(cr, SUPERUSER_ID, {})
    products = env['product.template'].sudo().search([
        ('is_storable', '=', True),
        ('ck_availability_mode', 'in', ('stock', 'order')),
    ])
    if products:
        products._ck_sync_allow_out_of_stock_order()
    _logger.info(
        'CK-CHECKOUT-STOCK-001 migration 94.0 : %s produit(s) stockables synchronisés.',
        len(products),
    )
