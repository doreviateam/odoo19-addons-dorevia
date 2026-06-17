# -*- coding: utf-8 -*-
"""Tests HTTP Section 4 — Acheter par univers · compose home."""

import re

from odoo.tests import tagged
from odoo.tests.common import HttpCase

from odoo.addons.dorevia_ck_marketone_content.home_discovery_pack import (
    DISCOVERY_PACK_SECTION_MARKER,
)
from odoo.addons.dorevia_ck_marketone_content.home_featured import (
    FEATURED_SECTION_MARKER,
)
from odoo.addons.dorevia_ck_marketone_content.home_univers import (
    UNIVERS_INTRO,
    UNIVERS_SECTION_MARKER,
    UNIVERS_TITLE,
)
from odoo.addons.dorevia_ck_marketone_content.hooks import (
    bootstrap_all_marketone_content,
)


@tagged('post_install', '-at_install', 'dorevia_ck_marketone_home_section4')
class TestCkHomeSection4UniversCompose(HttpCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        bootstrap_all_marketone_content(cls.env)

    def _univers_chunk(self, html):
        start = html.find(UNIVERS_SECTION_MARKER)
        self.assertGreater(start, 0)
        return html[start:start + 15000]

    def test_home_univers_block_present(self):
        html = self.url_open('/').text
        chunk = self._univers_chunk(html)
        self.assertIn(UNIVERS_TITLE, chunk)
        self.assertIn(UNIVERS_INTRO, chunk)
        self.assertEqual(chunk.count('ck-univers-card--'), 3)
        self.assertIn("Voir l'épicerie", chunk)
        self.assertIn('Découvrir les soins', chunk)
        self.assertIn("Explorer l'artisanat", chunk)

    def test_home_univers_order_after_featured_before_packs(self):
        html = self.url_open('/').text
        featured_pos = html.find(FEATURED_SECTION_MARKER)
        univers_pos = html.find(UNIVERS_SECTION_MARKER)
        pack_pos = html.find(DISCOVERY_PACK_SECTION_MARKER)
        self.assertGreater(featured_pos, 0)
        self.assertGreater(univers_pos, featured_pos)
        self.assertGreater(pack_pos, univers_pos)

    def test_home_univers_no_carousel_no_technical_urls(self):
        html = self.url_open('/').text
        chunk = self._univers_chunk(html)
        self.assertNotIn('data-bs-ride="carousel"', chunk)
        self.assertNotIn('route-hint', chunk)
        self.assertNotIn('Packs & découvertes', chunk)
        visible_urls = re.findall(r'>([^<]*/shop/category/[^<]*)<', chunk)
        self.assertFalse(visible_urls)

    def test_home_univers_responsive_grid_markup(self):
        html = self.url_open('/').text
        chunk = self._univers_chunk(html)
        self.assertIn('ck-univers-cards__grid', chunk)
        self.assertIn('ck-univers-card__overlay', chunk)
        self.assertEqual(chunk.count('ck-univers-card__img'), 3)
        self.assertEqual(chunk.count('ck-univers-card__media o_editable'), 3)
        self.assertIn('ck_univers_epicerie.jpg', chunk)
        self.assertIn('ck_univers_soin.jpg', chunk)
        self.assertIn('ck_univers_artisanat.jpg', chunk)

    def test_home_section3_non_regression(self):
        html = self.url_open('/').text
        self.assertIn('ck-featured-products--maquette', html)
        self.assertIn('Nos coups de cœur', html)
