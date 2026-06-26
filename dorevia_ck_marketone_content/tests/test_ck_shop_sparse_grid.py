# -*- coding: utf-8 -*-
"""Tests micro-polish — grille sparse centrée sur pages catégorie."""

from odoo.tests import tagged
from odoo.tests.common import HttpCase


@tagged('post_install', '-at_install', 'dorevia_ck_shop_note07_rebound')
class TestCkShopSparseGridHttp(HttpCase):

    def test_sparse_grid_class_on_single_product_category(self):
        html = self.url_open('/shop/category/boissons-123').text
        self.assertIn('ck-shop-grid--count-1', html)

    def test_sparse_grid_class_on_two_product_category(self):
        cat = self.env['product.public.category'].sudo().create({
            'name': 'CK Sparse Grid QA ephemeral',
        })
        products = self.env['product.template']
        for idx in range(2):
            products |= self.env['product.template'].sudo().create({
                'name': f'CK Sparse Grid QA Produit {idx}',
                'type': 'consu',
                'list_price': 5.0,
                'is_published': True,
                'public_categ_ids': [(4, cat.id)],
            })

        def _cleanup():
            products.sudo().unlink()
            cat.sudo().unlink()

        self.addCleanup(_cleanup)
        html = self.url_open(f'/shop/category/{cat.id}').text
        self.assertIn('ck-shop-grid--count-2', html)

    def test_no_sparse_grid_on_rich_category(self):
        html = self.url_open('/shop/category/epicerie-1').text
        self.assertNotIn('ck-shop-grid--count-', html)

    def test_no_sparse_grid_on_shop_root(self):
        html = self.url_open('/shop').text
        self.assertNotIn('ck-shop-grid--count-', html)
