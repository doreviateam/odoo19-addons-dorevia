# -*- coding: utf-8 -*-
"""Tests bootstrap_footer_legal_links — insertion liens légaux footer."""

from odoo.tests import tagged
from odoo.tests.common import TransactionCase

from odoo.addons.dorevia_ck_marketone_content.hooks import (
    bootstrap_footer_legal_links,
)
from odoo.addons.dorevia_ck_marketone_content.legal_pages import (
    FOOTER_CONTACT_LINK_MARKER,
    FOOTER_LEGAL_LINK_HTML,
    FOOTER_PRIVACY_LINK_HTML,
    FOOTER_TERMS_LINK_HTML,
)


def _get_footer_arch(env):
    website = env['website'].search([], limit=1)
    footer = env['ir.ui.view'].sudo().search([
        ('key', '=', 'website.footer_custom'),
        ('website_id', '=', website.id),
    ], limit=1)
    if not footer:
        footer = env['ir.ui.view'].sudo().search([
            ('key', '=', 'website.footer_custom'),
        ], limit=1)
    return footer


def _arch_str(footer):
    arch = footer.arch_db or footer.arch or ''
    if isinstance(arch, dict):
        arch = next(iter(arch.values()), '')
    return arch


@tagged('post_install', '-at_install', 'dorevia_ck_footer_legal')
class TestCkFooterLegalLinks(TransactionCase):

    def setUp(self):
        super().setUp()
        self.website = self.env['website'].search([], limit=1)
        self.assertTrue(self.website, 'Un website doit exister pour tester le footer')
        self.footer = _get_footer_arch(self.env)

    def _set_footer_arch(self, arch):
        self.footer.write({'arch': arch})

    def test_insere_trois_liens_avec_marqueur_contact(self):
        """Cas nominal : marqueur Contact présent → 3 liens insérés après lui."""
        base_arch = (
            '<footer><ul>'
            + FOOTER_CONTACT_LINK_MARKER
            + '</ul></footer>'
        )
        self._set_footer_arch(base_arch)

        result = bootstrap_footer_legal_links(self.env)

        self.assertTrue(result)
        arch = _arch_str(self.footer)
        self.assertIn('href="/legal"', arch)
        self.assertIn('href="/privacy"', arch)
        self.assertIn('href="/terms', arch)

    def test_idempotent_double_appel(self):
        """Un second appel n'insère pas les liens en double."""
        base_arch = (
            '<footer><ul>'
            + FOOTER_CONTACT_LINK_MARKER
            + '</ul></footer>'
        )
        self._set_footer_arch(base_arch)

        bootstrap_footer_legal_links(self.env)
        arch_after_first = _arch_str(self.footer)
        bootstrap_footer_legal_links(self.env)
        arch_after_second = _arch_str(self.footer)

        self.assertEqual(arch_after_first.count('href="/legal"'), 1)
        self.assertEqual(arch_after_second.count('href="/legal"'), 1)
        self.assertEqual(arch_after_second.count('href="/privacy"'), 1)
        self.assertEqual(arch_after_second.count('href="/terms'), 1)

    def test_fallback_sans_marqueur_contact(self):
        """Sans marqueur Contact, le fallback insère un bloc avant </footer>."""
        base_arch = '<footer><div><p>Aucun lien contact ici.</p></div></footer>'
        self._set_footer_arch(base_arch)

        result = bootstrap_footer_legal_links(self.env)

        self.assertTrue(result)
        arch = _arch_str(self.footer)
        self.assertIn('href="/legal"', arch)
        self.assertIn('href="/privacy"', arch)
        self.assertIn('href="/terms', arch)

    def test_arch_inchangee_si_liens_deja_presents(self):
        """Si les 3 liens sont déjà dans le footer, l'arch ne change pas."""
        base_arch = (
            '<footer><ul>'
            + FOOTER_CONTACT_LINK_MARKER
            + FOOTER_LEGAL_LINK_HTML
            + FOOTER_PRIVACY_LINK_HTML
            + FOOTER_TERMS_LINK_HTML
            + '</ul></footer>'
        )
        self._set_footer_arch(base_arch)
        arch_before = _arch_str(self.footer)

        bootstrap_footer_legal_links(self.env)
        arch_after = _arch_str(self.footer)

        self.assertEqual(arch_before, arch_after)

    def test_retourne_false_sans_vue_footer_custom(self):
        """Sans vue website.footer_custom, la fonction retourne False sans erreur."""
        footers = self.env['ir.ui.view'].sudo().search([
            ('key', '=', 'website.footer_custom'),
        ])
        saved_keys = [(v.id, v.key) for v in footers]
        footers.write({'key': 'website.__ck_test_disabled_footer__'})
        try:
            result = bootstrap_footer_legal_links(self.env)
        finally:
            for vid, key in saved_keys:
                self.env['ir.ui.view'].sudo().browse(vid).write({'key': key})
        self.assertFalse(result)
