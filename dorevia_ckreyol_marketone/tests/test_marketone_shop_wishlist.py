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
                    "name": "C-Kreyol UX-4 Wishlist Card",
                    "type": "consu",
                    "list_price": 9.5,
                    "sale_ok": True,
                    "is_published": True,
                }
            )
        cls.variant = cls.product.product_variant_id

    def _ensure_wishlist_item(self):
        self.authenticate(None, None)
        self.env["product.wishlist"].sudo().search(
            [
                ("product_id", "=", self.variant.id),
                ("website_id", "=", self.website.id),
            ]
        ).unlink()
        self.make_jsonrpc_request(
            "/shop/wishlist/add",
            {"product_id": self.variant.id},
        )

    def _open_wishlist_html(self):
        response = self.url_open("/shop/wishlist")
        self.assertEqual(response.status_code, 200)
        return response.text

    def test_shop_wishlist_page_http_200(self):
        response = self.url_open("/shop/wishlist")
        self.assertEqual(response.status_code, 200)

    def test_shop_wishlist_page_scope_class(self):
        response = self.url_open("/shop/wishlist")
        html = response.text
        self.assertIn("marketone-shop-wishlist", html)
        wrap_match = re.search(
            r'<div id="wrap"[^>]*class="([^"]*)"',
            html,
        )
        self.assertTrue(wrap_match, "Wrap wishlist attendu.")
        wrap_classes = wrap_match.group(1).split()
        self.assertIn("marketone-shop-wishlist", wrap_classes)
        self.assertNotIn(
            "marketone-shop",
            wrap_classes,
            "La page wishlist ne doit pas porter le scope boutique UX-4.",
        )

    def test_wishlist_card_compact_cart_markup(self):
        """Lot 3quinquies — CTA panier compact sans marketone-shop-card-cart."""
        self._ensure_wishlist_item()
        html = self._open_wishlist_html()
        self.assertIn("o_wishlist_item", html)
        wishlist_blocks = re.findall(
            r'<article[^>]*class="[^"]*o_wishlist_item[^"]*"[^>]*>.*?</article>',
            html,
            flags=re.DOTALL,
        )
        self.assertTrue(wishlist_blocks, "Au moins une carte wishlist attendue.")
        block = wishlist_blocks[0]
        self.assertIn("marketone-wishlist-card-cart--tile", block)
        self.assertIn("marketone-wishlist-card-cart__label", block)
        self.assertRegex(block, r'o_wish_add[^>]*marketone-wishlist-card-cart')
        self.assertNotRegex(block, r'o_wish_add[^>]*marketone-shop-card-cart')
        self.assertNotRegex(
            block,
            r'o_wish_add[^>]*>\s*<i[^>]*fa-shopping-cart[^>]*>\s*<span[^>]*>\s*Add to Cart',
        )

    def test_wishlist_card_price_and_remove_markup(self):
        """Lot 3quinquies — prix aligné boutique · retrait cœur overlay."""
        self._ensure_wishlist_item()
        html = self._open_wishlist_html()
        wishlist_blocks = re.findall(
            r'<article[^>]*class="[^"]*o_wishlist_item[^"]*"[^>]*>.*?</article>',
            html,
            flags=re.DOTALL,
        )
        self.assertTrue(wishlist_blocks, "Au moins une carte wishlist attendue.")
        block = wishlist_blocks[0]
        self.assertRegex(block, r'o_wish_price[^"]*marketone-shop-card-price')
        self.assertRegex(block, r'o_wish_rm[^"]*marketone-wishlist-card-remove')
        self.assertRegex(
            block,
            r'marketone-wishlist-card-remove[^>]*>\s*<i[^>]*fa-heart',
        )

    def test_wishlist_card_cart_btn_inside_image(self):
        """Lot 3quinquies — CTA panier ancré zone photo (pas pied de carte)."""
        self._ensure_wishlist_item()
        html = self._open_wishlist_html()
        wishlist_blocks = re.findall(
            r'<article[^>]*class="[^"]*o_wishlist_item[^"]*"[^>]*>.*?</article>',
            html,
            flags=re.DOTALL,
        )
        self.assertTrue(wishlist_blocks, "Au moins une carte wishlist attendue.")
        block = wishlist_blocks[0]
        idx_info = block.find("o_wsale_product_information")
        idx_add = block.find("o_wish_add")
        idx_img = block.find("oe_product_image")
        self.assertGreater(idx_info, 0, "Bloc information attendu.")
        self.assertGreater(idx_add, 0, "CTA panier attendu.")
        self.assertGreater(idx_img, 0, "Zone image attendue.")
        self.assertLess(
            idx_add,
            idx_info,
            "CTA panier doit être rendu dans la zone photo, avant le bloc information.",
        )

        """Lot 3quinquies — CTA Voir wishlist sans preview autorisée."""
        self._ensure_wishlist_item()
        html = self._open_wishlist_html()
        wishlist_blocks = re.findall(
            r'<article[^>]*class="[^"]*o_wishlist_item[^"]*"[^>]*>.*?</article>',
            html,
            flags=re.DOTALL,
        )
        self.assertTrue(wishlist_blocks, "Au moins une carte wishlist attendue.")
        for block in wishlist_blocks[:3]:
            cta_matches = re.findall(
                r'<a[^>]*class="[^"]*marketone-shop-card-cta[^"]*"[^>]*>',
                block,
            )
            for cta in cta_matches:
                self.assertIn(
                    'data-marketone-preview-allowed="False"',
                    cta,
                    "CTA Voir wishlist doit désactiver la preview.",
                )

    def test_shop_card_wishlist_overlay_functional(self):
        response = self.url_open("/shop")
        self.assertEqual(response.status_code, 200)
        html = response.text
        self.assertIn("marketone-shop-card-wishlist-wrap", html)
        self.assertRegex(
            html,
            r'marketone-shop-card-wishlist[^"]*btn',
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
            marketone_buttons = re.findall(
                r'class="[^"]*\bmarketone-shop-card-wishlist btn[^"]*"',
                block,
            )
            self.assertLessEqual(
                len(marketone_buttons),
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
