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
    UNIVERS_CARD_SNIPPET,
    UNIVERS_EDITABLE_MEDIA_MARKER,
    UNIVERS_INTRO,
    UNIVERS_SECTION_MARKER,
    UNIVERS_TITLE,
)
from odoo.addons.dorevia_ck_marketone_content.hooks import (
    bootstrap_all_marketone_content,
)


@tagged('post_install', '-at_install', 'dorevia_ck_marketone_home_section4')
class TestCkHomeSection4UniversCompose(HttpCase):
    FR_HEADERS = {'Accept-Language': 'fr-FR,fr;q=0.9'}

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        bootstrap_all_marketone_content(cls.env)

    def _open_fr_home(self):
        return self.url_open('/', headers=self.FR_HEADERS)

    def _univers_chunk(self, html):
        start = html.find(UNIVERS_SECTION_MARKER)
        self.assertGreater(start, 0)
        return html[start:start + 15000]

    def test_home_univers_block_present(self):
        html = self._open_fr_home().text
        chunk = self._univers_chunk(html)
        self.assertIn(UNIVERS_TITLE, chunk)
        self.assertIn(UNIVERS_INTRO, chunk)
        self.assertEqual(chunk.count('ck-univers-card--'), 4)
        self.assertIn("Voir l'épicerie", chunk)
        self.assertIn('Voir les boissons', chunk)
        self.assertIn('Découvrir les soins', chunk)
        self.assertIn("Explorer l'artisanat", chunk)
        self.assertIn('ck-univers-card--boissons', chunk)

    def test_home_univers_order_after_featured_before_packs(self):
        html = self._open_fr_home().text
        featured_pos = html.find(FEATURED_SECTION_MARKER)
        univers_pos = html.find(UNIVERS_SECTION_MARKER)
        pack_pos = html.find(DISCOVERY_PACK_SECTION_MARKER)
        self.assertGreater(featured_pos, 0)
        self.assertGreater(univers_pos, featured_pos)
        self.assertGreater(pack_pos, univers_pos)

    def test_home_univers_no_carousel_no_technical_urls(self):
        html = self._open_fr_home().text
        chunk = self._univers_chunk(html)
        self.assertNotIn('data-bs-ride="carousel"', chunk)
        self.assertNotIn('route-hint', chunk)
        self.assertNotIn('Packs & découvertes', chunk)
        visible_urls = re.findall(r'>([^<]*/shop/category/[^<]*)<', chunk)
        self.assertFalse(visible_urls)

    def test_home_univers_responsive_grid_markup(self):
        html = self._open_fr_home().text
        chunk = self._univers_chunk(html)
        self.assertIn('ck-univers-cards__grid', chunk)
        self.assertIn('ck-univers-card__overlay', chunk)
        self.assertEqual(chunk.count('ck-univers-card__img'), 4)
        self.assertEqual(chunk.count(UNIVERS_EDITABLE_MEDIA_MARKER), 4)
        self.assertEqual(chunk.count(f'data-snippet="{UNIVERS_CARD_SNIPPET}"'), 4)
        self.assertEqual(chunk.count('ck-univers-card__cover'), 4)
        self.assertNotIn('data-href=', chunk)
        self.assertIn('ck-univers-card__media o_editable', chunk)
        self.assertIn('ck-univers-card--epicerie', chunk)
        self.assertIn('ck-univers-card--boissons', chunk)
        self.assertNotIn('data-snippet="s_ck_univers_cards"', chunk.split('ck-univers-cards__grid')[0])
        self.assertIn('ck_univers_epicerie.jpg?v=6', chunk)
        self.assertIn('ck_univers_boissons.jpg?v=6', chunk)
        self.assertIn('ck_univers_soin.jpg', chunk)
        self.assertIn('ck_univers_artisanat.jpg', chunk)

    def test_home_section3_non_regression(self):
        html = self._open_fr_home().text
        self.assertIn('ck-featured-products--maquette', html)
        self.assertIn('Nos coups de cœur', html)
