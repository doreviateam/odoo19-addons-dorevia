# -*- coding: utf-8 -*-
"""Tests Lot 1 boutique — card produit CK alignée vedettes home."""

import re
import unittest

from odoo.tests import tagged
from odoo.tests.common import HttpCase, TransactionCase

from odoo.addons.dorevia_ck_marketone_content.home_featured import (
    _build_featured_rating_html,
    _get_featured_card_metadata_line,
    _get_featured_display_name,
    _get_shop_card_secondary_line,
    bootstrap_home_featured_products,
    build_featured_product_card_html,
    get_curated_featured_variants,
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

    def test_rating_u2_shop_view_installed(self):
        view = self.env['ir.ui.view'].search([
            ('key', '=', 'dorevia_ck_theme.products_item_ck_card_rating'),
        ], limit=1)
        self.assertTrue(view)
        arch = view.arch_db if isinstance(view.arch_db, str) else str(view.arch_db)
        self.assertIn('ck-card-rating', arch)
        self.assertIn('rating_count', arch)
        self.assertIn('visually-hidden', arch)

    def test_rating_u2_featured_rating_html(self):
        product = self.env['product.template'].create({
            'name': 'Rating U2 unit',
            'type': 'consu',
            'list_price': 5.0,
            'sale_ok': True,
        })
        self.assertEqual(_build_featured_rating_html(product), '')

        partner = self.env['res.partner'].sudo().create({
            'name': 'Client QA Rating-U2',
            'email': 'qa-rating-u2@example.test',
        })
        rating = self.env['rating.rating'].sudo().create({
            'res_model_id': self.env['ir.model'].sudo()._get('product.template').id,
            'res_model': 'product.template',
            'res_id': product.id,
            'partner_id': partner.id,
            'rated_partner_id': self.env.company.partner_id.id,
            'publisher_id': self.env.company.partner_id.id,
        })
        product.sudo().rating_apply(4.8, rating=rating, feedback='Recette U2.')
        product.invalidate_recordset(['rating_count', 'rating_avg'])

        html = _build_featured_rating_html(product)
        self.assertIn('ck-card-rating', html)
        self.assertIn('4,8', html)
        self.assertNotIn('4.8', html)
        self.assertIn('1 avis', html)
        self.assertIn('visually-hidden', html)
        self.assertIn('aria-hidden="true"', html)


@tagged('post_install', '-at_install', 'dorevia_ck_shop_card')
class TestCkShopProductCardCompose(HttpCase):
    FR_HEADERS = {'Accept-Language': 'fr-FR,fr;q=0.9'}

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
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

    def _apply_product_rating(self, product, rate=4.8, feedback='Avis QA Rating-U2.'):
        partner = self.env['res.partner'].sudo().create({
            'name': 'Client QA Rating-U2 HTTP',
            'email': 'qa-rating-u2-http@example.test',
        })
        rating = self.env['rating.rating'].sudo().create({
            'res_model_id': self.env['ir.model'].sudo()._get('product.template').id,
            'res_model': 'product.template',
            'res_id': product.id,
            'partner_id': partner.id,
            'rated_partner_id': self.env.company.partner_id.id,
            'publisher_id': self.env.company.partner_id.id,
        })
        product.sudo().rating_apply(rate, rating=rating, feedback=feedback)
        product.invalidate_recordset(['rating_count', 'rating_avg'])
        return rating

    def _card_chunk_for_product(self, html, product_name):
        grid_start = html.find('o_wsale_products_grid')
        self.assertGreater(grid_start, 0, 'Grille shop absente')
        grid_html = html[grid_start:grid_start + 300000]
        idx = grid_html.find(product_name)
        self.assertGreater(idx, 0, f'Produit {product_name!r} absent de la grille /shop')
        window_start = max(0, idx - 12000)
        window = grid_html[window_start:idx + 8000]
        rel_idx = idx - window_start
        for marker in ('ck-product-card--shop', 'oe_product_cart'):
            start = window.rfind(marker, 0, rel_idx)
            if start >= 0:
                return window[start:]
        self.fail(f'Card shop introuvable autour de {product_name!r}')

    def _first_shop_product_on_page(self):
        html = self._shop_html()
        chunk = self._first_product_card_chunk(html)
        match = re.search(
            r'ck-product-card__title[^>]*>.*?<a[^>]*>.*?<span[^>]*>([^<]+)</span>',
            chunk,
            re.S,
        )
        if not match:
            match = re.search(
                r'o_wsale_products_item_title[^>]*>.*?<a[^>]*>.*?<span[^>]*>([^<]+)</span>',
                chunk,
                re.S,
            )
        self.assertTrue(match, 'Titre produit introuvable sur la première card /shop')
        name = match.group(1).strip()
        product = self.env['product.template'].sudo().search([
            ('name', '=', name),
            ('is_published', '=', True),
        ], limit=1)
        if not product:
            product = self.env['product.template'].sudo().search([
                ('name', 'ilike', name),
                ('is_published', '=', True),
            ], limit=1)
        self.assertTrue(product, f'Produit {name!r} introuvable en BO')
        return product, name

    def _shop_card_html_for_product(self, product, display_name=None):
        display_name = display_name or product.name
        html = self.url_open('/shop', headers=self.FR_HEADERS).text
        return self._card_chunk_for_product(html, display_name)

    def test_rating_u2_shop_card_with_reviews(self):
        product, display_name = self._first_shop_product_on_page()
        product.rating_ids.sudo().unlink()
        self._apply_product_rating(product, rate=4.8)
        for _i in range(11):
            self._apply_product_rating(product, rate=5)

        chunk = self._shop_card_html_for_product(product, display_name)
        self.assertIn('ck-card-rating', chunk)
        self.assertIn('ck-rating-value', chunk)
        self.assertRegex(chunk, r'4,8|5[^0-9,<]')
        self.assertIn('12 avis', chunk)
        self.assertIn('visually-hidden', chunk)
        self.assertIn('Note ', chunk)
        self.assertIn(' sur 5', chunk)
        self.assertLess(chunk.index('ck-product-card__title'), chunk.index('ck-card-rating'))

    def test_rating_u2_shop_card_without_reviews(self):
        html = self.url_open('/shop', headers=self.FR_HEADERS).text
        for product in self.env['product.template'].sudo().search([
            ('is_published', '=', True),
            ('website_published', '=', True),
        ], limit=40):
            if product.rating_count or product.name not in html:
                continue
            chunk = self._card_chunk_for_product(html, product.name)
            self.assertNotIn('ck-card-rating', chunk)
            self.assertIn('ck-product-card__title', chunk)
            return
        raise unittest.SkipTest('Aucun produit publié sans avis visible sur /shop.')

    def test_rating_u2_home_featured_with_reviews_after_bootstrap(self):
        variants = get_curated_featured_variants(self.env)
        if not variants:
            raise unittest.SkipTest('Aucune vedette pour recette home.')
        variant = variants[0]
        product = variant.product_tmpl_id
        display_name = _get_featured_display_name(variant)
        product.rating_ids.sudo().unlink()
        self._apply_product_rating(product, rate=5)
        bootstrap_home_featured_products(self.env)

        html = self.url_open('/', headers=self.FR_HEADERS).text
        self.assertIn(display_name, html)
        start = html.find(display_name)
        chunk = html[html.rfind('ck-product-card--home', 0, start):start + 4000]
        self.assertIn('ck-card-rating', chunk)
        self.assertIn('1 avis', chunk)
        self.assertIn('visually-hidden', chunk)

    def test_rating_u2_home_featured_without_reviews(self):
        website = self.env['website'].get_current_website()
        variant = self.env['product.product'].sudo().create({
            'name': 'Rating U2 Home SSR Sans Avis',
            'type': 'consu',
            'list_price': 6.0,
            'sale_ok': True,
        })
        template = variant.product_tmpl_id
        template.write({'is_published': True, 'website_published': True})
        card_html = build_featured_product_card_html(self.env, website, variant)
        self.assertNotIn('ck-card-rating', card_html)
        self.assertIn('ck-product-card__title', card_html)
