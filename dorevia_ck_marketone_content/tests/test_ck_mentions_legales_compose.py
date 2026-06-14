# -*- coding: utf-8 -*-
"""Tests HTTP — pages légales /legal · /privacy · /terms et footer."""

from odoo.tests import tagged
from odoo.tests.common import HttpCase

from odoo.addons.dorevia_ck_marketone_content.hooks import (
    bootstrap_footer_legal_links,
    bootstrap_mentions_legales_page,
    bootstrap_privacy_page,
    bootstrap_terms_page,
)


@tagged('post_install', '-at_install', 'dorevia_ck_marketone_legal')
class TestCkMentionsLegalesCompose(HttpCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        bootstrap_mentions_legales_page(cls.env)
        bootstrap_privacy_page(cls.env)
        bootstrap_terms_page(cls.env)
        bootstrap_footer_legal_links(cls.env)

    def test_legal_page_http_200(self):
        self.assertEqual(self.url_open('/legal').status_code, 200)

    def test_privacy_page_http_200(self):
        self.assertEqual(self.url_open('/privacy').status_code, 200)

    def test_terms_page_http_200(self):
        self.assertEqual(self.url_open('/terms').status_code, 200)

    def test_legal_page_markers(self):
        html = self.url_open('/legal').text
        self.assertIn('ck-legal-page', html)
        self.assertIn('ck-legal-recette-banner', html)
        self.assertIn('Version recette interne', html)
        self.assertIn('Marketone SAS', html)
        self.assertIn('IONOS', html)
        self.assertIn('DONNÉE FICTIVE', html)
        self.assertIn('contact.ck@marketone.com', html)
        self.assertIn('/privacy', html)
        self.assertIn('/terms', html)

    def test_privacy_page_markers(self):
        html = self.url_open('/privacy').text
        self.assertIn('ck-privacy-page', html)
        self.assertIn('Politique de confidentialité', html)
        self.assertIn('Marketone SAS', html)
        self.assertIn('/legal', html)

    def test_terms_page_markers(self):
        html = self.url_open('/terms').text
        self.assertIn('ck-terms-page', html)
        self.assertIn('Conditions générales de vente', html)
        self.assertIn('id="cgv"', html)
        self.assertIn('MÉDIATEUR À CONFIRMER', html)

    def test_footer_legal_links_home(self):
        html = self.url_open('/').text
        self.assertIn('href="/legal"', html)
        self.assertIn('href="/privacy"', html)
        self.assertIn('href="/terms#cgv"', html)
        self.assertIn('Mentions légales', html)
        self.assertIn('Confidentialité', html)
        self.assertIn('CGV', html)

    def test_footer_legal_links_shop(self):
        html = self.url_open('/shop').text
        self.assertIn('href="/legal"', html)
        self.assertIn('href="/privacy"', html)
        self.assertIn('href="/terms#cgv"', html)
