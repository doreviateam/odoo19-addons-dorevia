# -*- coding: utf-8 -*-
"""Tests hooks V1 Hero / Lot 1 — rapprochement maquette."""

from odoo.tests import tagged
from odoo.tests.common import TransactionCase

from xml.sax.saxutils import escape

from odoo.addons.dorevia_ck_marketone_content.home_hero import (
    HERO_CAROUSEL_INTERVAL_MS,
    HERO_CAROUSEL_MARKER,
    HERO_CTA_PRODUCTEURS_LABEL,
    HERO_CTA_SHOP_LABEL,
    HERO_EDITABLE_MEDIA_MARKER,
    HERO_KICKER,
    HERO_SLIDE_SNIPPET,
    HERO_TITLE,
    HERO_VARIANT_MARKER,
    HERO_VISUAL_MAX_SLIDES,
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
        self.assertIn('href="/producteurs"', arch)
        self.assertIn(HERO_CTA_PRODUCTEURS_LABEL, arch)
        self.assertNotIn('website.s_cover_default_image', arch)
        self.assertIn('ck-hero__grid', arch)
        self.assertIn(HERO_CAROUSEL_MARKER, arch)
        self.assertIn(f'data-bs-interval="{HERO_CAROUSEL_INTERVAL_MS}"', arch)
        self.assertIn('ck_hero_home_v1', arch)
        self.assertIn('ck-hero__visual-media', arch)
        self.assertIn(HERO_EDITABLE_MEDIA_MARKER, arch)
        self.assertIn('ck-hero__slide-media o_editable', arch)
        self.assertEqual(arch.count(f'data-snippet="{HERO_SLIDE_SNIPPET}"'), HERO_VISUAL_MAX_SLIDES)
        self.assertGreaterEqual(arch.count('carousel-item'), 1)
        self.assertLessEqual(arch.count('carousel-item'), HERO_VISUAL_MAX_SLIDES)
        content_part = arch.split('ck-hero__visual-col', 1)[0]
        self.assertNotIn('data-bs-ride="carousel"', content_part)

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
