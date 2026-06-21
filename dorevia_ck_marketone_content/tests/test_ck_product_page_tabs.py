# -*- coding: utf-8 -*-
"""Tests unitaires — blocs verticaux + ancres fiche produit CK."""

from markupsafe import Markup

from odoo.tests import tagged
from odoo.tests.common import TransactionCase

from odoo.addons.dorevia_ck_marketone_content.hooks import PRODUCT_WEBSITE_DESCRIPTIONS
from odoo.addons.dorevia_ck_marketone_content.product_page_tabs import (
    _sanitize_section_body,
    build_ck_product_page_tabs,
)


@tagged('post_install', '-at_install', 'dorevia_ck_product_page_tabs')
class TestCkProductPageTabs(TransactionCase):
    def test_sanitize_removes_markdown_asterisks(self):
        body = Markup('<p>*Usage :* tartines, yaourts.</p>')
        cleaned = str(_sanitize_section_body(body))
        self.assertNotIn('*Usage', cleaned)
        self.assertIn('Usage :', cleaned)

    def test_blocks_group_bootstrap_confiture(self):
        product = self.env['product.template'].create({
            'name': 'Confiture blocs QA',
            'type': 'consu',
            'list_price': 5.5,
            'sale_ok': True,
            'is_published': True,
            'website_description': PRODUCT_WEBSITE_DESCRIPTIONS['Confiture de goyave'],
            'description_ecommerce': 'Confiture artisanale — sélection épicerie créole CK.',
        })
        blocks = build_ck_product_page_tabs(product)
        keys = [block['key'] for block in blocks]
        self.assertIn('discover', keys)
        self.assertIn('composition', keys)
        self.assertIn('conservation', keys)
        discover = next(block for block in blocks if block['key'] == 'discover')
        self.assertEqual(discover['anchor_id'], 'ck-section-discover')
        self.assertEqual(discover['nav_label'], 'Découvrir')
        section_keys = [section['key'] for section in discover['sections']]
        self.assertIn('origin_usage', section_keys)
        self.assertIn('usage', section_keys)
        composition = next(block for block in blocks if block['key'] == 'composition')
        comp_keys = [section['key'] for section in composition['sections']]
        self.assertIn('ingredients', comp_keys)

    def test_details_block_includes_specs(self):
        product = self.env['product.template'].create({
            'name': 'Produit specs QA',
            'type': 'consu',
            'list_price': 4.0,
            'sale_ok': True,
            'is_published': True,
            'ck_net_quantity': 320,
            'ck_net_quantity_uom_id': self.env['dorevia.ck.card.uom'].sudo().search(
                [('code', '=', 'g')], limit=1,
            ).id,
            'ck_reference_price_uom_id': self.env['dorevia.ck.card.uom'].sudo().search(
                [('code', '=', 'kg')], limit=1,
            ).id,
            'ck_show_reference_price': True,
        })
        blocks = build_ck_product_page_tabs(product)
        details = next((block for block in blocks if block['key'] == 'details'), None)
        self.assertIsNotNone(details)
        self.assertEqual(details['nav_label'], 'Détails')
        labels = [row['label'] for row in details['specs']]
        self.assertIn('Contenance', labels)

    def test_composition_hidden_without_content(self):
        product = self.env['product.template'].create({
            'name': 'Snack sans composition',
            'type': 'consu',
            'list_price': 3.0,
            'sale_ok': True,
            'is_published': True,
            'website_description': (
                '<div class="ck-product-enrich">'
                '<h3>Origine &amp; usage</h3><p>Snack salé.</p>'
                '</div>'
            ),
        })
        blocks = build_ck_product_page_tabs(product)
        keys = [block['key'] for block in blocks]
        self.assertNotIn('composition', keys)

    def test_empty_product_no_blocks(self):
        product = self.env['product.template'].create({
            'name': 'Produit vide blocs',
            'type': 'consu',
            'list_price': 1.0,
            'sale_ok': True,
            'is_published': True,
        })
        self.assertEqual(build_ck_product_page_tabs(product), [])

    def test_model_bridge_get_ck_product_page_tabs(self):
        product = self.env['product.template'].create({
            'name': 'Bridge blocs',
            'type': 'consu',
            'list_price': 2.0,
            'sale_ok': True,
            'is_published': True,
            'website_description': PRODUCT_WEBSITE_DESCRIPTIONS['Confiture de goyave'],
        })
        blocks = product.get_ck_product_page_tabs()
        self.assertTrue(blocks)
        self.assertEqual(blocks[0]['key'], 'discover')
