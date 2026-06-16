# -*- coding: utf-8 -*-
"""Tests hooks Section 3 — vedettes SSR maquette · ordre trust-bar → grille."""

from types import SimpleNamespace
from unittest.mock import patch

from odoo.tests import tagged
from odoo.tests.common import TransactionCase

from odoo.addons.dorevia_ck_marketone_content.home_featured import (
    FEATURED_CARD_MARKER,
    FEATURED_GRID_MARKER,
    FEATURED_TITLE,
    bootstrap_home_featured_products,
)
from odoo.addons.dorevia_ck_marketone_content.home_hero import bootstrap_home_hero
from odoo.addons.dorevia_ck_marketone_content.models.ir_http import IrHttp
from odoo.addons.dorevia_ck_marketone_content.home_reassurance import (
    FEATURED_MARKER,
    REASSURANCE_TRUST_BAR_MARKER,
    bootstrap_home_reassurance,
)


@tagged('post_install', '-at_install', 'dorevia_ck_marketone_home_section3')
class TestCkHomeSection3FeaturedHooks(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        bootstrap_home_hero(cls.env)
        bootstrap_home_reassurance(cls.env)
        bootstrap_home_featured_products(cls.env)

    def _homepage_arch(self):
        website = self.env['website'].search([], limit=1)
        page = self.env['website.page'].sudo().search([
            ('url', '=', '/'),
            ('website_id', '=', website.id),
        ], limit=1)
        self.assertTrue(page and page.view_id)
        return page.view_id.arch_db or page.view_id.arch or ''

    def test_bootstrap_order_trust_bar_before_featured(self):
        arch = self._homepage_arch()
        self.assertIn(REASSURANCE_TRUST_BAR_MARKER, arch)
        self.assertIn(FEATURED_MARKER, arch)
        self.assertLess(arch.find(REASSURANCE_TRUST_BAR_MARKER), arch.find(FEATURED_MARKER))

    def test_bootstrap_featured_maquette_arch(self):
        arch = self._homepage_arch()
        self.assertIn(FEATURED_GRID_MARKER, arch)
        self.assertIn(FEATURED_TITLE, arch)
        self.assertIn(FEATURED_CARD_MARKER, arch)
        self.assertIn('product-card-media', arch)
        self.assertIn('class="card-cta"', arch)

    def test_home_refresh_guard_skips_backend_paths(self):
        fake_request = SimpleNamespace(httprequest=SimpleNamespace(path='/odoo'))
        with patch('odoo.addons.dorevia_ck_marketone_content.models.ir_http.request', fake_request):
            self.assertFalse(IrHttp._ck_path_can_be_homepage())

    def test_home_refresh_guard_accepts_root_and_lang_paths(self):
        for path in ('/', '/fr'):
            fake_request = SimpleNamespace(httprequest=SimpleNamespace(path=path))
            with patch('odoo.addons.dorevia_ck_marketone_content.models.ir_http.request', fake_request):
                self.assertTrue(IrHttp._ck_path_can_be_homepage())
