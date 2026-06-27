# -*- coding: utf-8 -*-
"""Tests HTTP Lot 2 front — empilement vertical + ancres fiche produit CK."""

import re

from odoo.tests import tagged
from odoo.tests.common import HttpCase

from odoo.addons.dorevia_ck_marketone_content.hooks import (
    PRODUCT_WEBSITE_DESCRIPTIONS,
    bootstrap_published_products,
)


@tagged('post_install', '-at_install', 'dorevia_ck_product_page_lot2_front')
class TestCkProductPageLot2Front(HttpCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        bootstrap_published_products(cls.env)
        cls.goyave = cls.env['product.template'].search(
            [('name', 'ilike', 'confiture de goyave')],
            limit=1,
        )
        if not cls.goyave:
            cls.goyave = cls.env['product.template'].create({
                'name': 'Confiture de goyave',
                'type': 'consu',
                'list_price': 5.5,
                'sale_ok': True,
                'is_published': True,
                'website_description': PRODUCT_WEBSITE_DESCRIPTIONS['Confiture de goyave'],
                'description_ecommerce': 'Confiture artisanale — sélection épicerie créole CK.',
            })

    def _open_product(self, product=None):
        product = product or self.goyave
        url = product.website_url
        self.assertTrue(url)
        return self.url_open(url).text

    def _long_zone(self, html):
        start = html.find('ck-product-page__long-zone')
        self.assertGreater(start, 0)
        return html[start:start + 25000]

    def test_long_zone_structure(self):
        html = self._open_product()
        self.assertIn('ck-product-page__complement', html)
        self.assertIn('ck-product-page__long-zone', html)
        self.assertIn('ck-product-page__anchor-nav', html)
        self.assertNotIn('nav-tabs', html)
        self.assertNotIn('role="tablist"', html)
        self.assertNotIn('tab-pane', html)
        self.assertNotIn('À propos de ce produit', html)
        self.assertNotIn('Informations produit', html)

    def test_anchor_links_and_section_ids(self):
        html = self._open_product()
        zone = self._long_zone(html)
        self.assertIn('href="#ck-section-discover"', zone)
        self.assertIn('href="#ck-section-composition"', zone)
        self.assertIn('href="#ck-section-conservation"', zone)
        self.assertIn('id="ck-section-discover"', zone)
        self.assertIn('id="ck-section-composition"', zone)
        self.assertIn('ck-product-page__section--origin_usage', zone)
        self.assertIn('Origine &amp; usage', zone)
        self.assertNotIn('ck-product-enrich', html)

    def test_conservation_panels_visible_in_flow(self):
        html = self._open_product()
        zone = self._long_zone(html)
        self.assertIn('ck-product-page__section-panel', zone)
        self.assertIn('Avant ouverture', zone)
        self.assertIn('Après ouverture', zone)

    def test_no_raw_markdown_asterisks_in_long_zone(self):
        zone = self._long_zone(self._open_product())
        self.assertNotRegex(zone, r'\*Usage\s*:')

    def test_no_duplicate_lead_in_long_zone(self):
        lead = (self.goyave.description_ecommerce or '').strip()
        if not lead:
            self.skipTest('Pas d’accroche e-commerce.')
        zone = self._long_zone(self._open_product())
        self.assertNotIn(lead, zone)

    def test_empty_website_description_no_long_zone(self):
        empty = self.env['product.template'].sudo().create({
            'name': 'CK Long Zone Vide',
            'type': 'consu',
            'list_price': 2.0,
            'sale_ok': True,
            'is_published': True,
            'website_description': False,
            'description_sale': False,
        })
        html = self._open_product(empty)
        self.assertIn('ck-product-layout', html)
        self.assertNotIn('ck-product-page__long-zone', html)
        self.assertNotIn('ck-product-page__anchor-nav', html)

    def test_single_section_hides_anchor_nav(self):
        product = self.env['product.template'].sudo().create({
            'name': 'CK Une seule section',
            'type': 'consu',
            'list_price': 3.0,
            'sale_ok': True,
            'is_published': True,
            'website_description': (
                '<div class="ck-product-enrich">'
                '<h3>Origine &amp; usage</h3><p>Produit simple.</p>'
                '</div>'
            ),
        })
        html = self._open_product(product)
        self.assertIn('ck-product-page__long-zone', html)
        self.assertNotIn('ck-product-page__anchor-nav', html)

    def test_details_block_specs(self):
        product = self.goyave.sudo()
        product.write({
            'ck_net_quantity': 320,
            'ck_net_quantity_uom_id': self.env['dorevia.ck.card.uom'].sudo().search(
                [('code', '=', 'g')], limit=1,
            ).id,
            'ck_reference_price_uom_id': self.env['dorevia.ck.card.uom'].sudo().search(
                [('code', '=', 'kg')], limit=1,
            ).id,
            'ck_show_reference_price': True,
        })
        html = self._open_product(product)
        self.assertIn('id="ck-section-practical"', html)
        self.assertIn('Infos pratiques', html)
        self.assertIn('ck-product-page__specs', html)
        self.assertIn('Contenance', html)

    def test_public_user_product_page_with_ck_uom(self):
        product = self.goyave.sudo()
        product.write({
            'ck_net_quantity': 320,
            'ck_net_quantity_uom_id': self.env['dorevia.ck.card.uom'].sudo().search(
                [('code', '=', 'g')], limit=1,
            ).id,
            'ck_reference_price_uom_id': self.env['dorevia.ck.card.uom'].sudo().search(
                [('code', '=', 'kg')], limit=1,
            ).id,
            'ck_show_reference_price': True,
        })
        self.authenticate(None, None)
        response = self.url_open(product.website_url)
        self.assertEqual(response.status_code, 200, response.text[:500])
        self.assertNotIn('403', response.text)
        self.assertIn('ck-product-page__long-zone', response.text)

    def test_pro_gateway_discreet(self):
        html = self._open_product()
        self.assertIn('ck-product-page__pro-gateway', html)
        self.assertIn('Espace professionnel CK', html)
        self.assertNotIn('ck-product-pro-signal', html)

    def test_native_specs_hidden_when_long_zone(self):
        html = self._open_product()
        self.assertNotIn('id="product_full_spec"', html)

    def test_lot1_zone_haute_non_regression(self):
        html = self._open_product()
        self.assertIn('ck-product-layout', html)
        self.assertIn('ck-product-purchase__title', html)
        self.assertIn('ck-product-purchase__cart-btn', html)
        self.assertIn('Ajouter au panier', html)

    def test_shop_and_home_cards_non_regression(self):
        shop = self.url_open('/shop').text
        self.assertIn('ck-product-card--shop', shop)
        home = self.url_open('/').text
        self.assertIn('ck-product-card--home', home)

    def test_composition_block_when_ingredients(self):
        product = self.env['product.template'].sudo().create({
            'name': 'CK Ingrédients ancre',
            'type': 'consu',
            'list_price': 4.0,
            'sale_ok': True,
            'is_published': True,
            'website_description': (
                '<div class="ck-product-enrich">'
                '<h3>Ingrédients &amp; allergènes</h3>'
                '<p>Goyave, sucre.</p>'
                '</div>'
            ),
        })
        html = self._open_product(product)
        self.assertIn('id="ck-section-composition"', html)
        self.assertIn('ck-product-page__section--ingredients', html)
