# -*- coding: utf-8 -*-
"""Tests maintenance technique dorevia_ck_theme (sans contenu métier)."""

from odoo.tests import tagged
from odoo.tests.common import TransactionCase

from odoo.addons.dorevia_ck_theme.hooks import (
    LEGACY_PHASE3_VIEW_KEY,
    is_marketone_content_installed,
    remove_legacy_phase3_script_view,
)


@tagged('post_install', '-at_install', 'dorevia_ck_theme_technical')
class TestCkThemeTechnical(TransactionCase):
    def test_marketone_content_not_installed_by_default_on_theme_only(self):
        """Garde-fou §4bis : contenu absent si module content non installé."""
        Module = self.env['ir.module.module'].sudo()
        content = Module.search([('name', '=', 'dorevia_ck_marketone_content')], limit=1)
        if content and content.state == 'installed':
            self.skipTest('dorevia_ck_marketone_content installé — test thème seul non applicable')
        self.assertFalse(is_marketone_content_installed(self.env))

    def test_remove_legacy_phase3_script_view(self):
        products = self.env.ref('website_sale.products')
        legacy = self.env['ir.ui.view'].create({
            'name': 'Legacy Phase 3 shell view',
            'type': 'qweb',
            'mode': 'extension',
            'inherit_id': products.id,
            'arch_db': '<data/>',
            'key': LEGACY_PHASE3_VIEW_KEY,
        })
        remove_legacy_phase3_script_view(self.env)
        self.assertFalse(self.env['ir.ui.view'].search([('id', '=', legacy.id)]))
