# -*- coding: utf-8 -*-
"""Tests Lot A — collections commerciales BO (`marketone.shop.collection`)."""

from odoo.exceptions import ValidationError
from odoo.tests import tagged
from odoo.tests.common import HttpCase, TransactionCase


@tagged("post_install", "-at_install", "dorevia_marketone_collection_lot_a")
class TestMarketoneCollectionLotAModel(TransactionCase):
    """Modèle collection — contraintes MOA Lot A."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Collection = cls.env["marketone.shop.collection"]
        cls.product = cls.env["product.template"].create(
            {
                "name": "Produit test collection Lot A",
                "sale_ok": True,
                "website_published": True,
            }
        )

    def test_draft_collection_without_products(self):
        coll = self.Collection.create(
            {
                "name": "Brouillon vide",
                "slug": "brouillon-vide-lot-a",
                "website_published": False,
            }
        )
        self.assertFalse(coll.product_ids)
        self.assertEqual(coll.product_count, 0)

    def test_published_collection_requires_sellable_product(self):
        with self.assertRaises(ValidationError):
            self.Collection.create(
                {
                    "name": "Publiée vide",
                    "slug": "publiee-vide-lot-a",
                    "website_published": True,
                }
            )

    def test_published_collection_with_product(self):
        coll = self.Collection.create(
            {
                "name": "Apéritif test",
                "slug": "aperitif-test-lot-a",
                "website_published": True,
                "product_ids": [(6, 0, self.product.ids)],
            }
        )
        self.assertEqual(coll.product_count, 1)

    def test_slug_format_invalid(self):
        with self.assertRaises(ValidationError):
            self.Collection.create(
                {
                    "name": "Slug invalide",
                    "slug": "Slug_Invalide",
                    "website_published": False,
                }
            )

    def test_date_end_before_start(self):
        with self.assertRaises(ValidationError):
            self.Collection.create(
                {
                    "name": "Dates incohérentes",
                    "slug": "dates-incoherentes-lot-a",
                    "date_start": "2026-12-01",
                    "date_end": "2026-01-01",
                    "website_published": False,
                }
            )

    def test_product_m2m_inverse(self):
        coll = self.Collection.create(
            {
                "name": "M2M inverse",
                "slug": "m2m-inverse-lot-a",
                "website_published": True,
                "product_ids": [(6, 0, self.product.ids)],
            }
        )
        self.assertIn(coll, self.product.marketone_collection_ids)

    def test_unpublished_product_not_counted_for_publish_check(self):
        unpublished = self.env["product.template"].create(
            {
                "name": "Non publié shop",
                "sale_ok": True,
                "website_published": False,
            }
        )
        with self.assertRaises(ValidationError):
            self.Collection.create(
                {
                    "name": "Faux positif publish",
                    "slug": "faux-positif-publish-lot-a",
                    "website_published": True,
                    "product_ids": [(6, 0, unpublished.ids)],
                }
            )


@tagged("post_install", "-at_install", "dorevia_marketone_collection_lot_a")
class TestMarketoneCollectionLotANonRegression(HttpCase):
    """Pas de route / facette collection côté shop."""

    def test_shop_200_without_collection_facet(self):
        response = self.url_open("/shop")
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b"marketone_collection=", response.content)

    def test_shop_sidebar_non_regression(self):
        response = self.url_open("/shop")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"marketone-sidebar-cat-check", response.content)
