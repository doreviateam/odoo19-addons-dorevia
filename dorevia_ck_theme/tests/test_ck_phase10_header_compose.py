# -*- coding: utf-8 -*-
"""Tests Phase 10 — header / menu / branding CK · GO §5undecies."""

from odoo.tests import tagged
from odoo.tests.common import HttpCase


PHASE10_ROUTES = (
    '/',
    '/shop',
    '/professionnels',
    '/contactus',
    '/a-propos',
    '/producteur/atelier-hauts-goyaviers',
    '/recettes',
)


@tagged('post_install', '-at_install', 'dorevia_ck_theme_phase10')
class TestCkPhase10HeaderCompose(HttpCase):
    def setUp(self):
        super().setUp()
        # QA C1 : ces tests valident le rendu Phase 10 (header + routes /a-propos,
        # /recettes, /producteur/..., menus Boutique/Découvrir/Professionnels) qui
        # n'existe que lorsque le module de contenu CK est installé. Sur une base
        # « thème seul » (garde-fou §4bis), on saute la recette plutôt que d'échouer.
        content = self.env['ir.module.module'].sudo().search([
            ('name', '=', 'dorevia_ck_marketone_content'),
            ('state', '=', 'installed'),
        ], limit=1)
        if not content:
            self.skipTest(
                'dorevia_ck_marketone_content non installé — recette Phase 10 '
                '(header + routes contenu) non applicable en thème seul'
            )

    def test_header_ck_chrome_on_home(self):
        resp = self.url_open('/?qa_ts=phase10')
        self.assertEqual(resp.status_code, 200)
        html = resp.text
        self.assertIn('ck-header', html)
        self.assertIn('ck-theme', html)
        self.assertIn('ck-header__brand', html)
        self.assertIn('ck-header__brand-accent', html)
        self.assertIn('C-Kreyol', html)
        self.assertNotIn('Your Logo', html)
        self.assertNotRegex(
            html,
            r'data-name="Navbar Logo"[^>]*>[\s\S]*?<img[^>]+logo',
            msg='Logo image générique interdit — marque typographique CK attendue',
        )
        self.assertIn('Boutique', html)
        self.assertIn('Découvrir', html)
        self.assertIn('Professionnels', html)
        self.assertIn('o_mega_menu', html)

    def test_header_no_producteurs_nav_label(self):
        html = self.url_open('/?qa_ts=phase10').text
        self.assertNotRegex(html, r'>\s*Producteurs\s*</a>')

    def test_routes_non_regression_markers(self):
        markers = {
            '/': 'ck-featured-products__grid--stable',
            '/shop': 's_ck_shop_intro',
            '/professionnels': 'ck-pro-page',
            '/contactus': 'ck-contact-page',
            '/a-propos': 'ck-about-page',
            '/producteur/atelier-hauts-goyaviers': 'ck-producer-page',
            '/recettes': 'ck-recipes-page',
        }
        for path, needle in markers.items():
            with self.subTest(path=path):
                resp = self.url_open(f'{path}?qa_ts=phase10')
                self.assertEqual(resp.status_code, 200, path)
                self.assertIn('ck-header', resp.text, path)
                self.assertIn(needle, resp.text, path)
