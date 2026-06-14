# -*- coding: utf-8 -*-
"""Tests hooks Lot 2 — vedettes home SSR sans placeholders."""

from odoo.tests import tagged
from odoo.tests.common import TransactionCase

from odoo.addons.dorevia_ck_marketone_content.home_featured import (
    MIN_FEATURED_PRODUCTS,
    bootstrap_home_featured_products,
    card_fragment_is_valid,
    get_ready_featured_variants,
)

# PNG 1×1 valide (tests uniquement).
_TINY_PNG = (
    b'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAADElEQVR4nGP4z8AAAAMBAQDJ/pLvAAAAAElFTkSuQmCC'
)


@tagged('post_install', '-at_install', 'dorevia_ck_marketone_home_lot2')
class TestCkHomeLot2Hooks(TransactionCase):
    def _homepage_arch(self):
        page = self.env['website.page'].search([('url', '=', '/')], limit=1)
        self.assertTrue(page)
        arch = page.view_id.arch_db
        if isinstance(arch, dict):
            arch = next(iter(arch.values()))
        return arch

    def _assign_images_to_published_products(self, count=MIN_FEATURED_PRODUCTS):
        products = self.env['product.template'].search([
            ('is_published', '=', True),
            ('website_published', '=', True),
        ], limit=count)
        products.write({'image_1920': _TINY_PNG})
        return products.mapped('product_variant_id')

    def test_card_fragment_validation(self):
        valid = (
            '<a href="/shop/demo-1">'
            '<span class="oe_product_image_img" style="background-image: url(/web/image/product.product/1/image_512);"/>'
            '<span class="oe_currency_value">12.00</span></a>'
        )
        self.assertTrue(card_fragment_is_valid(valid))
        self.assertFalse(card_fragment_is_valid(valid.replace('oe_currency_value', '')))
        self.assertFalse(card_fragment_is_valid(valid.replace('/web/image/product.product/', '/web/image/website.s_cover_default_image')))

    def test_get_ready_variants_requires_images(self):
        variants = get_ready_featured_variants(self.env)
        if len(variants) >= MIN_FEATURED_PRODUCTS:
            for variant in variants:
                self.assertTrue(variant.product_tmpl_id.image_1920)

    def test_bootstrap_hides_featured_when_insufficient_images(self):
        self.env['product.template'].search([
            ('is_published', '=', True),
        ]).write({'image_1920': False})
        bootstrap_home_featured_products(self.env)
        arch = self._homepage_arch()
        self.assertNotIn('ck-featured-products__grid--stable', arch)

    def test_bootstrap_injects_ssr_grid_with_images(self):
        variants = self._assign_images_to_published_products(MIN_FEATURED_PRODUCTS)
        self.assertGreaterEqual(len(variants), MIN_FEATURED_PRODUCTS)
        self.assertTrue(bootstrap_home_featured_products(self.env))
        arch = self._homepage_arch()
        self.assertIn('ck-featured-products__grid--stable', arch)
        self.assertIn('Produits vedettes', arch)
        self.assertNotIn('s_dynamic_snippet_products', arch)
        self.assertGreaterEqual(arch.count('o_carousel_product_card'), MIN_FEATURED_PRODUCTS)
        self.assertGreaterEqual(len(__import__('re').findall(r'href="/shop/[^"]+"', arch)), MIN_FEATURED_PRODUCTS)

    def test_bootstrap_idempotent(self):
        self._assign_images_to_published_products(MIN_FEATURED_PRODUCTS)
        bootstrap_home_featured_products(self.env)
        arch_before = self._homepage_arch()
        bootstrap_home_featured_products(self.env)
        arch_after = self._homepage_arch()
        self.assertEqual(arch_before, arch_after)
