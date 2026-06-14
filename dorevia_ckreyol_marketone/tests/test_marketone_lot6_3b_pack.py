# -*- coding: utf-8 -*-
"""Tests Lot 6.3b — porte Kits & Coffrets (marketone_mode=pack)."""

import re
from urllib.parse import parse_qs, urlparse

from odoo.tests import tagged
from odoo.tests.common import HttpCase, TransactionCase

from odoo.addons.dorevia_ckreyol_marketone.controllers.website_sale import (
    MARKETONE_MODE_PACK,
    MARKETONE_MODE_PROMO,
)
from odoo.addons.dorevia_ckreyol_marketone.tests.marketone_gate_helpers import (
    assert_catalog_gate_policy_lot6_front,
    extract_site_header,
    html_without_site_header,
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


def _create_pack_product(env, name, *, component=None):
    """Produit pack publié avec un composant minimal."""
    if component is None:
        component = env["product.product"].create(
            {
                "name": f"Composant {name}",
                "type": "consu",
                "list_price": 6.0,
            }
        )
    template = env["product.template"].create(
        {
            "name": name,
            "type": "consu",
            "list_price": 29.0,
            "sale_ok": True,
            "is_published": True,
            "pack_ok": True,
            "pack_type": "non_detailed",
            "pack_component_price": "ignored",
        }
    )
    env["product.pack.line"].create(
        {
            "parent_product_id": template.product_variant_id.id,
            "product_id": component.id,
            "quantity": 1.0,
        }
    )
    return template


@tagged("post_install", "-at_install", "dorevia_marketone_lot6_3b_pack")
class TestMarketoneLot63bPackModel(TransactionCase):
    """Filtre pack_ok — pas de moteur pack parallèle."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.website = cls.env.ref("website.default_website")
        cls.product_pack = _create_pack_product(cls.env, "Pack Test Marketone")
        cls.product_regular = cls.env["product.template"].create(
            {
                "name": "Produit Unit Test Marketone",
                "type": "consu",
                "list_price": 11.0,
                "sale_ok": True,
                "is_published": True,
            }
        )

    def test_search_get_detail_pack_only(self):
        detail = self.env["product.template"]._search_get_detail(
            self.website,
            "name asc",
            _website_sale_search_options(
                self.env,
                marketone_pack_only=True,
            ),
        )
        flat = str(detail.get("base_domain") or [])
        self.assertIn("pack_ok", flat)
        self.assertIn("True", flat)

    def test_search_get_detail_pack_includes_pack_ok(self):
        detail = self.env["product.template"]._search_get_detail(
            self.website,
            "name asc",
            _website_sale_search_options(self.env, marketone_pack_only=True),
        )
        self.assertIn([("pack_ok", "=", True)], detail.get("base_domain") or [])


@tagged("post_install", "-at_install", "dorevia_marketone_lot6_3b_pack")
class TestMarketoneLot63bPackHttp(HttpCase):
    """HTTP — porte pack, alias 301, chip header, non-régression."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.website = cls.env["website"].search([], limit=1)
        cls.product_pack = _create_pack_product(cls.env, "Recette Pack HTTP Marketone")
        cls.product_out = cls.env["product.template"].search(
            [
                ("sale_ok", "=", True),
                ("is_published", "=", True),
                ("pack_ok", "=", False),
                ("id", "!=", cls.product_pack.id),
            ],
            limit=1,
        )
        if not cls.product_out:
            cls.product_out = cls.env["product.template"].create(
                {
                    "name": "Recette Hors Pack HTTP",
                    "type": "consu",
                    "list_price": 8.0,
                    "sale_ok": True,
                    "is_published": True,
                }
            )

    def test_pack_shop_200(self):
        response = self.url_open("/shop?marketone_mode=pack")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"marketone-shop", response.content)

    def test_pack_filters_products(self):
        response = self.url_open("/shop?marketone_mode=pack")
        text = response.text
        self.assertIn(self.product_pack.name, text)
        if self.product_out.name not in text:
            return
        self.assertNotIn(
            self.product_out.name,
            text,
            "Un produit sans pack_ok ne doit pas apparaître sur la porte pack.",
        )

    def test_pack_presentation_visible(self):
        response = self.url_open("/shop?marketone_mode=pack")
        text = response.text
        self.assertIn("Kits & Coffrets", text)
        self.assertIn("marketone-shop-pack-intro", text)
        self.assertIn("Tous les produits", text)

    def test_kits_301(self):
        response = self.url_open("/kits", allow_redirects=False)
        self.assertEqual(response.status_code, 301)
        location = response.headers.get("Location", "")
        parsed = urlparse(location)
        self.assertEqual(parsed.path, "/shop")
        qs = parse_qs(parsed.query)
        self.assertEqual(qs.get("marketone_mode"), [MARKETONE_MODE_PACK])

    def test_header_kits_chip(self):
        response = self.url_open("/shop")
        header = extract_site_header(response.text)
        self.assertIn('href="/kits"', header)
        self.assertIn("Kits & Coffrets", header)

    def test_header_promotions_still_present(self):
        response = self.url_open("/shop")
        header = extract_site_header(response.text)
        self.assertIn('href="/promotions"', header)
        self.assertIn("Promotions", header)

    def test_shop_gate_policy_with_header_gates(self):
        response = self.url_open("/shop")
        assert_catalog_gate_policy_lot6_front(self, response.text)
        body = html_without_site_header(response.text)
        self.assertIsNone(re.search(r"""href=['"]/kits""", body))
        self.assertIsNone(re.search(r"""href=['"]/promotions""", body))

    def test_pack_priority_over_promo(self):
        response = self.url_open(
            "/shop?marketone_mode=pack&marketone_mode=promo"
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"marketone-shop-pack-intro", response.content)
        self.assertNotIn(b"marketone-shop-promo-intro", response.content)

    def test_featured_origin_promo_unchanged(self):
        featured = self.url_open("/shop?marketone_mode=featured")
        self.assertEqual(featured.status_code, 200)
        origin = self.url_open("/shop?marketone_mode=origin")
        self.assertEqual(origin.status_code, 200)
        promo = self.url_open("/shop?marketone_mode=promo")
        self.assertEqual(promo.status_code, 200)
        self.assertIn(b"marketone-shop-promo-intro", promo.content)

    def test_unknown_mode_ignored(self):
        response = self.url_open("/shop?marketone_mode=unknown")
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b"marketone-shop-pack-intro", response.content)

    def _create_cart_order(self, quantity=1.0):
        partner = self.env.ref("base.public_partner")
        order = self.env["sale.order"].create(
            {
                "partner_id": partner.id,
                "website_id": self.website.id,
            }
        )
        order._cart_add(
            product_id=self.product_pack.product_variant_id.id,
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
        order = self._create_cart_order()
        self._bind_public_cart(order)
        checkout = self.url_open("/shop/checkout", allow_redirects=True)
        self.assertEqual(checkout.status_code, 200)
