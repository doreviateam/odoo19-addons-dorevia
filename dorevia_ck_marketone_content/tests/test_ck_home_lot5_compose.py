# -*- coding: utf-8 -*-
"""Tests HTTP Lot 5 — éditorial bas de page · non-régression lots 2–4."""

import re

from odoo.tests import tagged
from odoo.tests.common import HttpCase

from odoo.addons.dorevia_ck_marketone_content.home_dual_engage import (
    bootstrap_home_dual_engage,
)
from odoo.addons.dorevia_ck_marketone_content.home_editorial import (
    EDITORIAL_LINK_A_PROPOS,
    EDITORIAL_LINK_PRODUCER,
    EDITORIAL_LINK_RECIPES,
    EDITORIAL_LINK_DEMARCHE_LABEL,
    EDITORIAL_LINK_PRODUCER_LABEL,
    EDITORIAL_LINK_RECIPES_TEXT,
    EDITORIAL_TITLE,
    bootstrap_home_editorial,
)
from odoo.addons.dorevia_ck_marketone_content.hooks import (
    bootstrap_home_discovery_pack,
    bootstrap_home_featured_products,
)


@tagged('post_install', '-at_install', 'dorevia_ck_marketone_home_lot5')
class TestCkHomeLot5Compose(HttpCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        bootstrap_home_featured_products(cls.env)
        bootstrap_home_discovery_pack(cls.env)
        bootstrap_home_dual_engage(cls.env)
        bootstrap_home_editorial(cls.env)

    def _editorial_chunk(self, html):
        start = html.find('ck-home-editorial')
        self.assertGreater(start, 0)
        return html[start:start + 8000]

    def test_home_editorial_block_present(self):
        html = self.url_open('/').text
        chunk = self._editorial_chunk(html)
        self.assertIn(EDITORIAL_TITLE, chunk)
        self.assertIn('agro-produits transformés', chunk)
        self.assertIn(EDITORIAL_LINK_DEMARCHE_LABEL, chunk)

    def test_home_editorial_links_http_200(self):
        for path in (
            EDITORIAL_LINK_A_PROPOS,
            EDITORIAL_LINK_PRODUCER,
            EDITORIAL_LINK_RECIPES,
        ):
            self.assertEqual(self.url_open(path).status_code, 200, path)

    def test_home_editorial_order_after_dual(self):
        html = self.url_open('/').text
        self.assertLess(html.find('ck-dual-engage--compact'), html.find('ck-home-editorial'))

    def test_home_editorial_before_footer(self):
        html = self.url_open('/').text
        edito_pos = html.find('ck-home-editorial')
        footer_pos = html.find('<footer')
        self.assertGreater(edito_pos, 0)
        self.assertGreater(footer_pos, edito_pos)

    def test_home_editorial_all_links_present(self):
        html = self.url_open('/').text
        chunk = self._editorial_chunk(html)
        self.assertIn(f'href="{EDITORIAL_LINK_A_PROPOS}"', chunk)
        self.assertIn(f'href="{EDITORIAL_LINK_PRODUCER}"', chunk)
        self.assertIn(f'href="{EDITORIAL_LINK_RECIPES}"', chunk)
        self.assertIn(EDITORIAL_LINK_PRODUCER_LABEL, chunk)
        self.assertIn('Recettes', chunk)
        self.assertIn('savoirs →', chunk)

    def test_home_no_technical_leaks_in_editorial(self):
        html = self.url_open('/').text
        chunk = self._editorial_chunk(html)
        self.assertNotIn('Inspiration réf.', chunk)
        self.assertNotIn('route-hint', chunk)
        self.assertIsNone(re.search(r'\bTODO\b|\bFIXME\b', chunk))

    def test_home_lot2_lot3_lot4_non_regression(self):
        html = self.url_open('/').text
        self.assertIn('ck-featured-products__grid--stable', html)
        self.assertIn('ck-discovery-pack', html)
        self.assertIn('ck-dual-engage--compact', html)
        self.assertNotIn('s_ck_pro_banner', html)
