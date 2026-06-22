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
    _ensure_featured_category,
    _get_featured_labels_line,
    bootstrap_home_featured_products,
    get_curated_featured_variants,
)
from odoo.addons.dorevia_ck_marketone_content.home_hero import bootstrap_home_hero
from odoo.addons.dorevia_ck_marketone_content.home_reassurance import (
    REASSURANCE_TRUST_BAR_MARKER,
    bootstrap_home_reassurance,
)
from odoo.addons.dorevia_ck_marketone_content.hooks import bootstrap_home_featured_products

from odoo.addons.dorevia_ck_marketone_content.ck_product_placeholders import (
    CK_CREAM_PLACEHOLDER_PNG_B64,
    ensure_test_variant_images,
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
        if not curated_variants:
            raise unittest.SkipTest('Aucune vedette ck_is_featured sur instance seed.')
        cls.expected_featured_cards = len(curated_variants)
        variants = curated_variants
        if len(variants) < cls.expected_featured_cards:
            raise unittest.SkipTest('Catalogue insuffisant pour Section 3 vedettes.')
        for variant in variants:
            ensure_test_variant_images(variant)
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
        self.assertGreaterEqual(grid_chunk.count('card-cta--secondary'), expected)
        self.assertGreaterEqual(grid_chunk.count('class="card-cart-cta"'), expected)
        self.assertGreaterEqual(grid_chunk.count('ck-product-card__price-value'), expected)
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

    def test_stale_arch_rebuilt_by_sync(self):
        """Le sync (cron/boot) reconstruit la home si les étiquettes produit manquent.

        PR-3 (H2) : l'auto-réparation ne se fait plus via GET / (override
        ir_http._pre_dispatch supprimé) mais via
        product.template._ck_sync_home_featured_labels_on_startup() — appelée par
        le cron ck_cron_sync_home_featured et au démarrage du worker.
        """
        guadeloupe = self.env['product.tag'].sudo().create({'name': 'Guadeloupe'})
        epicerie = self.env['product.tag'].sudo().create({'name': 'Épicerie'})
        self.env['product.template'].sudo().create({
            'name': 'CK Vedette Sync Labels',
            'list_price': 4.5,
            'is_published': True,
            'website_published': True,
            'sale_ok': True,
            'ck_is_featured': True,
            'product_tag_ids': [(6, 0, [guadeloupe.id, epicerie.id])],
            'image_1920': CK_CREAM_PLACEHOLDER_PNG_B64,
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

        # Réparation par le sync (cron/boot), pas par une requête HTTP.
        self.env['product.template']._ck_sync_home_featured_labels_on_startup()
        view.invalidate_recordset(['arch_db'])
        self.assertIn('product-card-labels', view.arch_db or '')
        self.assertIn('Guadeloupe · Épicerie', view.arch_db or '')

    def test_home_featured_lot2_contract_intact(self):
        grid_chunk = self._featured_grid_chunk(self.url_open('/').text)
        self.assertNotIn('s_dynamic_snippet_products', grid_chunk)
        self.assertNotIn('data-bs-ride="carousel"', grid_chunk)
