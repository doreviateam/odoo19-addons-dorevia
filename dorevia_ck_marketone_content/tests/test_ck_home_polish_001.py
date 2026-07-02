# -*- coding: utf-8 -*-
"""Tests CK-HOME-POLISH-001 — newsletter neutralisée · bloc Pro home."""

import re

from odoo.tests import tagged
from odoo.tests.common import HttpCase, TransactionCase

from odoo.addons.dorevia_ck_marketone_content.home_dual_engage import (
    bootstrap_home_dual_engage,
    build_home_dual_engage_arch,
    dual_engage_home_arch_is_valid,
)
from odoo.addons.dorevia_ck_marketone_content.hooks import (
    PRO_DUAL_CTA_DEFAULT,
    PRO_DUAL_LEAD,
    PRO_DUAL_TITLE,
)


@tagged('post_install', '-at_install', 'dorevia_ck_home_polish_001')
class TestCkHomePolish001Hooks(TransactionCase):
    def test_build_home_pro_arch_without_newsletter(self):
        arch = build_home_dual_engage_arch(self.env)
        self.assertIn('ck-dual-engage--pro-only', arch)
        self.assertIn(PRO_DUAL_TITLE, arch)
        self.assertIn(PRO_DUAL_LEAD[:30], arch)
        self.assertIn(PRO_DUAL_CTA_DEFAULT, arch)
        self.assertNotIn('ck-newsletter-subscribe', arch)
        self.assertNotIn('s_newsletter_subscribe_form', arch)
        self.assertNotIn('Merci pour votre inscription', arch)

    def test_bootstrap_replaces_stale_newsletter_dual(self):
        page = self.env['website.page'].search([('url', '=', '/')], limit=1)
        self.assertTrue(page)
        arch = page.view_id.arch_db
        if isinstance(arch, dict):
            arch = next(iter(arch.values()))
        stale = arch.replace(
            'ck-dual-engage--pro-only',
            'ck-dual-engage--compact',
            1,
        )
        if stale == arch:
            stale = arch + '<div id="ck-newsletter-subscribe">Merci pour votre inscription !</div>'
        page.view_id.write({'arch_db': stale})
        self.assertFalse(dual_engage_home_arch_is_valid(stale, self.env))

        self.assertTrue(bootstrap_home_dual_engage(self.env))
        refreshed = page.view_id.arch_db
        if isinstance(refreshed, dict):
            refreshed = next(iter(refreshed.values()))
        self.assertTrue(dual_engage_home_arch_is_valid(refreshed, self.env))
        self.assertNotIn('Merci pour votre inscription', refreshed)


@tagged('post_install', '-at_install', 'dorevia_ck_home_polish_001')
class TestCkHomePolish001Compose(HttpCase):
    FR_HEADERS = {'Accept-Language': 'fr-FR,fr;q=0.9'}

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        bootstrap_home_dual_engage(cls.env)

    def _open_fr_home(self):
        return self.url_open('/', headers=self.FR_HEADERS)

    def test_home_no_newsletter_message_or_form(self):
        html = self._open_fr_home().text
        self.assertNotIn('Merci pour votre inscription', html)
        self.assertNotIn('ck-newsletter-subscribe', html)
        self.assertNotIn('s_newsletter_subscribe_form', html)

    def test_home_pro_block_present(self):
        html = self._open_fr_home().text
        self.assertIn('ck-dual-engage--pro-only', html)
        self.assertIn(PRO_DUAL_TITLE, html)
        self.assertIn('href="/professionnels"', html)

    def test_header_wishlist_and_cart_icons_distinct(self):
        html = self._open_fr_home().text
        match = re.search(r'<header[^>]*id="top"[^>]*>(.*?)</header>', html, re.S)
        self.assertTrue(match)
        nav = match.group(1)
        self.assertIn('fa-heart', nav)
        self.assertIn('fa-shopping-cart', nav)
        self.assertIn('/shop/wishlist', nav)
        self.assertIn('/shop/cart', nav)

    def test_header_empty_badges_hidden(self):
        html = self._open_fr_home().text
        match = re.search(r'<header[^>]*id="top"[^>]*>(.*?)</header>', html, re.S)
        self.assertTrue(match)
        nav = match.group(1)
        wish_badges = re.findall(
            r'<sup[^>]*class="[^"]*my_wish_quantity[^"]*"[^>]*>\s*0\s*</sup>',
            nav,
        )
        cart_badges = re.findall(
            r'<sup[^>]*class="[^"]*my_cart_quantity[^"]*"[^>]*>\s*0\s*</sup>',
            nav,
        )
        self.assertEqual(wish_badges, [])
        self.assertEqual(cart_badges, [])
