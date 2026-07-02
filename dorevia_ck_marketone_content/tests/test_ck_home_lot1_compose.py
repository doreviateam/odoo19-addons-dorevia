# -*- coding: utf-8 -*-
"""Tests HTTP V1 Hero / Lot 1 · non-régression lots 2–5."""

from odoo.tests import tagged
from odoo.tests.common import HttpCase

from odoo.addons.dorevia_ck_marketone_content.home_dual_engage import (
    bootstrap_home_dual_engage,
)
from odoo.addons.dorevia_ck_marketone_content.home_editorial import (
    bootstrap_home_editorial,
)
from odoo.addons.dorevia_ck_marketone_content.home_hero import (
    HERO_CAROUSEL_INTERVAL_MS,
    HERO_CAROUSEL_MARKER,
    HERO_CTA_PRODUCTEURS_LABEL,
    HERO_CTA_SHOP_LABEL,
    HERO_KICKER,
    HERO_TITLE,
    HERO_VARIANT_MARKER,
    HERO_VISUAL_MAX_SLIDES,
    bootstrap_home_hero,
)
from odoo.addons.dorevia_ck_marketone_content.hooks import (
    bootstrap_home_discovery_pack,
    bootstrap_home_featured_products,
)


@tagged('post_install', '-at_install', 'dorevia_ck_marketone_home_lot1')
class TestCkHomeLot1Compose(HttpCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        bootstrap_home_hero(cls.env)
        bootstrap_home_featured_products(cls.env)
        bootstrap_home_discovery_pack(cls.env)
        bootstrap_home_dual_engage(cls.env)
        bootstrap_home_editorial(cls.env)

    def _hero_chunk(self, html):
        start = html.find(HERO_VARIANT_MARKER)
        self.assertGreater(start, 0)
        return html[start:start + 8000]

    def test_home_hero_block_present(self):
        html = self.url_open('/').text
        chunk = self._hero_chunk(html)
        self.assertIn(HERO_TITLE, chunk)
        self.assertIn('Produits créoles', chunk)
        self.assertIn('Producteurs', chunk)
        self.assertIn(HERO_CTA_SHOP_LABEL, chunk)
        self.assertIn(HERO_CTA_PRODUCTEURS_LABEL, chunk)

    def test_home_hero_no_cover_default_image(self):
        html = self.url_open('/').text
        chunk = self._hero_chunk(html)
        self.assertNotIn('website.s_cover_default_image', chunk)
        self.assertNotIn('s_cover_default', chunk)

    def test_home_hero_ctas_http_200(self):
        self.assertEqual(self.url_open('/shop').status_code, 200)
        self.assertEqual(self.url_open('/producteurs').status_code, 200)

    def test_home_hero_before_featured(self):
        html = self.url_open('/').text
        self.assertLess(html.find(HERO_VARIANT_MARKER), html.find('ck-featured-products'))

    def test_home_hero_visual_present(self):
        html = self.url_open('/').text
        chunk = self._hero_chunk(html)
        self.assertIn('ck-hero__visual', chunk)
        self.assertIn('ck-hero__grid', chunk)
        self.assertNotIn('ratio-16x10', chunk)
        self.assertIn(HERO_CAROUSEL_MARKER, chunk)
        self.assertIn('ck_hero_home_v1', chunk)
        self.assertIn('ck-hero__visual-media', chunk)
        self.assertGreaterEqual(chunk.count('carousel-item'), 1)
        self.assertLessEqual(chunk.count('carousel-item'), HERO_VISUAL_MAX_SLIDES)

    def test_home_hero_carousel_image_only(self):
        html = self.url_open('/').text
        chunk = self._hero_chunk(html)
        content_part = chunk.split('ck-hero__visual-col', 1)[0]
        self.assertNotIn('data-bs-ride="carousel"', content_part)
        self.assertNotIn('carousel slide', content_part)
        visual_part = chunk.split('ck-hero__visual-col', 1)[-1]
        self.assertIn('data-bs-ride="carousel"', visual_part)
        self.assertIn(f'data-bs-interval="{HERO_CAROUSEL_INTERVAL_MS}"', visual_part)

    def test_home_lot2_to_lot5_non_regression(self):
        html = self.url_open('/').text
        self.assertIn('ck-featured-products__grid--stable', html)
        self.assertIn('ck-discovery-pack', html)
        self.assertIn('ck-dual-engage--compact', html)
        self.assertIn('ck-home-editorial', html)
        self.assertNotIn('s_ck_pro_banner', html)
