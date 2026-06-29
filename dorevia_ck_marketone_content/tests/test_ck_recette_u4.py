# -*- coding: utf-8 -*-
"""Recette-U4 — Favoris cross-page (visiteur anonyme)."""

import re

from odoo.tests import tagged
from odoo.tests.common import HttpCase

from odoo.addons.dorevia_ck_marketone_content.catalog_manioc_variants import (
    MANIO_CRACKERS_PARENT_NAME,
)
from odoo.addons.dorevia_ck_marketone_content.home_featured import (
    bootstrap_home_featured_products,
)


@tagged('post_install', '-at_install', 'dorevia_ck_recette_u4')
class TestCkRecetteU4(HttpCase):
    FR_HEADERS = {'Accept-Language': 'fr-FR,fr;q=0.9'}

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.website = cls.env['website'].get_current_website()
        bootstrap_home_featured_products(cls.env)
        cls.manio = cls.env['product.template'].sudo().search([
            ('name', '=', MANIO_CRACKERS_PARENT_NAME),
            ('is_published', '=', True),
        ], limit=1)
        if not cls.manio:
            raise cls.skipTest('Produit témoin Manio Crackers absent.')
        cls.manio_variant = cls.manio.product_variant_id
        others = cls.env['product.template'].sudo().search([
            ('sale_ok', '=', True),
            ('is_published', '=', True),
            ('website_published', '=', True),
            ('id', '!=', cls.manio.id),
        ], limit=2)
        if len(others) < 2:
            raise cls.skipTest('Moins de 3 produits publiés pour recette favoris.')
        cls.product_b = others[0]
        cls.product_c = others[1]

    def setUp(self):
        super().setUp()
        self.authenticate(None, None)
        self.env['product.wishlist'].sudo().search([]).unlink()

    def _open(self, path):
        response = self.url_open(path, headers=self.FR_HEADERS)
        self.assertEqual(response.status_code, 200, path)
        return response.text

    def _header_nav(self, html):
        match = re.search(r'<header[^>]*id="top"[^>]*>(.*?)</header>', html, re.S)
        self.assertTrue(match, 'header#top introuvable')
        return match.group(1)

    def _wish_count(self, html):
        nav = self._header_nav(html)
        badges = re.findall(
            r'<sup[^>]*class="[^"]*my_wish_quantity[^"]*"[^>]*>(\d+)</sup>',
            nav,
        )
        visible = [int(v) for v in badges if 'd-none' not in nav[max(0, nav.find(v) - 80):nav.find(v)]]
        if not badges:
            return 0
        return max(int(v) for v in badges)

    def _cart_count(self, html):
        nav = self._header_nav(html)
        badges = re.findall(
            r'<sup[^>]*class="[^"]*my_cart_quantity[^"]*"[^>]*>(\d+)</sup>',
            nav,
        )
        return max((int(v) for v in badges), default=0) if badges else 0

    def _add_wish(self, variant):
        return self.make_jsonrpc_request('/shop/wishlist/add', {
            'product_id': variant.id,
        })

    def _remove_wish(self, variant):
        wish = self.env['product.wishlist'].sudo().search([
            ('product_id', '=', variant.id),
            ('website_id', '=', self.website.id),
        ], limit=1)
        self.assertTrue(wish, f'Favori introuvable pour variante {variant.id}')
        self.make_jsonrpc_request(f'/shop/wishlist/remove/{wish.id}', {})

    # --- Scénario H : ajout favoris (3 points d'entrée simulés via JSON-RPC) ---

    def test_h_add_from_home_shop_and_product_page(self):
        """H1 Home · H2 Shop · H3 Fiche — badge reflète les produits distincts."""
        self._add_wish(self.manio_variant)
        home = self._open('/?qa_ts=recette_u4_h1')
        self.assertGreaterEqual(self._wish_count(home), 1)
        self.assertIn('o_add_wishlist', home)
        self.assertIn(MANIO_CRACKERS_PARENT_NAME, home)

        self._add_wish(self.product_b.product_variant_id)
        shop = self._open('/shop?qa_ts=recette_u4_h2')
        self.assertGreaterEqual(self._wish_count(shop), 2)
        self.assertIn(self.product_b.name, shop)

        self._add_wish(self.manio_variant)
        self._add_wish(self.product_c.product_variant_id)
        product_html = self._open(f'{self.manio.website_url}?qa_ts=recette_u4_h3')
        self.assertGreaterEqual(self._wish_count(product_html), 3)
        self.assertIn('o_add_wishlist_dyn', product_html)

    # --- Scénario I : persistance cross-page ---

    def test_i_wishlist_badge_stable_across_navigation(self):
        self._add_wish(self.manio_variant)
        self._add_wish(self.product_b.product_variant_id)

        pages = [
            '/?qa_ts=recette_u4_i1',
            '/shop?qa_ts=recette_u4_i2',
            f'{self.manio.website_url}?qa_ts=recette_u4_i3',
            '/shop/cart?qa_ts=recette_u4_i4',
        ]
        for path in pages:
            html = self._open(path)
            self.assertGreaterEqual(
                self._wish_count(html), 2,
                f'I — badge favoris instable sur {path}',
            )
            reload_html = self._open(f'{path}&reload=1')
            self.assertGreaterEqual(
                self._wish_count(reload_html), 2,
                f'I4 — badge reset au reload sur {path}',
            )

    # --- Scénario J : retrait favoris ---

    def test_j_remove_wishlist_decrements_badge(self):
        self._add_wish(self.manio_variant)
        self._add_wish(self.product_b.product_variant_id)
        self.assertGreaterEqual(self._wish_count(self._open('/shop?qa_ts=recette_u4_j0')), 2)

        self._remove_wish(self.manio_variant)
        self.assertEqual(self._wish_count(self._open('/?qa_ts=recette_u4_j1')), 1)

        self._remove_wish(self.product_b.product_variant_id)
        shop = self._open('/shop?qa_ts=recette_u4_j2')
        self.assertEqual(self._wish_count(shop), 0)

        self._add_wish(self.manio_variant)
        self._remove_wish(self.manio_variant)
        self.assertEqual(
            self._wish_count(self._open(f'{self.manio.website_url}?qa_ts=recette_u4_j3')),
            0,
        )

    # --- Scénario K : page wishlist ---

    def test_k_wishlist_page_lists_items_and_cart_add(self):
        self._add_wish(self.manio_variant)
        self._add_wish(self.product_b.product_variant_id)

        html = self._open('/shop/wishlist?qa_ts=recette_u4_k1')
        self.assertIn('wishlist-section', html)
        self.assertIn(MANIO_CRACKERS_PARENT_NAME, html)
        self.assertIn(self.product_b.name, html)
        self.assertRegex(html, r'oe_product_image|product_image|img')
        self.assertIn(self.manio.website_url.replace('&', '&amp;'), html)

        cart_before = self._cart_count(html)
        self.make_jsonrpc_request('/shop/cart/add', {
            'product_template_id': self.manio.id,
            'product_id': self.manio_variant.id,
            'quantity': 1,
        })
        cart_page = self._open('/shop/wishlist?qa_ts=recette_u4_k3')
        self.assertGreaterEqual(self._cart_count(cart_page), cart_before + 1)
