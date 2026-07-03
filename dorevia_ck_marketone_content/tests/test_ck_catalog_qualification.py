# -*- coding: utf-8 -*-
"""CATALOG-ARCHI-001 Lot B — _is_ck_qualified_for_public_exposure / ck_is_orphan."""

import base64

from odoo.tests import tagged
from odoo.tests.common import TransactionCase

# 1x1 px PNG transparent — image minimale valide pour les tests.
_TINY_PNG = base64.b64encode(
    b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01'
    b'\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01'
    b'\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82'
)


@tagged('post_install', '-at_install', 'dorevia_ck_catalog_qualification')
class TestCkCatalogQualification(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Category = cls.env['product.public.category'].sudo()
        cls.Product = cls.env['product.template'].sudo()
        cls.Partner = cls.env['res.partner'].sudo()
        cls.category = cls.Category.create({'name': 'TestCat Qualif'})

    def _make_product(self, **overrides):
        vals = {
            'name': 'Test Produit Qualif',
            'sale_ok': True,
            'is_published': True,
            'website_published': True,
            'list_price': 9.9,
            'image_1920': _TINY_PNG,
            'public_categ_ids': [(4, self.category.id)],
            'ck_availability_mode': 'stock',
        }
        vals.update(overrides)
        return self.Product.create(vals)

    def test_fully_qualified_with_origin_attribute(self):
        attribute = self.env['product.attribute'].create({'name': 'Origine test'})
        value = self.env['product.attribute.value'].create({
            'name': 'Guadeloupe', 'attribute_id': attribute.id,
        })
        product = self._make_product(attribute_line_ids=[(0, 0, {
            'attribute_id': attribute.id,
            'value_ids': [(6, 0, [value.id])],
        })])
        self.assertTrue(product._is_ck_qualified_for_public_exposure())

    def test_qualified_with_producer_instead_of_origin(self):
        producer = self.Partner.create({'name': 'Producteur Test', 'ck_is_producer': True})
        product = self._make_product(ck_producer_id=producer.id)
        self.assertTrue(product._is_ck_qualified_for_public_exposure())

    def test_missing_traceability_not_qualified(self):
        product = self._make_product()
        self.assertFalse(product._is_ck_qualified_for_public_exposure())

    def test_no_image_not_qualified(self):
        producer = self.Partner.create({'name': 'Producteur Test 2', 'ck_is_producer': True})
        product = self._make_product(image_1920=False, ck_producer_id=producer.id)
        self.assertFalse(product._is_ck_qualified_for_public_exposure())

    def test_no_category_not_qualified(self):
        producer = self.Partner.create({'name': 'Producteur Test 3', 'ck_is_producer': True})
        product = self._make_product(public_categ_ids=[(5, 0, 0)], ck_producer_id=producer.id)
        self.assertFalse(product._is_ck_qualified_for_public_exposure())

    def test_zero_price_not_qualified(self):
        producer = self.Partner.create({'name': 'Producteur Test 4', 'ck_is_producer': True})
        product = self._make_product(list_price=0.0, ck_producer_id=producer.id)
        self.assertFalse(product._is_ck_qualified_for_public_exposure())

    def test_variant_image_qualifies_when_template_image_missing(self):
        """Multi-variantes : une image sur une variante suffit (pas seulement product_variant_id)."""
        producer = self.Partner.create({'name': 'Producteur Test 5', 'ck_is_producer': True})
        attribute = self.env['product.attribute'].create({'name': 'Taille test'})
        v1 = self.env['product.attribute.value'].create({'name': 'S', 'attribute_id': attribute.id})
        v2 = self.env['product.attribute.value'].create({'name': 'M', 'attribute_id': attribute.id})
        product = self._make_product(
            image_1920=False,
            ck_producer_id=producer.id,
            attribute_line_ids=[(0, 0, {
                'attribute_id': attribute.id,
                'value_ids': [(6, 0, [v1.id, v2.id])],
            })],
        )
        product.product_variant_ids[-1].image_1920 = _TINY_PNG
        self.assertTrue(product._is_ck_qualified_for_public_exposure())


@tagged('post_install', '-at_install', 'dorevia_ck_catalog_qualification')
class TestCkOrphanProduct(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Category = cls.env['product.public.category'].sudo()
        cls.Product = cls.env['product.template'].sudo()

    def _make_product(self, categ, **overrides):
        vals = {
            'name': 'Test Produit Orphelin',
            'sale_ok': True,
            'is_published': True,
            'website_published': True,
            'public_categ_ids': [(4, categ.id)] if categ else [],
        }
        vals.update(overrides)
        return self.Product.create(vals)

    def test_active_category_not_orphan(self):
        categ = self.Category.create({'name': 'TestCat Orphan Active', 'ck_exposure_status': 'active'})
        product = self._make_product(categ)
        self.assertFalse(product.ck_is_orphan)

    def test_promise_category_not_orphan(self):
        categ = self.Category.create({'name': 'TestCat Orphan Promise', 'ck_exposure_status': 'promise'})
        product = self._make_product(categ)
        self.assertFalse(product.ck_is_orphan)

    def test_hidden_category_is_orphan(self):
        categ = self.Category.create({'name': 'TestCat Orphan Hidden', 'ck_exposure_status': 'hidden'})
        product = self._make_product(categ)
        self.assertTrue(product.ck_is_orphan)

    def test_no_category_is_orphan(self):
        product = self._make_product(None)
        self.assertTrue(product.ck_is_orphan)

    def test_unpublished_product_not_orphan(self):
        """Un produit non publié n'est pas signalé — pas de bruit BO inutile."""
        product = self._make_product(None, website_published=False, is_published=False)
        self.assertFalse(product.ck_is_orphan)

    def test_recomputes_on_category_status_change(self):
        categ = self.Category.create({'name': 'TestCat Orphan Dynamique', 'ck_exposure_status': 'active'})
        product = self._make_product(categ)
        self.assertFalse(product.ck_is_orphan)
        categ.write({'ck_exposure_status': 'hidden'})
        self.assertTrue(product.ck_is_orphan)
