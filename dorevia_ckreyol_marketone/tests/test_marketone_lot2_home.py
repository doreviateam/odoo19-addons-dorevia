# -*- coding: utf-8 -*-
"""Tests Lot 2 — identite front home C-Kreyol."""

import re

from odoo.tests import tagged
from odoo.tests.common import HttpCase


@tagged("post_install", "-at_install", "dorevia_marketone_lot2")
class TestMarketoneLot2Home(HttpCase):
    """Home identifiable Marketone (scope marketone-root Lot 2)."""

    def test_home_http_200(self):
        response = self.url_open("/")
        self.assertEqual(response.status_code, 200)

    def test_home_contains_marketone_root(self):
        response = self.url_open("/")
        self.assertIn(b"marketone-root", response.content)
        self.assertIn(b"marketone-home-intro", response.content)

    def test_home_contains_brand_marker(self):
        response = self.url_open("/")
        self.assertIn(b"C-Kreyol", response.content)
        self.assertIn(b"\xc3\x89picerie fine cr\xc3\xa9ole", response.content)

    def test_home_cta_shop_link(self):
        response = self.url_open("/")
        self.assertRegex(
            response.text,
            r'href=["\']/shop["\']',
            "CTA home doit pointer vers /shop.",
        )
        self.assertIn(b"D\xc3\xa9couvrir la boutique", response.content)

    def test_home_no_marketone_shop_scope(self):
        response = self.url_open("/")
        self.assertNotIn(
            b"marketone-shop",
            response.content,
            "La home ne doit pas porter marketone-shop (Lot 3).",
        )

    def test_home_no_catalog_gates_links(self):
        response = self.url_open("/")
        from odoo.addons.dorevia_ckreyol_marketone.tests.marketone_gate_helpers import (
            assert_catalog_gate_policy_lot6_front,
        )

        assert_catalog_gate_policy_lot6_front(self, response.text)
