# -*- coding: utf-8 -*-
"""Tests hooks Phase 5 — page /professionnels portable."""

from odoo.tests import tagged
from odoo.tests.common import TransactionCase

from odoo.addons.dorevia_ck_marketone_content.hooks import (
    PROFESSIONNELS_PAGE_URL,
    PROFESSIONNELS_VIEW_KEY,
    bootstrap_professionnels_page,
)


@tagged('post_install', '-at_install', 'dorevia_ck_theme_phase5')
class TestCkProPhase5Hooks(TransactionCase):
    def test_bootstrap_creates_professionnels_page(self):
        website = self.env['website'].search([], limit=1)
        self.assertTrue(website)
        page = self.env['website.page'].search([
            ('url', '=', PROFESSIONNELS_PAGE_URL),
            ('website_id', '=', website.id),
        ])
        if page:
            page.unlink()
        view = self.env['ir.ui.view'].sudo().search([('key', '=', PROFESSIONNELS_VIEW_KEY)])
        if view:
            view.unlink()

        self.assertTrue(bootstrap_professionnels_page(self.env))

        page = self.env['website.page'].search([
            ('url', '=', PROFESSIONNELS_PAGE_URL),
            ('website_id', '=', website.id),
        ], limit=1)
        self.assertTrue(page)
        self.assertTrue(page.is_published)
        arch = page.view_id.arch_db
        if isinstance(arch, dict):
            arch = next(iter(arch.values()))
        self.assertIn('ck-pro-page', arch)
        self.assertIn('t-call="website.layout"', arch)
        self.assertIn('ck-pro-form', arch)
        self.assertIn('crm.lead', arch)

    def test_bootstrap_idempotent(self):
        bootstrap_professionnels_page(self.env)
        page_before = self.env['website.page'].search([
            ('url', '=', PROFESSIONNELS_PAGE_URL),
        ], limit=1)
        bootstrap_professionnels_page(self.env)
        page_after = self.env['website.page'].search([
            ('url', '=', PROFESSIONNELS_PAGE_URL),
        ], limit=1)
        self.assertEqual(page_before.id, page_after.id)
