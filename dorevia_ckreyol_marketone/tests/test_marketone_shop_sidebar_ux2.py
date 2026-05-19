# -*- coding: utf-8 -*-
"""Tests UX-2 — présentation sidebar /shop."""

from odoo.tests import tagged
from odoo.tests.common import HttpCase


@tagged("post_install", "-at_install", "dorevia_marketone_shop_sidebar_ux2")
class TestMarketoneShopSidebarUx2(HttpCase):
    """Smoke HTML — classes UX-2 et facettes ouvertes."""

    def test_shop_sidebar_rail_class_present(self):
        response = self.url_open("/shop")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"marketone-sidebar-rail", response.content)
        self.assertIn(b"marketone-shop-collections-accordion", response.content)
        self.assertIn(b"marketone-shop-categories-accordion", response.content)

    def test_shop_attributes_accordion_expanded_on_desktop(self):
        response = self.url_open("/shop")
        self.assertEqual(response.status_code, 200)
        html = response.text
        grid = html.find('id="products_grid_before"')
        self.assertGreater(grid, -1)
        section = html[grid : grid + 12000]
        self.assertIn("accordion-collapse collapse show", section)
