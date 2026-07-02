# -*- coding: utf-8 -*-
"""Tests HTTP Lot 4 — dual Pro / Newsletter home · non-régression lots 2–3."""

import json
import re

from odoo.tests import tagged
from odoo.tests.common import HttpCase

from odoo.addons.dorevia_ck_marketone_content.home_dual_engage import (
    bootstrap_home_dual_engage,
)
from odoo.addons.dorevia_ck_marketone_content.hooks import (
    NEWSLETTER_MAILING_LIST_NAME,
    NEWSLETTER_RGPD_NOTE,
    PRO_DUAL_TITLE,
    bootstrap_home_discovery_pack,
    bootstrap_home_featured_products,
    bootstrap_newsletter_mailing_list,
)

QA_NEWSLETTER_TEST_EMAIL = 'qa-home-lot4-newsletter@test.ck.local'


@tagged('post_install', '-at_install', 'dorevia_ck_marketone_home_lot4')
class TestCkHomeLot4Compose(HttpCase):
    FR_HEADERS = {'Accept-Language': 'fr-FR,fr;q=0.9'}

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.mailing_list = bootstrap_newsletter_mailing_list(cls.env)
        bootstrap_home_featured_products(cls.env)
        bootstrap_home_discovery_pack(cls.env)
        bootstrap_home_dual_engage(cls.env)

    def _open_fr_home(self):
        return self.url_open('/', headers=self.FR_HEADERS)

    def _dual_chunk(self, html):
        start = html.find('ck-dual-engage--compact')
        self.assertGreater(start, 0)
        return html[start:start + 15000]

    def test_home_dual_block_present(self):
        html = self._open_fr_home().text
        chunk = self._dual_chunk(html)
        self.assertIn(PRO_DUAL_TITLE, chunk)
        self.assertIn('href="/professionnels"', chunk)
        self.assertIn('Recevez les nouveautés créoles', chunk)
        self.assertIn('ck-newsletter-subscribe', chunk)
        self.assertIn(f'data-list-id="{self.mailing_list.id}"', chunk)
        self.assertIn('Désinscription possible', chunk)

    def test_home_dual_two_columns_desktop(self):
        html = self._open_fr_home().text
        chunk = self._dual_chunk(html)
        self.assertGreaterEqual(chunk.count('col-lg-6'), 2)

    def test_home_dual_order_after_discovery(self):
        html = self._open_fr_home().text
        self.assertLess(html.find('ck-discovery-pack'), html.find('ck-dual-engage--compact'))

    def test_home_pro_banner_removed(self):
        html = self._open_fr_home().text
        self.assertNotIn('s_ck_pro_banner', html)
        self.assertNotIn('ck-pro-banner', html)

    def test_home_pro_cta_http_200(self):
        self.assertEqual(self.url_open('/professionnels').status_code, 200)

    def test_home_newsletter_subscribe_functional(self):
        self.env['mailing.contact'].sudo().search([
            ('email', '=', QA_NEWSLETTER_TEST_EMAIL),
        ]).unlink()
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
        contact = self.env['mailing.contact'].sudo().search([
            ('email', '=', QA_NEWSLETTER_TEST_EMAIL),
        ], limit=1)
        self.assertTrue(contact)
        self.assertIn(self.mailing_list, contact.list_ids)
        contact.unlink()

    def test_home_lot2_lot3_non_regression(self):
        html = self._open_fr_home().text
        self.assertIn('ck-featured-products__grid--stable', html)
        self.assertIn('ck-discovery-pack', html)
        self.assertIn('href="/kits"', html)

    def test_home_no_technical_leaks_in_dual(self):
        html = self._open_fr_home().text
        chunk = self._dual_chunk(html)
        self.assertNotIn('dynamic_snippet', chunk.lower())
        self.assertIsNone(re.search(r'\bTODO\b|\bFIXME\b', chunk))

    def test_mailing_list_bo_real(self):
        mailing_list = bootstrap_newsletter_mailing_list(self.env)
        self.assertEqual(mailing_list.name, NEWSLETTER_MAILING_LIST_NAME)
