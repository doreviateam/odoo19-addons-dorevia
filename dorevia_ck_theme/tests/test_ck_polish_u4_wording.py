# -*- coding: utf-8 -*-
"""Polish-U4 — Wording panier vide, réassurance fiche, confirmation."""

import re

from odoo.tests import tagged
from odoo.tests.common import HttpCase, TransactionCase

from odoo.addons.dorevia_ck_marketone_content.catalog_manioc_variants import (
    MANIO_CRACKERS_PARENT_NAME,
)


@tagged('post_install', '-at_install', 'dorevia_ck_shop_card')
class TestCkPolishU4WordingViews(TransactionCase):
    def test_cart_empty_view_installed(self):
        view = self.env['ir.ui.view'].search([
            ('key', '=', 'dorevia_ck_theme.cart_lines_ck_empty'),
        ], limit=1)
        self.assertTrue(view)
        arch = view.arch_db if isinstance(view.arch_db, str) else str(view.arch_db)
        self.assertIn('Votre panier est vide. Découvrez nos produits créoles sélectionnés.', arch)
        self.assertIn('Découvrir la sélection', arch)
        self.assertNotIn('>Boutique<', arch)
        self.assertNotIn('>Shop<', arch)

    def test_confirmation_view_installed(self):
        view = self.env['ir.ui.view'].search([
            ('key', '=', 'dorevia_ck_theme.confirmation_ck_wording'),
        ], limit=1)
        self.assertTrue(view)
        arch = view.arch_db if isinstance(view.arch_db, str) else str(view.arch_db)
        self.assertIn(
            'Merci ! Votre commande est confirmée. Vous recevrez un e-mail récapitulatif sous peu.',
            arch,
        )
        self.assertIn('Livraison suivie · Expédié depuis Nantes', arch)

    def test_product_reassurance_wording(self):
        view = self.env['ir.ui.view'].search([
            ('key', '=', 'dorevia_ck_theme.product_ck_terms_fr'),
        ], limit=1)
        self.assertTrue(view)
        arch = view.arch_db if isinstance(view.arch_db, str) else str(view.arch_db)
        for needle in (
            'En stock · Expédié depuis Nantes',
            'Livraison suivie · 2 à 3 jours ouvrables',
            'Retour selon CGV',
        ):
            self.assertIn(needle, arch)
        self.assertNotIn('En stock — expédié depuis Nantes', arch)
        self.assertNotIn('conditions de vente', arch)

    def test_cart_empty_en_gb_translation_loaded(self):
        view = self.env['ir.ui.view'].search([
            ('key', '=', 'dorevia_ck_theme.cart_lines_ck_empty'),
        ], limit=1)
        arch = view.with_context(lang='en_GB').arch
        self.assertIn('Your cart is empty. Discover our selected Creole products.', arch)
        self.assertIn('Discover the selection', arch)

    def test_confirmation_en_gb_translation_loaded(self):
        view = self.env['ir.ui.view'].search([
            ('key', '=', 'dorevia_ck_theme.confirmation_ck_wording'),
        ], limit=1)
        arch = view.with_context(lang='en_GB').arch
        self.assertIn('Thank you! Your order is confirmed.', arch)
        self.assertIn('Tracked delivery · Shipped from Nantes', arch)


@tagged('post_install', '-at_install', 'dorevia_ck_shop_card')
class TestCkPolishU4WordingHttp(HttpCase):
    FR_HEADERS = {'Accept-Language': 'fr-FR,fr;q=0.9'}

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product = cls.env['product.template'].sudo().search([
            ('name', '=', MANIO_CRACKERS_PARENT_NAME),
            ('is_published', '=', True),
            ('website_published', '=', True),
        ], limit=1)
        if not cls.product:
            raise cls.skipTest('Produit témoin Manio Crackers absent ou non publié.')

    def _open(self, path, headers=None):
        response = self.url_open(path, headers=headers or self.FR_HEADERS)
        self.assertEqual(response.status_code, 200, path)
        return response.text

    def test_manio_product_reassurance_compact(self):
        html = self._open(f'{self.product.website_url}?qa_ts=polish_u4_trust')
        trust = re.search(
            r'ck-product-purchase__trust-list[^>]*>(.*?)</ul>',
            html,
            re.S,
        )
        self.assertTrue(trust, 'Bloc réassurance absent')
        text = trust.group(1)
        self.assertIn('En stock · Expédié depuis Nantes', text)
        self.assertIn('Livraison suivie · 2 à 3 jours ouvrables', text)
        self.assertIn('Retour selon CGV', text)
        self.assertNotIn('conditions de vente', text)

    def test_empty_cart_en_gb_wording(self):
        """Polish-U4 i18n — panier vide aligné sur /en comme la fiche produit."""
        self.authenticate(None, None)
        response = self.url_open(
            '/en/shop/cart?qa_ts=polish_u4_empty_en',
            headers={'Accept-Language': 'en-GB,en;q=0.9'},
        )
        self.assertEqual(response.status_code, 200)
        html = response.text
        self.assertIn(
            'Your cart is empty. Discover our selected Creole products.',
            html,
        )
        self.assertRegex(
            html,
            r'<a\s+href="/(?:[a-z]{2}(?:-[A-Z]{2})?/)?shop"\s+class="[^"]*\bbtn-primary\b[^"]*"[^>]*>\s*Discover the selection\s*</a>',
        )
        self.assertNotIn(
            'Votre panier est vide. Découvrez nos produits créoles sélectionnés.',
            html,
        )
