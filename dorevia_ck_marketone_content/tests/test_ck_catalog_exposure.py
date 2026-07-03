# -*- coding: utf-8 -*-
"""CATALOG-ARCHI-001 Lot A — ck_exposure_status / _is_ck_exposable()."""

from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged('post_install', '-at_install', 'dorevia_ck_catalog_exposure')
class TestCkCatalogExposure(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Category = cls.env['product.public.category'].sudo()
        cls.Product = cls.env['product.template'].sudo()

    def _make_category(self, name, **vals):
        return self.Category.create({'name': name, 'sequence': 950, **vals})

    def _make_products(self, category, count, name_prefix):
        products = self.Product.browse()
        for idx in range(count):
            products |= self.Product.create({
                'name': f'{name_prefix} {idx}',
                'sale_ok': True,
                'is_published': True,
                'website_published': True,
                'public_categ_ids': [(4, category.id)],
            })
        return products

    def test_zero_products_not_exposable(self):
        cat = self._make_category('TestCat Expo Zero')
        self.assertFalse(cat._is_ck_exposable())

    def test_one_product_not_exposable(self):
        cat = self._make_category('TestCat Expo One')
        self._make_products(cat, 1, 'Test Produit Expo One')
        self.assertFalse(cat._is_ck_exposable())

    def test_two_products_without_editorial_not_exposable(self):
        cat = self._make_category('TestCat Expo Two Sans Editorial')
        self._make_products(cat, 2, 'Test Produit Expo Two Sans Editorial')
        self.assertFalse(cat._is_ck_exposable())

    def test_two_products_with_editorial_exposable(self):
        """Exception §6.3 : 2 produits + titre/description éditoriale suffisent."""
        cat = self._make_category(
            'TestCat Expo Two Avec Editorial',
            show_category_description=True,
            website_description='<p>Description éditoriale suffisante.</p>',
        )
        self._make_products(cat, 2, 'Test Produit Expo Two Avec Editorial')
        self.assertTrue(cat._is_ck_exposable())

    def test_three_products_exposable(self):
        cat = self._make_category('TestCat Expo Three')
        self._make_products(cat, 3, 'Test Produit Expo Three')
        self.assertTrue(cat._is_ck_exposable())

    def test_hidden_status_never_exposable_even_with_products(self):
        cat = self._make_category('TestCat Expo Hidden', ck_exposure_status='hidden')
        self._make_products(cat, 5, 'Test Produit Expo Hidden')
        self.assertFalse(cat._is_ck_exposable())

    def test_promise_status_never_exposable_even_with_products(self):
        cat = self._make_category('TestCat Expo Promise', ck_exposure_status='promise')
        self._make_products(cat, 5, 'Test Produit Expo Promise')
        self.assertFalse(cat._is_ck_exposable())

    def test_default_status_is_active(self):
        cat = self._make_category('TestCat Expo Default Status')
        self.assertEqual(cat.ck_exposure_status, 'active')
