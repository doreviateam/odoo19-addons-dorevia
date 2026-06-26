# -*- coding: utf-8 -*-
"""Tests Header CK V2.2 — navigation N3 + mega-menus."""

import re

from odoo.tests import tagged
from odoo.tests.common import HttpCase

from odoo.addons.dorevia_ck_marketone_content.nav_sync import bootstrap_ck_navigation
from odoo.addons.dorevia_ck_marketone_content.nav_v22_config import (
    LEGACY_NAV_COUPS_LABEL,
    LEGACY_NAV_MAISON_LABEL,
    NAV_COFFRETS_LABEL,
    NAV_COMMUNAUTE_LABEL,
    NAV_COMMUNAUTE_URL,
    NAV_ESPACE_PRO_LABEL,
    NAV_PRODUCTEURS_LABEL,
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

    def test_service_bar_v22_four_promises(self):
        html = self._home_html()
        self.assertIn('Produits sélectionnés', html)
        self.assertIn('Stocké/expédié depuis Nantes', html)

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

    def test_n3_nine_entries_present(self):
        html = self._home_html()
        nav = self._header_nav_chunk(html)
        for label in (
            'Tous nos produits',
            'Épicerie',
            'Communauté',
            NAV_PRODUCTEURS_LABEL,
            NAV_ESPACE_PRO_LABEL,
        ):
            self.assertIn(label, nav, label)
        boissons = self.env['website.menu'].sudo().search([
            ('name', '=', 'Boissons'),
            ('parent_id', '!=', False),
        ], limit=1)
        if boissons:
            self.assertIn('Boissons', nav)
        coffrets = self.env['website.menu'].sudo().search([
            ('name', '=', NAV_COFFRETS_LABEL),
            ('parent_id', '!=', False),
        ], limit=1)
        if coffrets:
            self.assertIn(NAV_COFFRETS_LABEL, nav)
        self.assertNotRegex(nav, r'>\s*Découvrir\s*</a>')

    def test_n3_group_css_classes(self):
        html = self._home_html()
        self.assertIn('ck-nav-n3-rayon', html)
        self.assertIn('ck-nav-n3-selection', html)
        self.assertIn('ck-nav-n3-relation', html)

    def test_mega_menu_grammar_markup(self):
        html = self._home_html()
        if 'ck-mega-menu' not in html:
            self.skipTest('Aucun mega-menu produit alimenté sur cette instance.')
        self.assertIn('ck-mega-menu__desktop', html)
        self.assertIn('Acheter par famille', html)

    def test_producteurs_direct_link(self):
        html = self._home_html()
        self.assertRegex(html, r'href="/nos-producteurs"')

    def test_espace_pro_dropdown_anchors(self):
        html = self._home_html()
        self.assertIn('ck-nav-espace-pro', html)
        self.assertIn('/professionnels#acheter', html)
        self.assertIn('/professionnels#contact', html)

    def test_communaute_placeholder_link(self):
        menu = self.env['website.menu'].sudo().search([
            ('name', '=', NAV_COMMUNAUTE_LABEL),
            ('parent_id', '!=', False),
        ], limit=1)
        self.assertTrue(menu, 'Communauté doit être présent en N3')
        self.assertEqual(menu.url, NAV_COMMUNAUTE_URL)
        self.assertFalse(menu.is_mega_menu)
        self.assertFalse(menu.child_id)

    def test_communaute_renders_hash_href(self):
        html = self._home_html()
        self.assertRegex(
            html,
            r'href="#"\s+class="[^"]*nav-link[^"]*"[^>]*>\s*<span>Communauté</span>',
        )

    def test_coups_de_coeur_absent_from_root_nav(self):
        root = self.env['website'].search([], limit=1).menu_id
        legacy = self.env['website.menu'].sudo().search([
            ('name', '=', LEGACY_NAV_COUPS_LABEL),
            ('parent_id', '=', root.id),
        ])
        self.assertFalse(legacy, 'Coups de cœur ne doit plus figurer en navigation principale')

    def test_soin_bien_etre_nav_label_desktop(self):
        html = self._home_html()
        nav = self._header_nav_chunk(html)
        self.assertIn('Soin &amp; Bien-être', nav)
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
