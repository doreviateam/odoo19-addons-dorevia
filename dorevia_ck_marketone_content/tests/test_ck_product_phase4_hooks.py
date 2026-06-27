# -*- coding: utf-8 -*-
"""Tests hooks Phase 4 — bootstrap descriptions produit."""

from odoo.tests import tagged
from odoo.tests.common import TransactionCase

from odoo.addons.dorevia_ck_marketone_content.hooks import bootstrap_published_products


@tagged('post_install', '-at_install', 'dorevia_ck_theme_phase4')
class TestCkProductPhase4Hooks(TransactionCase):
    def test_bootstrap_fills_empty_website_description(self):
        product = self.env['product.template'].create({
            'name': 'Confiture de goyave QA',
            'type': 'consu',
            'list_price': 8.9,
            'sale_ok': True,
            'is_published': True,
        })
        count = bootstrap_published_products(self.env)
        product.invalidate_recordset()
        self.assertGreaterEqual(count, 1)
        self.assertIn('ck-product-enrich', product.website_description or '')
        self.assertIn('Conservation', product.website_description or '')

    def test_bootstrap_preserves_existing_description(self):
        custom = '<p>Description MOA custom produit</p>'
        product = self.env['product.template'].create({
            'name': 'Produit QA preserve',
            'type': 'consu',
            'list_price': 5.0,
            'sale_ok': True,
            'is_published': True,
            'website_description': custom,
        })
        bootstrap_published_products(self.env)
        self.assertEqual(product.website_description, custom)

    def test_bootstrap_skips_website_description_when_v11_fields(self):
        product = self.env['product.template'].create({
            'name': 'Confiture de goyave QA v11',
            'type': 'consu',
            'list_price': 8.9,
            'sale_ok': True,
            'is_published': True,
            'ck_discover_html': '<p>Contenu V1.1 MOA.</p>',
        })
        bootstrap_published_products(self.env)
        product.invalidate_recordset()
        self.assertFalse((product.website_description or '').strip())

    def test_bootstrap_does_not_seed_manio_crackers_content(self):
        product = self.env['product.template'].create({
            'name': 'Manio Crackers QA bootstrap',
            'type': 'consu',
            'list_price': 3.6,
            'sale_ok': True,
            'is_published': True,
        })
        bootstrap_published_products(self.env)
        product.invalidate_recordset()
        self.assertFalse((product.website_description or '').strip())
        self.assertNotIn('ck-product-enrich', product.website_description or '')
        self.assertFalse((product.description_ecommerce or '').strip())
