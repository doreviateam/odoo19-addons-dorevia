# -*- coding: utf-8 -*-
"""Tests Lot 6.1 — porte Incontournables (marketone_mode=featured)."""

import re
from urllib.parse import parse_qs, urlparse

from odoo.tests import tagged
from odoo.tests.common import HttpCase, TransactionCase

from odoo.addons.dorevia_ckreyol_marketone.controllers.website_sale import (
    MARKETONE_FEATURED_PARAM,
)


def _website_sale_search_options(env, **extra):
    base = {
        "displayImage": True,
        "displayDescription": True,
        "displayExtraLink": True,
        "displayDetail": True,
        "display_currency": env.company.currency_id,
    }
    base.update(extra)
    return base


@tagged("post_install", "-at_install", "dorevia_marketone_lot6_1_featured")
class TestMarketoneLot61FeaturedModel(TransactionCase):
    """Logique ``_search_get_detail`` — pas de moteur parallèle."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.website = cls.env.ref("website.default_website")
        cls.featured_category = cls.env["product.public.category"].sudo().create(
            {
                "name": "Incontournables Test",
                "website_id": cls.website.id,
            }
        )
        cls.env["ir.config_parameter"].sudo().set_param(
            MARKETONE_FEATURED_PARAM,
            str(cls.featured_category.id),
        )
        cls.product_in = cls.env["product.template"].create(
            {
                "name": "Produit Incontournable Test",
                "type": "consu",
                "list_price": 15.0,
                "sale_ok": True,
                "is_published": True,
                "public_categ_ids": [(6, 0, [cls.featured_category.id])],
            }
        )
        cls.product_out = cls.env["product.template"].create(
            {
                "name": "Produit Hors Selection Test",
                "type": "consu",
                "list_price": 8.0,
                "sale_ok": True,
                "is_published": True,
            }
        )

    def test_search_get_detail_featured_restricts_domain(self):
        detail = self.env["product.template"]._search_get_detail(
            self.website,
            "name asc",
            _website_sale_search_options(
                self.env,
                marketone_featured_only=True,
                marketone_featured_category_id=self.featured_category.id,
            ),
        )
        flat = str(detail.get("base_domain") or [])
        self.assertIn("public_categ_ids", flat)
        self.assertIn(str(self.featured_category.id), flat)

    def test_search_get_detail_featured_invalid_empty(self):
        detail = self.env["product.template"]._search_get_detail(
            self.website,
            "name asc",
            _website_sale_search_options(
                self.env,
                marketone_featured_only=True,
                marketone_featured_category_invalid=True,
            ),
        )
        self.assertIn([("id", "=", 0)], detail.get("base_domain") or [])


@tagged("post_install", "-at_install", "dorevia_marketone_lot6_1_featured")
class TestMarketoneLot61FeaturedHttp(HttpCase):
    """HTTP — porte featured, alias 301, non-régression shop / tunnel."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.website = cls.env["website"].search([], limit=1)
        cls.featured_category = cls.env["product.public.category"].sudo().create(
            {
                "name": "Incontournables Recette",
                "website_id": cls.website.id,
            }
        )
        cls.env["ir.config_parameter"].sudo().set_param(
            MARKETONE_FEATURED_PARAM,
            str(cls.featured_category.id),
        )
        ProductTemplate = cls.env["product.template"]
        cls.product_in = ProductTemplate.create(
            {
                "name": "Recette Incontournable HTTP",
                "type": "consu",
                "list_price": 11.0,
                "sale_ok": True,
                "is_published": True,
                "public_categ_ids": [(6, 0, [cls.featured_category.id])],
            }
        )
        cls.product_out = ProductTemplate.search(
            [
                ("sale_ok", "=", True),
                ("is_published", "=", True),
                ("id", "!=", cls.product_in.id),
            ],
            limit=1,
        )
        if not cls.product_out:
            cls.product_out = ProductTemplate.create(
                {
                    "name": "Recette Hors Incontournables HTTP",
                    "type": "consu",
                    "list_price": 7.0,
                    "sale_ok": True,
                    "is_published": True,
                }
            )

    def test_featured_shop_200(self):
        response = self.url_open("/shop?marketone_mode=featured")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"marketone-shop", response.content)

    def test_featured_filters_products(self):
        response = self.url_open("/shop?marketone_mode=featured")
        text = response.text
        self.assertIn(self.product_in.name, text)
        if self.product_out.name not in text:
            return
        self.assertNotIn(
            self.product_out.name,
            text,
            "Un produit hors catégorie Incontournables ne doit pas apparaître.",
        )

    def test_featured_presentation_visible(self):
        response = self.url_open("/shop?marketone_mode=featured")
        text = response.text
        self.assertIn("Incontournables", text)
        self.assertIn("marketone-shop-featured-intro", text)
        self.assertIn("Tous les produits", text)
        self.assertIn('href="/shop"', text)

    def test_incontournables_301(self):
        response = self.url_open(
            "/incontournables",
            allow_redirects=False,
        )
        self.assertEqual(response.status_code, 301)
        location = response.headers.get("Location", "")
        parsed = urlparse(location)
        self.assertEqual(parsed.path, "/shop")
        qs = parse_qs(parsed.query)
        self.assertEqual(qs.get("marketone_mode"), ["featured"])

    def test_unknown_param_ignored(self):
        response = self.url_open("/shop?marketone_mode=unknown")
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b"marketone-shop-featured-intro", response.content)

    def test_shop_without_mode_unchanged(self):
        response = self.url_open("/shop")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"marketone-shop", response.content)
        self.assertNotIn(b"marketone-shop-featured-intro", response.content)

    def test_featured_no_gates_on_home(self):
        response = self.url_open("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"marketone-root", response.content)
        self.assertNotIn(b"marketone-shop-featured-intro", response.content)
        self.assertNotRegex(response.text, r"marketone_mode\s*=\s*featured")

    def _create_cart_order(self, quantity=1.0):
        partner = self.env.ref("base.public_partner")
        order = self.env["sale.order"].create(
            {
                "partner_id": partner.id,
                "website_id": self.website.id,
            }
        )
        order._cart_add(
            product_id=self.product_in.product_variant_id.id,
            quantity=quantity,
        )
        return order

    def _bind_public_cart(self, order):
        session = self.authenticate(None, None)
        session["sale_order_id"] = order.id
        from odoo.http import root

        root.session_store.save(session)

    def test_cart_checkout_regression(self):
        cart = self.url_open("/shop/cart")
        self.assertEqual(cart.status_code, 200)
        self.assertIn(b"marketone-cart", cart.content)
        order = self._create_cart_order()
        self._bind_public_cart(order)
        checkout = self.url_open("/shop/checkout", allow_redirects=True)
        self.assertEqual(checkout.status_code, 200)
        self.assertIn(b"marketone-checkout", checkout.content)

    def test_shop_plain_has_no_featured_intro(self):
        response = self.url_open("/shop")
        text = response.text
        self.assertIsNone(
            re.search(r"marketone_mode\s*=\s*featured", text),
            "Pas de lien porte featured sur /shop standard.",
        )
