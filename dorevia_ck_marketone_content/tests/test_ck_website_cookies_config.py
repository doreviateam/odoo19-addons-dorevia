# -*- coding: utf-8 -*-
"""Bootstrap — barre cookies native Odoo (website.cookies_bar)."""

from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged('post_install', '-at_install', 'dorevia_ck_shop_card')
class TestCkWebsiteCookiesConfig(TransactionCase):
    def test_cookies_bar_enabled_on_website(self):
        website = self.env['website'].get_current_website()
        self.assertTrue(
            website.cookies_bar,
            'La barre cookies native doit être activée (website.cookies_bar).',
        )

    def test_cookie_policy_page_published(self):
        website = self.env['website'].get_current_website()
        page = self.env['website.page'].search([
            ('website_id', '=', website.id),
            ('url', '=', '/cookie-policy'),
        ], limit=1)
        self.assertTrue(page, 'La page /cookie-policy doit exister.')
        self.assertTrue(page.is_published, 'La page /cookie-policy doit être publiée.')
