# -*- coding: utf-8 -*-
"""Tests catalogue MOA — Manio Crackers (variantes) + Galettes séparées."""

from odoo.tests import tagged
from odoo.tests.common import TransactionCase

from odoo.addons.dorevia_ck_marketone_content.catalog_manioc_variants import (
    CRACKER_FORMAT_VALUES,
    FORMAT_ATTRIBUTE_NAME,
    GALETTES_TEMPLATE_NAME,
    MANIO_CRACKERS_PARENT_NAME,
    bootstrap_catalog_vedettes_products,
)
from odoo.addons.dorevia_ck_marketone_content.home_featured import (
    MIN_FEATURED_PRODUCTS,
    _get_featured_display_name,
    bootstrap_home_featured_products,
    get_ready_featured_variants,
)

_TINY_PNG = (
    b'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAADElEQVR4nGP4z8AAAAMBAQDJ/pLvAAAAAElFTkSuQmCC'
)


@tagged('post_install', '-at_install', 'dorevia_ck_marketone_catalog_manioc')
class TestCkCatalogManiocVariants(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        parent = cls.env['product.template'].sudo().search([
            ('name', '=', MANIO_CRACKERS_PARENT_NAME),
        ], limit=1)
        if not parent:
            cls.skipTest('Template Manio Crackers absent.')
        parent.write({'image_1920': _TINY_PNG})
        for variant in parent.product_variant_ids:
            variant.write({'image_1920': _TINY_PNG})
        cls.assertTrue(bootstrap_catalog_vedettes_products(cls.env))

    def test_manioc_crackers_parent_two_format_variants(self):
        parent = self.env['product.template'].sudo().search([
            ('name', '=', MANIO_CRACKERS_PARENT_NAME),
        ], limit=1)
        line = parent.attribute_line_ids.filtered(
            lambda l: l.attribute_id.name == FORMAT_ATTRIBUTE_NAME
        )
        self.assertTrue(line)
        self.assertEqual(len(parent.product_variant_ids), 2)
        value_names = line.value_ids.mapped('name')
        for expected in CRACKER_FORMAT_VALUES:
            self.assertIn(expected, value_names)
        self.assertNotIn(GALETTES_TEMPLATE_NAME, value_names)

    def test_galettes_is_separate_single_variant_template(self):
        galettes = self.env['product.template'].sudo().search([
            ('name', '=', GALETTES_TEMPLATE_NAME),
        ], limit=1)
        self.assertTrue(galettes)
        self.assertTrue(galettes.is_published)
        self.assertEqual(len(galettes.product_variant_ids), 1)
        self.assertFalse(galettes.attribute_line_ids)

    def test_featured_display_names_use_cracker_variant_labels(self):
        parent = self.env['product.template'].sudo().search([
            ('name', '=', MANIO_CRACKERS_PARENT_NAME),
        ], limit=1)
        names = {_get_featured_display_name(v) for v in parent.product_variant_ids}
        self.assertIn('Manio Crackers salé', names)
        self.assertIn('Manio Crackers sucré', names)

    def test_featured_selection_five_moa_products(self):
        variants = get_ready_featured_variants(self.env)
        labels = [_get_featured_display_name(v) for v in variants]
        self.assertGreaterEqual(len(variants), MIN_FEATURED_PRODUCTS)
        self.assertIn('Confiture de goyave', labels)
        self.assertIn('Manio Crackers salé', labels)
        self.assertIn('Manio Crackers sucré', labels)
        self.assertIn(GALETTES_TEMPLATE_NAME, labels)
        self.assertIn('Savon vétiver', labels)

    def test_home_featured_arch_matches_bo_catalog(self):
        bootstrap_home_featured_products(self.env)
        page = self.env['website.page'].search([('url', '=', '/')], limit=1)
        arch = page.view_id.arch_db
        if isinstance(arch, dict):
            arch = next(iter(arch.values()))
        start = arch.find('ck-featured-products')
        end = arch.find('s_ck_category_links', start)
        chunk = arch[start:end] if start >= 0 else arch
        self.assertIn('Manio Crackers salé', chunk)
        self.assertIn('Manio Crackers sucré', chunk)
        self.assertIn(GALETTES_TEMPLATE_NAME, chunk)
        self.assertIn('attribute_values=', chunk)
        self.assertNotIn('manio-crackers-sale-5', chunk)
