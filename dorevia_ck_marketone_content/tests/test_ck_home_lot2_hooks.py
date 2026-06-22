# -*- coding: utf-8 -*-
"""Tests hooks Lot 2 — vedettes home SSR sans placeholders."""

from odoo.tests import tagged
from odoo.tests.common import TransactionCase

from odoo.addons.dorevia_ck_marketone_content.home_featured import (
    _variant_has_valid_image,
    bootstrap_home_featured_products,
    card_fragment_is_valid,
    get_curated_featured_variants,
)
from odoo.addons.dorevia_ck_marketone_content.tests.ck_home_lot2_utils import (
    FEATURED_TEST_MIN_CARDS,
    clear_ck_is_featured,
    ensure_featured_catalog,
    restore_ck_is_featured,
)

from odoo.addons.dorevia_ck_marketone_content.ck_product_placeholders import (
    CK_CREAM_PLACEHOLDER_PNG_B64,
)


@tagged('post_install', '-at_install', 'dorevia_ck_marketone_home_lot2')
class TestCkHomeLot2Hooks(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls._featured_backup = clear_ck_is_featured(cls.env)
        ensure_featured_catalog(cls.env)

    @classmethod
    def tearDownClass(cls):
        restore_ck_is_featured(cls.env, cls._featured_backup)
        super().tearDownClass()

    def _homepage_arch(self):
        page = self.env['website.page'].search([('url', '=', '/')], limit=1)
        self.assertTrue(page)
        arch = page.view_id.arch_db
        if isinstance(arch, dict):
            arch = next(iter(arch.values()))
        return arch

    def test_card_fragment_validation(self):
        valid = (
            '<article class="ck-product-card product-card ck-product-card--interactive">'
            '<a href="/shop/demo-1" class="ck-product-card__cover card-cta" aria-label="Voir le produit : Demo">'
            '<div class="product-card-media" style="background-image:url(\'/web/image/product.template/1/image_512\')">'
            '</div></a><div class="product-card-foot">'
            '<span class="ck-product-card__price-value price">12,00 €</span>'
            '<div class="product-card-actions">'
            '<a href="/shop/demo-1" class="card-cta card-cta--secondary">Voir le produit</a>'
            '</div></div></article>'
        )
        self.assertTrue(card_fragment_is_valid(valid))
        self.assertFalse(card_fragment_is_valid(valid.replace('ck-product-card__price-value', '')))
        self.assertFalse(card_fragment_is_valid(valid.replace('/web/image/product.template/', '/web/image/website.s_cover_default_image')))

    def test_get_featured_variants_require_images(self):
        variants = get_curated_featured_variants(self.env)
        if len(variants) >= FEATURED_TEST_MIN_CARDS:
            for variant in variants:
                self.assertTrue(_variant_has_valid_image(variant))

    def _featured_section_slice(self, arch):
        marker = 'data-snippet="s_ck_featured_products"'
        pos = arch.find(marker)
        if pos < 0:
            return ''
        start = arch.rfind('<section', 0, pos)
        end = arch.find('</section>', pos)
        if start < 0 or end < 0:
            return ''
        return arch[start:end + len('</section>')]

    def test_bootstrap_hides_featured_when_no_featured_products(self):
        self.env['product.template'].sudo().search([('ck_is_featured', '=', True)]).write({
            'ck_is_featured': False,
        })
        bootstrap_home_featured_products(self.env)
        arch = self._homepage_arch()
        self.assertNotIn('ck-featured-products__grid--stable', arch)

    def test_bootstrap_injects_ssr_grid_with_images(self):
        ensure_featured_catalog(self.env)
        variants = get_curated_featured_variants(self.env)
        self.assertGreaterEqual(len(variants), FEATURED_TEST_MIN_CARDS)
        self.assertTrue(bootstrap_home_featured_products(self.env))
        arch = self._homepage_arch()
        self.assertIn('ck-featured-products__grid--stable', arch)
        self.assertIn('Nos coups de cœur', arch)
        self.assertIn('Toute la boutique', arch)
        self.assertNotIn('s_dynamic_snippet_products', arch)
        self.assertGreaterEqual(arch.count('ck-product-card'), FEATURED_TEST_MIN_CARDS)
        self.assertGreaterEqual(len(__import__('re').findall(r'href="/shop/[^"]+"', arch)), FEATURED_TEST_MIN_CARDS)

    def test_bootstrap_idempotent(self):
        ensure_featured_catalog(self.env)
        self.assertTrue(bootstrap_home_featured_products(self.env))
        arch_before = self._homepage_arch()
        bootstrap_home_featured_products(self.env)
        arch_after = self._homepage_arch()
        self.assertEqual(
            self._featured_section_slice(arch_before),
            self._featured_section_slice(arch_after),
        )
