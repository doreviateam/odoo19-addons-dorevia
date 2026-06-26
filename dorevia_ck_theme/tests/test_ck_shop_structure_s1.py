# -*- coding: utf-8 -*-
"""Tests Lot S1 — Shop Structure V1 sobre (dorevia_ck_theme)."""

import re

from odoo.tests import tagged
from odoo.tests.common import HttpCase

from odoo.addons.dorevia_ck_marketone_content.hooks import EPICERIE_CATEGORY_NAME


@tagged('post_install', '-at_install', 'dorevia_ck_shop_s1')
class TestCkShopStructureS1(HttpCase):
    """Promesse CK, sidebar, compteur intro, non-régression catalogue."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        content = cls.env['ir.module.module'].sudo().search([
            ('name', '=', 'dorevia_ck_marketone_content'),
            ('state', '=', 'installed'),
        ], limit=1)
        if not content:
            raise cls.skipTest(
                'dorevia_ck_marketone_content non installé — recette shop S1 non applicable'
            )
        cls.category = cls.env['product.public.category'].search(
            [('name', '=', EPICERIE_CATEGORY_NAME)],
            limit=1,
        )

    def _shop_html(self, path='/shop'):
        resp = self.url_open(path)
        self.assertEqual(resp.status_code, 200, path)
        return resp.text

    def test_shop_intro_promise_and_wording(self):
        html = self._shop_html()
        self.assertIn('s_ck_shop_intro', html)
        self.assertIn('Boutique C-Kréyòl', html)
        self.assertIn(
            'Produits créoles sélectionnés, aux origines identifiées.',
            html,
        )
        self.assertNotIn('Boutique C-Kreyol', html)
        self.assertNotRegex(
            html,
            r'ck-shop-intro[\s\S]{0,800}(Nantes|livraison|Europe)',
            msg='Intro S1 : pas de promesse logistique',
        )

    def test_shop_counter_in_intro_not_toolbar(self):
        html = self._shop_html()
        intro = re.search(
            r'class="[^"]*s_ck_shop_intro[^"]*"[\s\S]*?</section>',
            html,
        )
        self.assertTrue(intro, 'Intro shop introuvable')
        intro_html = intro.group(0)
        self.assertIn('ck-shop-intro__note', intro_html)
        self.assertRegex(
            intro_html,
            r'\d+\s+produit',
            msg='Compteur dynamique attendu dans l’intro',
        )
        note = re.search(
            r'class="[^"]*ck-shop-intro__note[^"]*"[\s\S]*?</p>',
            intro_html,
        )
        self.assertTrue(note, 'Note compteur intro introuvable')
        self.assertIn('en rayon', note.group(0))
        self.assertNotIn('sélectionnés', note.group(0))
        self.assertNotIn('ck-shop-toolbar__count', html)

    def test_shop_sidebar_microcopy(self):
        """Note 07 Lot A : sidebar masquée, drawer filtres actif avec microcopy CK."""
        html = self._shop_html()
        # Sidebar masquée — Note 07 ajoute d-none sur aside#products_grid_before
        self.assertRegex(
            html,
            r'<aside\b[^>]*\bd-none\b[^>]*id="products_grid_before"'
            r'|<aside\b[^>]*id="products_grid_before"[^>]*\bd-none\b',
            msg='Sidebar #products_grid_before doit avoir d-none (Note 07 Lot A)',
        )
        # Drawer présent dans le DOM
        self.assertIn('o_wsale_offcanvas', html)
        # Microcopy drawer — sections filtres CK (Micro-lot 3B)
        self.assertIn('Origines', html)
        self.assertIn('Producteurs', html)
        self.assertIn('Préférences', html)
        if 'o_wsale_price_range_option' in html:
            self.assertIn('Budget</b>', html)

    def test_shop_native_tools_preserved(self):
        html = self._shop_html()
        self.assertIn('o_wsale_products_header', html)
        self.assertIn('o_wsale_categories_filmstrip', html)
        self.assertIn('ck-shop-sidebar', html)
        self.assertIn('o_wsale_products_grid', html)
        self.assertIn('ck-product-card--shop', html)
        self.assertIn('o_wsale_offcanvas', html)

    def test_category_epicerie_non_regression(self):
        if not self.category:
            self.skipTest('Catégorie Épicerie absente sur instance seed.')
        slug = self.env['ir.http'].sudo()._slug(self.category)
        path = f'/shop/category/{slug}'
        html = self._shop_html(path)
        self.assertIn('o_wsale_products_grid', html)
        self.assertRegex(
            html,
            r'id="o_wsale_products_grid"[\s\S]*oe_product',
            'Grille catégorie sans produit',
        )

    def test_shop_grid_four_columns_desktop(self):
        html = self._shop_html()
        self.assertRegex(html, r'--o-wsale-ppr:\s*4')
        self.assertIn('g-col-lg-3', html)

    def test_shop_no_horizontal_overflow_marker(self):
        html = self._shop_html()
        intro_count = len(re.findall(r'class="[^"]*s_ck_shop_intro', html))
        self.assertEqual(intro_count, 1, 'Intro shop dupliquée')
