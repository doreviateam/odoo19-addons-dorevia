# -*- coding: utf-8 -*-
"""Tests hooks Phase 8 — page /recettes portable."""

from odoo.tests import tagged
from odoo.tests.common import TransactionCase

from odoo.addons.dorevia_ck_marketone_content.hooks import (
    RECIPES_PAGE_URL,
    RECIPES_VIEW_KEY,
    bootstrap_recipes_page,
)


@tagged('post_install', '-at_install', 'dorevia_ck_theme_phase8')
class TestCkPhase8Hooks(TransactionCase):
    def test_bootstrap_creates_recipes_page(self):
        website = self.env['website'].search([], limit=1)
        self.assertTrue(website)
        page = self.env['website.page'].search([
            ('url', '=', RECIPES_PAGE_URL),
            ('website_id', '=', website.id),
        ])
        if page:
            page.unlink()
        view = self.env['ir.ui.view'].sudo().search([('key', '=', RECIPES_VIEW_KEY)])
        if view:
            view.unlink()

        self.assertTrue(bootstrap_recipes_page(self.env))

        page = self.env['website.page'].search([
            ('url', '=', RECIPES_PAGE_URL),
            ('website_id', '=', website.id),
        ], limit=1)
        self.assertTrue(page)
        self.assertTrue(page.is_published)
        arch = page.view_id.arch_db
        if isinstance(arch, dict):
            arch = next(iter(arch.values()))
        self.assertIn('ck-recipes-page', arch)
        self.assertIn('t-call="website.layout"', arch)
        self.assertIn('Recettes &amp; savoirs CK', arch)
        self.assertIn('ck-recipes-cards', arch)
        self.assertIn('Clafoutis créole au goyavier', arch)
        self.assertIn('Première commande CK', arch)

    def test_bootstrap_idempotent(self):
        bootstrap_recipes_page(self.env)
        page_before = self.env['website.page'].search([
            ('url', '=', RECIPES_PAGE_URL),
        ], limit=1)
        bootstrap_recipes_page(self.env)
        page_after = self.env['website.page'].search([
            ('url', '=', RECIPES_PAGE_URL),
        ], limit=1)
        self.assertEqual(page_before.id, page_after.id)
