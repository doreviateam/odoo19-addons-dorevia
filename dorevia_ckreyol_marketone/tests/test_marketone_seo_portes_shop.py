# -*- coding: utf-8 -*-
"""Tests SEO portes /shop — canonical et noindex (MOA D1–D6)."""

import html
import re
from urllib.parse import parse_qs, urlparse

from odoo.tests import tagged
from odoo.tests.common import HttpCase


def _head_canonical_href(html):
    match = re.search(
        r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']+)["\']',
        html,
        re.I,
    )
    if not match:
        match = re.search(
            r'<link[^>]+href=["\']([^"\']+)["\'][^>]+rel=["\']canonical["\']',
            html,
            re.I,
        )
    return match.group(1) if match else None


def _head_robots_content(html):
    match = re.search(
        r'<meta[^>]+name=["\']robots["\'][^>]+content=["\']([^"\']+)["\']',
        html,
        re.I,
    )
    return match.group(1) if match else None


def _canonical_query(canonical_href):
    parsed = urlparse(html.unescape(canonical_href or ""))
    return parse_qs(parsed.query)


@tagged("post_install", "-at_install", "dorevia_marketone_seo_portes_shop")
class TestMarketoneSeoPortesShop(HttpCase):
    """Head tags — canonical whitelist et noindex porte + bruit."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.website = cls.env["website"].search([], limit=1)
        cls.attr_origin = cls.env.ref(
            "dorevia_ckreyol_marketone.marketone_product_attribute_origin"
        )
        cls.val_g = cls.env["product.attribute.value"].create(
            {"name": "SEO Origine G", "attribute_id": cls.attr_origin.id}
        )
        cls.val_m = cls.env["product.attribute.value"].create(
            {"name": "SEO Origine M", "attribute_id": cls.attr_origin.id}
        )
        cls.profile_g = cls.env["marketone.shop.origin"].create(
            {
                "attribute_value_id": cls.val_g.id,
                "slug": "guadeloupe-seo",
                "name_visitor": "Guadeloupe SEO",
                "website_id": False,
                "website_published": True,
            }
        )
        cls.profile_m = cls.env["marketone.shop.origin"].create(
            {
                "attribute_value_id": cls.val_m.id,
                "slug": "martinique-seo",
                "name_visitor": "Martinique SEO",
                "website_id": False,
                "website_published": True,
            }
        )
        cls.featured_category = cls.env["product.public.category"].sudo().create(
            {"name": "Incontournables SEO", "website_id": cls.website.id}
        )
        cls.env["ir.config_parameter"].sudo().set_param(
            "dorevia_ckreyol_marketone.featured_public_category_id",
            str(cls.featured_category.id),
        )

    def test_bare_shop_canonical_self(self):
        response = self.url_open("/shop")
        self.assertEqual(response.status_code, 200)
        href = _head_canonical_href(response.text)
        self.assertTrue(href)
        self.assertIn("/shop", href)
        qs = _canonical_query(href)
        self.assertNotIn("marketone_mode", qs)

    def test_porte_t2_canonical_self(self):
        for mode in ("featured", "promo", "pack", "origin"):
            response = self.url_open(f"/shop?marketone_mode={mode}")
            self.assertEqual(response.status_code, 200)
            qs = _canonical_query(_head_canonical_href(response.text))
            self.assertEqual(qs.get("marketone_mode"), [mode])

    def test_porte_t3_origin_canonical_self(self):
        response = self.url_open(
            "/shop?marketone_mode=origin&marketone_origin=guadeloupe-seo"
        )
        self.assertEqual(response.status_code, 200)
        href = _head_canonical_href(response.text)
        qs = _canonical_query(href)
        self.assertEqual(qs.get("marketone_mode"), ["origin"], href)
        self.assertEqual(qs.get("marketone_origin"), ["guadeloupe-seo"], href)

    def test_porte_t4_filter_noindex_canonical_porte(self):
        response = self.url_open(
            "/shop?marketone_mode=featured&order=website_sequence+asc"
        )
        self.assertEqual(response.status_code, 200)
        robots = _head_robots_content(response.text)
        self.assertIsNotNone(robots)
        self.assertIn("noindex", robots.lower())
        self.assertIn("follow", robots.lower())
        qs = _canonical_query(_head_canonical_href(response.text))
        self.assertEqual(qs.get("marketone_mode"), ["featured"])
        self.assertNotIn("order", qs)

    def test_porte_t2_alone_indexable(self):
        response = self.url_open("/shop?marketone_mode=featured")
        self.assertEqual(response.status_code, 200)
        robots = _head_robots_content(response.text)
        self.assertIsNone(robots)

    def test_multi_origin_noindex_canonical_porte_seule(self):
        response = self.url_open(
            "/shop?marketone_mode=origin"
            "&marketone_origin=guadeloupe-seo"
            "&marketone_origin=martinique-seo"
        )
        self.assertEqual(response.status_code, 200)
        robots = _head_robots_content(response.text)
        self.assertIsNotNone(robots)
        self.assertIn("noindex", robots.lower())
        qs = _canonical_query(_head_canonical_href(response.text))
        self.assertEqual(qs.get("marketone_mode"), ["origin"])
        self.assertNotIn("marketone_origin", qs)

    def test_alias_301_non_regression(self):
        response = self.url_open("/kits", allow_redirects=False)
        self.assertEqual(response.status_code, 301)
        location = response.headers.get("Location", "")
        qs = parse_qs(urlparse(location).query)
        self.assertEqual(qs.get("marketone_mode"), ["pack"])

    def test_homepage_200_layout_seo_hooks(self):
        """Non-régression : layout global (accueil) sans 500 QWeb."""
        response = self.url_open("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"marketone-root", response.content)
