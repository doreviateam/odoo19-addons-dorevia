# -*- coding: utf-8 -*-
"""UX-4 Lots 1–2 — interactions in-place depuis /shop sans navigation.

Tag CI :

    --test-tags=dorevia_marketone_shop_in_place
"""

import re

from odoo.tests import tagged
from odoo.tests.common import HttpCase


@tagged("post_install", "-at_install", "dorevia_marketone_shop_in_place")
class TestMarketoneShopInPlaceWishlist(HttpCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.website = cls.env["website"].search([], limit=1)
        cls.product = cls.env["product.template"].search(
            [
                ("sale_ok", "=", True),
                ("is_published", "=", True),
            ],
            limit=1,
        )
        if not cls.product:
            cls.product = cls.env["product.template"].create(
                {
                    "name": "C-Kreyol UX-4 Wishlist Toggle",
                    "type": "consu",
                    "list_price": 8.5,
                    "sale_ok": True,
                    "is_published": True,
                }
            )
        cls.variant = cls.product.product_variant_id

    def test_shop_grid_wishlist_uses_is_in_wishlist(self):
        response = self.url_open("/shop")
        self.assertEqual(response.status_code, 200)
        html = response.text
        self.assertIn("marketone-shop-card-wishlist", html)
        self.assertIn('data-action="o_wishlist"', html)
        self.assertNotRegex(
            html,
            r'marketone-shop-card-wishlist[^"]*\bo_add_wishlist\b',
            "Grille UX-4 : pas de classe o_add_wishlist (handler Odoo 19 add-only).",
        )
        self.assertNotRegex(
            html,
            r'marketone-shop-card-wishlist[^>]*disabled',
            "Le coeur grille ne doit pas etre disabled (toggle UX-4).",
        )

    def test_wishlist_toggle_add_remove_json(self):
        self.authenticate(None, None)
        self.make_jsonrpc_request(
            "/shop/wishlist/add",
            {"product_id": self.variant.id},
        )
        wishes = self.env["product.wishlist"].sudo().search(
            [
                ("product_id", "=", self.variant.id),
                ("website_id", "=", self.website.id),
            ]
        )
        self.assertTrue(wishes, "Produit attendu en wishlist apres add JSON.")

        self.make_jsonrpc_request(
            "/shop/wishlist/remove_by_product",
            {"product_id": self.variant.id},
        )
        wishes_after = self.env["product.wishlist"].sudo().search(
            [
                ("product_id", "=", self.variant.id),
                ("website_id", "=", self.website.id),
            ]
        )
        self.assertFalse(
            wishes_after,
            "Produit retire via remove_by_product.",
        )

    def test_shop_stays_on_shop_after_wishlist_json_ops(self):
        self.authenticate(None, None)
        self.make_jsonrpc_request(
            "/shop/wishlist/add",
            {"product_id": self.variant.id},
        )
        response = self.url_open("/shop")
        self.assertEqual(response.status_code, 200)
        self.assertIn("/shop", response.url)
        self.assertRegex(
            response.text,
            r'marketone-shop-card-wishlist',
        )

    def test_no_duplicate_grid_wishlist_button(self):
        response = self.url_open("/shop")
        html = response.text
        card_blocks = re.findall(
            r'<form[^>]*class="[^"]*oe_product_cart[^"]*"[^>]*>.*?</form>',
            html,
            flags=re.DOTALL,
        )
        self.assertTrue(card_blocks, "Au moins une carte produit attendue.")
        for block in card_blocks[:3]:
            marketone_buttons = re.findall(
                r'class="[^"]*\bmarketone-shop-card-wishlist btn[^"]*"',
                block,
            )
            self.assertLessEqual(
                len(marketone_buttons),
                1,
                "Une seule action wishlist Marketone par carte.",
            )


@tagged("post_install", "-at_install", "dorevia_marketone_shop_in_place")
class TestMarketoneShopInPlaceCart(HttpCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.website = cls.env["website"].search([], limit=1)
        cls.product = cls.env["product.template"].search(
            [
                ("sale_ok", "=", True),
                ("is_published", "=", True),
            ],
            limit=1,
        )
        if not cls.product:
            cls.product = cls.env["product.template"].create(
                {
                    "name": "C-Kreyol UX-4 Cart In-Place",
                    "type": "consu",
                    "list_price": 12.0,
                    "sale_ok": True,
                    "is_published": True,
                }
            )
        cls.variant = cls.product.product_variant_id

    def test_shop_grid_cart_uses_marketone_handler(self):
        response = self.url_open("/shop")
        self.assertEqual(response.status_code, 200)
        html = response.text
        self.assertIn("marketone-shop-card-cart", html)
        self.assertIn("marketone-shop-card-cart-feedback", html)
        self.assertIn("Ajouté au panier", html)
        self.assertIn("Voir le panier", html)
        self.assertNotRegex(
            html,
            r'marketone-shop-card-cart[^"]*\ba-submit\b',
            "Grille UX-4 : pas de classe a-submit (handler WebsiteSale en double).",
        )

    def test_cart_add_jsonrpc_adds_product_line(self):
        self.authenticate(None, None)
        self.make_jsonrpc_request(
            "/shop/cart/add",
            {
                "product_template_id": self.product.id,
                "product_id": self.variant.id,
                "quantity": 1,
            },
        )

        cart = self.env["sale.order"].sudo().search(
            [
                ("website_id", "=", self.website.id),
                ("state", "=", "draft"),
                ("partner_id", "=", self.env.ref("base.public_partner").id),
            ],
            limit=1,
        )
        self.assertTrue(cart, "Panier brouillon attendu apres add JSON.")
        line = cart.order_line.filtered(
            lambda line: line.product_id.id == self.variant.id
        )
        self.assertTrue(line, "Ligne produit attendue dans le panier.")
        self.assertGreaterEqual(line[0].product_uom_qty, 1)

    def test_shop_stays_on_shop_after_cart_json_add(self):
        self.authenticate(None, None)
        self.make_jsonrpc_request(
            "/shop/cart/add",
            {
                "product_template_id": self.product.id,
                "product_id": self.variant.id,
                "quantity": 1,
            },
        )
        response = self.url_open("/shop")
        self.assertEqual(response.status_code, 200)
        self.assertIn("/shop", response.url)
        self.assertIn("marketone-shop-card-cart-feedback", response.text)
