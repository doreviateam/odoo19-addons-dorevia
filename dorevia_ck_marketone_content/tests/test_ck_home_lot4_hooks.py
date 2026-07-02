# -*- coding: utf-8 -*-
"""Tests hooks Lot 4 — dual Pro / Newsletter home."""

import re

from odoo.tests import tagged
from odoo.tests.common import TransactionCase

from odoo.addons.dorevia_ck_marketone_content.home_dual_engage import (
    DUAL_ENGAGE_HOME_DATA_NAME,
    bootstrap_home_dual_engage,
    build_home_dual_engage_arch,
    dual_engage_home_arch_is_valid,
)
from odoo.addons.dorevia_ck_marketone_content.hooks import (
    NEWSLETTER_RGPD_NOTE,
    PRO_DUAL_TITLE,
    bootstrap_newsletter_mailing_list,
)


@tagged('post_install', '-at_install', 'dorevia_ck_marketone_home_lot4')
class TestCkHomeLot4Hooks(TransactionCase):
    def _homepage_arch(self):
        page = self.env['website.page'].search([('url', '=', '/')], limit=1)
        self.assertTrue(page)
        arch = page.view_id.arch_db
        if isinstance(arch, dict):
            arch = next(iter(arch.values()))
        return arch

    def test_build_home_dual_arch_markers(self):
        arch = build_home_dual_engage_arch(self.env)
        self.assertIn('ck-dual-engage--compact', arch)
        self.assertIn(DUAL_ENGAGE_HOME_DATA_NAME, arch)
        self.assertIn(PRO_DUAL_TITLE, arch)
        self.assertIn('href="/professionnels"', arch)
        self.assertIn('ck-newsletter-subscribe', arch)
        mailing_list = bootstrap_newsletter_mailing_list(self.env)
        self.assertIn(f'data-list-id="{mailing_list.id}"', arch)
        self.assertIn("S'inscrire", arch)
        self.assertTrue(re.search(r'placeholder="[^"]*e-mail"', arch, re.I))
        self.assertIn('pt48 pb48', arch)
        self.assertIn('Merci pour votre inscription', arch)
        self.assertNotIn('Thanks for registering', arch)

    def test_bootstrap_replaces_dual_and_removes_pro_banner(self):
        self.assertTrue(bootstrap_home_dual_engage(self.env))
        arch = self._homepage_arch()
        self.assertTrue(dual_engage_home_arch_is_valid(arch, self.env))
        self.assertNotIn('s_ck_pro_banner', arch)
        self.assertIn(NEWSLETTER_RGPD_NOTE, arch)

    def test_bootstrap_order_after_discovery_pack(self):
        bootstrap_home_dual_engage(self.env)
        arch = self._homepage_arch()
        self.assertLess(arch.find('ck-discovery-pack'), arch.find('ck-dual-engage'))

    def test_bootstrap_idempotent(self):
        bootstrap_home_dual_engage(self.env)
        arch_before = self._homepage_arch()
        bootstrap_home_dual_engage(self.env)
        self.assertEqual(arch_before, self._homepage_arch())

    def test_lot2_lot3_non_regression(self):
        bootstrap_home_dual_engage(self.env)
        arch = self._homepage_arch()
        self.assertIn('ck-featured-products__grid--stable', arch)
        self.assertIn('ck-discovery-pack', arch)
