# -*- coding: utf-8 -*-
"""Tests Lot 6.2 — porte Origines (marketone_mode=origin)."""

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


@tagged("post_install", "-at_install", "dorevia_marketone_lot6_2_origin")
class TestMarketoneLot62OriginModel(TransactionCase):
    """Logique ``_search_get_detail`` et profil ``marketone.shop.origin``."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.website = cls.env.ref("website.default_website")
        cls.attr_origin = cls.env.ref(
            "dorevia_ckreyol_marketone.marketone_product_attribute_origin"
        )
        cls.val_g = cls.env["product.attribute.value"].create(
            {"name": "Origine G Test", "attribute_id": cls.attr_origin.id}
        )
        cls.val_m = cls.env["product.attribute.value"].create(
            {"name": "Origine M Test", "attribute_id": cls.attr_origin.id}
        )
        cls.profile_g = cls.env["marketone.shop.origin"].create(
            {
                "attribute_value_id": cls.val_g.id,
                "slug": "guadeloupe-test",
                "name_visitor": "Guadeloupe",
                "website_id": cls.website.id,
                "website_published": True,
            }
        )
        cls.product_g = cls.env["product.template"].create(
            {
                "name": "Produit Origine G",
                "type": "consu",
                "list_price": 10.0,
                "sale_ok": True,
                "is_published": True,
            }
        )
        cls.product_g.write(
            {
                "attribute_line_ids": [
                    (
                        0,
                        0,
                        {
                            "attribute_id": cls.attr_origin.id,
                            "value_ids": [(6, 0, [cls.val_g.id])],
                        },
                    )
                ]
            }
        )
        cls.product_plain = cls.env["product.template"].create(
            {
                "name": "Produit Sans Origine",
                "type": "consu",
                "list_price": 5.0,
                "sale_ok": True,
                "is_published": True,
            }
        )

    def test_search_get_detail_origin_facet_restricts(self):
        detail = self.env["product.template"]._search_get_detail(
            self.website,
            "name asc",
            _website_sale_search_options(
                self.env,
                marketone_origin_mode=True,
                marketone_origin_attribute_value_ids=[self.val_g.id],
            ),
        )
        flat = str(detail.get("base_domain") or [])
        self.assertIn("attribute_line_ids.value_ids", flat)
        self.assertIn(str(self.val_g.id), flat)

    def test_search_get_detail_origin_mode_alone_no_filter(self):
        detail = self.env["product.template"]._search_get_detail(
            self.website,
            "name asc",
            _website_sale_search_options(
                self.env,
                marketone_origin_mode=True,
                marketone_origin_only=True,
            ),
        )
        flat = str(detail.get("base_domain") or [])
        self.assertNotIn("attribute_line_ids.value_ids", flat)

    def test_search_get_detail_origin_invalid_empty(self):
        detail = self.env["product.template"]._search_get_detail(
            self.website,
            "name asc",
            _website_sale_search_options(
                self.env,
                marketone_origin_mode=True,
                marketone_origin_invalid=True,
            ),
        )
        self.assertIn([("id", "=", 0)], detail.get("base_domain") or [])

    def test_resolve_published_slugs(self):
        Origin = self.env["marketone.shop.origin"]
        found = Origin._marketone_resolve_published_slugs(
            ["guadeloupe-test", "inconnu"],
            website=self.website,
        )
        self.assertEqual(found, self.profile_g)

    def test_product_origin_shop_lines(self):
        lines = self.product_g._marketone_get_origin_shop_lines(
            website=self.website
        )
        self.assertEqual(len(lines), 1)
        self.assertEqual(lines[0]["label"], "Guadeloupe")
        self.assertIn("marketone_mode=origin", lines[0]["url"])
        self.assertIn("guadeloupe-test", lines[0]["url"])
        self.assertEqual(
            lines[0]["culture_url"],
            "/culture/guadeloupe-test",
        )


@tagged("post_install", "-at_install", "dorevia_marketone_lot6_2_origin")
class TestMarketoneLot62OriginHttp(HttpCase):
    """HTTP — porte Origines, alias, non-régression."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.website = cls.env["website"].search([], limit=1)
        cls.attr_origin = cls.env.ref(
            "dorevia_ckreyol_marketone.marketone_product_attribute_origin"
        )
        cls.val_g = cls.env["product.attribute.value"].create(
            {"name": "HTTP Origine G", "attribute_id": cls.attr_origin.id}
        )
        cls.profile_g = cls.env["marketone.shop.origin"].create(
            {
                "attribute_value_id": cls.val_g.id,
                "slug": "guadeloupe-http",
                "name_visitor": "Guadeloupe HTTP",
                "website_id": cls.website.id,
                "website_published": True,
            }
        )
        cls.product_g = cls.env["product.template"].create(
            {
                "name": "HTTP Produit Origine G",
                "type": "consu",
                "list_price": 12.0,
                "sale_ok": True,
                "is_published": True,
                "attribute_line_ids": [
                    (
                        0,
                        0,
                        {
                            "attribute_id": cls.attr_origin.id,
                            "value_ids": [(6, 0, [cls.val_g.id])],
                        },
                    )
                ],
            }
        )
        cls.product_plain = cls.env["product.template"].search(
            [
                ("sale_ok", "=", True),
                ("is_published", "=", True),
                ("id", "!=", cls.product_g.id),
            ],
            limit=1,
        )
        if not cls.product_plain:
            cls.product_plain = cls.env["product.template"].create(
                {
                    "name": "HTTP Produit Sans Origine",
                    "type": "consu",
                    "list_price": 6.0,
                    "sale_ok": True,
                    "is_published": True,
                }
            )
        cls.featured_category = cls.env["product.public.category"].sudo().create(
            {"name": "Incontournables HTTP 62", "website_id": cls.website.id}
        )
        cls.env["ir.config_parameter"].sudo().set_param(
            MARKETONE_FEATURED_PARAM,
            str(cls.featured_category.id),
        )

    def test_origin_shop_200(self):
        response = self.url_open("/shop?marketone_mode=origin")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"marketone-shop-origin-intro", response.content)

    def test_origin_mode_alone_full_catalog(self):
        response = self.url_open("/shop?marketone_mode=origin")
        text = response.text
        self.assertIn(self.product_plain.name, text)
        self.assertIn(self.product_g.name, text)

    def test_origin_facet_filters_products(self):
        response = self.url_open(
            "/shop?marketone_mode=origin&marketone_origin=guadeloupe-http"
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.product_g.name, response.text)
        self.assertNotIn(self.product_plain.name, response.text)

    def test_origines_301(self):
        response = self.url_open("/origines", allow_redirects=False)
        self.assertEqual(response.status_code, 301)
        parsed = urlparse(response.headers.get("Location", ""))
        self.assertEqual(parsed.path, "/shop")
        qs = parse_qs(parsed.query)
        self.assertEqual(qs.get("marketone_mode"), ["origin"])

    def test_invalid_origin_redirect_bare_shop(self):
        response = self.url_open(
            "/shop?marketone_mode=origin&marketone_origin=slug-inconnu",
            allow_redirects=False,
        )
        self.assertIn(response.status_code, (301, 302))
        location = response.headers.get("Location", "")
        parsed = urlparse(location)
        self.assertEqual(parsed.path, "/shop")
        self.assertFalse(parse_qs(parsed.query).get("marketone_mode"))

    def test_unknown_mode_ignored(self):
        response = self.url_open("/shop?marketone_mode=unknown")
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b"marketone-shop-origin-intro", response.content)

    def test_ckr_origin_param_ignored(self):
        response = self.url_open(
            "/shop?marketone_mode=origin&ckr_origin=guadeloupe-http"
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"marketone-shop-origin-intro", response.content)
        self.assertIn(self.product_plain.name, response.text)

    def test_featured_unchanged_with_origin_available(self):
        response = self.url_open("/shop?marketone_mode=featured")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"marketone-shop-featured-intro", response.content)
        self.assertNotIn(b"marketone-shop-origin-intro", response.content)

    def test_mode_priority_featured_over_origin(self):
        response = self.url_open(
            "/shop?marketone_mode=featured&marketone_mode=origin"
        )
        self.assertIn(b"marketone-shop-featured-intro", response.content)
        self.assertNotIn(b"marketone-shop-origin-intro", response.content)

    def test_cart_checkout_regression(self):
        partner = self.env.ref("base.public_partner")
        order = self.env["sale.order"].create(
            {"partner_id": partner.id, "website_id": self.website.id}
        )
        order._cart_add(
            product_id=self.product_g.product_variant_id.id,
            quantity=1,
        )
        session = self.authenticate(None, None)
        session["sale_order_id"] = order.id
        from odoo.http import root

        root.session_store.save(session)
        cart = self.url_open("/shop/cart")
        self.assertEqual(cart.status_code, 200)
        self.assertIn(b"marketone-cart", cart.content)
        checkout = self.url_open("/shop/checkout", allow_redirects=True)
        self.assertEqual(checkout.status_code, 200)
        self.assertIn(b"marketone-checkout", checkout.content)

    def test_product_page_origin_link(self):
        url = self.product_g.website_url
        response = self.url_open(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"marketone-product-origins", response.content)
        self.assertIn(b"guadeloupe-http", response.content)
