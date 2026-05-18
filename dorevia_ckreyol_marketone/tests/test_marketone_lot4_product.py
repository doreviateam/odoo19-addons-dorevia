# -*- coding: utf-8 -*-
"""Tests Lot 4 — presentation fiche produit (marketone-product)."""

import re

from odoo.tests import tagged
from odoo.tests.common import HttpCase


@tagged("post_install", "-at_install", "dorevia_marketone_lot4")
class TestMarketoneLot4Product(HttpCase):
    """Fiche produit habillee ; home et liste hors scope product."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        ProductTemplate = cls.env["product.template"]
        cls.test_product = ProductTemplate.search(
            [
                ("sale_ok", "=", True),
                ("is_published", "=", True),
            ],
            limit=1,
        )
        if not cls.test_product:
            cls.test_product = ProductTemplate.create(
                {
                    "name": "C-Kreyol Recette Marketone 4",
                    "type": "consu",
                    "list_price": 14.9,
                    "sale_ok": True,
                    "is_published": True,
                }
            )

    def _product_url(self):
        url = self.test_product.website_url
        self.assertTrue(url, "Produit de recette sans website_url.")
        return url

    def test_product_http_200(self):
        response = self.url_open(self._product_url())
        self.assertEqual(response.status_code, 200)

    def test_product_has_marketone_product_scope(self):
        response = self.url_open(self._product_url())
        self.assertIn(b"marketone-product", response.content)

    def test_shop_has_no_marketone_product(self):
        response = self.url_open("/shop")
        self.assertIn(b"marketone-shop", response.content)
        self.assertNotIn(
            b"marketone-product",
            response.content,
            "La liste /shop ne doit pas porter marketone-product.",
        )

    def test_home_has_no_marketone_product(self):
        response = self.url_open("/")
        self.assertIn(b"marketone-root", response.content)
        self.assertNotIn(b"marketone-product", response.content)

    def test_product_has_no_marketone_shop(self):
        response = self.url_open(self._product_url())
        self.assertNotIn(
            b"marketone-shop",
            response.content,
            "La fiche produit ne doit pas porter marketone-shop.",
        )

    def test_product_has_add_to_cart(self):
        response = self.url_open(self._product_url())
        text = response.text
        self.assertTrue(
            re.search(
                r"add_to_cart|js_add_cart|o_wsale_product_details_content_section_cta",
                text,
            ),
            "Controle ajout panier website_sale attendu sur la fiche.",
        )

    def test_product_no_catalog_gates(self):
        response = self.url_open(self._product_url())
        text = response.text
        for forbidden in (
            r"marketone_mode=",
            r"ckr_mode=",
            r"/promotions",
            r"/kits",
        ):
            self.assertIsNone(
                re.search(forbidden, text),
                f"Lien porte catalogue interdit sur fiche : {forbidden}",
            )
