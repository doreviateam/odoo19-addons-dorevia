# -*- coding: utf-8 -*-
"""Tests hooks Phase 7 — fiche producteur pilote portable."""

from odoo.tests import tagged
from odoo.tests.common import TransactionCase

from odoo.addons.dorevia_ck_marketone_content.hooks import (
    PRODUCER_PAGE_URL,
    PRODUCER_VIEW_KEY,
    bootstrap_producer_page,
)


@tagged('post_install', '-at_install', 'dorevia_ck_theme_phase7')
class TestCkPhase7Hooks(TransactionCase):
    def test_bootstrap_creates_producer_page(self):
        website = self.env['website'].search([], limit=1)
        self.assertTrue(website)
        page = self.env['website.page'].search([
            ('url', '=', PRODUCER_PAGE_URL),
            ('website_id', '=', website.id),
        ])
        if page:
            page.unlink()
        view = self.env['ir.ui.view'].sudo().search([('key', '=', PRODUCER_VIEW_KEY)])
        if view:
            view.unlink()

        self.assertTrue(bootstrap_producer_page(self.env))

        page = self.env['website.page'].search([
            ('url', '=', PRODUCER_PAGE_URL),
            ('website_id', '=', website.id),
        ], limit=1)
        self.assertTrue(page)
        self.assertTrue(page.is_published)
        arch = page.view_id.arch_db
        if isinstance(arch, dict):
            arch = next(iter(arch.values()))
        self.assertIn('ck-producer-page', arch)
        self.assertIn('t-call="website.layout"', arch)
        self.assertIn('Atelier Les Hauts Goyaviers', arch)
        self.assertIn('ck-producer-products', arch)
        self.assertIn('Pourquoi CK sélectionne', arch)

    def test_bootstrap_idempotent(self):
        bootstrap_producer_page(self.env)
        page_before = self.env['website.page'].search([
            ('url', '=', PRODUCER_PAGE_URL),
        ], limit=1)
        bootstrap_producer_page(self.env)
        page_after = self.env['website.page'].search([
            ('url', '=', PRODUCER_PAGE_URL),
        ], limit=1)
        self.assertEqual(page_before.id, page_after.id)
