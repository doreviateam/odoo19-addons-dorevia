# -*- coding: utf-8 -*-
"""Tests HTTP Section 3 — vedettes home · cartes maquette CK."""

import re
import unittest

from odoo.tests import tagged
from odoo.tests.common import HttpCase

from odoo.addons.dorevia_ck_marketone_content.catalog_manioc_variants import (
    bootstrap_catalog_vedettes_products,
)
from odoo.addons.dorevia_ck_marketone_content.home_featured import (
    FEATURED_CARD_MARKER,
    FEATURED_TITLE,
    MIN_FEATURED_PRODUCTS,
    get_ready_featured_variants,
)
from odoo.addons.dorevia_ck_marketone_content.home_hero import bootstrap_home_hero
from odoo.addons.dorevia_ck_marketone_content.home_reassurance import (
    REASSURANCE_TRUST_BAR_MARKER,
    bootstrap_home_reassurance,
)
from odoo.addons.dorevia_ck_marketone_content.hooks import bootstrap_home_featured_products

_TINY_PNG = (
    b'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAADElEQVR4nGP4z8AAAAMBAQDJ/pLvAAAAAElFTkSuQmCC'
)

_CARD_MEDIA_RE = re.compile(
    r'product-card-media[^>]*background-image:\s*url\(',
    re.IGNORECASE,
)


@tagged('post_install', '-at_install', 'dorevia_ck_marketone_home_section3')
class TestCkHomeSection3FeaturedCompose(HttpCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        bootstrap_catalog_vedettes_products(cls.env)
        variants = get_ready_featured_variants(cls.env)
        if len(variants) < MIN_FEATURED_PRODUCTS:
            raise unittest.SkipTest('Catalogue insuffisant pour Section 3 vedettes.')
        for variant in variants:
            variant.write({'image_1920': _TINY_PNG})
            if variant.product_tmpl_id:
                variant.product_tmpl_id.write({'image_1920': _TINY_PNG})
        bootstrap_home_hero(cls.env)
        bootstrap_home_reassurance(cls.env)
        bootstrap_home_featured_products(cls.env)

    def _featured_grid_chunk(self, html):
        grid_start = html.find('ck-featured-products__grid--stable')
        self.assertGreater(grid_start, 0)
        return html[grid_start:grid_start + 120000]

    def test_home_featured_maquette_header(self):
        html = self.url_open('/').text
        self.assertIn(FEATURED_TITLE, html)
        self.assertIn('Sélection CK', html)
        self.assertIn('Toute la boutique', html)
        self.assertIn('ck-featured-products--maquette', html)

    def test_home_featured_after_trust_bar(self):
        html = self.url_open('/').text
        self.assertLess(html.find(REASSURANCE_TRUST_BAR_MARKER), html.find('ck-featured-products'))

    def test_home_featured_maquette_cards(self):
        grid_chunk = self._featured_grid_chunk(self.url_open('/').text)
        self.assertGreaterEqual(grid_chunk.count(FEATURED_CARD_MARKER), MIN_FEATURED_PRODUCTS)
        self.assertGreaterEqual(len(_CARD_MEDIA_RE.findall(grid_chunk)), MIN_FEATURED_PRODUCTS)
        self.assertGreaterEqual(grid_chunk.count('class="card-cta"'), MIN_FEATURED_PRODUCTS)
        self.assertGreaterEqual(grid_chunk.count('class="price"'), MIN_FEATURED_PRODUCTS)
        self.assertNotIn('o_carousel_product_card', grid_chunk)

    def test_home_featured_lot2_contract_intact(self):
        grid_chunk = self._featured_grid_chunk(self.url_open('/').text)
        self.assertNotIn('s_dynamic_snippet_products', grid_chunk)
        self.assertNotIn('data-bs-ride="carousel"', grid_chunk)
