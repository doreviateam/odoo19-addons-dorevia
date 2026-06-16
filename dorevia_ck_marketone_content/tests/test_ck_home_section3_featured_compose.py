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
    _ensure_featured_category,
    _get_featured_labels_line,
    bootstrap_home_featured_products,
    get_curated_featured_variants,
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
        curated_variants = get_curated_featured_variants(cls.env)
        fallback_variants = get_ready_featured_variants(cls.env)
        variants = curated_variants or fallback_variants
        cls.expected_featured_cards = len(curated_variants) or MIN_FEATURED_PRODUCTS
        if len(variants) < cls.expected_featured_cards:
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
        self.assertIn('savoir-faire créole', html)
        self.assertIn('Toute la boutique', html)
        self.assertIn('ck-featured-products--maquette', html)

    def test_home_featured_after_trust_bar(self):
        html = self.url_open('/').text
        self.assertLess(html.find(REASSURANCE_TRUST_BAR_MARKER), html.find('ck-featured-products'))

    def test_home_featured_maquette_cards(self):
        grid_chunk = self._featured_grid_chunk(self.url_open('/').text)
        expected = self.expected_featured_cards
        self.assertGreaterEqual(grid_chunk.count(FEATURED_CARD_MARKER), expected)
        self.assertGreaterEqual(len(_CARD_MEDIA_RE.findall(grid_chunk)), expected)
        self.assertGreaterEqual(grid_chunk.count('class="card-cta"'), expected)
        self.assertGreaterEqual(grid_chunk.count('class="price"'), expected)
        self.assertNotIn('o_carousel_product_card', grid_chunk)

    def test_home_featured_card_shows_product_tags_line(self):
        """Étiquettes produit BO visibles sous le nom sur la card home."""
        curated = get_curated_featured_variants(self.env)
        if not curated:
            raise unittest.SkipTest('Aucune vedette curatée pour le test étiquettes.')
        tagged_template = curated[0].product_tmpl_id.sudo()
        guadeloupe = self.env['product.tag'].sudo().create({
            'name': 'Guadeloupe',
            'sequence': 10,
        })
        epicerie = self.env['product.tag'].sudo().create({
            'name': 'Épicerie',
            'sequence': 20,
        })
        tagged_template.write({
            'product_tag_ids': [(6, 0, [guadeloupe.id, epicerie.id])],
        })
        labels_line = _get_featured_labels_line(tagged_template)
        self.assertEqual(labels_line, 'Guadeloupe · Épicerie')
        grid_chunk = self._featured_grid_chunk(self.url_open('/').text)
        self.assertIn('product-card-labels', grid_chunk)
        self.assertIn('Guadeloupe · Épicerie', grid_chunk)

    def test_home_http_rebuilds_stale_arch_without_product_labels(self):
        """GET / reconstruit la home si les étiquettes produit manquent (arch périmée)."""
        import re

        category = _ensure_featured_category(self.env)
        guadeloupe = self.env['product.tag'].sudo().create({
            'name': 'Guadeloupe',
            'sequence': 10,
        })
        epicerie = self.env['product.tag'].sudo().create({
            'name': 'Épicerie',
            'sequence': 20,
        })
        self.env['product.template'].sudo().create({
            'name': 'CK Vedette HTTP Labels',
            'list_price': 4.5,
            'is_published': True,
            'website_published': True,
            'sale_ok': True,
            'public_categ_ids': [(4, category.id)],
            'product_tag_ids': [(6, 0, [guadeloupe.id, epicerie.id])],
            'image_1920': _TINY_PNG,
        })
        bootstrap_home_featured_products(self.env)
        page = self.env['website.page'].sudo().search([('url', '=', '/')], limit=1)
        view = page.view_id.sudo()
        stale_arch = re.sub(
            r'<p class="product-card-labels">[^<]*</p>\s*',
            '',
            view.arch_db or '',
        )
        view.write({'arch_db': stale_arch})
        self.assertNotIn('<p class="product-card-labels">', view.arch_db or '')

        grid_chunk = self._featured_grid_chunk(self.url_open('/').text)
        self.assertIn('product-card-labels', grid_chunk)
        self.assertIn('Guadeloupe · Épicerie', grid_chunk)

    def test_home_featured_lot2_contract_intact(self):
        grid_chunk = self._featured_grid_chunk(self.url_open('/').text)
        self.assertNotIn('s_dynamic_snippet_products', grid_chunk)
        self.assertNotIn('data-bs-ride="carousel"', grid_chunk)
