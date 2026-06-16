# -*- coding: utf-8 -*-
"""Tests hooks Lot 3 — Coffrets découverte home."""

from odoo.tests import tagged
from odoo.tests.common import TransactionCase

from odoo.addons.dorevia_ck_marketone_content.home_discovery_pack import (
    DISCOVERY_PACK_CTA_URL,
    DISCOVERY_PACK_SECTION_MARKER,
    DISCOVERY_PACK_TITLE,
    bootstrap_home_discovery_pack,
    build_discovery_pack_arch,
    discovery_pack_arch_is_valid,
    get_discovery_pack_product,
)


@tagged('post_install', '-at_install', 'dorevia_ck_marketone_home_lot3')
class TestCkHomeLot3Hooks(TransactionCase):
    def _homepage_arch(self):
        page = self.env['website.page'].search([('url', '=', '/')], limit=1)
        self.assertTrue(page)
        arch = page.view_id.arch_db
        if isinstance(arch, dict):
            arch = next(iter(arch.values()))
        return arch

    def test_build_discovery_pack_arch_markers(self):
        arch = build_discovery_pack_arch(self.env)
        self.assertIn(DISCOVERY_PACK_SECTION_MARKER, arch)
        self.assertIn(DISCOVERY_PACK_TITLE, arch)
        self.assertIn(f'href="{DISCOVERY_PACK_CTA_URL}"', arch)
        self.assertIn('Pack', arch)
        self.assertNotIn('website.s_cover_default_image', arch)

    def test_bootstrap_injects_discovery_block(self):
        from odoo.addons.dorevia_ck_marketone_content.home_univers import bootstrap_home_univers

        bootstrap_home_univers(self.env)
        self.assertTrue(bootstrap_home_discovery_pack(self.env))
        arch = self._homepage_arch()
        self.assertTrue(discovery_pack_arch_is_valid(arch))
        univers_pos = arch.find('ck-univers-cards')
        if univers_pos < 0:
            univers_pos = arch.find('s_ck_category_links')
        pack_pos = arch.find(DISCOVERY_PACK_SECTION_MARKER)
        dual_pos = arch.find('ck-dual-engage')
        self.assertGreater(pack_pos, univers_pos)
        self.assertGreater(dual_pos, pack_pos)

    def test_bootstrap_idempotent(self):
        bootstrap_home_discovery_pack(self.env)
        arch_before = self._homepage_arch()
        bootstrap_home_discovery_pack(self.env)
        arch_after = self._homepage_arch()
        self.assertEqual(arch_before, arch_after)

    def test_get_discovery_pack_product_optional(self):
        product = get_discovery_pack_product(self.env)
        if product:
            self.assertTrue(product.is_published)
            self.assertTrue(product.image_1920)

    def test_lot2_featured_non_regression(self):
        bootstrap_home_discovery_pack(self.env)
        arch = self._homepage_arch()
        self.assertIn('ck-featured-products__grid--stable', arch)
