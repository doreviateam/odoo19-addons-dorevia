# -*- coding: utf-8 -*-
"""S2 — entrées historiques V1 délèguent à la navigation catalogue V3."""

from odoo.tests import tagged
from odoo.tests.common import TransactionCase

from odoo.addons.dorevia_ck_marketone_content.nav_sync import (
    bootstrap_ck_navigation_v1,
    snapshot_ck_catalogue_navigation,
    sync_ck_catalogue_navigation_for_website,
    sync_ck_navigation_v1_for_website,
)
from odoo.addons.dorevia_ck_marketone_content.nav_v22_config import (
    NAV_CSS_N3_RAYON,
    NAV_CSS_SHOP_ROOT,
    NAV_PRO_PAGE_URL,
    NAV_V1_BOUTIQUE_LABEL,
    NAV_V1_PRODUCTEURS_LABEL,
    NAV_V1_PROFESSIONNELS_LABEL,
)


@tagged('post_install', '-at_install', 'dorevia_ck_nav_v1')
class TestCkNavV1Sync(TransactionCase):
    """V1 ne purge plus Épicerie : délègue à V3 catalogue."""

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
            self.env['website.page'].sudo().create({
                'name': 'Professionnels QA NAV002',
                'url': NAV_PRO_PAGE_URL,
                'is_published': True,
                'website_id': self.website.id,
            })

    def _ensure_pro_page_unpublished(self):
        page = self.env['website.page'].sudo().search([
            ('url', '=', NAV_PRO_PAGE_URL),
        ], limit=1)
        if page:
            page.write({'is_published': False})

    def test_v1_boutique_exists(self):
        sync_ck_navigation_v1_for_website(self.env, self.website)
        menu = self._menu_by_name(NAV_V1_BOUTIQUE_LABEL)
        self.assertTrue(menu, 'Boutique doit exister (délégation V3)')
        self.assertEqual(menu.url, '/shop')

    def test_v1_producteurs_exists(self):
        sync_ck_navigation_v1_for_website(self.env, self.website)
        menu = self._menu_by_name(NAV_V1_PRODUCTEURS_LABEL)
        self.assertTrue(menu, 'Producteurs doit exister (délégation V3)')
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

    def test_v1_no_mega_menus(self):
        sync_ck_navigation_v1_for_website(self.env, self.website)
        root_menus = self.Menu.search([
            ('website_id', '=', self.website.id),
            ('parent_id', '=', self.root.id),
        ])
        mega = root_menus.filtered('is_mega_menu')
        self.assertFalse(mega, 'Aucun mega-menu en racine après délégation V1→V3')

    def test_v1_does_not_purge_epicerie_when_exposable(self):
        """S2 : V1 ne doit plus supprimer Épicerie si la catégorie catalogue est exposable."""
        Category = self.env['product.public.category'].sudo()
        epicerie = Category.search([
            ('name', '=', 'Épicerie'),
            ('parent_id', '=', False),
        ], limit=1)
        if not epicerie or not epicerie._is_ck_exposable():
            self.skipTest('Épicerie exposable absente sur cette instance')
        sync_ck_navigation_v1_for_website(self.env, self.website)
        self.assertTrue(
            self._menu_by_name('Épicerie'),
            'Épicerie catalogue doit survivre à bootstrap_ck_navigation_v1',
        )

    def test_v1_communaute_kept_as_v3_root(self):
        """V1 délègue à V3 : Communauté devient racine éditoriale (S6-B1)."""
        self.Menu.search([
            ('website_id', '=', self.website.id),
            ('parent_id', '=', self.root.id),
            ('name', '=', 'Communauté'),
        ]).unlink()
        existing = self.Menu.create({
            'name': 'Communauté',
            'url': '#',
            'website_id': self.website.id,
            'parent_id': self.root.id,
            'sequence': 999,
        })
        sync_ck_navigation_v1_for_website(self.env, self.website)
        menu = self._menu_by_name('Communauté')
        self.assertTrue(menu)
        self.assertEqual(menu.id, existing.id)
        self.assertEqual(menu.sequence, 55)

    def test_v1_espace_pro_removed(self):
        self.Menu.create({
            'name': 'Espace pro',
            'url': '#',
            'website_id': self.website.id,
            'parent_id': self.root.id,
            'sequence': 999,
        })
        sync_ck_navigation_v1_for_website(self.env, self.website)
        self.assertFalse(self._menu_by_name('Espace pro'))

    def test_v1_boutique_shop_root_css(self):
        """V1 délègue à V3 : Boutique porte ck-nav-shop-root, pas un mega ni un rayon V2.2."""
        sync_ck_navigation_v1_for_website(self.env, self.website)
        menu = self._menu_by_name(NAV_V1_BOUTIQUE_LABEL)
        self.assertTrue(menu)
        css = (menu.ck_nav_css_class or '').split()
        self.assertIn(NAV_CSS_SHOP_ROOT, css)
        self.assertNotIn(NAV_CSS_N3_RAYON, css)
        self.assertFalse(menu.is_mega_menu)

    def test_v1_fixed_roots_order(self):
        self._ensure_pro_page_published()
        sync_ck_navigation_v1_for_website(self.env, self.website)
        boutique = self._menu_by_name(NAV_V1_BOUTIQUE_LABEL)
        producteurs = self._menu_by_name(NAV_V1_PRODUCTEURS_LABEL)
        professionnels = self._menu_by_name(NAV_V1_PROFESSIONNELS_LABEL)
        self.assertTrue(boutique and producteurs and professionnels)
        self.assertLess(boutique.sequence, producteurs.sequence)
        self.assertLess(producteurs.sequence, professionnels.sequence)

    def test_v1_delegates_same_state_as_v3(self):
        sync_ck_catalogue_navigation_for_website(self.env, self.website)
        expected = snapshot_ck_catalogue_navigation(self.env, self.website)
        sync_ck_navigation_v1_for_website(self.env, self.website)
        actual = snapshot_ck_catalogue_navigation(self.env, self.website)
        self.assertEqual(actual, expected)

    def test_v1_idempotent_structured(self):
        sync_ck_navigation_v1_for_website(self.env, self.website)
        before = snapshot_ck_catalogue_navigation(self.env, self.website)
        sync_ck_navigation_v1_for_website(self.env, self.website)
        after = snapshot_ck_catalogue_navigation(self.env, self.website)
        self.assertEqual(after, before)
        boutique_count = self.Menu.search_count([
            ('website_id', '=', self.website.id),
            ('parent_id', '=', self.root.id),
            ('name', '=', NAV_V1_BOUTIQUE_LABEL),
        ])
        self.assertEqual(boutique_count, 1)

    def test_v1_bootstrap_returns_count(self):
        count = bootstrap_ck_navigation_v1(self.env)
        self.assertGreaterEqual(count, 1)
