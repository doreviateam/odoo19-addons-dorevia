# -*- coding: utf-8 -*-
"""Recette Wishlist-U1 — compteur header visiteur après refresh."""

import re

from odoo.tests import tagged
from odoo.tests.common import HttpCase


@tagged('post_install', '-at_install', 'dorevia_ck_wishlist_u1')
class TestCkWishlistU1(HttpCase):
    FR_HEADERS = {'Accept-Language': 'fr-FR,fr;q=0.9'}

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.website = cls.env['website'].get_current_website()
        cls.product = cls.env['product.template'].sudo().search([
            ('sale_ok', '=', True),
            ('is_published', '=', True),
            ('website_published', '=', True),
        ], limit=1)
        if not cls.product:
            raise cls.skipTest('Aucun produit publié pour recette wishlist.')
        cls.variant = cls.product.product_variant_id

    def _header_nav(self, html):
        match = re.search(r'<header[^>]*id="top"[^>]*>(.*?)</header>', html, re.S)
        self.assertTrue(match, 'header#top introuvable')
        return match.group(1)

    def _assert_wish_count_in_nav(self, nav_html, expected):
        badges = re.findall(
            r'<sup[^>]*class="[^"]*my_wish_quantity[^"]*"[^>]*>(\d+)</sup>',
            nav_html,
        )
        self.assertTrue(badges, 'Badge my_wish_quantity introuvable dans le header.')
        self.assertTrue(
            any(int(value) == expected for value in badges),
            f'Compteur {expected} attendu, trouvé {badges!r}',
        )

    def test_anonymous_wishlist_header_count_persists_after_reload(self):
        """Scénario A — visiteur : add → refresh → compteur conservé."""
        self.authenticate(None, None)
        self.make_jsonrpc_request(
            '/shop/wishlist/add',
            {'product_id': self.variant.id},
        )

        first_html = self.url_open(
            f'{self.product.website_url}?qa_ts=wishlist_u1',
            headers=self.FR_HEADERS,
        ).text
        self._assert_wish_count_in_nav(self._header_nav(first_html), 1)

        second_html = self.url_open(
            f'{self.product.website_url}?qa_ts=wishlist_u1_reload',
            headers=self.FR_HEADERS,
        ).text
        self._assert_wish_count_in_nav(self._header_nav(second_html), 1)

    def test_anonymous_wishlist_remove_resets_counter_after_reload(self):
        self.authenticate(None, None)
        self.make_jsonrpc_request(
            '/shop/wishlist/add',
            {'product_id': self.variant.id},
        )
        wish = self.env['product.wishlist'].sudo().search([
            ('product_id', '=', self.variant.id),
            ('website_id', '=', self.website.id),
            ('partner_id', '=', False),
        ], order='id desc', limit=1)
        self.assertTrue(wish)
        self.make_jsonrpc_request(
            f'/shop/wishlist/remove/{wish.id}',
            {},
        )

        html = self.url_open(
            '/shop?qa_ts=wishlist_u1_removed',
            headers=self.FR_HEADERS,
        ).text
        nav = self._header_nav(html)
        badges = re.findall(
            r'<sup[^>]*class="[^"]*my_wish_quantity[^"]*"[^>]*>(\d+)</sup>',
            nav,
        )
        self.assertTrue(all(int(value) == 0 for value in badges), badges)

    def test_logged_user_wishlist_header_count_after_reload(self):
        """Scénario B — connecté : non-régression (page /shop, évite ACL fiche produit)."""
        portal_group = self.env.ref('base.group_portal')
        website_editor = self.env.ref('website.group_website_designer')
        partner = self.env['res.partner'].sudo().create({
            'name': 'QA Wishlist-U1',
            'email': 'qa-wishlist-u1@example.test',
        })
        self.env['res.users'].sudo().create({
            'name': 'QA Wishlist-U1',
            'login': 'qa_wishlist_u1@example.test',
            'password': 'qa_wishlist_u1',
            'partner_id': partner.id,
            'group_ids': [(6, 0, [portal_group.id, website_editor.id])],
        })
        self.authenticate('qa_wishlist_u1@example.test', 'qa_wishlist_u1')
        self.make_jsonrpc_request(
            '/shop/wishlist/add',
            {'product_id': self.variant.id},
        )

        html = self.url_open(
            '/shop?qa_ts=wishlist_u1_logged',
            headers=self.FR_HEADERS,
        ).text
        self._assert_wish_count_in_nav(self._header_nav(html), 1)

        reload_html = self.url_open(
            '/shop?qa_ts=wishlist_u1_logged_reload',
            headers=self.FR_HEADERS,
        ).text
        self._assert_wish_count_in_nav(self._header_nav(reload_html), 1)
