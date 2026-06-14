# -*- coding: utf-8 -*-
"""Tests Lot 6.3a — porte Promotions (marketone_mode=promo)."""

import re
from urllib.parse import parse_qs, urlparse

from odoo.tests import tagged
from odoo.tests.common import HttpCase, TransactionCase

from odoo.addons.dorevia_ckreyol_marketone.controllers.website_sale import (
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


def _promo_item_vals(pricelist, product, **extra):
    vals = {
        "pricelist_id": pricelist.id,
        "applied_on": "1_product",
        "product_tmpl_id": product.id,
        "compute_price": "percentage",
        "percent_price": 10.0,
    }
    vals.update(extra)
    return vals


@tagged("post_install", "-at_install", "dorevia_marketone_lot6_3a_promo")
class TestMarketoneLot63aPromoModel(TransactionCase):
    """Résolveur pricelist — pas de moteur promo parallèle."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.website = cls.env.ref("website.default_website")
        cls.pricelist_a = cls.env["product.pricelist"].create(
            {"name": "Marketone Promo Test A", "currency_id": cls.env.company.currency_id.id}
        )
        cls.pricelist_b = cls.env["product.pricelist"].create(
            {"name": "Marketone Promo Test B", "currency_id": cls.env.company.currency_id.id}
        )
        cls.product_promo = cls.env["product.template"].create(
            {
                "name": "Produit Promo Test",
                "type": "consu",
                "list_price": 20.0,
                "sale_ok": True,
                "is_published": True,
            }
        )
        cls.product_regular = cls.env["product.template"].create(
            {
                "name": "Produit Standard Test",
                "type": "consu",
                "list_price": 12.0,
                "sale_ok": True,
                "is_published": True,
            }
        )
        cls.env["product.pricelist.item"].create(
            _promo_item_vals(cls.pricelist_a, cls.product_promo)
        )

    def test_get_promo_template_ids_product_level(self):
        ids = self.pricelist_a._marketone_get_promo_template_ids(
            pricelist=self.pricelist_a
        )
        self.assertEqual(ids, {self.product_promo.id})

    def test_get_promo_template_ids_empty(self):
        ids = self.pricelist_b._marketone_get_promo_template_ids(
            pricelist=self.pricelist_b
        )
        self.assertEqual(ids, set())

    def test_get_promo_template_ids_global(self):
        self.env["product.pricelist.item"].create(
            {
                "pricelist_id": self.pricelist_b.id,
                "applied_on": "3_global",
                "compute_price": "percentage",
                "percent_price": 5.0,
            }
        )
        ids = self.pricelist_b._marketone_get_promo_template_ids(
            pricelist=self.pricelist_b
        )
        self.assertIsNone(ids)

    def test_non_reducer_item_ignored(self):
        self.env["product.pricelist.item"].create(
            _promo_item_vals(
                self.pricelist_b,
                self.product_regular,
                percent_price=0.0,
            )
        )
        ids = self.pricelist_b._marketone_get_promo_template_ids(
            pricelist=self.pricelist_b
        )
        self.assertEqual(ids, set())

    def test_multi_pricelist_visitor_isolation(self):
        self.env["product.pricelist.item"].create(
            _promo_item_vals(self.pricelist_b, self.product_regular, percent_price=12.0)
        )
        ids_a = self.pricelist_a._marketone_get_promo_template_ids(
            pricelist=self.pricelist_a
        )
        ids_b = self.pricelist_b._marketone_get_promo_template_ids(
            pricelist=self.pricelist_b
        )
        self.assertEqual(ids_a, {self.product_promo.id})
        self.assertEqual(ids_b, {self.product_regular.id})

    def test_search_get_detail_promo_restricts_domain(self):
        detail = self.env["product.template"]._search_get_detail(
            self.website,
            "name asc",
            _website_sale_search_options(
                self.env,
                marketone_promo_only=True,
                marketone_promo_template_ids=[self.product_promo.id],
            ),
        )
        flat = str(detail.get("base_domain") or [])
        self.assertIn(str(self.product_promo.id), flat)

    def test_search_get_detail_promo_empty(self):
        detail = self.env["product.template"]._search_get_detail(
            self.website,
            "name asc",
            _website_sale_search_options(
                self.env,
                marketone_promo_only=True,
                marketone_promo_empty=True,
            ),
        )
        self.assertIn([("id", "=", 0)], detail.get("base_domain") or [])

    def test_search_get_detail_promo_global_no_extra_domain(self):
        detail = self.env["product.template"]._search_get_detail(
            self.website,
            "name asc",
            _website_sale_search_options(
                self.env,
                marketone_promo_only=True,
                marketone_promo_global=True,
            ),
        )
        base = detail.get("base_domain") or []
        self.assertFalse(
            any("marketone_promo" in str(part) for part in base),
            "Promo globale : pas de domaine produit supplémentaire.",
        )


@tagged("post_install", "-at_install", "dorevia_marketone_lot6_3a_promo")
class TestMarketoneLot63aPromoHttp(HttpCase):
    """HTTP — porte promo, alias 301, chip header, non-régression."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.website = cls.env["website"].search([], limit=1)
        public_partner = cls.env.ref("base.public_partner")
        cls.pricelist = public_partner.property_product_pricelist
        if not cls.pricelist:
            cls.pricelist = cls.env["product.pricelist"].search([], limit=1)
            public_partner.property_product_pricelist = cls.pricelist
        ProductTemplate = cls.env["product.template"]
        cls.product_promo = ProductTemplate.create(
            {
                "name": "Recette Promo HTTP Marketone",
                "type": "consu",
                "list_price": 18.0,
                "sale_ok": True,
                "is_published": True,
            }
        )
        cls.product_out = ProductTemplate.search(
            [
                ("sale_ok", "=", True),
                ("is_published", "=", True),
                ("id", "!=", cls.product_promo.id),
            ],
            limit=1,
        )
        if not cls.product_out:
            cls.product_out = ProductTemplate.create(
                {
                    "name": "Recette Hors Promo HTTP",
                    "type": "consu",
                    "list_price": 9.0,
                    "sale_ok": True,
                    "is_published": True,
                }
            )
        cls.env["product.pricelist.item"].create(
            _promo_item_vals(cls.pricelist, cls.product_promo, percent_price=15.0)
        )

    def setUp(self):
        super().setUp()
        Item = self.env["product.pricelist.item"]
        for pl in self.env["product.pricelist"].search([]):
            if Item.search_count(
                [
                    ("pricelist_id", "=", pl.id),
                    ("product_tmpl_id", "=", self.product_promo.id),
                ]
            ):
                continue
            Item.create(_promo_item_vals(pl, self.product_promo, percent_price=15.0))

    def test_promo_shop_200(self):
        response = self.url_open("/shop?marketone_mode=promo")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"marketone-shop", response.content)

    def test_promo_filters_products(self):
        response = self.url_open("/shop?marketone_mode=promo")
        text = response.text
        self.assertIn(self.product_promo.name, text)
        if self.product_out.name not in text:
            return
        self.assertNotIn(
            self.product_out.name,
            text,
            "Un produit sans item promo actif ne doit pas apparaître.",
        )

    def test_promo_presentation_visible(self):
        response = self.url_open("/shop?marketone_mode=promo")
        text = response.text
        self.assertIn("Promotions", text)
        self.assertIn("marketone-shop-promo-intro", text)
        self.assertIn("Tous les produits", text)

    def test_promotions_301(self):
        response = self.url_open("/promotions", allow_redirects=False)
        self.assertEqual(response.status_code, 301)
        location = response.headers.get("Location", "")
        parsed = urlparse(location)
        self.assertEqual(parsed.path, "/shop")
        qs = parse_qs(parsed.query)
        self.assertEqual(qs.get("marketone_mode"), [MARKETONE_MODE_PROMO])

    def test_header_promotions_chip(self):
        response = self.url_open("/shop")
        header = extract_site_header(response.text)
        self.assertIn('href="/promotions"', header)
        self.assertIn("Promotions", header)

    def test_no_kits_outside_header(self):
        response = self.url_open("/shop?marketone_mode=promo")
        body = html_without_site_header(response.text)
        self.assertIsNone(re.search(r"""href=['"]/kits""", body))

    def test_shop_gate_policy_with_header_promo(self):
        response = self.url_open("/shop")
        assert_catalog_gate_policy_lot6_front(self, response.text)
        body = html_without_site_header(response.text)
        self.assertIsNone(re.search(r"""href=['"]/promotions""", body))

    def test_featured_origin_unchanged(self):
        featured = self.url_open("/shop?marketone_mode=featured")
        self.assertEqual(featured.status_code, 200)
        origin = self.url_open("/shop?marketone_mode=origin")
        self.assertEqual(origin.status_code, 200)

    def test_unknown_mode_ignored(self):
        response = self.url_open("/shop?marketone_mode=unknown")
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b"marketone-shop-promo-intro", response.content)

    def _create_cart_order(self, quantity=1.0):
        partner = self.env.ref("base.public_partner")
        order = self.env["sale.order"].create(
            {
                "partner_id": partner.id,
                "website_id": self.website.id,
            }
        )
        order._cart_add(
            product_id=self.product_promo.product_variant_id.id,
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
