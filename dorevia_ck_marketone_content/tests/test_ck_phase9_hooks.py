# -*- coding: utf-8 -*-
"""Tests hooks Phase 9 — newsletter M9 · mailing list · dual compact."""

from odoo.tests import tagged
from odoo.tests.common import TransactionCase

from odoo.addons.dorevia_ck_marketone_content.hooks import (
    CONTACTUS_VIEW_KEY,
    NEWSLETTER_MAILING_LIST_NAME,
    PROFESSIONNELS_VIEW_KEY,
    bootstrap_contactus_page,
    bootstrap_newsletter_mailing_list,
    bootstrap_professionnels_page,
    build_contactus_page_arch,
    build_professionnels_page_arch,
)


@tagged('post_install', '-at_install', 'dorevia_ck_theme_phase9')
class TestCkPhase9Hooks(TransactionCase):
    def test_bootstrap_creates_mailing_list(self):
        mailing_list = bootstrap_newsletter_mailing_list(self.env)
        self.assertTrue(mailing_list)
        self.assertEqual(mailing_list.name, NEWSLETTER_MAILING_LIST_NAME)

    def test_bootstrap_idempotent_mailing_list(self):
        first = bootstrap_newsletter_mailing_list(self.env)
        second = bootstrap_newsletter_mailing_list(self.env)
        self.assertEqual(first.id, second.id)

    def test_contactus_arch_includes_newsletter_dual(self):
        arch = build_contactus_page_arch(self.env)
        self.assertIn('ck-dual-engage--compact', arch)
        self.assertIn('ck-newsletter-subscribe', arch)
        self.assertIn('s_newsletter_subscribe', arch)
        self.assertIn('Désinscription possible', arch)
        self.assertIn('ck-contact-page', arch)
        self.assertIn('contactus_form', arch)

    def test_professionnels_arch_includes_newsletter_dual(self):
        arch = build_professionnels_page_arch(self.env)
        self.assertIn('ck-dual-engage--compact', arch)
        self.assertIn('href="#ck-pro-form"', arch)
        self.assertIn('ck-pro-form', arch)
        self.assertIn('crm.lead', arch)
        self.assertIn('ck-newsletter-subscribe', arch)

    def test_bootstrap_contactus_page(self):
        self.assertTrue(bootstrap_contactus_page(self.env))
        view = self.env['ir.ui.view'].sudo().search([('key', '=', CONTACTUS_VIEW_KEY)])
        arch = view.arch_db
        self.assertIn('ck-dual-engage--compact', arch)
        mailing_list = bootstrap_newsletter_mailing_list(self.env)
        self.assertIn(f'data-list-id="{mailing_list.id}"', arch)

    def test_bootstrap_professionnels_page(self):
        self.assertTrue(bootstrap_professionnels_page(self.env))
        view = self.env['ir.ui.view'].sudo().search([('key', '=', PROFESSIONNELS_VIEW_KEY)])
        arch = view.arch_db
        self.assertIn('ck-dual-engage--compact', arch)

    def test_bootstrap_pages_idempotent(self):
        bootstrap_contactus_page(self.env)
        bootstrap_professionnels_page(self.env)
        contact_page = self.env['website.page'].search([
            ('url', '=', '/contactus'),
            ('website_id', '=', False),
        ], limit=1)
        pro_page = self.env['website.page'].search([
            ('url', '=', '/professionnels'),
            ('website_id', '=', False),
        ], limit=1)
        bootstrap_contactus_page(self.env)
        bootstrap_professionnels_page(self.env)
        self.assertEqual(contact_page, self.env['website.page'].search([
            ('url', '=', '/contactus'),
            ('website_id', '=', False),
        ], limit=1))
        self.assertEqual(pro_page, self.env['website.page'].search([
            ('url', '=', '/professionnels'),
            ('website_id', '=', False),
        ], limit=1))
