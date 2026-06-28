# -*- coding: utf-8 -*-
"""Tests HTTP Phase 9 — newsletter M9 · contact · pro (dorevia_ck_theme)."""

import json

from odoo.tests import tagged
from odoo.tests.common import HttpCase

from odoo.addons.dorevia_ck_marketone_content.hooks import (
    NEWSLETTER_MAILING_LIST_NAME,
    RECIPES_PAGE_URL,
    bootstrap_a_propos_page,
    bootstrap_contactus_page,
    bootstrap_newsletter_mailing_list,
    bootstrap_producer_page,
    bootstrap_professionnels_page,
    bootstrap_recipes_page,
)

QA_NEWSLETTER_TEST_EMAIL = 'qa-phase9-newsletter@test.ck.local'


@tagged('post_install', '-at_install', 'dorevia_ck_theme_phase9')
class TestCkPhase9Compose(HttpCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.mailing_list = bootstrap_newsletter_mailing_list(cls.env)
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

    def _cleanup_newsletter_test_contact(self):
        self.env['mailing.contact'].sudo().search([
            ('email', '=', QA_NEWSLETTER_TEST_EMAIL),
        ]).unlink()

    def test_mailing_list_bo_real(self):
        mailing_list = bootstrap_newsletter_mailing_list(self.env)
        self.assertEqual(mailing_list.name, NEWSLETTER_MAILING_LIST_NAME)

    def test_contactus_newsletter_dual(self):
        html = self.url_open('/contactus').text
        self._assert_website_layout(html)
        self.assertIn('ck-contact-page', html)
        self.assertIn('id="contactus_form"', html)
        self.assertIn('ck-dual-engage--compact', html)
        self.assertIn('ck-newsletter-subscribe', html)
        self.assertIn('Recevez les nouveautés créoles', html)
        self.assertIn('Désinscription possible', html)
        self.assertIn(f'data-list-id="{self.mailing_list.id}"', html)
        self.assertIn('href="/professionnels"', html)

    def test_professionnels_newsletter_dual(self):
        html = self.url_open('/professionnels').text
        self._assert_website_layout(html)
        self.assertIn('ck-pro-page', html)
        self.assertIn('id="ck-pro-form"', html)
        self.assertIn('data-model_name="crm.lead"', html)
        self.assertIn('ck-dual-engage--compact', html)
        self.assertIn('ck-newsletter-subscribe', html)
        self.assertIn('href="#ck-pro-form"', html)

    def test_newsletter_subscribe_functional(self):
        self._cleanup_newsletter_test_contact()
        payload = json.dumps({
            'jsonrpc': '2.0',
            'method': 'call',
            'params': {
                'list_id': self.mailing_list.id,
                'value': QA_NEWSLETTER_TEST_EMAIL,
                'subscription_type': 'email',
            },
            'id': 1,
        })
        resp = self.url_open(
            '/website_mass_mailing/subscribe',
            data=payload.encode(),
            headers={'Content-Type': 'application/json'},
        )
        self.assertEqual(resp.status_code, 200)
        self.assertIn('"result"', resp.text)
        contact = self.env['mailing.contact'].sudo().search([
            ('email', '=', QA_NEWSLETTER_TEST_EMAIL),
        ], limit=1)
        self.assertTrue(contact)
        self.assertIn(self.mailing_list, contact.list_ids)
        self._cleanup_newsletter_test_contact()

    def test_home_dual_phase2_intact(self):
        html = self.url_open('/').text
        self.assertIn('ck-dual-engage', html)
        self.assertIn('ck-featured-products__grid--stable', html)

    def test_recipes_phase8_intact(self):
        html = self.url_open(RECIPES_PAGE_URL).text
        self.assertIn('ck-recipes-page', html)

    def test_shop_phase3_intact(self):
        html = self.url_open('/shop').text
        self.assertIn('ck-shop-intro--title-only', html)

    def test_product_phase4_intact(self):
        if not self.product:
            self.skipTest('Aucun produit publié.')
        html = self.url_open(self.product.website_url).text
        self.assertIn('ck-product-page', html)

    def test_producer_phase7_intact(self):
        html = self.url_open('/producteur/atelier-hauts-goyaviers').text
        self.assertIn('ck-producer-page', html)

    def test_no_popup_newsletter(self):
        html = self.url_open('/contactus').text
        self.assertNotIn('s_newsletter_subscribe_popup', html)
