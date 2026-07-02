# -*- coding: utf-8 -*-
"""Tests hooks Lot 5 — éditorial bas de page home."""

from odoo.tests import tagged
from odoo.tests.common import TransactionCase

from odoo.addons.dorevia_ck_marketone_content.home_editorial import (
    EDITORIAL_LINK_A_PROPOS,
    EDITORIAL_LINK_PRODUCER,
    EDITORIAL_LINK_RECIPES,
    EDITORIAL_SECTION_MARKER,
    EDITORIAL_TITLE,
    bootstrap_home_editorial,
    build_home_editorial_arch,
    editorial_home_arch_is_valid,
)


@tagged('post_install', '-at_install', 'dorevia_ck_marketone_home_lot5')
class TestCkHomeLot5Hooks(TransactionCase):
    def _homepage_arch(self):
        page = self.env['website.page'].search([('url', '=', '/')], limit=1)
        self.assertTrue(page)
        arch = page.view_id.arch_db
        if isinstance(arch, dict):
            arch = next(iter(arch.values()))
        return arch

    def test_build_home_editorial_arch_markers(self):
        arch = build_home_editorial_arch()
        self.assertIn(EDITORIAL_SECTION_MARKER, arch)
        self.assertIn(EDITORIAL_TITLE, arch)
        self.assertIn(f'href="{EDITORIAL_LINK_A_PROPOS}"', arch)
        self.assertIn(f'href="{EDITORIAL_LINK_PRODUCER}"', arch)
        self.assertIn(f'href="{EDITORIAL_LINK_RECIPES}"', arch)
        self.assertNotIn('Inspiration réf.', arch)

    def test_bootstrap_injects_editorial_block(self):
        self.assertTrue(bootstrap_home_editorial(self.env))
        arch = self._homepage_arch()
        self.assertTrue(editorial_home_arch_is_valid(arch))

    def test_bootstrap_order_after_dual(self):
        bootstrap_home_editorial(self.env)
        arch = self._homepage_arch()
        self.assertLess(arch.find('ck-dual-engage'), arch.find(EDITORIAL_SECTION_MARKER))

    def test_bootstrap_idempotent(self):
        bootstrap_home_editorial(self.env)
        arch_before = self._homepage_arch()
        bootstrap_home_editorial(self.env)
        self.assertEqual(arch_before, self._homepage_arch())

    def test_lot2_lot3_lot4_non_regression(self):
        bootstrap_home_editorial(self.env)
        arch = self._homepage_arch()
        self.assertIn('ck-featured-products__grid--stable', arch)
        self.assertIn('ck-discovery-pack', arch)
        self.assertIn('ck-dual-engage--pro-only', arch)
        self.assertNotIn('s_ck_pro_banner', arch)
