# -*- coding: utf-8 -*-
"""S2 — Navigation V3 canonique : idempotence structurée, neutralisation V1/V2.2."""

from odoo.tests import tagged
from odoo.tests.common import TransactionCase

from odoo.addons.dorevia_ck_marketone_content.nav_sync import (
    NAV_MOBILE_UNIVERS_LABEL,
    bootstrap_ck_catalogue_navigation,
    bootstrap_ck_navigation,
    bootstrap_ck_navigation_v1,
    snapshot_ck_catalogue_navigation,
    sync_ck_catalogue_navigation_for_website,
    sync_ck_navigation_for_website,
    sync_ck_navigation_v1_for_website,
)
from odoo.addons.dorevia_ck_marketone_content.nav_v22_config import (
    NAV_CATALOGUE_BOUTIQUE_LABEL,
    NAV_CATALOGUE_PRODUCTEURS_LABEL,
    NAV_CATALOGUE_PROFESSIONNELS_LABEL,
    NAV_CATALOGUE_PROFESSIONNELS_URL,
    NAV_COMMUNAUTE_LABEL,
    NAV_ESPACE_PRO_LABEL,
    NAV_PRODUCTEURS_LABEL,
)


@tagged('post_install', '-at_install', 'dorevia_ck_nav_s2')
class TestCkNavS2CanonicalV3(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.website = cls.env['website'].search([], limit=1)
        cls.Menu = cls.env['website.menu'].sudo()
        cls.root = cls.website.menu_id
        Category = cls.env['product.public.category'].sudo()
        Product = cls.env['product.template'].sudo()

        cls.epicerie = Category.create({
            'name': 'Épicerie S2 Canon',
            'sequence': 800,
        })
        cls.sucree = Category.create({
            'name': 'Épicerie sucrée S2',
            'parent_id': cls.epicerie.id,
            'sequence': 10,
        })
        cls.salee = Category.create({
            'name': 'Épicerie salée S2',
            'parent_id': cls.epicerie.id,
            'sequence': 20,
        })
        cls.archived = Category.create({
            'name': 'Épicerie archivée S2',
            'sequence': 810,
            'ck_exposure_status': 'archived',
        })

        for cat in (cls.epicerie, cls.sucree, cls.salee, cls.archived):
            for idx in range(3):
                Product.create({
                    'name': f'Test S2 {cat.name} {idx}',
                    'sale_ok': True,
                    'is_published': True,
                    'website_published': True,
                    'public_categ_ids': [(4, cat.id)],
                })

        page = cls.env['website.page'].sudo().search([
            ('url', '=', NAV_CATALOGUE_PROFESSIONNELS_URL),
        ], limit=1)
        if page:
            page.write({'is_published': True})
        else:
            view = cls.env['ir.ui.view'].sudo().create({
                'name': 'Test Page S2 Pro',
                'type': 'qweb',
                'key': 'test.ck_nav_s2_pro',
                'arch': '<t t-name="test.ck_nav_s2"><div>/professionnels</div></t>',
            })
            cls.env['website.page'].sudo().create({
                'name': 'Professionnels S2',
                'url': NAV_CATALOGUE_PROFESSIONNELS_URL,
                'is_published': True,
                'website_id': cls.website.id,
                'view_id': view.id,
            })

    def _root_menu(self, name):
        return self.Menu.search([
            ('website_id', '=', self.website.id),
            ('parent_id', '=', self.root.id),
            ('name', '=', name),
        ], limit=1)

    def _sync(self):
        sync_ck_catalogue_navigation_for_website(self.env, self.website)

    def test_s2_first_creation_canonical_roots(self):
        self._sync()
        self.assertTrue(self._root_menu(NAV_CATALOGUE_BOUTIQUE_LABEL))
        self.assertTrue(self._root_menu(self.epicerie.name))
        self.assertTrue(self._root_menu(NAV_CATALOGUE_PRODUCTEURS_LABEL))
        self.assertTrue(self._root_menu(NAV_CATALOGUE_PROFESSIONNELS_LABEL))

        parent = self._root_menu(self.epicerie.name)
        child_names = set(parent.child_id.mapped('name'))
        self.assertEqual(child_names, {self.sucree.name, self.salee.name})

    def test_s2_structured_idempotence(self):
        self._sync()
        before = snapshot_ck_catalogue_navigation(self.env, self.website)
        self.assertTrue(before)
        self._sync()
        after = snapshot_ck_catalogue_navigation(self.env, self.website)
        self.assertEqual(after, before)

    def test_s2_no_duplicate_canonical_roots(self):
        self._sync()
        self._sync()
        for name in (
            NAV_CATALOGUE_BOUTIQUE_LABEL,
            self.epicerie.name,
            NAV_CATALOGUE_PRODUCTEURS_LABEL,
            NAV_CATALOGUE_PROFESSIONNELS_LABEL,
        ):
            count = self.Menu.search_count([
                ('website_id', '=', self.website.id),
                ('parent_id', '=', self.root.id),
                ('name', '=', name),
            ])
            self.assertEqual(count, 1, f'Un seul menu racine pour « {name} »')

    def test_s2_category_links_and_ids(self):
        self._sync()
        menu = self._root_menu(self.epicerie.name)
        self.assertEqual(menu.ck_nav_category_id.id, self.epicerie.id)
        self.assertIn('/shop/category/', menu.url or '')
        for child in menu.child_id:
            self.assertTrue(child.ck_nav_category_id)
            self.assertIn('/shop/category/', child.url or '')

    def test_s2_no_residual_v22_labels(self):
        for name in (NAV_COMMUNAUTE_LABEL, NAV_ESPACE_PRO_LABEL, NAV_PRODUCTEURS_LABEL):
            self.Menu.create({
                'name': name,
                'url': '#',
                'website_id': self.website.id,
                'parent_id': self.root.id,
                'sequence': 990,
                'is_mega_menu': True,
                'ck_nav_css_class': 'ck-nav-n3-rayon',
            })
        self._sync()
        self.assertFalse(self._root_menu(NAV_COMMUNAUTE_LABEL))
        self.assertFalse(self._root_menu(NAV_ESPACE_PRO_LABEL))
        self.assertFalse(self._root_menu(NAV_PRODUCTEURS_LABEL))  # « Nos producteurs »
        self.assertTrue(self._root_menu(NAV_CATALOGUE_PRODUCTEURS_LABEL))

    def test_s2_archived_category_absent(self):
        self._sync()
        self.assertFalse(self._root_menu(self.archived.name))

    def test_s2_bo_rename_menu_label_preserved_when_category_unchanged(self):
        """Doctrine : le libellé menu suit la catégorie ; une édition BO du name
        sans changement de catégorie est réalignée sur category.name au resync.
        """
        self._sync()
        menu = self._root_menu(self.epicerie.name)
        menu.write({'name': 'Libellé BO temporaire S2'})
        self._sync()
        menu_reloaded = self.Menu.browse(menu.id)
        self.assertEqual(menu_reloaded.name, self.epicerie.name)
        self.assertEqual(menu_reloaded.ck_nav_category_id.id, self.epicerie.id)

    def test_s2_bo_sequence_preserved(self):
        self._sync()
        menu = self._root_menu(self.epicerie.name)
        menu.write({'sequence': 4242})
        self._sync()
        self.assertEqual(self.Menu.browse(menu.id).sequence, 4242)

    def test_s2_v1_and_v22_entrypoints_delegate(self):
        self._sync()
        expected = snapshot_ck_catalogue_navigation(self.env, self.website)
        sync_ck_navigation_v1_for_website(self.env, self.website)
        self.assertEqual(
            snapshot_ck_catalogue_navigation(self.env, self.website),
            expected,
        )
        sync_ck_navigation_for_website(self.env, self.website)
        self.assertEqual(
            snapshot_ck_catalogue_navigation(self.env, self.website),
            expected,
        )

    def test_s2_bootstrap_aliases_same_count(self):
        c1 = bootstrap_ck_catalogue_navigation(self.env)
        c2 = bootstrap_ck_navigation(self.env)
        c3 = bootstrap_ck_navigation_v1(self.env)
        self.assertEqual(c1, c2)
        self.assertEqual(c2, c3)
        self.assertGreaterEqual(c1, 1)

    def test_s2_no_mobile_univers_group(self):
        self.Menu.create({
            'name': NAV_MOBILE_UNIVERS_LABEL,
            'url': '#',
            'website_id': self.website.id,
            'parent_id': self.root.id,
            'sequence': 995,
            'ck_nav_css_class': 'ck-nav-mobile-univers',
        })
        self._sync()
        self.assertFalse(self._root_menu(NAV_MOBILE_UNIVERS_LABEL))

    def test_s2_multi_website_if_available(self):
        Website = self.env['website'].sudo()
        if Website.search_count([]) < 2:
            second = Website.create({'name': 'S2 Second Site'})
        else:
            second = Website.search([('id', '!=', self.website.id)], limit=1)
        self.assertTrue(second.menu_id)
        ok = sync_ck_catalogue_navigation_for_website(self.env, second)
        self.assertTrue(ok)
        before = snapshot_ck_catalogue_navigation(self.env, second)
        sync_ck_catalogue_navigation_for_website(self.env, second)
        after = snapshot_ck_catalogue_navigation(self.env, second)
        self.assertEqual(after, before)
