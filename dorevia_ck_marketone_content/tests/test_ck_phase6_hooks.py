# -*- coding: utf-8 -*-
"""Tests hooks Phase 6 — /contactus · /a-propos portable."""

from odoo.tests import tagged
from odoo.tests.common import TransactionCase

from odoo.addons.dorevia_ck_marketone_content.hooks import (
    A_PROPOS_PAGE_URL,
    A_PROPOS_VIEW_KEY,
    CONTACTUS_PAGE_URL,
    CONTACTUS_VIEW_KEY,
    bootstrap_a_propos_page,
    bootstrap_contactus_page,
)


@tagged('post_install', '-at_install', 'dorevia_ck_theme_phase6')
class TestCkPhase6Hooks(TransactionCase):
    def test_bootstrap_creates_a_propos_page(self):
        website = self.env['website'].search([], limit=1)
        self.assertTrue(website)
        page = self.env['website.page'].search([
            ('url', '=', A_PROPOS_PAGE_URL),
            ('website_id', '=', website.id),
        ])
        if page:
            page.unlink()
        view = self.env['ir.ui.view'].sudo().search([('key', '=', A_PROPOS_VIEW_KEY)])
        if view:
            view.unlink()

        self.assertTrue(bootstrap_a_propos_page(self.env))

        page = self.env['website.page'].search([
            ('url', '=', A_PROPOS_PAGE_URL),
            ('website_id', '=', website.id),
        ], limit=1)
        self.assertTrue(page)
        self.assertTrue(page.is_published)
        arch = page.view_id.arch_db
        if isinstance(arch, dict):
            arch = next(iter(arch.values()))
        self.assertIn('ck-about-page', arch)
        self.assertIn('t-call="website.layout"', arch)
        self.assertIn('/shop', arch)
        self.assertIn('/professionnels', arch)
        self.assertIn('/contactus', arch)

    def test_bootstrap_contactus_page(self):
        self.assertTrue(bootstrap_contactus_page(self.env))
        website = self.env['website'].search([], limit=1)
        page = self.env['website.page'].search([
            ('url', '=', CONTACTUS_PAGE_URL),
            ('website_id', '=', website.id),
        ], limit=1)
        self.assertTrue(page)
        arch = page.view_id.arch_db
        if isinstance(arch, dict):
            arch = next(iter(arch.values()))
        self.assertIn('ck-contact-page', arch)
        self.assertIn('t-call="website.layout"', arch)
        self.assertIn('mail.mail', arch)
        self.assertIn('contactus_form', arch)
        self.assertNotIn('Ma société', arch)
        self.assertNotIn('Fake Buena Vista', arch)

    def test_bootstrap_idempotent(self):
        bootstrap_contactus_page(self.env)
        bootstrap_a_propos_page(self.env)
        contact_before = self.env['website.page'].search([
            ('url', '=', CONTACTUS_PAGE_URL),
        ], limit=1)
        about_before = self.env['website.page'].search([
            ('url', '=', A_PROPOS_PAGE_URL),
        ], limit=1)
        bootstrap_contactus_page(self.env)
        bootstrap_a_propos_page(self.env)
        contact_after = self.env['website.page'].search([
            ('url', '=', CONTACTUS_PAGE_URL),
        ], limit=1)
        about_after = self.env['website.page'].search([
            ('url', '=', A_PROPOS_PAGE_URL),
        ], limit=1)
        self.assertEqual(contact_before.id, contact_after.id)
        self.assertEqual(about_before.id, about_after.id)
