# -*- coding: utf-8 -*-
"""Lot Nav-Shop — sync navigation catalogue dynamique + règle visibilité."""

from odoo.tests import tagged
from odoo.tests.common import TransactionCase

from odoo.addons.dorevia_ck_marketone_content.ck_product_placeholders import (
    CK_CREAM_PLACEHOLDER_PNG_B64,
)
from odoo.addons.dorevia_ck_marketone_content.nav_sync import (
    NAV_MOBILE_UNIVERS_LABEL,
    NAV_SHOP_ALL_LABEL,
    build_shop_nav_trees,
    get_nav_category_mapping,
    sync_ck_navigation_for_website,
    _category_has_published_products,
)


@tagged('post_install', '-at_install', 'dorevia_ck_marketone_nav_sync')
class TestCkNavSync(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.website = cls.env['website'].search([], limit=1)
        cls.Category = cls.env['product.public.category'].sudo()
        cls.Menu = cls.env['website.menu'].sudo()
        cls.root = cls.website.menu_id

    def _menu_by_name(self, name, parent=None):
        parent = parent or self.root
        return self.Menu.search([
            ('website_id', '=', self.website.id),
            ('parent_id', '=', parent.id),
            ('name', '=', name),
        ], limit=1)

    def _create_published_product(self, name, categories):
        return self.env['product.template'].sudo().create({
            'name': name,
            'type': 'consu',
            'is_published': True,
            'website_published': True,
            'sale_ok': True,
            'list_price': 5.0,
            'public_categ_ids': [(6, 0, categories.ids)],
            'image_1920': CK_CREAM_PLACEHOLDER_PNG_B64,
        })

    def test_category_empty_is_not_visible(self):
        cat = self.Category.create({'name': 'CK Nav Empty QA Cat'})
        self.assertFalse(_category_has_published_products(self.env, cat))

    def test_unpublished_product_hides_category_menu(self):
        cat = self.Category.create({'name': 'CK Nav Unpub QA Cat'})
        product = self.env['product.template'].sudo().create({
            'name': 'CK Nav Unpub QA Product',
            'type': 'consu',
            'is_published': False,
            'website_published': False,
            'sale_ok': True,
            'list_price': 4.5,
            'public_categ_ids': [(4, cat.id)],
            'image_1920': CK_CREAM_PLACEHOLDER_PNG_B64,
        })
        self.assertFalse(_category_has_published_products(self.env, cat))
        product.write({'is_published': True, 'website_published': True})
        self.assertTrue(_category_has_published_products(self.env, cat))

    def test_shop_nav_trees_from_public_categories(self):
        trees = build_shop_nav_trees(self.env, self.Category)
        self.assertTrue(trees, msg='Au moins une racine catalogue éligible attendue')
        names = [tree['name'] for tree in trees]
        self.assertIn('Épicerie', names)

    def test_level2_not_exposed_as_header_children_v22(self):
        """V2.2 — familles L2 dans mega-menu HTML, pas en website.menu enfants."""
        root_cat = self.Category.create({'name': 'CK Nav QA Root L2', 'sequence': 99990})
        child_cat = self.Category.create({
            'name': 'CK Nav QA Child L2',
            'parent_id': root_cat.id,
            'sequence': 1,
        })
        self._create_published_product('CK Nav QA Root Product', root_cat)
        self._create_published_product('CK Nav QA Child Product', child_cat)
        sync_ck_navigation_for_website(self.env, self.website)
        parent_menu = self._menu_by_name('CK Nav QA Root L2')
        self.assertFalse(parent_menu, msg='Racine QA ad hoc non gérée en N3 V2.2')
        self.assertFalse(self._menu_by_name('CK Nav QA Child L2', parent=self.root))

    def test_nav_shop_l2_seed_creates_subcategories(self):
        from odoo.addons.dorevia_ck_marketone_content.nav_shop_l2_seed import seed_nav_shop_l2_categories

        epicerie = self.Category.search([('name', '=', 'Épicerie'), ('parent_id', '=', False)], limit=1)
        if not epicerie:
            epicerie = self.Category.create({'name': 'Épicerie', 'sequence': 10000})
        seed_nav_shop_l2_categories(self.env)
        biscuits = self.Category.search([
            ('name', '=', 'Biscuits'),
            ('parent_id', '=', epicerie.id),
        ], limit=1)
        self.assertTrue(biscuits)

    def test_level3_not_in_header(self):
        root_cat = self.Category.create({'name': 'CK Nav QA Root L3', 'sequence': 99991})
        l2 = self.Category.create({'name': 'CK Nav QA L2 L3', 'parent_id': root_cat.id})
        l3 = self.Category.create({'name': 'CK Nav QA L3 Hidden', 'parent_id': l2.id})
        self._create_published_product('CK Nav QA L3 Product', l3)
        sync_ck_navigation_for_website(self.env, self.website)
        self.assertFalse(self._menu_by_name('CK Nav QA L3 Hidden'))

    def test_mobile_univers_group_removed_v22(self):
        sync_ck_navigation_for_website(self.env, self.website)
        self.assertFalse(self._menu_by_name(NAV_MOBILE_UNIVERS_LABEL))

    def test_public_user_can_read_category_shop_url_on_mega_menu(self):
        """Le header public peut résoudre l'URL catégorie d'un mega-menu rayon."""
        epicerie = self.Category.search([('name', '=', 'Épicerie'), ('parent_id', '=', False)], limit=1)
        if not epicerie:
            self.skipTest('Épicerie absente')
        if not _category_has_published_products(self.env, epicerie):
            self._create_published_product('CK Nav QA Epicerie', epicerie)
        sync_ck_navigation_for_website(self.env, self.website)
        menu = self._menu_by_name('Épicerie')
        if not menu:
            self.skipTest('Menu Épicerie non visible')
        public_menu = menu.with_user(self.env.ref('base.public_user'))
        self.assertIn('/shop/category/', public_menu._ck_nav_category_shop_url())

    def test_get_nav_category_mapping_has_dynamic_rows(self):
        mapping = get_nav_category_mapping(self.env)
        self.assertEqual(mapping[0]['menu_label'], NAV_SHOP_ALL_LABEL)
        level1 = [row for row in mapping if row.get('level') == 1]
        self.assertTrue(level1)
