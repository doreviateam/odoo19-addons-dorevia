# -*- coding: utf-8 -*-
"""Tests Lot 5 — smoke panier / checkout (marketone-cart / marketone-checkout)."""

import re

from odoo.http import root
from odoo.tests import tagged
from odoo.tests.common import HttpCase


@tagged("post_install", "-at_install", "dorevia_marketone_lot5")
class TestMarketoneLot5CartCheckout(HttpCase):
    """Tunnel invité standard website_sale ; presentation Marketone uniquement."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        ProductTemplate = cls.env["product.template"]
        cls.website = cls.env["website"].search([], limit=1)
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
                    "name": "C-Kreyol Recette Marketone 5",
                    "type": "consu",
                    "list_price": 9.9,
                    "sale_ok": True,
                    "is_published": True,
                }
            )
        cls.test_variant = cls.test_product.product_variant_id

    def _bind_public_cart(self, order):
        session = self.authenticate(None, None)
        session["sale_order_id"] = order.id
        root.session_store.save(session)

    def _create_cart_order(self, quantity=1.0):
        partner = self.env.ref("base.public_partner")
        order = self.env["sale.order"].create(
            {
                "partner_id": partner.id,
                "website_id": self.website.id,
            }
        )
        order._cart_add(
            product_id=self.test_variant.id,
            quantity=quantity,
        )
        return order

    def _add_to_cart_jsonrpc(self, quantity=1):
        self.authenticate(None, None)
        self.make_jsonrpc_request(
            "/shop/cart/add",
            {
                "product_template_id": self.test_product.id,
                "product_id": self.test_variant.id,
                "quantity": quantity,
            },
        )

    def test_cart_http_200_empty(self):
        self.authenticate(None, None)
        response = self.url_open("/shop/cart")
        self.assertEqual(response.status_code, 200)

    def test_cart_has_marketone_cart_scope(self):
        order = self._create_cart_order()
        self._bind_public_cart(order)
        response = self.url_open("/shop/cart")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"marketone-cart", response.content)

    def _open_checkout_flow(self):
        """Odoo 19 CE : /shop/checkout redirige souvent vers /shop/address (invité)."""
        return self.url_open("/shop/checkout", allow_redirects=True)

    def test_checkout_http_200_with_cart(self):
        order = self._create_cart_order()
        self._bind_public_cart(order)
        response = self._open_checkout_flow()
        self.assertEqual(response.status_code, 200)

    def test_checkout_has_marketone_checkout_scope(self):
        order = self._create_cart_order()
        self._bind_public_cart(order)
        response = self._open_checkout_flow()
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"marketone-checkout", response.content)

    def test_add_to_cart_via_jsonrpc_then_cart_page(self):
        self._add_to_cart_jsonrpc()
        response = self.url_open("/shop/cart")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"marketone-cart", response.content)
        self.assertTrue(
            re.search(r"o_cart_product|cart_products|js_cart_lines", response.text),
            "Structure panier website_sale attendue.",
        )

    def test_cart_has_line_controls(self):
        order = self._create_cart_order()
        self._bind_public_cart(order)
        response = self.url_open("/shop/cart")
        text = response.text
        self.assertTrue(
            re.search(r"js_quantity|cart_lines_quantity|quantity", text),
            "Controle quantite panier attendu.",
        )
        self.assertTrue(
            re.search(r"js_delete_product|fa-trash", text),
            "Controle suppression ligne attendu.",
        )

    def test_cart_no_other_product_scopes(self):
        order = self._create_cart_order()
        self._bind_public_cart(order)
        response = self.url_open("/shop/cart")
        content = response.content
        self.assertNotIn(b"marketone-shop", content)
        self.assertNotIn(b"marketone-product", content)

    def test_checkout_no_marketone_cart_scope(self):
        order = self._create_cart_order()
        self._bind_public_cart(order)
        response = self._open_checkout_flow()
        self.assertIn(b"marketone-checkout", response.content)
        self.assertNotIn(
            b"marketone-cart",
            response.content,
            "Le checkout ne doit pas porter marketone-cart.",
        )

    def test_checkout_no_catalog_gates(self):
        order = self._create_cart_order()
        self._bind_public_cart(order)
        response = self._open_checkout_flow()
        text = response.text
        for forbidden in (
            r"marketone_mode=",
            r"ckr_mode=",
            r"/promotions",
            r"/kits",
        ):
            self.assertIsNone(
                re.search(forbidden, text),
                f"Lien porte catalogue interdit sur checkout : {forbidden}",
            )

    def test_cart_no_catalog_gates(self):
        order = self._create_cart_order()
        self._bind_public_cart(order)
        response = self.url_open("/shop/cart")
        text = response.text
        for forbidden in (
            r"marketone_mode=",
            r"ckr_mode=",
            r"/promotions",
            r"/kits",
        ):
            self.assertIsNone(
                re.search(forbidden, text),
                f"Lien porte catalogue interdit sur panier : {forbidden}",
            )

    def test_home_unchanged_after_cart_flow(self):
        order = self._create_cart_order()
        self._bind_public_cart(order)
        self.url_open("/shop/cart")
        response = self.url_open("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"marketone-root", response.content)
        self.assertNotIn(b"marketone-cart", response.content)

    def test_shop_unchanged_after_cart_flow(self):
        order = self._create_cart_order()
        self._bind_public_cart(order)
        self.url_open("/shop/cart")
        response = self.url_open("/shop")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"marketone-shop", response.content)
        self.assertNotIn(b"marketone-cart", response.content)
