# -*- coding: utf-8 -*-
"""Tests HTTP Lot 2 — vedettes home SSR · liens produits · pas de carousel."""

import re

from odoo.tests import tagged
from odoo.tests.common import HttpCase

from odoo.addons.dorevia_ck_marketone_content.home_featured import MIN_FEATURED_PRODUCTS
from odoo.addons.dorevia_ck_marketone_content.hooks import bootstrap_home_featured_products

_TINY_PNG = (
    b'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAADElEQVR4nGP4z8AAAAMBAQDJ/pLvAAAAAElFTkSuQmCC'
)


@tagged('post_install', '-at_install', 'dorevia_ck_marketone_home_lot2')
class TestCkHomeLot2Compose(HttpCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        products = cls.env['product.template'].search([
            ('is_published', '=', True),
            ('website_published', '=', True),
        ], limit=MIN_FEATURED_PRODUCTS)
        if len(products) < MIN_FEATURED_PRODUCTS:
            cls.skipTest('Catalogue insuffisant pour Lot 2.')
        products.write({'image_1920': _TINY_PNG})
        bootstrap_home_featured_products(cls.env)

    def test_home_featured_ssr_present(self):
        html = self.url_open('/').text
        grid_start = html.find('ck-featured-products__grid--stable')
        self.assertGreater(grid_start, 0)
        grid_chunk = html[grid_start:grid_start + 120000]
        self.assertIn('Produits vedettes', html)
        self.assertNotIn('s_dynamic_snippet_products', grid_chunk)
        self.assertNotIn('website.s_cover_default_image', grid_chunk)

    def test_home_featured_cards_count(self):
        html = self.url_open('/').text
        grid_start = html.find('ck-featured-products__grid--stable')
        self.assertGreater(grid_start, 0)
        grid_chunk = html[grid_start:grid_start + 120000]
        cards = grid_chunk.count('o_carousel_product_card')
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
        self.assertGreaterEqual(grid_chunk.count('oe_currency_value'), MIN_FEATURED_PRODUCTS)
        self.assertGreaterEqual(
            len(re.findall(r'background-image:\s*url\(/web/image/product\.', grid_chunk)),
            MIN_FEATURED_PRODUCTS,
        )

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
