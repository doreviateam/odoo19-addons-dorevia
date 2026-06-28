# -*- coding: utf-8 -*-
"""Tests Lot 1 boutique — card produit CK alignée vedettes home."""

import unittest

from odoo.tests import tagged
from odoo.tests.common import HttpCase, TransactionCase

from odoo.addons.dorevia_ck_marketone_content.home_featured import (
    _get_featured_card_metadata_line,
    _get_shop_card_secondary_line,
)


@tagged('post_install', '-at_install', 'dorevia_ck_shop_card')
class TestCkShopProductCardHooks(TransactionCase):
    def test_shop_card_view_installed(self):
        view = self.env['ir.ui.view'].search([
            ('key', '=', 'dorevia_ck_theme.products_item_ck_card'),
        ], limit=1)
        self.assertTrue(view)
        arch = view.arch_db if isinstance(view.arch_db, str) else str(view.arch_db)
        self.assertIn('ck-product-card--shop', arch)
        self.assertIn('ck-product-card__foot', arch)
        self.assertIn('ck-product-card__actions', arch)

        buttons = self.env['ir.ui.view'].search([
            ('key', '=', 'dorevia_ck_theme.shop_product_buttons_ck_card'),
        ], limit=1)
        self.assertTrue(buttons)
        btn_arch = buttons.arch_db if isinstance(buttons.arch_db, str) else str(buttons.arch_db)
        self.assertIn('card-cart-cta', btn_arch)
        self.assertIn('Ajouter au panier', btn_arch)
        self.assertNotIn('visually-hidden', btn_arch)
        self.assertNotIn('card-cta--secondary', btn_arch)

    def test_metadata_view_installed(self):
        view = self.env['ir.ui.view'].search([
            ('key', '=', 'dorevia_ck_marketone_content.products_item_ck_card_metadata'),
        ], limit=1)
        self.assertTrue(view)
        arch = view.arch_db if isinstance(view.arch_db, str) else str(view.arch_db)
        self.assertIn('get_ck_shop_card_metadata_line', arch)
        self.assertIn('ck-product-card__meta', arch)
        self.assertNotIn('ck-product-card__origin', arch)
        self.assertNotIn('get_ck_shop_card_origin_label', arch)

    def test_metadata_line_matches_home_canon(self):
        """La ligne meta boutique inclut l'origine — parité vedettes Home."""
        website = self.env['website'].search([], limit=1)
        product = self.env['product.template'].search([
            ('sale_ok', '=', True),
            ('is_published', '=', True),
        ], limit=1)
        self.assertTrue(product)
        variant = product.product_variant_id
        expected_home = _get_featured_card_metadata_line(self.env, website, variant)
        expected_shop = _get_shop_card_secondary_line(self.env, website, variant)
        self.assertEqual(product.get_ck_shop_card_metadata_line(variant), expected_shop)
        self.assertEqual(expected_shop, expected_home)


@tagged('post_install', '-at_install', 'dorevia_ck_shop_card')
class TestCkShopProductCardCompose(HttpCase):
    FR_HEADERS = {'Accept-Language': 'fr-FR,fr;q=0.9'}

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        from odoo.addons.dorevia_ck_marketone_content.home_featured import (
            bootstrap_home_featured_products,
        )
        bootstrap_home_featured_products(cls.env)
        cls.product = cls.env['product.template'].search(
            [('sale_ok', '=', True), ('is_published', '=', True)],
            limit=1,
        )
        if not cls.product:
            cls.product = cls.env['product.template'].create({
                'name': 'CK Shop Card Recette',
                'type': 'consu',
                'list_price': 12.5,
                'sale_ok': True,
                'is_published': True,
            })

    def _first_product_card_chunk(self, html):
        start = html.find('ck-product-card--shop')
        self.assertGreater(start, 0)
        return html[start:start + 12000]

    def _shop_html(self):
        return self.url_open('/shop', headers=self.FR_HEADERS).text

    def test_shop_card_structure_http(self):
        html = self._shop_html()
        chunk = self._first_product_card_chunk(html)
        self.assertIn('ck-product-card__title', chunk)
        self.assertIn('ck-product-card__foot', chunk)
        self.assertIn('ck-product-card__price', chunk)
        self.assertIn('ck-product-card__actions', chunk)
        self.assertIn('ck-product-card__image', chunk)

    def test_shop_card_ctas_french(self):
        html = self._shop_html()
        chunk = self._first_product_card_chunk(html)
        self.assertIn('Ajouter au panier', chunk)
        self.assertIn('card-cart-cta', chunk)
        self.assertNotIn('Add to Cart', chunk)
        self.assertNotIn('card-cta--secondary', chunk)

    def test_shop_card_cta_label_visible(self):
        """Le libellé panier ne doit pas être masqué (CTA unifié Home/Shop)."""
        html = self._shop_html()
        chunk = self._first_product_card_chunk(html)
        self.assertRegex(
            chunk,
            r'card-cart-cta__label[^>]*>Ajouter au panier</span>',
        )
        self.assertNotIn('card-cart-cta__label visually-hidden', chunk)

    def test_shop_card_product_link_via_title_or_image(self):
        """Accès fiche produit via image / titre — pas de second CTA en pied de card."""
        html = self._shop_html()
        chunk = self._first_product_card_chunk(html)
        self.assertRegex(chunk, r'oe_product_image_link|o_wsale_products_item_title')
        foot_start = chunk.find('ck-product-card__foot')
        self.assertGreater(foot_start, 0)
        foot = chunk[foot_start:foot_start + 2500]
        self.assertNotIn('Voir le produit', foot)
        self.assertNotIn('card-cta--secondary', foot)

    def test_shop_card_cart_cta_always_in_dom(self):
        """Le CTA panier ne doit pas dépendre du survol image (actions_onhover Odoo)."""
        html = self._shop_html()
        chunk = self._first_product_card_chunk(html)
        self.assertRegex(
            chunk,
            r'ck-product-card__foot[\s\S]{0,4000}Ajouter au panier',
        )

    def test_shop_card_image_zone(self):
        html = self._shop_html()
        chunk = self._first_product_card_chunk(html)
        self.assertIn('ck-product-card__image', chunk)
        self.assertRegex(chunk, r'oe_product_image_img|ck-product-card__image')

    def test_shop_card_no_description_sale_leak(self):
        html = self._shop_html()
        grid_start = html.find('o_wsale_products_grid')
        self.assertGreater(grid_start, 0)
        grid_chunk = html[grid_start:grid_start + 200000]
        self.assertNotIn('oe_subdescription', grid_chunk)

    def test_shop_card_no_separate_origin_label(self):
        """Pas de label origine séparé au-dessus du titre (canon Home)."""
        html = self._shop_html()
        chunk = self._first_product_card_chunk(html)
        self.assertNotIn('ck-product-card__origin', chunk)

    def test_shop_card_metadata_line_http(self):
        """Ligne meta boutique alignée home (origine · format · prix réf.)."""
        product = None
        expected = ''
        for template in self.env['product.template'].sudo().search([
            ('sale_ok', '=', True),
            ('is_published', '=', True),
            ('website_published', '=', True),
        ]):
            line = template.get_ck_shop_card_metadata_line(template.product_variant_id)
            if line:
                product = template
                expected = line
                break
        if not product:
            raise unittest.SkipTest('Aucun produit publié avec ligne meta card.')
        html = self._shop_html()
        chunk = self._first_product_card_chunk(html)
        self.assertIn('ck-product-card__meta', chunk)
        self.assertIn(expected, html)

    def test_shop_home_wishlist_non_regression(self):
        html = self._shop_html()
        chunk = self._first_product_card_chunk(html)
        self.assertIn('o_add_wishlist', chunk)
        self.assertIn('data-action="o_wishlist"', chunk)

    def test_shop_home_non_regression(self):
        html = self.url_open('/').text
        self.assertIn('ck-featured-products--maquette', html)
        self.assertIn('ck-product-card--home', html)
        self.assertIn('ck-product-card__meta', html)
        self.assertIn('card-cart-cta', html)
        self.assertIn('ck-product-card__title-link', html)

    def test_shop_grid_four_columns(self):
        """Grille catalogue — shop_ppr=4 (aligné Home 4 colonnes desktop)."""
        html = self._shop_html()
        self.assertRegex(html, r'--o-wsale-ppr:\s*4')
        self.assertIn('g-col-lg-3', html)
        website = self.env['website'].get_current_website()
        self.assertEqual(website.shop_ppr, 4)

    def test_shop_page_scope_unchanged(self):
        html = self._shop_html()
        self.assertIn('ck-shop-page', html)
        self.assertIn('ck-shop-intro--title-only', html)
        self.assertIn('o_wsale_products_grid', html)
