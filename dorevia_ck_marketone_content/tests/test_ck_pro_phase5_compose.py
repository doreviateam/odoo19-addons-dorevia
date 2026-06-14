# -*- coding: utf-8 -*-
"""Tests HTTP Phase 5 — page /professionnels + CRM (dorevia_ck_theme)."""

from odoo.tests import tagged
from odoo.tests.common import HttpCase

from odoo.addons.dorevia_ck_marketone_content.hooks import bootstrap_professionnels_page


@tagged('post_install', '-at_install', 'dorevia_ck_theme_phase5')
class TestCkProPhase5Compose(HttpCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        bootstrap_professionnels_page(cls.env)
        cls.product = cls.env['product.template'].search(
            [('is_published', '=', True), ('sale_ok', '=', True)],
            limit=1,
        )

    def _professionnels_html(self):
        return self.url_open('/professionnels').text

    def _assert_website_layout(self, html):
        self.assertIn('<html', html.lower())
        self.assertIn('web.assets_frontend', html)

    def test_professionnels_website_layout(self):
        self._assert_website_layout(self._professionnels_html())

    def test_professionnels_page_http_200(self):
        self.assertEqual(self.url_open('/professionnels').status_code, 200)

    def test_professionnels_page_phase5_markers(self):
        html = self._professionnels_html()
        self.assertIn('ck-pro-page', html)
        self.assertIn('id="ck-pro-form"', html)
        self.assertIn('data-model_name="crm.lead"', html)
        self.assertIn('Espace professionnel', html)
        self.assertIn('Producteurs', html)
        self.assertIn('fournisseur', html)
        self.assertIn('distributeur', html)
        self.assertIn('Boutiques', html)
        self.assertIn('pas de commande B2B', html)

    def test_professionnels_form_native_fields(self):
        html = self._professionnels_html()
        self.assertIn('name="description"', html)
        self.assertIn('name="email_from"', html)
        self.assertIn('s_website_form_send', html)
        self.assertNotIn('portail', html.lower())

    def test_crm_form_submission_creates_lead(self):
        marker = 'Phase 5 CK test lead qualification producteur'
        before = self.env['crm.lead'].sudo().search_count([
            ('description', 'ilike', marker),
        ])

        payload = {
            'name': 'Demande professionnelle CK',
            'partner_name': 'Structure Test Phase 5',
            'contact_name': 'Contact QA CK',
            'email_from': 'phase5-qa@ck-marketone.test',
            'description': marker,
        }
        resp = self.url_open('/website/form/crm.lead', data=payload)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('"id"', resp.text)

        after = self.env['crm.lead'].sudo().search_count([
            ('description', 'ilike', marker),
        ])
        self.assertGreater(after, before)

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

    def test_cart_http_200(self):
        self.assertEqual(self.url_open('/shop/cart').status_code, 200)

    def test_professionnels_no_public_pricing(self):
        html = self._professionnels_html()
        self.assertNotIn('pricelist', html.lower())
        self.assertIn('pas de tarif automatique', html.lower())
