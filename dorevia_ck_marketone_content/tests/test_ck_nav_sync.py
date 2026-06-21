# -*- coding: utf-8 -*-
"""Lot Nav-1 — sync navigation + règle visibilité catégories."""

from odoo.tests import tagged
from odoo.tests.common import TransactionCase

from odoo.addons.dorevia_ck_marketone_content.ck_product_placeholders import (
    CK_CREAM_PLACEHOLDER_PNG_B64,
)
from odoo.addons.dorevia_ck_marketone_content.nav_sync import (
    NAV_DECOUVRIR_LABEL,
    NAV_MOBILE_UNIVERS_LABEL,
    NAV_SHOP_ALL_LABEL,
    bootstrap_ck_navigation,
    get_nav_category_mapping,
    sync_ck_navigation_for_website,
    _category_has_published_products,
    _find_public_category,
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

    def test_bootstrap_creates_nav_v2_structure(self):
        bootstrap_ck_navigation(self.env)
        self.assertTrue(self._menu_by_name(NAV_SHOP_ALL_LABEL))
        decouvrir = self._menu_by_name(NAV_DECOUVRIR_LABEL)
        self.assertTrue(decouvrir)
        self.assertTrue(decouvrir.is_mega_menu)
        self.assertIn('/professionnels', decouvrir.mega_menu_content or '')
        self.assertIn('/contactus', decouvrir.mega_menu_content or '')
        self.assertNotIn('Épicerie créole', decouvrir.mega_menu_content or '')

    def test_legacy_top_level_professionnels_hidden(self):
        bootstrap_ck_navigation(self.env)
        legacy = self.Menu.search([
            ('website_id', '=', self.website.id),
            ('parent_id', '=', self.root.id),
            ('name', '=', 'Professionnels'),
        ])
        self.assertFalse(legacy)

    def test_mobile_univers_group_when_category_visible(self):
        cat = _find_public_category(self.Category, ('Épicerie créole', 'Épicerie'))
        if not cat:
            self.skipTest('Catégorie Épicerie absente sur instance seed.')
        if not _category_has_published_products(self.env, cat):
            self.skipTest('Épicerie sans produit publié — skip groupe mobile.')
        sync_ck_navigation_for_website(self.env, self.website)
        mobile = self._menu_by_name(NAV_MOBILE_UNIVERS_LABEL)
        self.assertTrue(mobile)
        child = self._menu_by_name('Épicerie', parent=mobile)
        self.assertTrue(child)
        self.assertEqual(child.url, cat and self.env['ir.http'].sudo()._slug(cat) and
                        f'/shop/category/{self.env["ir.http"].sudo()._slug(cat)}')

    def test_soin_bien_etre_label_on_desktop_menu(self):
        bootstrap_ck_navigation(self.env)
        menu = self._menu_by_name('Soin & Bien-être')
        if not menu:
            cat = _find_public_category(
                self.Category,
                ('Maison & bien-être', 'Soin & bien-être', 'Soin'),
            )
            if cat and _category_has_published_products(self.env, cat):
                self.fail('Menu Soin & Bien-être absent alors que catégorie exploitable.')
            self.skipTest('Catégorie Soin non exploitable — menu masqué conforme MOA.')
        self.assertEqual(menu.name, 'Soin & Bien-être')
        self.assertEqual(menu.ck_nav_css_class, 'ck-nav-desktop-universe')
