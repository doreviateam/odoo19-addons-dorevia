# -*- coding: utf-8 -*-
"""Tests CK-CHECKOUT-STOCK-001 — sync stock CK et message panier."""
from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged('post_install', '-at_install')
class TestCkCheckoutStock001(TransactionCase):

    def test_ck_availability_stock_syncs_allow_out_of_stock_false(self):
        product = self.env['product.template'].create({
            'name': 'CK Stock Test',
            'type': 'consu',
            'is_storable': True,
            'sale_ok': True,
            'list_price': 1.0,
            'ck_availability_mode': 'stock',
        })
        product.write({'ck_availability_mode': 'stock'})
        self.assertFalse(product.allow_out_of_stock_order)

    def test_ck_availability_order_syncs_allow_out_of_stock_true(self):
        product = self.env['product.template'].create({
            'name': 'CK Order Test',
            'type': 'consu',
            'is_storable': True,
            'sale_ok': True,
            'list_price': 1.0,
            'ck_availability_mode': 'order',
        })
        product.write({'ck_availability_mode': 'order'})
        self.assertTrue(product.allow_out_of_stock_order)

    def test_shop_warning_stock_message_ck(self):
        line = self.env['sale.order.line'].create({
            'order_id': self.env['sale.order'].create({'partner_id': self.env.ref('base.public_partner').id}).id,
            'product_id': self.env['product.product'].create({
                'name': 'Warn test',
                'type': 'consu',
                'is_storable': True,
            }).id,
            'product_uom_qty': 1,
        })
        warning = line._set_shop_warning_stock(10, 2, save=False)
        self.assertIn('limitée au stock disponible', warning)
        self.assertIn('2', warning)
