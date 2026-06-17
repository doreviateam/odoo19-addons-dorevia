# -*- coding: utf-8 -*-
"""Tests HTTP Lot 2 — vedettes home SSR · liens produits · pas de carousel."""

import re

from odoo.tests import tagged
from odoo.tests.common import HttpCase

from odoo.addons.dorevia_ck_marketone_content.home_featured import MIN_FEATURED_PRODUCTS
from odoo.addons.dorevia_ck_marketone_content.hooks import bootstrap_home_featured_products
from odoo.addons.dorevia_ck_marketone_content.tests.ck_home_lot2_utils import (
    detach_featured_curation,
    ensure_auto_featured_catalog,
    restore_featured_curation,
)

_CARD_IMAGE_RE = re.compile(
    r"background-image:\s*url\(\s*(?:&#39;|['\"])?/web/image/product\.(?:template|product)/\d+/",
    re.IGNORECASE,
)


@tagged('post_install', '-at_install', 'dorevia_ck_marketone_home_lot2')
class TestCkHomeLot2Compose(HttpCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Lot2 option B : chemin auto + seuil MIN_FEATURED_PRODUCTS (pas la curation BO).
        cls._curation_backup = detach_featured_curation(cls.env)
        ensure_auto_featured_catalog(cls.env)
        bootstrap_home_featured_products(cls.env)

    @classmethod
    def tearDownClass(cls):
        restore_featured_curation(cls.env, cls._curation_backup)
        super().tearDownClass()

    def test_home_featured_ssr_present(self):
        html = self.url_open('/').text
        grid_start = html.find('ck-featured-products__grid--stable')
        self.assertGreater(grid_start, 0)
        grid_chunk = html[grid_start:grid_start + 120000]
        self.assertIn('Nos coups de cœur', html)
        self.assertIn('Toute la boutique', html)
        self.assertNotIn('s_dynamic_snippet_products', grid_chunk)
        self.assertNotIn('website.s_cover_default_image', grid_chunk)

    def test_home_featured_cards_count(self):
        html = self.url_open('/').text
        grid_start = html.find('ck-featured-products__grid--stable')
        self.assertGreater(grid_start, 0)
        grid_chunk = html[grid_start:grid_start + 120000]
        cards = grid_chunk.count('ck-product-card')
        self.assertGreaterEqual(cards, MIN_FEATURED_PRODUCTS)

    def test_home_featured_product_links_200(self):
        html = self.url_open('/').text
        grid_start = html.find('ck-featured-products__grid--stable')
        grid_chunk = html[grid_start:grid_start + 120000]
        links = re.findall(r'href="(/shop/[^"]+)"', grid_chunk)
        self.assertGreaterEqual(len(links), MIN_FEATURED_PRODUCTS)
        for href in links[:MIN_FEATURED_PRODUCTS]:
            self.assertEqual(self.url_open(href).status_code, 200)

    def test_home_featured_prices_and_images(self):
        html = self.url_open('/').text
        grid_start = html.find('ck-featured-products__grid--stable')
        grid_chunk = html[grid_start:grid_start + 120000]
        self.assertGreaterEqual(grid_chunk.count('class="price"'), MIN_FEATURED_PRODUCTS)
        self.assertGreaterEqual(len(_CARD_IMAGE_RE.findall(grid_chunk)), MIN_FEATURED_PRODUCTS)
        self.assertGreaterEqual(grid_chunk.count('Voir le produit'), MIN_FEATURED_PRODUCTS)

    def test_home_no_carousel_in_featured(self):
        html = self.url_open('/').text
        grid_start = html.find('ck-featured-products__grid--stable')
        grid_chunk = html[grid_start:grid_start + 120000]
        self.assertNotIn('s_dynamic_snippet_products', grid_chunk)
        self.assertNotIn('data-bs-ride="carousel"', grid_chunk)
        self.assertNotIn('carousel slide', grid_chunk)

    def test_home_dual_phase2_intact(self):
        html = self.url_open('/').text
        self.assertIn('ck-dual-engage', html)
