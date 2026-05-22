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
        self.assertNotIn(
            "marketone-shop-card-cart-feedback__link",
            html,
            "Tuile UX-4 : pas de lien « Voir le panier » sur la carte (navigation panier via header).",
        )
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

    def _marketone_default_no_variant_ptav_ids(self, product):
        return product.attribute_line_ids.filtered(
            lambda line: line.attribute_id.create_variant == "no_variant"
            and len(line.value_ids) == 1
        ).mapped("product_template_value_ids").ids

    def test_shop_grid_exposes_default_no_variant_ptav(self):
        product = self.env["product.template"].search(
            [
                ("name", "ilike", "Maniocookies"),
                ("sale_ok", "=", True),
                ("is_published", "=", True),
            ],
            limit=1,
        )
        if not product:
            self.skipTest("Produit Maniocookies requis pour consolidation origine.")
        ptav_ids = self._marketone_default_no_variant_ptav_ids(product)
        self.assertTrue(ptav_ids, "Origine unique attendue sur Maniocookies.")
        response = self.url_open("/shop?search=Maniocookies")
        self.assertEqual(response.status_code, 200)
        for ptav_id in ptav_ids:
            self.assertIn(
                f'data-marketone-no-variant-ptav-ids="{",".join(map(str, ptav_ids))}"',
                response.text,
                "PTAV origine doit etre expose dans la tuile grille.",
            )
            break

    def test_cart_double_add_consolidates_single_line_with_origin(self):
        """Lot 2 — double add avec PTAV origine : une ligne qty 2 (standard Odoo)."""
        self.authenticate(None, None)
        product = self.env["product.template"].search(
            [
                ("name", "ilike", "Maniocookies"),
                ("sale_ok", "=", True),
                ("is_published", "=", True),
            ],
            limit=1,
        )
        if not product:
            self.skipTest("Produit Maniocookies requis pour consolidation origine.")
        variant = product.product_variant_id
        ptav_ids = self._marketone_default_no_variant_ptav_ids(product)
        partner = self.env.ref("base.public_partner")
        self.env["sale.order"].sudo().search(
            [
                ("partner_id", "=", partner.id),
                ("website_id", "=", self.website.id),
                ("state", "=", "draft"),
            ]
        ).unlink()

        payload = {
            "product_template_id": product.id,
            "product_id": variant.id,
            "quantity": 1,
            "no_variant_attribute_value_ids": ptav_ids,
        }
        self.make_jsonrpc_request("/shop/cart/add", payload)
        self.make_jsonrpc_request("/shop/cart/add", payload)

        cart = self.env["sale.order"].sudo().search(
            [
                ("partner_id", "=", partner.id),
                ("website_id", "=", self.website.id),
                ("state", "=", "draft"),
            ],
            limit=1,
        )
        lines = cart.order_line.filtered(
            lambda line: line.product_id.id == variant.id
        )
        self.assertEqual(len(lines), 1, "Consolidation sur une seule ligne attendue.")
        self.assertEqual(lines.product_uom_qty, 2.0)


@tagged("post_install", "-at_install", "dorevia_marketone_shop_in_place")
class TestMarketoneShopInPlacePreview(HttpCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.website = cls.env["website"].search([], limit=1)
        cls.simple_product = cls.env["product.template"].search(
            [
                ("sale_ok", "=", True),
                ("is_published", "=", True),
            ],
            limit=20,
        ).filtered(lambda product: product._marketone_preview_full_allowed())[:1]

    def test_shop_grid_preview_shell_and_cta_data(self):
        response = self.url_open("/shop")
        self.assertEqual(response.status_code, 200)
        html = response.text
        self.assertIn("marketone_shop_preview_offcanvas", html)
        self.assertIn("marketone-shop-preview-offcanvas__close", html)
        self.assertIn("Découvrir le produit", html)
        self.assertIn('aria-label="Fermer l&#39;aperçu"', html)
        self.assertNotIn("marketone-shop-preview-offcanvas__close-text", html)
        self.assertIn("marketone-shop-card-preview-slot", html)
        self.assertIn("data-marketone-preview-allowed", html)
        self.assertIn("data-product-template-id", html)
        self.assertIn('data-marketone-preview-allowed="True"', html)
        self.assertRegex(
            html,
            r'marketone-shop-card-cta[^>]*href="/shop/[^"]+"',
            "CTA Voir conserve href fiche (fallback / SEO).",
        )

    def test_preview_route_returns_fragment_for_simple_product(self):
        if not self.simple_product or not self.simple_product._marketone_preview_full_allowed():
            self.skipTest("Produit simple publié requis pour preview V1.")
        response = self.url_open(
            f"/shop/product/preview/{self.simple_product.id}"
        )
        self.assertEqual(response.status_code, 200)
        html = response.text
        self.assertIn("marketone-shop-preview", html)
        self.assertIn("marketone-shop-preview__close", html)
        self.assertIn("Découvrir le produit", html)
        self.assertIn("Fermer", html)
        self.assertIn("marketone-shop-preview__media-frame", html)
        self.assertIn("marketone-shop-preview__full-link", html)
        self.assertIn("Voir la fiche complète", html)
        self.assertIn("marketone-shop-card-cart", html)
        self.assertIn("marketone-shop-card-wishlist", html)

    def test_preview_route_not_found_for_unknown_product(self):
        response = self.url_open("/shop/product/preview/999999999")
        self.assertEqual(response.status_code, 404)

    def test_preview_full_allowed_false_for_multi_variant_template(self):
        multi = self.env["product.template"].search(
            [
                ("sale_ok", "=", True),
                ("is_published", "=", True),
            ],
            limit=50,
        ).filtered(lambda product: product.product_variant_count > 1)[:1]
        if not multi:
            attr = self.env["product.attribute"].create({"name": "Taille UX4 Test"})
            val_s = self.env["product.attribute.value"].create(
                {"name": "S", "attribute_id": attr.id}
            )
            val_m = self.env["product.attribute.value"].create(
                {"name": "M", "attribute_id": attr.id}
            )
            multi = self.env["product.template"].create(
                {
                    "name": "C-Kreyol UX-4 Preview Multi",
                    "type": "consu",
                    "list_price": 9.0,
                    "sale_ok": True,
                    "is_published": True,
                    "attribute_line_ids": [
                        (
                            0,
                            0,
                            {
                                "attribute_id": attr.id,
                                "value_ids": [(6, 0, [val_s.id, val_m.id])],
                            },
                        )
                    ],
                }
            )
        self.assertFalse(multi._marketone_preview_full_allowed())
        response = self.url_open(f"/shop/product/preview/{multi.id}")
        self.assertEqual(response.status_code, 404)
