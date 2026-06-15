# -*- coding: utf-8 -*-
"""Tests hooks V1 Hero / Lot 1 — rapprochement maquette."""

from odoo.tests import tagged
from odoo.tests.common import TransactionCase

from xml.sax.saxutils import escape

from odoo.addons.dorevia_ck_marketone_content.home_hero import (
    HERO_CTA_PRO_LABEL,
    HERO_CTA_SHOP_LABEL,
    HERO_KICKER,
    HERO_TITLE,
    HERO_VARIANT_MARKER,
    bootstrap_home_hero,
    build_home_hero_arch,
    hero_home_arch_is_valid,
)


@tagged('post_install', '-at_install', 'dorevia_ck_marketone_home_lot1')
class TestCkHomeLot1Hooks(TransactionCase):
    def _homepage_arch(self):
        page = self.env['website.page'].search([('url', '=', '/')], limit=1)
        self.assertTrue(page)
        arch = page.view_id.arch_db
        if isinstance(arch, dict):
            arch = next(iter(arch.values()))
        return arch

    def test_build_home_hero_arch_markers(self):
        arch = build_home_hero_arch(self.env)
        self.assertIn(HERO_VARIANT_MARKER, arch)
        self.assertIn(HERO_TITLE, arch)
        self.assertIn(escape(HERO_KICKER), arch)
        self.assertIn('href="/shop"', arch)
        self.assertIn(HERO_CTA_SHOP_LABEL, arch)
        self.assertIn('href="/professionnels"', arch)
        self.assertIn(HERO_CTA_PRO_LABEL, arch)
        self.assertNotIn('website.s_cover_default_image', arch)
        self.assertNotIn('ratio-16x10', arch)
        self.assertTrue(
            'ck-hero__visual-media' in arch or 'ck-hero__visual--editorial' in arch
        )

    def test_bootstrap_replaces_hero(self):
        self.assertTrue(bootstrap_home_hero(self.env))
        arch = self._homepage_arch()
        self.assertTrue(hero_home_arch_is_valid(arch))

    def test_bootstrap_hero_before_featured(self):
        bootstrap_home_hero(self.env)
        arch = self._homepage_arch()
        self.assertLess(arch.find(HERO_VARIANT_MARKER), arch.find('ck-featured-products'))

    def test_bootstrap_idempotent(self):
        bootstrap_home_hero(self.env)
        arch_before = self._homepage_arch()
        bootstrap_home_hero(self.env)
        self.assertEqual(arch_before, self._homepage_arch())

    def test_lot2_to_lot5_non_regression(self):
        bootstrap_home_hero(self.env)
        arch = self._homepage_arch()
        self.assertIn('ck-featured-products__grid--stable', arch)
        self.assertIn('ck-discovery-pack', arch)
        self.assertIn('ck-dual-engage--compact', arch)
        self.assertIn('ck-home-editorial', arch)
