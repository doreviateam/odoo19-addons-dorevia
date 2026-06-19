# -*- coding: utf-8 -*-
"""Tests HTTP — accessibilité et mention RGPD du formulaire contact B2C (dorevia_ck_theme)."""

from odoo.tests import tagged
from odoo.tests.common import HttpCase

from odoo.addons.dorevia_ck_marketone_content.hooks import bootstrap_contactus_page


@tagged('post_install', '-at_install', 'dorevia_ck_theme_contactus_a11y')
class TestCkContactusA11yRgpd(HttpCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        bootstrap_contactus_page(cls.env)

    def _contactus_html(self):
        return self.url_open('/contactus').text

    def test_contactus_form_submit_button_keyboard_accessible(self):
        """Garde-fou a11y : <a role="button"> ne réagit pas à la touche Espace —
        le bouton d'envoi doit être un <button> natif (Entrée + Espace gratuits)."""
        html = self._contactus_html()
        self.assertIn('<button type="button" class="btn btn-primary s_website_form_send">', html)
        self.assertNotRegex(html, r'<a[^>]+s_website_form_send')

    def test_contactus_required_fields_have_accessible_mark(self):
        """Garde-fou a11y : l'astérisque des champs obligatoires a un équivalent texte."""
        html = self._contactus_html()
        self.assertIn('s_website_form_mark" aria-hidden="true"', html)
        self.assertIn('class="visually-hidden"> (obligatoire)</span>', html)

    def test_contactus_form_has_rgpd_notice(self):
        html = self._contactus_html()
        self.assertIn('href="/privacy"', html)
