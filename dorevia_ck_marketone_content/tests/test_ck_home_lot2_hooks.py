# -*- coding: utf-8 -*-
"""Tests hooks Lot 2 — vedettes home SSR sans placeholders."""

from odoo.tests import tagged
from odoo.tests.common import TransactionCase

from odoo.addons.dorevia_ck_marketone_content.home_featured import (
    MIN_FEATURED_PRODUCTS,
    _variant_has_valid_image,
    bootstrap_home_featured_products,
    card_fragment_is_valid,
    get_ready_featured_variants,
)
from odoo.addons.dorevia_ck_marketone_content.tests.ck_home_lot2_utils import (
    detach_featured_curation,
    ensure_auto_featured_catalog,
    restore_featured_curation,
)

from odoo.addons.dorevia_ck_marketone_content.ck_product_placeholders import (
    CK_CREAM_PLACEHOLDER_PNG_B64,
)


@tagged('post_install', '-at_install', 'dorevia_ck_marketone_home_lot2')
class TestCkHomeLot2Hooks(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Lot2 option B : chemin auto + seuil MIN_FEATURED_PRODUCTS (pas la curation BO).
        cls._curation_backup = detach_featured_curation(cls.env)
        ensure_auto_featured_catalog(cls.env)

    @classmethod
    def tearDownClass(cls):
        restore_featured_curation(cls.env, cls._curation_backup)
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
            '<a href="/shop/demo-1" class="ck-product-card__cover" aria-label="Voir le produit : Demo"></a>'
            '<div class="product-card-media" style="background-image:url(\'/web/image/product.template/1/image_512\')">'
            '</div><div class="product-card-foot"><span class="price">12,00 €</span>'
            '<div class="product-card-actions">'
            '<a href="/shop/demo-1" class="card-cta card-cta--secondary">Voir le produit</a>'
            '</div></div></article>'
        )
        self.assertTrue(card_fragment_is_valid(valid))
        self.assertFalse(card_fragment_is_valid(valid.replace('class="price"', '')))
        self.assertFalse(card_fragment_is_valid(valid.replace('/web/image/product.template/', '/web/image/website.s_cover_default_image')))

    def test_get_ready_variants_requires_images(self):
        variants = get_ready_featured_variants(self.env)
        if len(variants) >= MIN_FEATURED_PRODUCTS:
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

    def test_bootstrap_hides_featured_when_insufficient_images(self):
        templates = self.env['product.template'].search([('is_published', '=', True)])
        templates.write({'image_1920': False})
        attachment = self.env['ir.attachment'].sudo()
        for model_name, record_ids in (
            ('product.template', templates.ids),
            ('product.product', templates.mapped('product_variant_ids').ids),
        ):
            if record_ids:
                attachment.search([
                    ('res_model', '=', model_name),
                    ('res_id', 'in', record_ids),
                    ('res_field', 'like', 'image_%'),
                ]).unlink()
        templates.invalidate_recordset()
        templates.mapped('product_variant_ids').invalidate_recordset()
        bootstrap_home_featured_products(self.env)
        arch = self._homepage_arch()
        self.assertNotIn('ck-featured-products__grid--stable', arch)

    def test_bootstrap_injects_ssr_grid_with_images(self):
        ensure_auto_featured_catalog(self.env)
        variants = get_ready_featured_variants(self.env)
        self.assertGreaterEqual(len(variants), MIN_FEATURED_PRODUCTS)
        self.assertTrue(bootstrap_home_featured_products(self.env))
        arch = self._homepage_arch()
        self.assertIn('ck-featured-products__grid--stable', arch)
        self.assertIn('Nos coups de cœur', arch)
        self.assertIn('Toute la boutique', arch)
        self.assertNotIn('s_dynamic_snippet_products', arch)
        self.assertGreaterEqual(arch.count('ck-product-card'), MIN_FEATURED_PRODUCTS)
        self.assertGreaterEqual(len(__import__('re').findall(r'href="/shop/[^"]+"', arch)), MIN_FEATURED_PRODUCTS)

    def test_bootstrap_idempotent(self):
        ensure_auto_featured_catalog(self.env)
        self.assertTrue(bootstrap_home_featured_products(self.env))
        arch_before = self._homepage_arch()
        bootstrap_home_featured_products(self.env)
        arch_after = self._homepage_arch()
        self.assertEqual(
            self._featured_section_slice(arch_before),
            self._featured_section_slice(arch_after),
        )
