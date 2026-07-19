# -*- coding: utf-8 -*-
"""Tests Header CK V2.2 — navigation N3 + mega-menus."""

import re

from odoo.tests import tagged
from odoo.tests.common import HttpCase, TransactionCase

from odoo.addons.dorevia_ck_marketone_content.nav_sync import bootstrap_ck_navigation
from odoo.addons.dorevia_ck_marketone_content.nav_v22_config import (
    LEGACY_NAV_COUPS_LABEL,
    LEGACY_NAV_MAISON_LABEL,
    NAV_CATALOGUE_PRODUCTEURS_LABEL,
    NAV_COMMUNAUTE_LABEL,
    NAV_ESPACE_PRO_LABEL,
)


@tagged('post_install', '-at_install', 'dorevia_ck_header_v22')
class TestCkHeaderV22Compose(HttpCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        content = cls.env['ir.module.module'].sudo().search([
            ('name', '=', 'dorevia_ck_marketone_content'),
            ('state', '=', 'installed'),
        ], limit=1)
        if not content:
            raise cls.skipTest('dorevia_ck_marketone_content requis')
        bootstrap_ck_navigation(cls.env)

    def _home_html(self):
        resp = self.url_open('/?qa_ts=header_v22')
        self.assertEqual(resp.status_code, 200)
        return resp.text

    def _assert_contains_fr_or_en(self, html, fr, en):
        self.assertTrue(fr in html or en in html, msg=f'Texte FR ou EN attendu: {fr!r} / {en!r}')

    def test_service_bar_v22_four_promises(self):
        html = self._home_html()
        self._assert_contains_fr_or_en(html, 'Produits sélectionnés', 'Selected products')
        self._assert_contains_fr_or_en(html, 'Stocké/expédié depuis Nantes', 'Stored & shipped from Nantes')

    def test_baseline_epicerie_creole_desktop(self):
        html = self._home_html()
        self.assertIn('ck-header__brand-img', html)
        self.assertIn('dorevia_ck_theme/static/src/img/ck-logo.svg', html)

    def test_search_placeholder_v22(self):
        html = self._home_html()
        self.assertIn('Rechercher un produit, une saveur, une île...', html)

    def _header_nav_chunk(self, html):
        match = re.search(r'<header[^>]*id="top"[^>]*>(.*?)</header>', html, re.S)
        self.assertTrue(match, msg='header#top introuvable')
        return match.group(1)

    def _assert_shop_root_accessible_label(self, html):
        self.assertTrue(
            'aria-label="Accueil"' in html
            or 'aria-label="Home"' in html,
            msg='Libellé accessible Accueil/Home attendu sur l’icône maison',
        )
        self.assertTrue(
            'title="Accueil"' in html
            or 'title="Home"' in html,
            msg='Title Accueil/Home attendu sur l’icône maison',
        )

    def test_catalogue_roots_and_home_icon(self):
        """S2 / V3 : Accueil = icône maison ; racines Producteurs / Professionnels."""
        html = self._home_html()
        nav = self._header_nav_chunk(html)
        self.assertNotRegex(nav, r'>\s*Tous nos produits\s*<')
        self.assertIn('ck-nav-shop-root', nav)
        self._assert_shop_root_accessible_label(nav)
        self.assertIn('fa-home', nav)
        self.assertNotRegex(nav, r'>\s*Boutique\s*</')
        self.assertIn(NAV_CATALOGUE_PRODUCTEURS_LABEL, nav)
        self.assertRegex(nav, r'href="(?:/[a-z]{2}(?:-[A-Z]{2})?)?/professionnels"')
        # Entrées V2.2 neutralisées par la délégation V3
        self.assertNotIn(NAV_COMMUNAUTE_LABEL, nav)
        self.assertNotIn(NAV_ESPACE_PRO_LABEL, nav)
        self.assertNotRegex(nav, r'>\s*Découvrir\s*</a>')
        epicerie = self.env['website.menu'].sudo().search([
            ('name', '=', 'Épicerie'),
            ('parent_id', '!=', False),
        ], limit=1)
        if epicerie:
            self.assertIn('Épicerie', nav)

    def test_no_v22_n3_group_css_classes(self):
        """S2 : plus de marqueurs CSS de regroupement N3 V2.2 dans le header."""
        html = self._home_html()
        self.assertNotIn('ck-nav-n3-rayon', html)
        self.assertNotIn('ck-nav-n3-selection', html)
        self.assertNotIn('ck-nav-n3-relation', html)

    def test_shop_root_icon_active_on_shop_pages(self):
        resp = self.url_open('/shop?qa_ts=header_v22_nav_u2')
        self.assertEqual(resp.status_code, 200)
        nav = self._header_nav_chunk(resp.text)
        self.assertRegex(
            nav,
            r'class="[^"]*ck-nav-shop-root__link[^"]*active[^"]*"',
            msg='Icône racine boutique active attendue sur /shop',
        )

    def test_mega_menu_grammar_markup(self):
        html = self._home_html()
        if 'ck-mega-menu' not in html:
            self.skipTest('Aucun mega-menu produit alimenté sur cette instance.')
        self.assertIn('ck-mega-menu__desktop', html)
        self.assertIn('Acheter par famille', html)

    def test_producteurs_direct_link(self):
        html = self._home_html()
        self.assertRegex(html, r'href="(?:/[a-z]{2}(?:-[A-Z]{2})?)?/producteurs"')

    def test_professionnels_direct_link(self):
        """S2 / V3 : Professionnels est un lien racine (plus de dropdown Espace pro)."""
        html = self._home_html()
        self.assertNotIn('ck-nav-espace-pro', html)
        self.assertRegex(html, r'href="(?:/[a-z]{2}(?:-[A-Z]{2})?)?/professionnels"')

    def test_communaute_absent_after_v3(self):
        menu = self.env['website.menu'].sudo().search([
            ('name', '=', NAV_COMMUNAUTE_LABEL),
            ('parent_id', '!=', False),
        ], limit=1)
        self.assertFalse(menu, 'Communauté doit être absente après sync V3')

    def test_communaute_not_rendered_in_header(self):
        html = self._home_html()
        self.assertNotRegex(
            html,
            r'>\s*Communauté\s*<',
            msg='Communauté ne doit plus apparaître dans le header V3',
        )

    def test_coups_de_coeur_absent_from_root_nav(self):
        root = self.env['website'].search([], limit=1).menu_id
        legacy = self.env['website.menu'].sudo().search([
            ('name', '=', LEGACY_NAV_COUPS_LABEL),
            ('parent_id', '=', root.id),
        ])
        self.assertFalse(legacy, 'Coups de cœur ne doit plus figurer en navigation principale')

    def test_legacy_maison_label_absent(self):
        html = self._home_html()
        nav = self._header_nav_chunk(html)
        self.assertNotIn('Maison &amp; Bien-être', nav)
        self.assertNotIn(LEGACY_NAV_MAISON_LABEL, nav)

    def test_decouvrir_removed_from_nav(self):
        decouvrir = self.env['website.menu'].sudo().search([
            ('name', '=', 'Découvrir'),
            ('parent_id', '!=', False),
        ])
        self.assertFalse(decouvrir)

    def test_three_levels_structure(self):
        html = self._home_html()
        self.assertIn('ck-header__identity-row', html)
        self.assertIn('ck-header__nav-row', html)

    def _desktop_actions_chunk(self, html):
        if 'ck-header__identity-row' not in html:
            self.skipTest('Header H1.2 absent')
        return html.split('ck-header__identity-row', 1)[1].split('ck-header__nav-row', 1)[0]

    def test_wishlist_link_desktop_header(self):
        html = self._home_html()
        actions = self._desktop_actions_chunk(html)
        self.assertIn('o_wsale_my_wish', actions)
        self.assertIn('/shop/wishlist', actions)
        self.assertTrue(
            'Mes favoris' in actions or 'Favourites' in actions,
            msg='Libellé wishlist FR ou EN attendu dans le header desktop.',
        )
        self.assertIn('o_wsale_my_cart', actions)
        wish_pos = actions.find('o_wsale_my_wish')
        cart_pos = actions.find('o_wsale_my_cart')
        self.assertGreater(cart_pos, wish_pos, 'Wishlist doit précéder le panier')

    def test_wishlist_link_mobile_header(self):
        html = self._home_html()
        mobile = html.split('o_header_mobile', 1)[-1] if 'o_header_mobile' in html else ''
        self.assertIn('o_wsale_my_wish', mobile)
        self.assertIn('/shop/wishlist', mobile)
        self.assertIn('ck-header-mobile__wishlist-menu-link', mobile)
        self.assertTrue(
            'Mes favoris' in mobile or 'Favourites' in mobile,
            msg='Libellé wishlist FR ou EN attendu dans le header mobile.',
        )
        self.assertNotIn('o_wsale_my_wish_hide_empty', mobile)
