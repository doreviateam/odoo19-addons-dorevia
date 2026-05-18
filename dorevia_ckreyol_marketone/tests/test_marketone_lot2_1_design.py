# -*- coding: utf-8 -*-
"""Tests Lot 2.1 — design system minimal Artisanal Terroir."""

import re

from odoo.tests import tagged
from odoo.tests.common import HttpCase, TransactionCase


@tagged("post_install", "-at_install", "dorevia_marketone_lot2_1")
class TestMarketoneLot21DesignHttp(HttpCase):
    """Enveloppe site : chrome C-Kreyol sans contenu Odoo generique."""

    def test_home_http_200(self):
        self.assertEqual(self.url_open("/").status_code, 200)

    def test_shop_http_200(self):
        self.assertEqual(self.url_open("/shop").status_code, 200)

    def test_home_contains_marketone_root(self):
        content = self.url_open("/").content
        self.assertIn(b"marketone-root", content)

    def test_shop_contains_marketone_shop(self):
        content = self.url_open("/shop").content
        self.assertIn(b"marketone-shop", content)

    def test_chrome_contains_brand_text(self):
        content = self.url_open("/").content
        self.assertIn(b"C-Kreyol", content)
        self.assertIn(b'marketone-chrome__brand-text', content)
        self.assertIn(b'class="marketone-chrome', content)

    def test_footer_marketone_scope(self):
        content = self.url_open("/").content
        self.assertIn(b"marketone-footer", content)

    def test_footer_no_odoo_generic_blocks(self):
        html = self.url_open("/").text
        footer_match = re.search(
            r'<footer[^>]*id="bottom"[^>]*>(.*?)</footer>',
            html,
            flags=re.DOTALL,
        )
        self.assertTrue(footer_match, "Bloc footer introuvable dans la page.")
        footer_html = footer_match.group(1)
        for forbidden in (
            "About us",
            "Useful Links",
            "info@yourcompany.example.com",
            "+1 555-555-5556",
            "Your Logo",
        ):
            self.assertNotIn(
                forbidden,
                footer_html,
                f"Contenu footer Odoo generique encore present : {forbidden}",
            )

    def test_footer_no_powered_by_odoo_visible(self):
        text = self.url_open("/").text
        self.assertNotIn(
            "Powered by odoo",
            text,
            "La mention Powered by odoo ne doit pas etre visible.",
        )


@tagged("post_install", "-at_install", "dorevia_marketone_lot2_1")
class TestMarketoneLot21DesignInstall(TransactionCase):
    """Non-regression modules interdits."""

    def test_legacy_and_theme_not_installed(self):
        for name in ("dorevia_ckreyol_marketplace", "theme_classic_store"):
            mod = self.env["ir.module.module"].search([("name", "=", name)], limit=1)
            self.assertNotEqual(
                mod.state,
                "installed",
                f"{name} ne doit pas etre installe.",
            )

    def test_optional_shop_modules_not_installed(self):
        for name in ("website_sale_wishlist", "website_sale_comparison"):
            mod = self.env["ir.module.module"].search([("name", "=", name)], limit=1)
            self.assertNotEqual(
                mod.state,
                "installed",
                f"{name} ne doit pas etre installe.",
            )
