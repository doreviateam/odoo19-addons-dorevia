# -*- coding: utf-8 -*-
"""Tests conformité branding / footer CK — reproductibilité à l'installation fraîche.

Couvre le gap corrigé : sur install fraîche (valeurs Odoo par défaut), le
branding société et le footer CK doivent être posés automatiquement, sans
contenu Odoo par défaut résiduel, de façon gardée et idempotente.
"""

from odoo.tests import tagged
from odoo.tests.common import TransactionCase

from odoo.addons.dorevia_ck_marketone_content.hooks import (
    BRAND_EMAIL,
    BRAND_NAME,
    bootstrap_brand_name,
)


def _arch(view):
    arch = view.arch_db or view.arch or ''
    if isinstance(arch, dict):
        arch = next(iter(arch.values()), '')
    return arch or ''


@tagged('post_install', '-at_install', 'dorevia_ck_marketone_branding_footer')
class TestCkBrandingFooter(TransactionCase):
    def _company_website(self):
        website = self.env['website'].sudo().search([], limit=1)
        return website.company_id.sudo(), website

    def test_branding_seeded_after_install(self):
        company, website = self._company_website()
        self.assertEqual(website.name, BRAND_NAME)
        self.assertEqual(company.name, BRAND_NAME)
        self.assertEqual(company.email, BRAND_EMAIL)

    def test_footer_ck_view_active_and_conformant(self):
        footer = self.env['ir.ui.view'].sudo().search(
            [('key', '=', 'website.footer_custom')], limit=1)
        self.assertTrue(footer, 'website.footer_custom doit exister')
        self.assertTrue(footer.active, 'le footer CK doit être actif')
        arch = _arch(footer)
        self.assertIn('C-Kréyòl', arch)
        for column in ('Boutique', 'Découvrir'):
            self.assertIn(column, arch)
        for forbidden in ('yourcompany.example.com', 'We are a team', 'Company name'):
            self.assertNotIn(forbidden, arch)

    def test_copyright_branded(self):
        copyright_view = self.env['ir.ui.view'].sudo().search(
            [('key', '=', 'website.footer_copyright_company_name')], limit=1)
        self.assertTrue(copyright_view)
        arch = _arch(copyright_view)
        self.assertIn('C-Kréyòl', arch)
        self.assertNotIn('Company name', arch)

    def test_branding_idempotent_second_pass(self):
        """Après install, un second passage ne réécrit rien (valeurs CK hors défauts)."""
        self.assertFalse(bootstrap_brand_name(self.env))

    def test_branding_never_overwrites_intentional_values(self):
        """Garde-fou : un nom / email renseigné intentionnellement n'est jamais écrasé."""
        company, website = self._company_website()
        company.write({'name': 'Acme SARL', 'email': 'contact@acme.example'})
        website.write({'name': 'Acme Shop'})
        bootstrap_brand_name(self.env)
        self.assertEqual(company.name, 'Acme SARL')
        self.assertEqual(company.email, 'contact@acme.example')
        self.assertEqual(website.name, 'Acme Shop')
