# -*- coding: utf-8 -*-
"""Tests unitaires — sections bas de fiche produit CK Lot 2."""

from markupsafe import Markup

from odoo.tests import tagged
from odoo.tests.common import TransactionCase

from odoo.addons.dorevia_ck_marketone_content.hooks import (
    PRODUCT_WEBSITE_DESCRIPTIONS,
    bootstrap_published_products,
)
from odoo.addons.dorevia_ck_marketone_content.product_page_details import (
    build_ck_product_page_detail_sections,
)


@tagged('post_install', '-at_install', 'dorevia_ck_product_page_lot2')
class TestCkProductPageDetails(TransactionCase):
    def _sections(self, product):
        return build_ck_product_page_detail_sections(product)

    def test_parse_bootstrap_confiture_sections(self):
        product = self.env['product.template'].create({
            'name': 'Confiture de goyave QA Lot2',
            'type': 'consu',
            'list_price': 8.9,
            'sale_ok': True,
            'is_published': True,
        })
        bootstrap_published_products(self.env)
        product.invalidate_recordset()
        sections = self._sections(product)
        keys = [section['key'] for section in sections]
        self.assertIn('origin_usage', keys)
        self.assertIn('usage', keys)
        self.assertIn('conservation', keys)
        origin = next(section for section in sections if section['key'] == 'origin_usage')
        self.assertEqual(origin['title'], 'Origine & usage')
        self.assertIn('goyave', str(origin['body']).lower())

    def test_empty_product_returns_no_sections(self):
        product = self.env['product.template'].create({
            'name': 'Produit vide Lot2',
            'type': 'consu',
            'list_price': 1.0,
            'sale_ok': True,
            'is_published': True,
        })
        self.assertEqual(self._sections(product), [])

    def test_description_sale_fallback(self):
        product = self.env['product.template'].create({
            'name': 'Produit description sale',
            'type': 'consu',
            'list_price': 2.0,
            'sale_ok': True,
            'is_published': True,
            'description_sale': '<p>Texte long description sale pour la fiche.</p>',
        })
        sections = self._sections(product)
        self.assertEqual(len(sections), 1)
        self.assertEqual(sections[0]['key'], 'origin_usage')

    def test_conservation_subtitles(self):
        html = (
            '<div class="ck-product-enrich">'
            '<h3>Conservation</h3>'
            '<p>Avant ouverture : au sec. Après ouverture : au frais.</p>'
            '</div>'
        )
        product = self.env['product.template'].create({
            'name': 'Produit conservation',
            'type': 'consu',
            'list_price': 3.0,
            'sale_ok': True,
            'is_published': True,
            'website_description': html,
        })
        sections = self._sections(product)
        conservation = next(section for section in sections if section['key'] == 'conservation')
        self.assertEqual(len(conservation['subtitles']), 2)
        self.assertEqual(conservation['subtitles'][0]['title'], 'Avant ouverture')

    def test_ingredients_section_from_heading(self):
        html = (
            '<div class="ck-product-enrich">'
            '<h3>Ingrédients &amp; allergènes</h3>'
            '<p>Goyave, sucre. Peut contenir des traces de fruits à coque.</p>'
            '</div>'
        )
        product = self.env['product.template'].create({
            'name': 'Produit ingrédients',
            'type': 'consu',
            'list_price': 4.0,
            'sale_ok': True,
            'is_published': True,
            'website_description': html,
        })
        sections = self._sections(product)
        self.assertEqual(sections[0]['key'], 'ingredients')
        self.assertEqual(sections[0]['title'], 'Ingrédients & allergènes')

    def test_model_bridge_method(self):
        product = self.env['product.template'].create({
            'name': 'Confiture de goyave bridge',
            'type': 'consu',
            'list_price': 8.9,
            'sale_ok': True,
            'is_published': True,
            'website_description': PRODUCT_WEBSITE_DESCRIPTIONS['Confiture de goyave'],
        })
        sections = product.get_ck_product_page_detail_sections()
        self.assertTrue(sections)
        self.assertIsInstance(sections[0]['body'], Markup)
