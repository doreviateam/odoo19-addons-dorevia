# -*- coding: utf-8 -*-
"""Tests Phase 10 / Nav-1 — header / menu / branding CK."""

import re

from odoo.tests import tagged
from odoo.tests.common import HttpCase

from odoo.addons.dorevia_ck_marketone_content.nav_sync import bootstrap_ck_navigation


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
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        content = cls.env['ir.module.module'].sudo().search([
            ('name', '=', 'dorevia_ck_marketone_content'),
            ('state', '=', 'installed'),
        ], limit=1)
        if not content:
            raise cls.skipTest(
                'dorevia_ck_marketone_content non installé — recette header Nav non applicable'
            )
        bootstrap_ck_navigation(cls.env)

    def _home_html(self):
        resp = self.url_open('/?qa_ts=phase10')
        self.assertEqual(resp.status_code, 200)
        return resp.text

    def test_header_ck_chrome_on_home(self):
        html = self._home_html()
        self.assertIn('ck-header', html)
        self.assertIn('ck-theme', html)
        self.assertIn('ck-header__brand', html)
        self.assertIn('ck-header__brand-accent', html)
        self.assertRegex(html, r'C-[\s\S]{0,24}?Kr[eéè]yòl')
        self.assertRegex(
            html,
            r'aria-label="C-Kréyòl — Accueil"[^>]*>[\s\S]*?ck-header__brand',
            msg='Marque header doit être C-Kréyòl (graphie MOA)',
        )
        self.assertNotIn('Your Logo', html)
        self.assertNotIn('fonts.googleapis.com', html)
        self.assertNotRegex(html, r'family=DM\+Sans|family=Fraunces')
        self.assertNotRegex(
            html,
            r'data-name="Navbar Logo"[^>]*>[\s\S]*?<img[^>]+logo',
            msg='Logo image générique interdit — marque typographique CK attendue',
        )
        self.assertIn('Tous nos produits', html)
        self.assertIn('Découvrir', html)
        self.assertIn('o_mega_menu', html)
        self.assertIn('/professionnels', html)
        self.assertIn('/contactus', html)

    def test_header_h1_service_bar_global(self):
        html = self._home_html()
        self.assertIn('ck-header-service-bar', html)
        self.assertIn('Produits créoles sélectionnés', html)
        self.assertIn('Origines identifiées', html)
        self.assertIn('Livraison suivie', html)
        for path in ('/shop', '/contactus'):
            with self.subTest(path=path):
                resp = self.url_open(f'{path}?qa_ts=phase10')
                self.assertEqual(resp.status_code, 200, path)
                self.assertIn('ck-header-service-bar', resp.text, path)

    def test_header_h1_search_products_central(self):
        html = self._home_html()
        self.assertIn('ck-header__search', html)
        self.assertIn('Rechercher un produit, une saveur...', html)
        self.assertRegex(
            html,
            r'data-search-type="products"',
            msg='Recherche header limitée au catalogue produits',
        )

    def test_header_h1_mobile_chrome_menu_label(self):
        html = self._home_html()
        self.assertRegex(
            html,
            r'data-bs-target="#top_menu_collapse_mobile"[^>]*aria-label="Menu"',
            msg='Burger mobile doit porter aria-label Menu',
        )
        self.assertIn('ck-header-mobile-chrome', html)
        offcanvas = self._mobile_offcanvas_chunk(html)
        self.assertNotIn('Rechercher un produit, une saveur...', offcanvas)

    def test_header_no_top_level_professionnels_or_contact_cta(self):
        html = self._home_html()
        top_menu = re.search(r'id="top_menu"[^>]*>(.*?)</ul>', html, re.S)
        self.assertTrue(top_menu, msg='top_menu introuvable')
        chunk = top_menu.group(1)
        self.assertNotRegex(chunk, r'>\s*Professionnels\s*<')
        self.assertNotRegex(chunk, r'>\s*Contactez-nous\s*<')
        self.assertNotIn('btn_cta', chunk)

    def test_header_no_producteurs_nav_label(self):
        html = self._home_html()
        self.assertNotRegex(html, r'>\s*Producteurs\s*</a>')

    def test_header_soin_bien_etre_label_when_visible(self):
        html = self._home_html()
        if 'Soin &amp; Bien-être' in html or 'Soin & Bien-être' in html:
            self.assertRegex(html, r'Soin (&amp;|&) Bien-être')

    def test_hero_carousel_pause_button_rendered(self):
        html = self._home_html()
        self.assertIn('ck-hero__visual-pause', html)
        self.assertIn('aria-pressed="false"', html)

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

    def test_decouvrir_mega_has_no_commerce_duplicates(self):
        html = self._home_html()
        links = re.search(r'ck-nav-decouvrir-links">(.*?)</nav>', html, re.S)
        self.assertTrue(links, msg='Mega Découvrir sans liens éditoriaux')
        self.assertNotIn('/shop/category/', links.group(1))

    def _desktop_top_menu_chunk(self, html):
        match = re.search(
            r'<nav[^>]*class="[^"]*d-none d-lg-block[^"]*"[^>]*>.*?'
            r'<ul[^>]*id="top_menu"[^>]*>(.*?)</ul>',
            html,
            re.S,
        )
        self.assertTrue(match, msg='Menu desktop #top_menu introuvable')
        return match.group(1)

    def _mobile_offcanvas_chunk(self, html):
        match = re.search(
            r'id="top_menu_collapse_mobile"[^>]*>(.*?)</div>\s*</div>',
            html,
            re.S,
        )
        self.assertTrue(match, msg='Offcanvas mobile introuvable')
        return match.group(1)

    def test_desktop_top_menu_mobile_univers_has_hide_class(self):
        """B1 — Nos univers porte ck-nav-mobile-univers (masqué desktop via SCSS)."""
        html = self._home_html()
        desktop_menu = self._desktop_top_menu_chunk(html)
        self.assertRegex(
            desktop_menu,
            r'class="[^"]*ck-nav-mobile-univers[^"]*"[^>]*>[\s\S]*?'
            r'<span>Nos univers</span>',
            msg='Nos univers doit porter ck-nav-mobile-univers dans #top_menu desktop',
        )

    def test_mobile_offcanvas_no_duplicate_universe_entries(self):
        """B2 — Épicerie / Soin ne doivent pas apparaître en double (accordéon + plat)."""
        html = self._home_html()
        mobile = self._mobile_offcanvas_chunk(html)
        for pattern in (r'>\s*Épicerie\s*<', r'>\s*Soin (&amp;|&) Bien-être\s*<'):
            matches = re.findall(pattern, mobile)
            if matches:
                self.assertEqual(
                    len(matches),
                    1,
                    msg=f'Entrée univers dupliquée dans le drawer mobile ({len(matches)}×)',
                )
