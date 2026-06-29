# -*- coding: utf-8 -*-
"""Recette-U3 — Shop → fiche produit → panier (produit témoin Manio Crackers)."""

import re
import time

from odoo.tests import tagged
from odoo.tests.common import HttpCase

from odoo.addons.dorevia_ck_marketone_content.catalog_manioc_variants import (
    MANIO_CRACKERS_PARENT_NAME,
)
from odoo.addons.dorevia_ck_marketone_content.home_featured import (
    bootstrap_home_featured_products,
)


@tagged('post_install', '-at_install', 'dorevia_ck_recette_u3')
class TestCkRecetteU3(HttpCase):
    FR_HEADERS = {'Accept-Language': 'fr-FR,fr;q=0.9'}

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.website = cls.env['website'].get_current_website()
        cls.product = cls.env['product.template'].sudo().search([
            ('name', '=', MANIO_CRACKERS_PARENT_NAME),
            ('is_published', '=', True),
            ('website_published', '=', True),
        ], limit=1)
        if not cls.product:
            raise cls.skipTest('Produit témoin Manio Crackers absent ou non publié.')
        cls.variant = cls.product.product_variant_id
        bootstrap_home_featured_products(cls.env)

    def _open(self, path):
        response = self.url_open(path, headers=self.FR_HEADERS)
        self.assertEqual(response.status_code, 200, path)
        return response.text

    def _header_nav(self, html):
        match = re.search(r'<header[^>]*id="top"[^>]*>(.*?)</header>', html, re.S)
        self.assertTrue(match, 'header#top introuvable')
        return match.group(1)

    def _cart_count(self, nav_html):
        badges = re.findall(
            r'<sup[^>]*class="[^"]*my_cart_quantity[^"]*"[^>]*>(\d+)</sup>',
            nav_html,
        )
        return max((int(v) for v in badges), default=0) if badges else 0

    def _wish_count(self, nav_html):
        badges = re.findall(
            r'<sup[^>]*class="[^"]*my_wish_quantity[^"]*"[^>]*>(\d+)</sup>',
            nav_html,
        )
        return max((int(v) for v in badges), default=0) if badges else 0

    def _manio_shop_card(self, html):
        grid_start = html.find('o_wsale_products_grid')
        self.assertGreater(grid_start, 0, 'D1 — grille shop absente')
        grid = html[grid_start:grid_start + 400000]
        idx = grid.find(MANIO_CRACKERS_PARENT_NAME)
        self.assertGreater(idx, 0, 'D1 — Manio Crackers absent de /shop')
        window = grid[max(0, idx - 12000):idx + 8000]
        rel = idx - max(0, idx - 12000)
        for marker in ('ck-product-card--shop', 'oe_product_cart'):
            start = window.rfind(marker, 0, rel)
            if start >= 0:
                return window[start:]
        self.fail('Card shop Manio introuvable')

    # --- Scénario D : Shop → grille ---

    def test_d1_shop_grid_loads(self):
        html = self._open('/shop?qa_ts=recette_u3_d1')
        self.assertIn('o_wsale_products_grid', html)
        self.assertIn('ck-product-card--shop', html)
        self._manio_shop_card(html)

    def test_d2_shop_cards_have_price_and_image(self):
        chunk = self._manio_shop_card(self._open('/shop?qa_ts=recette_u3_d2'))
        self.assertIn('ck-product-card__image', chunk)
        self.assertIn('ck-product-card__price', chunk)
        self.assertRegex(chunk, r'oe_product_image_img|ck-product-card__image')
        self.assertRegex(chunk, r'oe_currency_value|ck-product-card__price')

    def test_d3_shop_card_parity_with_home_canon(self):
        shop_chunk = self._manio_shop_card(self._open('/shop?qa_ts=recette_u3_d3'))
        for marker in (
            'ck-product-card__title',
            'ck-product-card__meta',
            'ck-product-card__foot',
            'card-cart-cta',
            'Ajouter au panier',
        ):
            self.assertIn(marker, shop_chunk, f'D3 — {marker} manquant sur card shop')
        home = self._open('/?qa_ts=recette_u3_d3_home')
        self.assertIn(MANIO_CRACKERS_PARENT_NAME, home)
        self.assertIn('ck-product-card--home', home)

    def test_d4_shop_default_sort_present(self):
        html = self._open('/shop?qa_ts=recette_u3_d4')
        self.assertTrue(
            'website_sale_sort' in html or 'o_wsale_products_main_row' in html,
            'D4 — contrôle tri shop absent',
        )
        self.assertGreater(html.count('ck-product-card--shop'), 0)

    # --- Scénario E : Shop → fiche ---

    def test_e1_navigate_product_page_from_shop(self):
        t0 = time.monotonic()
        html = self._open(f'{self.product.website_url}?qa_ts=recette_u3_e1')
        elapsed = time.monotonic() - t0
        self.assertLess(elapsed, 3.0, 'E1 — chargement fiche > 3s')
        self.assertIn(MANIO_CRACKERS_PARENT_NAME, html)

    def test_e2_product_page_u2_checks(self):
        """B1-B5 U2 — prix, producteur, réassurance stock/livraison, galerie."""
        html = self._open(f'{self.product.website_url}?qa_ts=recette_u3_e2')
        self.assertIn('ck-product-purchase__title', html)
        self.assertRegex(html, r'oe_currency_value|product_price')
        if self.product.ck_producer_id:
            self.assertIn(self.product.ck_producer_id.name, html)
        self.assertIn('En stock — expédié depuis Nantes', html)
        self.assertIn('Livraison suivie 2 à 3 jours ouvrables', html)
        self.assertIn('ck-product-layout__gallery', html)
        self.assertTrue(
            'product_detail_img' in html or 'o-carousel-product' in html,
            'B5 — galerie produit absente',
        )

    # --- Scénario F : Fiche → panier ---

    def test_f1_f3_add_to_cart_updates_badge(self):
        self.authenticate(None, None)
        self.make_jsonrpc_request('/shop/cart/add', {
            'product_template_id': self.product.id,
            'product_id': self.variant.id,
            'quantity': 1,
        })
        html = self._open(f'{self.product.website_url}?qa_ts=recette_u3_f')
        nav = self._header_nav(html)
        self.assertGreaterEqual(self._cart_count(nav), 1, 'F2 — badge panier non incrémenté')
        self.assertIn('id="top_menu"', html)

    # --- Scénario G : Cross-page persistance ---

    def test_g1_cart_badge_stable_on_shop_return(self):
        self.authenticate(None, None)
        self.make_jsonrpc_request('/shop/cart/add', {
            'product_template_id': self.product.id,
            'product_id': self.variant.id,
            'quantity': 1,
        })
        shop_html = self._open('/shop?qa_ts=recette_u3_g1')
        self.assertGreaterEqual(
            self._cart_count(self._header_nav(shop_html)), 1,
            'G1 — badge panier à 0 sur retour /shop',
        )
        reload_html = self._open('/shop?qa_ts=recette_u3_g1_reload')
        self.assertGreaterEqual(
            self._cart_count(self._header_nav(reload_html)), 1,
            'G1 — flash compteur panier au reload /shop',
        )

    def test_g2_wishlist_badge_stable_on_shop_return(self):
        self.authenticate(None, None)
        self.make_jsonrpc_request('/shop/wishlist/add', {
            'product_id': self.variant.id,
        })
        shop_html = self._open('/shop?qa_ts=recette_u3_g2')
        self.assertGreaterEqual(
            self._wish_count(self._header_nav(shop_html)), 1,
            'G2 — badge favoris à 0 sur retour /shop',
        )

    def test_g3_mobile_grid_responsive_markup(self):
        html = self._open('/shop?qa_ts=recette_u3_g3')
        self.assertIn('viewport', html)
        chunk = self._manio_shop_card(html)
        self.assertIn('ck-product-card__title', chunk)
        self.assertNotIn('card-cart-cta__label visually-hidden', chunk)
        self.assertRegex(html, r'g-col-6|col-6|o_wsale_products_grid')
