# -*- coding: utf-8 -*-
"""PR-2 H3 — guard anti-écrasement des pages CMS (empreinte de seed)."""

from odoo.tests import tagged
from odoo.tests.common import TransactionCase

from odoo.addons.dorevia_ck_marketone_content.hooks import (
    A_PROPOS_VIEW_KEY,
    bootstrap_a_propos_page,
)


@tagged('post_install', '-at_install', 'dorevia_ck_marketone_cms_guard')
class TestCkCmsSeedGuard(TransactionCase):
    def _about_view(self):
        page = self.env['website.page'].sudo().search([('url', '=', '/a-propos')], limit=1)
        return page.view_id

    def test_preserve_moa_edit(self):
        """Une édition BO après seed n'est pas écrasée par un re-bootstrap."""
        bootstrap_a_propos_page(self.env)
        view = self._about_view()
        self.assertTrue(view, 'page /a-propos absente après bootstrap')

        view.write({'arch': view.arch_db.replace('</div>', '<!-- EDIT MOA --></div>', 1)})
        edited = view.arch_db

        bootstrap_a_propos_page(self.env)  # ne doit pas réécrire
        self.assertEqual(view.arch_db, edited)
        self.assertIn('EDIT MOA', view.arch_db)

    def test_seed_param_set_and_idempotent(self):
        """Le seed est posé et un re-bootstrap sur page non éditée reste idempotent."""
        bootstrap_a_propos_page(self.env)
        param = self.env['ir.config_parameter'].sudo()
        self.assertTrue(param.get_param(f'ck_seed_arch.{A_PROPOS_VIEW_KEY}'))

        bootstrap_a_propos_page(self.env)  # page non éditée → re-seed idempotent
        self.assertIn('ck-about-page', self._about_view().arch_db)
