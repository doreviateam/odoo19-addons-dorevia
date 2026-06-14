# -*- coding: utf-8 -*-
"""Tests HTTP Phase 6 — /contactus · /a-propos (dorevia_ck_theme)."""

from odoo.tests import tagged
from odoo.tests.common import HttpCase

from odoo.addons.dorevia_ck_marketone_content.hooks import (
    bootstrap_a_propos_page,
    bootstrap_contactus_page,
    bootstrap_professionnels_page,
)


@tagged('post_install', '-at_install', 'dorevia_ck_theme_phase6')
class TestCkPhase6Compose(HttpCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        bootstrap_professionnels_page(cls.env)
        bootstrap_contactus_page(cls.env)
        bootstrap_a_propos_page(cls.env)
        cls.product = cls.env['product.template'].search(
            [('is_published', '=', True), ('sale_ok', '=', True)],
            limit=1,
        )

    def _assert_website_layout(self, html):
        self.assertIn('<html', html.lower())
        self.assertIn('web.assets_frontend', html)

    def test_contactus_website_layout(self):
        self._assert_website_layout(self.url_open('/contactus').text)

    def test_a_propos_website_layout(self):
        self._assert_website_layout(self.url_open('/a-propos').text)

    def test_contactus_http_200(self):
        self.assertEqual(self.url_open('/contactus').status_code, 200)

    def test_contactus_phase6_markers(self):
        html = self.url_open('/contactus').text
        self.assertIn('ck-contact-page', html)
        self.assertIn('id="contactus_form"', html)
        self.assertIn('data-model_name="mail.mail"', html)
        self.assertIn('Nous contacter', html)
        self.assertIn('/professionnels', html)
        self.assertIn('ck-contact-form', html)
        self.assertNotIn('Ma société', html)
        self.assertNotIn('Fake Buena Vista', html)
        self.assertNotIn('crm.lead', html)

    def test_a_propos_http_200(self):
        self.assertEqual(self.url_open('/a-propos').status_code, 200)

    def test_a_propos_phase6_markers(self):
        html = self.url_open('/a-propos').text
        self.assertIn('ck-about-page', html)
        self.assertIn('Notre mission', html)
        self.assertIn('Notre sélection', html)
        self.assertIn('Logistique', html)
        self.assertIn('href="/shop"', html)
        self.assertIn('href="/professionnels"', html)
        self.assertIn('href="/contactus"', html)
        self.assertNotIn('/recettes', html)
        self.assertNotIn('/producteur/', html)
        self.assertIn('pas de portail opaque', html.lower())

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
        self.assertIn('ck-product-pro-signal', html)

    def test_professionnels_phase5_intact(self):
        html = self.url_open('/professionnels').text
        self.assertIn('ck-pro-page', html)
        self.assertIn('ck-pro-form', html)

    def test_cart_http_200(self):
        self.assertEqual(self.url_open('/shop/cart').status_code, 200)
