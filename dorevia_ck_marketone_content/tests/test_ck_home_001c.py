# -*- coding: utf-8 -*-
"""Tests CK-HOME-001C — marque C-Kréyòl, newsletter FR, carte Boissons."""

from odoo.tests import tagged
from odoo.tests.common import TransactionCase

from odoo.addons.dorevia_ck_marketone_content.home_dual_engage import (
    bootstrap_home_dual_engage,
    dual_engage_home_arch_is_valid,
)
from odoo.addons.dorevia_ck_marketone_content.hooks import (
    BRAND_NAME,
    BRAND_NAME_LEGACY,
    bootstrap_brand_name,
    bootstrap_footer_copyright_brand,
)


@tagged('post_install', '-at_install', 'dorevia_ck_home_001c')
class TestCkHome001c(TransactionCase):
    def _homepage_arch(self):
        page = self.env['website.page'].search([('url', '=', '/')], limit=1)
        self.assertTrue(page)
        arch = page.view_id.arch_db
        if isinstance(arch, dict):
            arch = next(iter(arch.values()))
        return arch, page

    def test_bootstrap_brand_name_from_legacy_only(self):
        website = self.env['website'].sudo().search([], limit=1)
        self.assertTrue(website)
        company = website.company_id.sudo()
        website.write({'name': BRAND_NAME_LEGACY})
        company.write({'name': BRAND_NAME_LEGACY})

        self.assertTrue(bootstrap_brand_name(self.env))
        self.assertEqual(website.name, BRAND_NAME)
        self.assertEqual(company.name, BRAND_NAME)

        website.write({'name': 'Autre marque'})
        company.write({'name': 'Société réelle'})
        bootstrap_brand_name(self.env)
        self.assertEqual(website.name, 'Autre marque')
        self.assertEqual(company.name, 'Société réelle')

    def test_bootstrap_footer_copyright_brand_replaces_legacy(self):
        View = self.env['ir.ui.view'].sudo()
        view = View.search([('key', '=', 'dorevia_ck_marketone_content.terms_page')], limit=1)
        if not view:
            self.skipTest('terms_page absent')
        arch = view.arch_db
        if isinstance(arch, dict):
            arch = next(iter(arch.values()), '')
        backup = arch
        if BRAND_NAME in arch:
            view.write({'arch_db': arch.replace(BRAND_NAME, BRAND_NAME_LEGACY, 1)})
        elif BRAND_NAME_LEGACY not in arch:
            view.write({'arch_db': f'<t><p>{BRAND_NAME_LEGACY}</p></t>'})
        self.assertTrue(bootstrap_footer_copyright_brand(self.env))
        refreshed = view.arch_db
        if isinstance(refreshed, dict):
            refreshed = next(iter(refreshed.values()), '')
        self.assertNotIn(BRAND_NAME_LEGACY, refreshed)
        self.assertIn(BRAND_NAME, refreshed)
        view.write({'arch_db': backup})

    def test_dual_engage_invalidates_stale_english_newsletter_snapshot(self):
        arch, page = self._homepage_arch()
        if 'ck-dual-engage' not in arch:
            bootstrap_home_dual_engage(self.env)
            arch, page = self._homepage_arch()

        stale = arch.replace('Merci pour votre inscription', 'Thanks for registering!', 1)
        if stale == arch:
            stale = arch.replace("S'inscrire", 'Subscribe', 1)
        page.view_id.write({'arch_db': stale})
        self.assertFalse(dual_engage_home_arch_is_valid(stale, self.env))

        self.assertTrue(bootstrap_home_dual_engage(self.env))
        refreshed = self._homepage_arch()[0]
        self.assertNotIn('Thanks for registering', refreshed)
        self.assertIn('Merci pour votre inscription', refreshed)
        self.assertTrue(dual_engage_home_arch_is_valid(refreshed, self.env))
