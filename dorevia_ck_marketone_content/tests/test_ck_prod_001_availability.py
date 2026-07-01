# -*- coding: utf-8 -*-
"""Tests CK-PROD-001 — champ ck_availability_mode et rendu fiche produit "Sur commande"."""

from odoo.tests import tagged
from odoo.tests.common import HttpCase, TransactionCase

from odoo.addons.dorevia_ck_marketone_content.product_page_v11 import (
    build_ck_product_page_metadata_line,
)


# ---------------------------------------------------------------------------
# Tests modèle — TransactionCase
# ---------------------------------------------------------------------------

@tagged('post_install', '-at_install', 'dorevia_ck_prod_001')
class TestCkAvailabilityModeModel(TransactionCase):

    def test_ck_availability_mode_field_exists(self):
        fields = self.env['product.template']._fields
        self.assertIn('ck_availability_mode', fields)
        field = fields['ck_availability_mode']
        self.assertEqual(field.type, 'selection')
        keys = [k for k, _ in field.selection]
        self.assertIn('stock', keys)
        self.assertIn('order', keys)
        self.assertIn('soon', keys)

    def test_ck_availability_mode_default_is_stock(self):
        product = self.env['product.template'].create({
            'name': 'Produit default disponibilité QA',
            'type': 'consu',
            'list_price': 5.0,
            'sale_ok': True,
        })
        self.assertEqual(product.ck_availability_mode, 'stock')

    def test_ck_availability_mode_in_bo_view(self):
        from lxml import etree
        arch = self.env['product.template'].get_views([(False, 'form')])['views']['form']['arch']
        root = etree.fromstring(arch.encode())
        sales = root.xpath("//page[@name='sales']")
        self.assertEqual(len(sales), 1)
        xml = etree.tostring(sales[0], encoding='unicode')
        self.assertIn('name="ck_availability_mode"', xml)

    def test_origin_badge_suppresses_metadata_origin(self):
        badge = self.env['ck.product.badge'].create({
            'name': 'Guadeloupe PROD001 QA',
            'code': 'guadeloupe_prod001_qa',
            'badge_type': 'origin',
        })
        attr = self.env['product.attribute'].sudo().search([
            ('name', 'ilike', 'origine'),
        ], limit=1)
        product = self.env['product.template'].create({
            'name': 'Produit badge origine QA',
            'type': 'consu',
            'list_price': 10.0,
            'sale_ok': True,
            'ck_badge_ids': [(6, 0, badge.ids)],
        })
        if attr:
            self.env['product.template.attribute.line'].create({
                'product_tmpl_id': product.id,
                'attribute_id': attr.id,
                'value_ids': [(0, 0, {'name': 'Guadeloupe', 'attribute_id': attr.id})],
            })
        variant = product.product_variant_id
        line = str(build_ck_product_page_metadata_line(self.env, product, variant))
        self.assertNotIn('Guadeloupe', line)

    def test_no_origin_badge_keeps_metadata_origin(self):
        attr = self.env['product.attribute'].sudo().search([
            ('name', 'ilike', 'origine'),
        ], limit=1)
        if not attr:
            self.skipTest('Attribut Origine absent.')
        product = self.env['product.template'].create({
            'name': 'Produit sans badge origine QA',
            'type': 'consu',
            'list_price': 10.0,
            'sale_ok': True,
        })
        self.env['product.template.attribute.line'].create({
            'product_tmpl_id': product.id,
            'attribute_id': attr.id,
            'value_ids': [(0, 0, {'name': 'Martinique', 'attribute_id': attr.id})],
        })
        variant = product.product_variant_id
        line = str(build_ck_product_page_metadata_line(self.env, product, variant))
        self.assertIn('Martinique', line)

    def test_migration_tambour_groka(self):
        from odoo import SUPERUSER_ID
        products = self.env['product.template'].search([
            ('name', '=', 'Tambour Gro Ka'),
        ])
        if not products:
            products = self.env['product.template'].create({
                'name': 'Tambour Gro Ka',
                'type': 'consu',
                'list_price': 435.0,
                'sale_ok': True,
            })
        products.write({'ck_availability_mode': 'stock'})

        # Simule la logique de migration 19.0.1.71.0.
        from odoo import api
        env = api.Environment(self.cr, SUPERUSER_ID, {})
        found = env['product.template'].search(
            [('name', '=', 'Tambour Gro Ka')], limit=1,
        )
        self.assertTrue(found)
        if found.ck_availability_mode != 'order':
            found.ck_availability_mode = 'order'

        found.invalidate_recordset(['ck_availability_mode'])
        self.assertEqual(found.ck_availability_mode, 'order')


# ---------------------------------------------------------------------------
# Tests front — HttpCase
# ---------------------------------------------------------------------------

@tagged('post_install', '-at_install', 'dorevia_ck_prod_001')
class TestCkAvailabilityModeFront(HttpCase):
    FR_HEADERS = {'Accept-Language': 'fr-FR,fr;q=0.9'}

    def _make_product(self, name, **vals):
        base = {
            'name': name,
            'type': 'consu',
            'list_price': 10.0,
            'sale_ok': True,
            'is_published': True,
        }
        base.update(vals)
        return self.env['product.template'].sudo().create(base)

    def _open(self, product):
        return self.url_open(product.website_url, headers=self.FR_HEADERS).text

    # --- stock (comportement standard, non-régression) ---

    def test_stock_mode_reassurance(self):
        product = self._make_product('Stock Mode QA PROD001')
        html = self._open(product)
        self.assertIn('En stock · Expédié depuis Nantes', html)
        self.assertIn('Livraison suivie · 2 à 3 jours ouvrables', html)
        self.assertIn('Retour selon CGV', html)
        self.assertNotIn('Sur commande', html)

    def test_stock_mode_cta_label(self):
        product = self._make_product('Stock CTA QA PROD001')
        html = self._open(product)
        self.assertIn('Ajouter au panier', html)
        self.assertNotIn('Commander cette pièce', html)

    # --- order ---

    def test_order_mode_reassurance_wording(self):
        product = self._make_product('Order Reassurance QA PROD001',
                                     ck_availability_mode='order')
        html = self._open(product)
        self.assertIn('Sur commande', html)
        self.assertIn('Accompagnement C-Kréyòl', html)
        self.assertIn('Livraison suivie avec emballage adapté', html)
        self.assertIn('Conditions de retour applicables', html)
        self.assertNotIn('En stock · Expédié depuis Nantes', html)
        self.assertNotIn('2 à 3 jours ouvrables', html)

    def test_order_mode_cta_label(self):
        product = self._make_product('Order CTA QA PROD001',
                                     ck_availability_mode='order')
        html = self._open(product)
        self.assertIn('Commander cette pièce', html)
        self.assertNotIn('Ajouter au panier', html)

    def test_order_mode_micro_line(self):
        product = self._make_product('Order Micro-ligne QA PROD001',
                                     ck_availability_mode='order')
        html = self._open(product)
        self.assertIn('ck-product-purchase__order-note', html)
        self.assertIn('Pièce artisanale proposée sur commande', html)

    def test_stock_mode_no_micro_line(self):
        product = self._make_product('Stock sans micro-ligne QA PROD001')
        html = self._open(product)
        self.assertNotIn('ck-product-purchase__order-note', html)
        self.assertNotIn('Pièce artisanale proposée sur commande', html)

    # --- soon : fallback standard (non-régression) ---

    def test_soon_mode_standard_fallback(self):
        product = self._make_product('Soon Mode QA PROD001',
                                     ck_availability_mode='soon')
        html = self._open(product)
        self.assertIn('En stock · Expédié depuis Nantes', html)
        self.assertIn('Ajouter au panier', html)
        self.assertNotIn('Commander cette pièce', html)
        self.assertNotIn('ck-product-purchase__order-note', html)

    # --- producteur ligne éditoriale ---

    def test_producer_editorial_line(self):
        producer = self.env['res.partner'].sudo().create({
            'name': 'GoZié Lantan QA',
            'ck_is_producer': True,
            'city': 'Le Gosier',
        })
        product = self._make_product('Tambour QA PROD001',
                                     ck_producer_id=producer.id)
        html = self._open(product)
        self.assertIn('ck-product-purchase__producer-line', html)
        self.assertIn('Par GoZié Lantan QA', html)
        self.assertIn('Le Gosier', html)
        self.assertNotIn('ck-chip--producer', html)

    def test_producer_editorial_line_without_city(self):
        producer = self.env['res.partner'].sudo().create({
            'name': 'Artisan Sans Ville QA',
            'ck_is_producer': True,
        })
        product = self._make_product('Produit sans ville QA PROD001',
                                     ck_producer_id=producer.id)
        html = self._open(product)
        self.assertIn('ck-product-purchase__producer-line', html)
        self.assertIn('Par Artisan Sans Ville QA', html)
