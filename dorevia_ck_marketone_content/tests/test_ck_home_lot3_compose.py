# -*- coding: utf-8 -*-
"""Tests HTTP Lot 3 — Coffrets découverte home · non-régression Lot 2."""

import re

from odoo.tests import tagged
from odoo.tests.common import HttpCase

from odoo.addons.dorevia_ck_marketone_content.home_discovery_pack import (
    DISCOVERY_PACK_CTA_URL,
    DISCOVERY_PACK_SECTION_MARKER,
    DISCOVERY_PACK_TITLE,
)
from odoo.addons.dorevia_ck_marketone_content.hooks import (
    bootstrap_home_discovery_pack,
    bootstrap_home_featured_products,
)


@tagged('post_install', '-at_install', 'dorevia_ck_marketone_home_lot3')
class TestCkHomeLot3Compose(HttpCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        bootstrap_home_featured_products(cls.env)
        bootstrap_home_discovery_pack(cls.env)

    def _discovery_chunk(self, html):
        start = html.find(DISCOVERY_PACK_SECTION_MARKER)
        self.assertGreater(start, 0)
        return html[start:start + 12000]

    def test_home_discovery_block_present(self):
        html = self.url_open('/').text
        chunk = self._discovery_chunk(html)
        self.assertIn(DISCOVERY_PACK_TITLE, chunk)
        self.assertIn('Pack', chunk)
        self.assertIn(f'href="{DISCOVERY_PACK_CTA_URL}"', chunk)
        self.assertNotIn('website.s_cover_default_image', chunk)
        self.assertNotIn('s_cover_default', chunk)

    def test_home_discovery_order_after_categories(self):
        html = self.url_open('/').text
        cat_pos = html.find('s_ck_category_links')
        pack_pos = html.find(DISCOVERY_PACK_SECTION_MARKER)
        dual_pos = html.find('ck-dual-engage')
        self.assertGreater(cat_pos, 0)
        self.assertGreater(pack_pos, cat_pos)
        self.assertGreater(dual_pos, pack_pos)

    def test_home_discovery_horizontal_layout(self):
        html = self.url_open('/').text
        chunk = self._discovery_chunk(html)
        self.assertIn('ck-discovery-pack__card', chunk)
        self.assertIn('col-md-5', chunk)
        self.assertIn('col-md-7', chunk)

    def test_home_lot2_featured_non_regression(self):
        html = self.url_open('/').text
        self.assertIn('ck-featured-products__grid--stable', html)
        self.assertNotIn('s_dynamic_snippet_products', html)

    def test_home_discovery_no_carousel(self):
        html = self.url_open('/').text
        chunk = self._discovery_chunk(html)
        self.assertNotIn('data-bs-ride="carousel"', chunk)
        self.assertNotIn('s_dynamic_snippet_products', chunk)

    def test_kits_link_present_in_block(self):
        html = self.url_open('/').text
        chunk = self._discovery_chunk(html)
        self.assertEqual(len(re.findall(rf'href="{re.escape(DISCOVERY_PACK_CTA_URL)}"', chunk)), 1)

    def test_kits_route_when_marketone_installed(self):
        """Porte /kits — 200 ou 301 si module Chantier B actif sur l'instance."""
        marketone = self.env['ir.module.module'].search([
            ('name', '=', 'dorevia_ckreyol_marketone'),
            ('state', '=', 'installed'),
        ], limit=1)
        if not marketone:
            self.skipTest('dorevia_ckreyol_marketone non installé — lien /kits vérifié en HTML uniquement.')
        response = self.url_open(DISCOVERY_PACK_CTA_URL, allow_redirects=False)
        self.assertIn(response.status_code, (200, 301, 302, 303, 307, 308))
