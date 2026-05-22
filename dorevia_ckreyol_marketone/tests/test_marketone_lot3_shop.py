# -*- coding: utf-8 -*-
"""Tests Lot 3 — presentation boutique /shop (marketone-shop)."""

import re

from odoo.tests import tagged
from odoo.tests.common import HttpCase


@tagged("post_install", "-at_install", "dorevia_marketone_lot3")
class TestMarketoneLot3Shop(HttpCase):
    """Liste /shop habillee ; fiche produit et home hors scope shop."""

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
                    "name": "C-Kreyol Recette Marketone",
                    "type": "consu",
                    "list_price": 12.5,
                    "sale_ok": True,
                    "is_published": True,
                }
            )

    def test_shop_http_200(self):
        response = self.url_open("/shop")
        self.assertEqual(response.status_code, 200)

    def test_shop_has_marketone_shop_scope(self):
        response = self.url_open("/shop")
        self.assertIn(b"marketone-shop", response.content)

    def test_shop_has_wsale_structure(self):
        response = self.url_open("/shop")
        self.assertIn(b"o_wsale_products_page", response.content)
        self.assertIn(b"o_wsale_products", response.content)

    def test_shop_grid_ppr_four(self):
        """Grille dense desktop — shop_ppr = 4 (TICKET_MARKETONE_BOUTIQUE_VISUAL_PARITY)."""
        response = self.url_open("/shop")
        self.assertIn(
            b'data-ppr="4"',
            response.content,
            "La grille boutique doit utiliser 4 colonnes sur desktop large.",
        )

    def test_home_has_no_marketone_shop(self):
        response = self.url_open("/")
        self.assertIn(b"marketone-root", response.content)
        self.assertNotIn(b"marketone-shop", response.content)

    def test_shop_has_no_home_blocks(self):
        response = self.url_open("/shop")
        self.assertNotIn(b"marketone-home-intro", response.content)

    def test_product_page_no_marketone_shop_yet(self):
        url = self.test_product.website_url
        self.assertTrue(url, "Produit de recette sans website_url.")
        response = self.url_open(url)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(
            b"marketone-shop",
            response.content,
            "La fiche produit reste hors scope Lot 3 (Lot 4).",
        )

    def test_shop_no_catalog_gates(self):
        response = self.url_open("/shop")
        text = response.text
        # Alias portes uniquement (pas les slugs catégorie /shop/category/incontournables-*).
        gate_href = r"""href=['"]/(?:promotions|kits|incontournables|origines)(?:['"?]|$)"""
        for forbidden in (
            r"marketone_mode=",
            r"ckr_mode=",
            gate_href,
        ):
            self.assertIsNone(
                re.search(forbidden, text),
                f"Lien porte catalogue interdit sur /shop : {forbidden}",
            )

    def test_shop_website_sale_controls_present(self):
        response = self.url_open("/shop")
        text = response.text
        self.assertTrue(
            re.search(r"o_wsale_products|oe_product|products_grid", text),
            "Structure liste website_sale attendue sur /shop.",
        )

    def test_shop_conversion_tile_structure(self):
        """Tuile conversion MOA — titre 2 lignes, CTA Voir fiche, prix droite, panier survol."""
        response = self.url_open("/shop")
        self.assertEqual(response.status_code, 200)
        html = response.text
        self.assertIn("marketone-shop-card-title", html)
        self.assertIn("marketone-shop-card-footer", html)
        self.assertIn("marketone-shop-card-cta", html)
        cta_match = re.search(r"<a\b[^>]*marketone-shop-card-cta[^>]*>", html)
        self.assertIsNotNone(cta_match, "Ancre CTA conversion attendue dans /shop.")
        self.assertRegex(
            cta_match.group(0),
            r'href="/shop/[^"]+"',
            "CTA Voir doit pointer vers la fiche produit.",
        )
        self.assertIn("marketone-shop-card-wishlist", html)
        self.assertIn("data-action=\"o_wishlist\"", html)
        self.assertNotIn("marketone-shop-card-wishlist--visual", html)
        self.assertNotIn("oe_subdescription", html)
        self.assertIn("o_wsale_product_btn", html)

    def test_shop_tile_photo_full_bleed_markup(self):
        """Grille — cover natif + classe dérivé pour rognage aplat v1.1 bake-in."""
        response = self.url_open("/shop")
        self.assertEqual(response.status_code, 200)
        html = response.text
        self.assertIn("o_wsale_products_opt_thumb_cover", html)
        self.assertIn("marketone-shop-tile-photo", html)
