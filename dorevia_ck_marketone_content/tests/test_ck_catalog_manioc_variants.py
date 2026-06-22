# -*- coding: utf-8 -*-
"""Tests catalogue MOA — Manio Crackers (variantes) + Galettes séparées."""

import unittest

from odoo.tests import tagged
from odoo.tests.common import TransactionCase

from odoo.addons.dorevia_ck_marketone_content.catalog_manioc_variants import (
    CRACKER_FORMAT_VALUES,
    FORMAT_ATTRIBUTE_ALIASES,
    GALETTES_TEMPLATE_NAME,
    MANIO_CRACKERS_PARENT_NAME,
    bootstrap_catalog_vedettes_products,
    cracker_format_attribute_line,
)
from odoo.addons.dorevia_ck_marketone_content.home_featured import (
    _get_featured_display_name,
    _get_featured_price_label,
    bootstrap_home_featured_products,
    build_featured_product_card_html,
    get_curated_featured_variants,
)

from odoo.addons.dorevia_ck_marketone_content.ck_product_placeholders import (
    ensure_test_product_image,
    ensure_test_variant_images,
)

MOA_FEATURED_TEMPLATE_NAMES = (
    'Confiture de goyave',
    MANIO_CRACKERS_PARENT_NAME,
    GALETTES_TEMPLATE_NAME,
    'Savon vétiver',
)


def _names_include_salty(names):
    return any('sal' in (name or '').lower() for name in names)


def _names_include_sweet(names):
    return any('sucr' in (name or '').lower() for name in names)


def ensure_moa_featured_catalog(env):
    """Jeux MOA vedettes explicites — indépendant de la catégorie Coups de cœur seed."""
    Template = env['product.template'].sudo()
    Template.search([('ck_is_featured', '=', True)]).write({'ck_is_featured': False})
    for name in MOA_FEATURED_TEMPLATE_NAMES:
        template = Template.search([('name', '=', name)], limit=1)
        if not template:
            continue
        template.write({
            'ck_is_featured': True,
            'is_published': True,
            'website_published': True,
            'sale_ok': True,
        })
        ensure_test_product_image(template, 'image_1920')
        for variant in template.product_variant_ids:
            ensure_test_variant_images(variant)


@tagged('post_install', '-at_install', 'dorevia_ck_marketone_catalog_manioc')
class TestCkCatalogManiocVariants(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        parent = cls.env['product.template'].sudo().search([
            ('name', '=', MANIO_CRACKERS_PARENT_NAME),
        ], limit=1)
        if not parent:
            raise unittest.SkipTest('Template Manio Crackers absent.')
        ensure_test_product_image(parent, 'image_1920')
        for variant in parent.product_variant_ids:
            ensure_test_variant_images(variant)
        if not bootstrap_catalog_vedettes_products(cls.env):
            raise unittest.SkipTest('Bootstrap catalogue vedettes MOA impossible.')

    def test_manioc_crackers_parent_two_format_variants(self):
        parent = self.env['product.template'].sudo().search([
            ('name', '=', MANIO_CRACKERS_PARENT_NAME),
        ], limit=1)
        line = cracker_format_attribute_line(parent)
        self.assertTrue(line)
        self.assertIn(line.attribute_id.name, FORMAT_ATTRIBUTE_ALIASES)
        self.assertEqual(len(parent.product_variant_ids), 2)
        value_names = line.value_ids.mapped('name')
        self.assertTrue(_names_include_salty(value_names))
        self.assertTrue(_names_include_sweet(value_names))
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
        self.assertTrue(_names_include_salty(names))
        self.assertTrue(_names_include_sweet(names))

    def test_featured_selection_five_moa_products(self):
        ensure_moa_featured_catalog(self.env)
        variants = get_curated_featured_variants(self.env)
        labels = [_get_featured_display_name(v) for v in variants]
        self.assertGreaterEqual(len(variants), 5)
        self.assertIn('Confiture de goyave', labels)
        self.assertTrue(_names_include_salty(labels))
        self.assertTrue(_names_include_sweet(labels))
        self.assertIn(GALETTES_TEMPLATE_NAME, labels)
        self.assertIn('Savon vétiver', labels)

    def test_featured_price_uses_variant_lst_price_without_pricelist(self):
        """Sans pricelist publique, chaque card doit refléter le lst_price de sa variante."""
        parent = self.env['product.template'].sudo().search([
            ('name', '=', MANIO_CRACKERS_PARENT_NAME),
        ], limit=1)
        sale = parent.product_variant_ids.filtered(
            lambda v: 'sucr' not in (v.display_name or '').lower()
            and 'sal' in (v.display_name or '').lower()
        )[:1]
        sweet = parent.product_variant_ids.filtered(
            lambda v: 'sucr' in (v.display_name or '').lower()
        )[:1]
        self.assertTrue(sale and sweet)
        self.assertAlmostEqual(sale.lst_price, 3.6)
        self.assertAlmostEqual(sweet.lst_price, 3.5)
        website = self.env['website'].search([], limit=1)
        self.assertEqual(_get_featured_price_label(self.env, website, sale), '3,60\u00a0€')
        self.assertEqual(_get_featured_price_label(self.env, website, sweet), '3,50\u00a0€')
        sale_card = build_featured_product_card_html(self.env, website, sale)
        sweet_card = build_featured_product_card_html(self.env, website, sweet)
        self.assertIn('3,60', sale_card)
        self.assertIn('3,50', sweet_card)
        self.assertIn(f'data-product-id="{sale.id}"', sale_card)
        self.assertIn(f'data-product-id="{sweet.id}"', sweet_card)

    def test_home_featured_arch_matches_bo_catalog(self):
        ensure_moa_featured_catalog(self.env)
        bootstrap_home_featured_products(self.env)
        page = self.env['website.page'].search([('url', '=', '/')], limit=1)
        arch = page.view_id.arch_db
        if isinstance(arch, dict):
            arch = next(iter(arch.values()))
        start = arch.find('ck-featured-products')
        end = arch.find('s_ck_category_links', start)
        chunk = arch[start:end] if start >= 0 else arch
        self.assertTrue(_names_include_salty([chunk]))
        self.assertTrue(_names_include_sweet([chunk]))
        self.assertIn(GALETTES_TEMPLATE_NAME, chunk)
        self.assertIn('attribute_values=', chunk)
        self.assertNotIn('manio-crackers-sale-5', chunk)
