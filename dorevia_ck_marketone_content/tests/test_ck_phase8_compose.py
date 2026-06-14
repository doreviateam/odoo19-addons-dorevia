# -*- coding: utf-8 -*-
"""Tests HTTP Phase 8 — page /recettes (dorevia_ck_theme)."""

from odoo.tests import tagged
from odoo.tests.common import HttpCase

from odoo.addons.dorevia_ck_marketone_content.hooks import (
    PRODUCER_PAGE_URL,
    RECIPES_PAGE_URL,
    bootstrap_a_propos_page,
    bootstrap_contactus_page,
    bootstrap_producer_page,
    bootstrap_professionnels_page,
    bootstrap_recipes_page,
)


@tagged('post_install', '-at_install', 'dorevia_ck_theme_phase8')
class TestCkPhase8Compose(HttpCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        bootstrap_professionnels_page(cls.env)
        bootstrap_contactus_page(cls.env)
        bootstrap_a_propos_page(cls.env)
        bootstrap_producer_page(cls.env)
        bootstrap_recipes_page(cls.env)
        cls.product = cls.env['product.template'].search(
            [('is_published', '=', True), ('sale_ok', '=', True)],
            limit=1,
        )

    def _assert_website_layout(self, html):
        lowered = html.lower()
        self.assertIn('<html', lowered)
        self.assertIn('web.assets_frontend', html)
        self.assertIn('<header', lowered)

    def _recipes_html(self):
        return self.url_open(RECIPES_PAGE_URL).text

    def test_recipes_page_website_layout(self):
        self._assert_website_layout(self._recipes_html())

    def test_recipes_page_http_200(self):
        self.assertEqual(self.url_open(RECIPES_PAGE_URL).status_code, 200)

    def test_recipes_page_phase8_markers(self):
        html = self._recipes_html()
        self.assertIn('ck-recipes-page', html)
        self.assertIn('Recettes & savoirs CK', html)
        self.assertIn('ck-recipes-cards', html)
        self.assertIn('Clafoutis créole au goyavier', html)
        self.assertIn('Première commande CK', html)
        self.assertIn('Comprendre la sélection CK', html)
        self.assertIn('href="/shop"', html)
        self.assertIn('href="/a-propos"', html)
        self.assertIn('href="/contactus"', html)
        self.assertIn('atelier-hauts-goyaviers', html)
        self.assertNotIn('fiche-produit.html', html)
        self.assertNotIn('website_blog', html.lower())

    def test_recipes_six_cards(self):
        html = self._recipes_html()
        self.assertEqual(html.count('ck-recipes-cards__grid'), 1)
        for title in (
            'Clafoutis créole au goyavier',
            'Bien choisir en boutique',
            'Galettes et snacks manioc',
            'Première commande CK',
            'Savons et routine quotidienne',
            'Comprendre la sélection CK',
        ):
            self.assertIn(title, html)

    def test_recipes_no_fictitious_links(self):
        html = self._recipes_html()
        for bad in ('/recettes/confiture', 'categorie.html', '/shop/confiture-passion'):
            self.assertNotIn(bad, html)

    def test_producer_phase7_intact(self):
        html = self.url_open(PRODUCER_PAGE_URL).text
        self.assertIn('ck-producer-page', html)
        self.assertIn('<html', html.lower())

    def test_home_phase2_intact(self):
        html = self.url_open('/').text
        self.assertIn('ck-featured-products__grid--stable', html)

    def test_shop_phase3_intact(self):
        html = self.url_open('/shop').text
        self.assertIn('s_ck_shop_intro', html)

    def test_product_phase4_intact(self):
        if not self.product:
            self.skipTest('Aucun produit publié.')
        html = self.url_open(self.product.website_url).text
        self.assertIn('ck-product-page', html)
        self.assertNotIn('ck-recipes-page', html)

    def test_contactus_phase6_intact(self):
        html = self.url_open('/contactus').text
        self.assertIn('ck-contact-page', html)

    def test_a_propos_phase6_intact(self):
        html = self.url_open('/a-propos').text
        self.assertIn('ck-about-page', html)

    def test_professionnels_phase5_intact(self):
        html = self.url_open('/professionnels').text
        self.assertIn('ck-pro-page', html)

    def test_cart_http_200(self):
        self.assertEqual(self.url_open('/shop/cart').status_code, 200)
