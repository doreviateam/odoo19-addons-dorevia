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

    def _assert_contains_fr_or_en(self, html, fr, en):
        self.assertTrue(fr in html or en in html, msg=f'Texte FR ou EN attendu: {fr!r} / {en!r}')

    def _assert_shop_root_accessible_label(self, html):
        self.assertTrue(
            'aria-label="Boutique - Tous les produits"' in html
            or 'aria-label="Shop - All products"' in html,
            msg='Libellé accessible FR ou EN attendu sur l’icône racine boutique',
        )
        self.assertTrue(
            'title="Boutique - Tous les produits"' in html
            or 'title="Shop - All products"' in html,
            msg='Title FR ou EN attendu sur l’icône racine boutique',
        )

    def test_header_ck_chrome_on_home(self):
        html = self._home_html()
        self.assertIn('ck-header', html)
        self.assertIn('ck-theme', html)
        self.assertIn('ck-header__brand-img', html)
        self.assertIn('dorevia_ck_theme/static/src/img/ck-logo.svg', html)
        self.assertRegex(
            html,
            r'alt="C-Kréyòl"[^>]*class="[^"]*ck-header__brand-img',
            msg='Logo header doit porter alt C-Kréyòl',
        )
        self.assertRegex(
            html,
            r'aria-label="C-Kréyòl — Accueil"[^>]*>[\s\S]*?ck-header__brand-img',
            msg='Marque header doit être C-Kréyòl (graphie MOA)',
        )
        self.assertEqual(
            html.count('dorevia_ck_theme/static/src/img/ck-logo.svg'),
            2,
            msg='Logo desktop et mobile doivent partager la même source SVG',
        )
        self.assertNotIn('Your Logo', html)
        self.assertNotIn('fonts.googleapis.com', html)
        self.assertNotRegex(html, r'family=DM\+Sans|family=Fraunces')
        self.assertNotIn('ck-header__brand-accent', html)
        self.assertNotRegex(html, r'>\s*Tous nos produits\s*<')
        self.assertIn('ck-nav-shop-root', html)
        self._assert_shop_root_accessible_label(html)
        self.assertIn('Espace pro', html)
        if 'ck-mega-menu' in html:
            self.assertIn('o_mega_menu', html)
        self.assertIn('/professionnels', html)
        self.assertIn('/contactus', html)

    def test_header_h1_service_bar_global(self):
        html = self._home_html()
        self.assertIn('ck-header-service-bar', html)
        self._assert_contains_fr_or_en(html, 'Produits sélectionnés', 'Selected products')
        self._assert_contains_fr_or_en(html, 'Origines identifiées', 'Identified origins')
        self._assert_contains_fr_or_en(html, 'Livraison suivie', 'Tracked delivery')
        for path in ('/shop', '/contactus'):
            with self.subTest(path=path):
                resp = self.url_open(f'{path}?qa_ts=phase10')
                self.assertEqual(resp.status_code, 200, path)
                self.assertIn('ck-header-service-bar', resp.text, path)

    def test_header_h1_search_products_central(self):
        html = self._home_html()
        self.assertIn('ck-header__search', html)
        self.assertIn('Rechercher un produit, une saveur, une île...', html)
        self.assertRegex(
            html,
            r'data-search-type="products"',
            msg='Recherche header limitée au catalogue produits',
        )

    def test_header_h1_2_three_levels_desktop(self):
        """Lot H1.2 — header desktop structuré en 3 niveaux (promesse · identité · exploration)."""
        html = self._home_html()
        self.assertIn('ck-header__main', html)
        self.assertIn('ck-header__identity-row', html)
        self.assertIn('ck-header__nav-row', html)
        self.assertRegex(
            html,
            r'ck-header__identity-row[\s\S]{0,4000}ck-header__search',
            msg='Recherche doit appartenir au niveau identité/achat',
        )
        self.assertRegex(
            html,
            r'ck-header__nav-row[\s\S]{0,2000}id="top_menu"',
            msg='Navigation catalogue doit être sur la ligne exploration dédiée',
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
        if 'Maison &amp; bien-être' in html or 'Maison & bien-être' in html:
            self.assertRegex(html, r'Maison (&amp;|&) bien-être')

    def test_header_boissons_when_category_visible(self):
        html = self._home_html()
        mapping = __import__(
            'odoo.addons.dorevia_ck_marketone_content.nav_sync',
            fromlist=['get_nav_category_mapping'],
        ).get_nav_category_mapping(self.env)
        boissons = next((r for r in mapping if r.get('category_name') == 'Boissons'), None)
        if boissons and boissons.get('visible'):
            self.assertIn('Boissons', html)

    def test_header_nos_producteurs_when_v22(self):
        html = self._home_html()
        if 'Nos producteurs' in html:
            self.assertIn('/nos-producteurs', html)

    def test_header_mega_split_when_product_mega(self):
        html = self._home_html()
        if 'ck-nav-mega-split' not in html:
            self.skipTest('Aucun mega-menu produit rayon sur instance seed.')
        self.assertIn('ck-nav-mega-split__link', html)
        self.assertIn('ck-nav-mega-split__toggle', html)

    def test_hero_carousel_pause_button_rendered(self):
        html = self._home_html()
        if 'ck-hero__visual-carousel--multi' not in html:
            self.skipTest('Hero mono-slide — bouton pause non requis.')
        self.assertIn('ck-hero__visual-pause', html)
        self.assertIn('aria-pressed="false"', html)

    def test_routes_non_regression_markers(self):
        markers = {
            '/': 'ck-featured-products__grid--stable',
            '/shop': 'ck-shop-intro--title-only',
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

    def test_decouvrir_removed_in_v22(self):
        html = self._home_html()
        self.assertNotIn('ck-nav-decouvrir-links', html)

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

    def test_desktop_top_menu_no_mobile_univers_v22(self):
        """V2.2 — Nos univers retiré ; entrées N3 plates."""
        html = self._home_html()
        desktop_menu = self._desktop_top_menu_chunk(html)
        self.assertNotRegex(
            desktop_menu,
            r'>\s*Nos univers\s*<',
            msg='Nos univers ne doit plus figurer en N3 V2.2',
        )

    def test_mobile_offcanvas_no_duplicate_leaf_universe_without_l2(self):
        """B2 Nav-Shop — racines sans L2 : une seule occurrence visible (classe ck_nav_css_class conservée)."""
        html = self._home_html()
        mobile = self._mobile_offcanvas_chunk(html)
        for pattern in (
            r'>\s*Épicerie\s*<',
            r'>\s*Maison (&amp;|&) bien-être\s*<',
            r'>\s*Artisanat &amp; Culture\s*<',
            r'>\s*Communauté\s*<',
        ):
            matches = re.findall(pattern, mobile)
            if matches:
                self.assertEqual(
                    len(matches),
                    1,
                    msg=f'Entrée dupliquée dans le drawer mobile ({len(matches)}×)',
                )
