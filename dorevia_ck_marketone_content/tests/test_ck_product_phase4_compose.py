# -*- coding: utf-8 -*-
"""Tests HTTP Phase 4 — fiche produit portable (dorevia_ck_theme)."""

import re

from odoo.tests import tagged
from odoo.tests.common import HttpCase

from odoo.addons.dorevia_ck_marketone_content.hooks import bootstrap_published_products


@tagged('post_install', '-at_install', 'dorevia_ck_theme_phase4')
class TestCkProductPhase4Compose(HttpCase):
    FR_HEADERS = {'Accept-Language': 'fr-FR,fr;q=0.9'}

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        bootstrap_published_products(cls.env)
        cls.product = cls.env['product.template'].search(
            [('is_published', '=', True), ('sale_ok', '=', True)],
            limit=1,
        )
        if not cls.product:
            cls.product = cls.env['product.template'].create({
                'name': 'CK Theme Phase 4 Recette',
                'type': 'consu',
                'list_price': 9.9,
                'sale_ok': True,
                'is_published': True,
            })
            bootstrap_published_products(cls.env)
        cat = cls.env['product.public.category'].search([('name', 'ilike', 'épicerie')], limit=1)
        if cat:
            cls.product.write({'public_categ_ids': [(4, cat.id)]})

    def _open_fr(self, url):
        return self.url_open(url, headers=self.FR_HEADERS)

    def test_module_product_compose_view_installed(self):
        view = self.env['ir.ui.view'].search([
            ('key', '=', 'dorevia_ck_theme.product_ck_compose'),
        ], limit=1)
        self.assertTrue(view, 'Vue portable Phase 4 absente — -u dorevia_ck_theme requis.')

    def test_product_page_http_200(self):
        url = self.product.website_url
        self.assertTrue(url)
        self.assertEqual(self._open_fr(url).status_code, 200)

    def test_product_page_native_purchase_block(self):
        html = self._open_fr(self.product.website_url).text
        self.assertIn('ck-product-page', html)
        self.assertIn('id="add_to_cart"', html)
        self.assertIn('o_wsale_product_page', html)
        self.assertRegex(html, r'product_price|o_wsale_product_details_content_section_price')

    def test_product_page_lot1_layout(self):
        html = self._open_fr(self.product.website_url).text
        self.assertIn('ck-product-layout', html)
        self.assertIn('ck-product-layout__gallery', html)
        self.assertIn('ck-product-layout__buy', html)
        self.assertIn('ck-product-purchase', html)
        self.assertIn('ck-product-purchase__title', html)

    def test_product_page_lot1_french_cta(self):
        html = self._open_fr(self.product.website_url).text
        self.assertIn('Ajouter au panier', html)
        self.assertIn('ck-product-purchase__cart-btn', html)

    def test_product_page_lot1_reassurance(self):
        html = self._open_fr(self.product.website_url).text
        self.assertIn('ck-product-purchase__trust', html)
        self.assertIn('Livraison suivie · 2 à 3 jours ouvrables', html)
        self.assertIn('Conditions générales', html)

    def test_product_page_metadata_line_when_available(self):
        from odoo.addons.dorevia_ck_marketone_content.home_featured import (
            _get_featured_card_metadata_line,
        )
        website = self.env['website'].get_current_website()
        variant = self.product.product_variant_id
        expected = _get_featured_card_metadata_line(self.env, website, variant)
        if not expected:
            self.skipTest('Produit sans métadonnées card.')
        html = self._open_fr(self.product.website_url).text
        self.assertIn('ck-product-purchase__meta', html)
        self.assertIn(expected, html)

    def test_product_page_phase4_compose(self):
        html = self._open_fr(self.product.website_url).text
        self.assertIn('ck-product-page__pro-gateway', html)
        self.assertIn('href="/professionnels"', html)
        self.assertIn('Espace professionnel CK', html)

    def test_product_description_when_bootstrapped(self):
        if 'Confiture' not in (self.product.name or ''):
            self.product.write({'name': 'Confiture de goyave'})
            bootstrap_published_products(self.env)
        html = self._open_fr(self.product.website_url).text
        self.assertIn('ck-product-page__complement', html)
        self.assertIn('Découvrir', html)
        self.assertIn('Origine &amp; usage', html)
        self.assertIn('Conservation', html)
        self.assertNotIn('ck-product-enrich', html)
        self.assertNotIn('id="product_full_description"', html)

    def test_product_page_lot2_b2b_gateway(self):
        html = self._open_fr(self.product.website_url).text
        self.assertIn('ck-product-page__pro-gateway', html)
        self.assertIn('Espace professionnel CK', html)
        self.assertNotIn('s_ck_product_pro_signal', html)

    def test_product_page_lot1_intact_with_lot2(self):
        html = self._open_fr(self.product.website_url).text
        self.assertIn('ck-product-layout', html)
        self.assertIn('ck-product-purchase__cart-btn', html)

    def test_product_category_chips_when_assigned(self):
        if not self.product.public_categ_ids:
            self.skipTest('Produit sans catégorie e-commerce.')
        html = self._open_fr(self.product.website_url).text
        self.assertIn('ck-product-purchase__chips', html)
        self.assertIn('ck-chip', html)

    def test_cart_page_http_200(self):
        self.assertEqual(self._open_fr('/shop/cart').status_code, 200)

    def test_shop_phase3_intact(self):
        html = self._open_fr('/shop').text
        self.assertIn('ck-shop-intro--title-only', html)

    def test_home_no_product_pro_signal(self):
        html = self._open_fr('/').text
        self.assertNotIn('ck-product-pro-signal', html)
        self.assertIn('ck-featured-products__grid--stable', html)

    def test_no_producer_link_without_cms_target(self):
        html = self._open_fr(self.product.website_url).text
        self.assertNotIn('fiche-producteur', html)
        self.assertNotIn('/producteur/', html)
