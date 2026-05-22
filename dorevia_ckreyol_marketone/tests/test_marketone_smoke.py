# -*- coding: utf-8 -*-
"""Smoke Lot 1 — installation et non-regression website_sale minimale."""

from odoo.tests import tagged
from odoo.tests.common import HttpCase, TransactionCase


@tagged("post_install", "-at_install", "dorevia_marketone_smoke")
class TestMarketoneSmokeInstall(TransactionCase):
    """Verifications ORM apres installation du module."""

    def test_module_state_installed(self):
        mod = self.env["ir.module.module"].search(
            [("name", "=", "dorevia_ckreyol_marketone")],
            limit=1,
        )
        self.assertTrue(mod, "Module dorevia_ckreyol_marketone introuvable.")
        self.assertEqual(mod.state, "installed")

    def test_socle_dependencies_installed(self):
        for name in ("website", "website_sale", "portal"):
            mod = self.env["ir.module.module"].search([("name", "=", name)], limit=1)
            self.assertEqual(mod.state, "installed", f"{name} doit rester installe.")

    def test_legacy_and_theme_not_installed(self):
        for name in ("dorevia_ckreyol_marketplace", "theme_classic_store"):
            mod = self.env["ir.module.module"].search([("name", "=", name)], limit=1)
            self.assertNotEqual(
                mod.state,
                "installed",
                f"{name} ne doit pas etre installe sur la base Marketone.",
            )

    def test_wishlist_dependency_installed(self):
        mod = self.env["ir.module.module"].search(
            [("name", "=", "website_sale_wishlist")],
            limit=1,
        )
        self.assertEqual(
            mod.state,
            "installed",
            "website_sale_wishlist doit etre installe (dependance Marketone).",
        )

    def test_comparison_module_not_installed(self):
        mod = self.env["ir.module.module"].search(
            [("name", "=", "website_sale_comparison")],
            limit=1,
        )
        self.assertNotEqual(
            mod.state,
            "installed",
            "website_sale_comparison ne doit pas etre installe au Lot 1.",
        )


@tagged("post_install", "-at_install", "dorevia_marketone_smoke")
class TestMarketoneSmokeHttp(HttpCase):
    """Pages website_sale standard accessibles apres install Marketone."""

    def test_home_http_200(self):
        response = self.url_open("/")
        self.assertEqual(response.status_code, 200)

    def test_shop_http_200(self):
        response = self.url_open("/shop")
        self.assertEqual(response.status_code, 200)
