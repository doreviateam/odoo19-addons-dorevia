# -*- coding: utf-8 -*-
"""Tests HTTP Phase 3 — composition shop portable (dorevia_ck_theme)."""

import re

from odoo.tests import tagged
from odoo.tests.common import HttpCase

from odoo.addons.dorevia_ck_marketone_content.hooks import EPICERIE_CATEGORY_NAME


@tagged('post_install', '-at_install', 'dorevia_ck_theme_phase3')
class TestCkShopPhase3Compose(HttpCase):
    """Shop natif + blocs CK · non-régression home · vue module."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product = cls.env['product.template'].search(
            [('sale_ok', '=', True), ('is_published', '=', True)],
            limit=1,
        )
        if not cls.product:
            cls.product = cls.env['product.template'].create({
                'name': 'CK Theme Phase 3 Recette',
                'type': 'consu',
                'list_price': 9.9,
                'sale_ok': True,
                'is_published': True,
            })
        cls.category = cls.env['product.public.category'].search(
            [('name', '=', EPICERIE_CATEGORY_NAME)],
            limit=1,
        )
        if not cls.category:
            cls.category = cls.env['product.public.category'].create({
                'name': EPICERIE_CATEGORY_NAME,
            })
        cls.product.write({'public_categ_ids': [(4, cls.category.id)]})

    def test_module_compose_view_is_installed(self):
        view = self.env['ir.ui.view'].search([
            ('key', '=', 'dorevia_ck_theme.products_ck_shop_compose'),
        ], limit=1)
        self.assertTrue(view, 'Vue portable Phase 3 absente — -u dorevia_ck_theme requis.')

    def test_no_legacy_shell_compose_view(self):
        legacy = self.env['ir.ui.view'].search([
            ('key', '=', 'ck_marketone_phase3.shop_compose'),
        ])
        self.assertFalse(legacy, 'Vue shell legacy encore présente — migration Phase 3 incomplète.')

    def test_shop_http_200(self):
        self.assertEqual(self.url_open('/shop').status_code, 200)

    def test_shop_has_ck_scope_and_native_grid(self):
        content = self.url_open('/shop').content
        self.assertIn(b'ck-shop-page', content)
        self.assertIn(b'o_wsale_products_grid', content)

    def test_shop_has_phase3_compose_blocks(self):
        html = self.url_open('/shop').text
        self.assertIn('s_ck_shop_intro', html)
        self.assertIn('Boutique C-Kreyol', html)
        self.assertIn('s_ck_reassurance', html)
        self.assertIn('Producteurs et transformateurs repérés par CK.', html)
        self.assertIn('ck-shop-pro-signal', html)
        self.assertIn('href="/professionnels"', html)

    def test_shop_product_links_in_grid(self):
        html = self.url_open('/shop').text
        self.assertRegex(
            html,
            r'id="o_wsale_products_grid"[\s\S]*href="/shop/[^"]+-\d+"',
            'Grille shop sans lien produit publié.',
        )

    def test_home_has_no_shop_intro(self):
        html = self.url_open('/').text
        self.assertNotIn('s_ck_shop_intro', html, 'Intro shop ne doit pas fuiter sur la home.')

    def test_category_page_when_epicerie_exists(self):
        slug = self.env['ir.http'].sudo()._slug(self.category)
        response = self.url_open(f'/shop/category/{slug}')
        self.assertEqual(response.status_code, 200)
        html = response.text
        self.assertIn('o_wsale_category_description', html)
        self.assertRegex(
            html,
            r'id="o_wsale_products_grid"[\s\S]*oe_product',
            'Catégorie principale sans produit en grille.',
        )

    def test_shop_no_horizontal_overflow_marker(self):
        """Smoke : pas de double composition (legacy + module)."""
        html = self.url_open('/shop').text
        intro_count = len(re.findall(r'class="[^"]*s_ck_shop_intro', html))
        self.assertEqual(intro_count, 1, 'Intro shop dupliquée — vérifier vues coexistent.')
