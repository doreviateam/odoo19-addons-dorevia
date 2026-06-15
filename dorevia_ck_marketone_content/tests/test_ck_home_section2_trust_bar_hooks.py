# -*- coding: utf-8 -*-
"""Tests Section 2 — trust-bar réassurance post-Hero."""

from odoo.tests import tagged
from odoo.tests.common import TransactionCase

from odoo.addons.dorevia_ck_marketone_content.home_hero import HERO_VARIANT_MARKER
from odoo.addons.dorevia_ck_marketone_content.home_reassurance import (
    FEATURED_MARKER,
    REASSURANCE_TRUST_BAR_MARKER,
    TRUST_BAR_COPY_MARKER,
    bootstrap_home_reassurance,
    build_home_reassurance_arch,
    reassurance_home_arch_is_valid,
)


@tagged('post_install', '-at_install', 'dorevia_ck_marketone_home_section2')
class TestCkHomeSection2TrustBarHooks(TransactionCase):
    def _homepage_arch(self):
        page = self.env['website.page'].search([('url', '=', '/')], limit=1)
        self.assertTrue(page)
        arch = page.view_id.arch_db
        if isinstance(arch, dict):
            arch = next(iter(arch.values()))
        return arch

    def test_build_home_reassurance_arch_markers(self):
        arch = build_home_reassurance_arch()
        self.assertIn(REASSURANCE_TRUST_BAR_MARKER, arch)
        self.assertIn('ck-reassurance__grid', arch)
        self.assertIn('Livraison France', arch)
        self.assertIn('Europe', arch)
        self.assertIn('Paiement sécurisé', arch)
        self.assertIn('Producteurs sélectionnés', arch)
        self.assertIn(TRUST_BAR_COPY_MARKER, arch)
        self.assertNotIn('parcours checkout natif', arch)

    def test_bootstrap_replaces_reassurance(self):
        self.assertTrue(bootstrap_home_reassurance(self.env))
        arch = self._homepage_arch()
        self.assertTrue(reassurance_home_arch_is_valid(arch))

    def test_bootstrap_order_hero_reassurance_featured(self):
        bootstrap_home_reassurance(self.env)
        arch = self._homepage_arch()
        self.assertLess(arch.find(HERO_VARIANT_MARKER), arch.find(REASSURANCE_TRUST_BAR_MARKER))
        self.assertLess(arch.find(REASSURANCE_TRUST_BAR_MARKER), arch.find(FEATURED_MARKER))

    def test_bootstrap_idempotent(self):
        bootstrap_home_reassurance(self.env)
        arch_before = self._homepage_arch()
        bootstrap_home_reassurance(self.env)
        self.assertEqual(arch_before, self._homepage_arch())

    def test_lot1_to_lot5_non_regression(self):
        bootstrap_home_reassurance(self.env)
        arch = self._homepage_arch()
        self.assertIn(HERO_VARIANT_MARKER, arch)
        self.assertIn('ck-featured-products__grid--stable', arch)
        self.assertIn('ck-discovery-pack', arch)
        self.assertIn('ck-dual-engage--compact', arch)
        self.assertIn('ck-home-editorial', arch)
