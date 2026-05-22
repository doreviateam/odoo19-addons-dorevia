# -*- coding: utf-8 -*-
"""Wishlist standard Odoo — activation et cosmétique CK (sans logique métier).

Tag CI :

    --test-tags=dorevia_marketone_shop_wishlist
"""

import re

from odoo.tests import tagged
from odoo.tests.common import HttpCase, TransactionCase


@tagged("post_install", "-at_install", "dorevia_marketone_shop_wishlist")
class TestMarketoneShopWishlistInstall(TransactionCase):
    def test_wishlist_module_installed(self):
        mod = self.env["ir.module.module"].search(
            [("name", "=", "website_sale_wishlist")],
            limit=1,
        )
        self.assertEqual(mod.state, "installed")

    def test_grid_wishlist_button_odoo_disabled(self):
        view = self.env.ref("website_sale_wishlist.add_to_wishlist", raise_if_not_found=False)
        self.assertTrue(view, "Vue add_to_wishlist attendue.")
        self.assertFalse(view.active, "Doublon grille Odoo doit rester desactive.")


@tagged("post_install", "-at_install", "dorevia_marketone_shop_wishlist")
class TestMarketoneShopWishlistHttp(HttpCase):
    def test_shop_wishlist_page_http_200(self):
        response = self.url_open("/shop/wishlist")
        self.assertEqual(response.status_code, 200)

    def test_shop_wishlist_page_scope_class(self):
        response = self.url_open("/shop/wishlist")
        self.assertIn("marketone-shop-wishlist", response.text)

    def test_shop_card_wishlist_overlay_functional(self):
        response = self.url_open("/shop")
        self.assertEqual(response.status_code, 200)
        html = response.text
        self.assertIn("marketone-shop-card-wishlist-wrap", html)
        self.assertRegex(
            html,
            r'marketone-shop-card-wishlist[^"]*o_add_wishlist',
        )
        self.assertIn('data-action="o_wishlist"', html)
        self.assertNotIn("marketone-shop-card-wishlist--visual", html)

    def test_shop_no_duplicate_grid_wishlist_button(self):
        """Bouton wishlist natif grille Odoo desactive — overlay unique coin image."""
        response = self.url_open("/shop")
        html = response.text
        card_blocks = re.findall(
            r'<form[^>]*class="[^"]*oe_product_cart[^"]*"[^>]*>.*?</form>',
            html,
            flags=re.DOTALL,
        )
        self.assertTrue(card_blocks, "Au moins une carte produit attendue.")
        for block in card_blocks[:3]:
            wishlist_buttons = re.findall(
                r'class="[^"]*o_add_wishlist[^"]*"',
                block,
            )
            self.assertLessEqual(
                len(wishlist_buttons),
                1,
                "Une seule action wishlist par carte (overlay coin image).",
            )

    def test_header_wishlist_link_present(self):
        response = self.url_open("/shop")
        self.assertIn("o_wsale_my_wish", response.text)

    def test_product_page_http_200(self):
        product = self.env["product.template"].search(
            [("website_published", "=", True), ("sale_ok", "=", True)],
            limit=1,
        )
        self.assertTrue(product, "Produit publie requis pour smoke fiche.")
        response = self.url_open(product.website_url)
        self.assertEqual(response.status_code, 200)

    def test_cart_page_http_200(self):
        response = self.url_open("/shop/cart")
        self.assertEqual(response.status_code, 200)
