# -*- coding: utf-8 -*-
"""CK-NAV-002 — Navigation V1 simplifiée (Boutique · Producteurs · Professionnels)."""

from odoo.tests import tagged
from odoo.tests.common import TransactionCase

from odoo.addons.dorevia_ck_marketone_content.nav_sync import (
    bootstrap_ck_navigation_v1,
    sync_ck_navigation_v1_for_website,
)
from odoo.addons.dorevia_ck_marketone_content.nav_v22_config import (
    NAV_CSS_N3_RAYON,
    NAV_CSS_SHOP_ROOT,
    NAV_PRO_PAGE_URL,
    NAV_V1_BOUTIQUE_LABEL,
    NAV_V1_BOUTIQUE_SEQUENCE,
    NAV_V1_PRODUCTEURS_LABEL,
    NAV_V1_PRODUCTEURS_SEQUENCE,
    NAV_V1_PROFESSIONNELS_LABEL,
    NAV_V1_PROFESSIONNELS_SEQUENCE,
)


@tagged('post_install', '-at_install', 'dorevia_ck_nav_v1')
class TestCkNavV1Sync(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.website = cls.env['website'].search([], limit=1)
        cls.Menu = cls.env['website.menu'].sudo()
        cls.root = cls.website.menu_id

    def _menu_by_name(self, name):
        return self.Menu.search([
            ('website_id', '=', self.website.id),
            ('parent_id', '=', self.root.id),
            ('name', '=', name),
        ], limit=1)

    def _ensure_pro_page_published(self):
        page = self.env['website.page'].sudo().search([
            ('url', '=', NAV_PRO_PAGE_URL),
        ], limit=1)
        if page:
            page.write({'is_published': True})
        else:
            page = self.env['website.page'].sudo().create({
                'name': 'Professionnels QA NAV002',
                'url': NAV_PRO_PAGE_URL,
                'is_published': True,
                'website_id': self.website.id,
            })
        return page

    def _ensure_pro_page_unpublished(self):
        page = self.env['website.page'].sudo().search([
            ('url', '=', NAV_PRO_PAGE_URL),
        ], limit=1)
        if page:
            page.write({'is_published': False})

    # --- entrées V1 présentes ---

    def test_v1_boutique_exists(self):
        sync_ck_navigation_v1_for_website(self.env, self.website)
        menu = self._menu_by_name(NAV_V1_BOUTIQUE_LABEL)
        self.assertTrue(menu, 'Boutique doit exister en nav V1')
        self.assertEqual(menu.url, '/shop')

    def test_v1_producteurs_exists(self):
        sync_ck_navigation_v1_for_website(self.env, self.website)
        menu = self._menu_by_name(NAV_V1_PRODUCTEURS_LABEL)
        self.assertTrue(menu, 'Producteurs doit exister en nav V1')
        self.assertEqual(menu.url, '/producteurs')

    def test_v1_professionnels_visible_if_page_published(self):
        self._ensure_pro_page_published()
        sync_ck_navigation_v1_for_website(self.env, self.website)
        menu = self._menu_by_name(NAV_V1_PROFESSIONNELS_LABEL)
        self.assertTrue(menu, 'Professionnels doit exister si /professionnels est publiée')
        self.assertEqual(menu.url, NAV_PRO_PAGE_URL)

    def test_v1_professionnels_absent_if_page_unpublished(self):
        self._ensure_pro_page_unpublished()
        sync_ck_navigation_v1_for_website(self.env, self.website)
        menu = self._menu_by_name(NAV_V1_PROFESSIONNELS_LABEL)
        self.assertFalse(menu, 'Professionnels doit être absent si /professionnels non publiée')

    # --- mega-menus V2.2 absents ---

    def test_v1_no_mega_menus(self):
        sync_ck_navigation_v1_for_website(self.env, self.website)
        root_menus = self.Menu.search([
            ('website_id', '=', self.website.id),
            ('parent_id', '=', self.root.id),
        ])
        mega = root_menus.filtered('is_mega_menu')
        self.assertFalse(mega, 'Aucun mega-menu ne doit exister en racine après nav V1')

    def test_v1_epicerie_removed(self):
        sync_ck_navigation_v1_for_website(self.env, self.website)
        self.assertFalse(self._menu_by_name('Épicerie'))

    def test_v1_communaute_removed(self):
        sync_ck_navigation_v1_for_website(self.env, self.website)
        self.assertFalse(self._menu_by_name('Communauté'))

    def test_v1_espace_pro_removed(self):
        sync_ck_navigation_v1_for_website(self.env, self.website)
        self.assertFalse(self._menu_by_name('Espace pro'))

    # --- CSS propre sur les entrées V1 ---

    def test_v1_boutique_no_special_css(self):
        sync_ck_navigation_v1_for_website(self.env, self.website)
        menu = self._menu_by_name(NAV_V1_BOUTIQUE_LABEL)
        self.assertTrue(menu)
        css = (menu.ck_nav_css_class or '').split()
        self.assertNotIn(NAV_CSS_SHOP_ROOT, css, 'Boutique V1 ne doit pas porter ck-nav-shop-root')
        self.assertNotIn(NAV_CSS_N3_RAYON, css, 'Boutique V1 ne doit pas porter ck-nav-n3-rayon')
        self.assertFalse(menu.is_mega_menu, 'Boutique V1 ne doit pas être un mega-menu')

    # --- séquences ---

    def test_v1_order_sequence(self):
        self._ensure_pro_page_published()
        sync_ck_navigation_v1_for_website(self.env, self.website)
        boutique = self._menu_by_name(NAV_V1_BOUTIQUE_LABEL)
        producteurs = self._menu_by_name(NAV_V1_PRODUCTEURS_LABEL)
        professionnels = self._menu_by_name(NAV_V1_PROFESSIONNELS_LABEL)
        self.assertTrue(boutique and producteurs and professionnels)
        self.assertEqual(boutique.sequence, NAV_V1_BOUTIQUE_SEQUENCE)
        self.assertEqual(producteurs.sequence, NAV_V1_PRODUCTEURS_SEQUENCE)
        self.assertEqual(professionnels.sequence, NAV_V1_PROFESSIONNELS_SEQUENCE)
        self.assertLess(boutique.sequence, producteurs.sequence)
        self.assertLess(producteurs.sequence, professionnels.sequence)

    # --- idempotence ---

    def test_v1_idempotent(self):
        """Deux passages consécutifs ne créent pas de doublons."""
        sync_ck_navigation_v1_for_website(self.env, self.website)
        sync_ck_navigation_v1_for_website(self.env, self.website)
        boutique_count = self.Menu.search_count([
            ('website_id', '=', self.website.id),
            ('parent_id', '=', self.root.id),
            ('name', '=', NAV_V1_BOUTIQUE_LABEL),
        ])
        self.assertEqual(boutique_count, 1, 'Une seule entrée Boutique après double sync')

    # --- bootstrap multi-sites ---

    def test_v1_bootstrap_returns_count(self):
        count = bootstrap_ck_navigation_v1(self.env)
        self.assertGreaterEqual(count, 1)
