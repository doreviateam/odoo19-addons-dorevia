# -*- coding: utf-8 -*-
"""Tests HTTP Lot 3 — Coffrets découverte home · non-régression Lot 2."""

import re
from urllib.parse import parse_qs, urlparse

from odoo.tests import tagged
from odoo.tests.common import HttpCase

from odoo.addons.dorevia_ck_marketone_content.home_discovery_pack import (
    DISCOVERY_PACK_CTA_URL,
    DISCOVERY_PACK_SECTION_MARKER,
    DISCOVERY_PACK_TITLE,
)
from odoo.addons.dorevia_ck_marketone_content.catalog_discovery_pack import (
    bootstrap_catalog_discovery_pack_product,
)
from odoo.addons.dorevia_ck_marketone_content.hooks import (
    bootstrap_home_discovery_pack,
    bootstrap_home_featured_products,
)

_KITS_HREF_RE = re.compile(r'href="(?:/[a-z]{2})?/kits"')


@tagged('post_install', '-at_install', 'dorevia_ck_marketone_home_lot3')
class TestCkHomeLot3Compose(HttpCase):
    FR_HEADERS = {'Accept-Language': 'fr-FR,fr;q=0.9'}

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        bootstrap_catalog_discovery_pack_product(cls.env)
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
        self.assertTrue(_KITS_HREF_RE.search(chunk), 'lien /kits attendu dans le bloc coffret')
        self.assertNotIn('website.s_cover_default_image', chunk)
        self.assertNotIn('s_cover_default', chunk)
        self.assertNotIn('ck-discovery-pack__visual--editorial', chunk)
        self.assertNotIn('stretched-link', chunk)
        self.assertIn('ck-discovery-pack__cta', chunk)
        self.assertTrue(
            '/web/image/product.' in chunk or 'ck_discovery_pack.jpg' in chunk,
            'visuel coffret qualifié attendu',
        )

    def test_home_discovery_order_after_univers(self):
        html = self.url_open('/').text
        univers_pos = html.find('ck-univers-cards')
        if univers_pos < 0:
            univers_pos = html.find('s_ck_category_links')
        pack_pos = html.find(DISCOVERY_PACK_SECTION_MARKER)
        dual_pos = html.find('ck-dual-engage')
        self.assertGreater(univers_pos, 0)
        self.assertGreater(pack_pos, univers_pos)
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
        self.assertEqual(len(_KITS_HREF_RE.findall(chunk)), 1)

    def test_kits_route_when_marketone_installed(self):
        """Porte /kits — 301 vers collection pack (content module)."""
        response = self.url_open('/kits', headers=self.FR_HEADERS, allow_redirects=False)
        self.assertEqual(response.status_code, 301)
        location = response.headers.get('Location', '')
        qs = parse_qs(urlparse(location).query)
        self.assertEqual(qs.get('marketone_mode'), ['pack'])
        self.assertIn('/shop', urlparse(location).path)
