# -*- coding: utf-8 -*-
"""Tests HTTP Phase 7 — fiche producteur pilote (dorevia_ck_theme)."""

from odoo.tests import tagged
from odoo.tests.common import HttpCase

from odoo.addons.dorevia_ck_marketone_content.hooks import (
    PRODUCER_PAGE_URL,
    bootstrap_a_propos_page,
    bootstrap_contactus_page,
    bootstrap_producer_page,
    bootstrap_professionnels_page,
)


@tagged('post_install', '-at_install', 'dorevia_ck_theme_phase7')
class TestCkPhase7Compose(HttpCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        bootstrap_professionnels_page(cls.env)
        bootstrap_contactus_page(cls.env)
        bootstrap_a_propos_page(cls.env)
        bootstrap_producer_page(cls.env)
        cls.product = cls.env['product.template'].search(
            [('is_published', '=', True), ('sale_ok', '=', True)],
            limit=1,
        )

    def _assert_website_layout(self, html):
        lowered = html.lower()
        self.assertIn('<html', lowered)
        self.assertIn('web.assets_frontend', html)
        self.assertIn('<header', lowered)

    def _producer_html(self):
        return self.url_open(PRODUCER_PAGE_URL).text

    def test_producer_page_website_layout(self):
        self._assert_website_layout(self._producer_html())

    def test_producer_page_http_200(self):
        self.assertEqual(self.url_open(PRODUCER_PAGE_URL).status_code, 200)

    def test_producer_page_phase7_markers(self):
        html = self._producer_html()
        self.assertIn('ck-producer-page', html)
        self.assertIn('Atelier Les Hauts Goyaviers', html)
        self.assertIn('Saint-Pierre', html)
        self.assertIn('Savoir-faire', html)
        self.assertIn('Pourquoi CK sélectionne', html)
        self.assertIn('ck-producer-products', html)
        self.assertIn('href="/shop"', html)
        self.assertIn('href="/contactus"', html)
        self.assertIn('href="/professionnels"', html)
        self.assertNotIn('/recettes', html)
        self.assertNotIn('portail', html.lower())

    def test_producer_no_broken_shop_links(self):
        html = self._producer_html()
        for bad in ('/shop/confiture-passion', '/shop/gelee-chouchou', 'fiche-produit.html'):
            self.assertNotIn(bad, html)

    def test_product_page_phase4_unchanged_no_producer_link(self):
        if not self.product:
            self.skipTest('Aucun produit publié.')
        html = self.url_open(self.product.website_url).text
        self.assertIn('ck-product-page', html)
        self.assertNotIn('atelier-hauts-goyaviers', html)

    def test_home_phase2_intact(self):
        html = self.url_open('/').text
        self.assertIn('ck-featured-products__grid--stable', html)

    def test_shop_phase3_intact(self):
        html = self.url_open('/shop').text
        self.assertIn('s_ck_shop_intro', html)

    def test_contactus_phase6_intact(self):
        html = self.url_open('/contactus').text
        self.assertIn('ck-contact-page', html)
        self.assertIn('<html', html.lower())
        self.assertIn('web.assets_frontend', html)

    def test_a_propos_phase6_intact(self):
        html = self.url_open('/a-propos').text
        self.assertIn('ck-about-page', html)
        self.assertIn('<html', html.lower())
        self.assertIn('web.assets_frontend', html)

    def test_professionnels_phase5_intact(self):
        html = self.url_open('/professionnels').text
        self.assertIn('ck-pro-page', html)
        self.assertIn('<html', html.lower())
        self.assertIn('web.assets_frontend', html)

    def test_cart_http_200(self):
        self.assertEqual(self.url_open('/shop/cart').status_code, 200)
