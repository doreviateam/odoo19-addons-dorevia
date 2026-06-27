# -*- coding: utf-8 -*-
"""Tests note 08 — modèle de données fiche produit CK V1.1."""

from odoo.exceptions import ValidationError
from odoo.tests import tagged
from odoo.tests.common import HttpCase, TransactionCase

from odoo.addons.dorevia_ck_marketone_content.models.product_template import (
    CK_ECOMMERCE_LEAD_MAX_CHARS,
)
from odoo.addons.dorevia_ck_marketone_content.product_page_tabs import (
    build_ck_product_page_tabs,
)


@tagged('post_install', '-at_install', 'dorevia_ck_product_page_note08')
class TestCkProductPageNote08Models(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.badge = cls.env['ck.product.badge'].create({
            'name': 'Guadeloupe QA',
            'code': 'guadeloupe_qa',
            'badge_type': 'origin',
        })
        cls.producer = cls.env['res.partner'].create({
            'name': 'Producteur QA Note08',
            'ck_is_producer': True,
            'ck_producer_short_description': 'Savoir-faire artisanal.',
            'ck_producer_location_label': 'Abymes, Guadeloupe',
        })
        cls.non_producer = cls.env['res.partner'].create({
            'name': 'Fournisseur non producteur',
            'ck_is_producer': False,
        })

    def test_product_ck_fields_and_producer_domain(self):
        product = self.env['product.template'].create({
            'name': 'Produit note08 QA',
            'type': 'consu',
            'list_price': 5.0,
            'sale_ok': True,
            'ck_discover_html': '<p>Découvrir ce produit.</p>',
            'ck_ingredients': 'Goyave, sucre.',
            'ck_allergens': 'Peut contenir des traces de fruits à coque.',
            'ck_conservation_before': 'Conserver au sec.',
            'ck_conservation_after': 'Après ouverture, réfrigérer.',
            'ck_packaging_label': 'Pot verre 320 g',
            'ck_badge_ids': [(6, 0, self.badge.ids)],
            'ck_producer_id': self.producer.id,
        })
        self.assertEqual(product.ck_producer_id, self.producer)
        self.assertIn(self.badge, product.ck_badge_ids)

        domain = product._fields['ck_producer_id'].domain
        self.assertEqual(domain, "[('ck_is_producer', '=', True)]")

    def test_producer_block_requires_ck_is_producer(self):
        product = self.env['product.template'].create({
            'name': 'Produit producteur invalide',
            'type': 'consu',
            'list_price': 4.0,
            'sale_ok': True,
            'ck_producer_id': self.non_producer.id,
        })
        blocks = build_ck_product_page_tabs(product)
        self.assertFalse(any(block['key'] == 'producer' for block in blocks))

    def test_description_ecommerce_rejects_long_plain_text(self):
        long_text = 'a' * (CK_ECOMMERCE_LEAD_MAX_CHARS + 1)
        with self.assertRaises(ValidationError):
            self.env['product.template'].create({
                'name': 'Accroche trop longue QA',
                'type': 'consu',
                'list_price': 3.0,
                'sale_ok': True,
                'description_ecommerce': f'<p>{long_text}</p>',
            })

    def test_description_ecommerce_allows_max_plain_text(self):
        text = 'a' * CK_ECOMMERCE_LEAD_MAX_CHARS
        product = self.env['product.template'].create({
            'name': 'Accroche limite QA',
            'type': 'consu',
            'list_price': 3.0,
            'sale_ok': True,
            'description_ecommerce': f'<p>{text}</p>',
        })
        self.assertTrue(product.id)


@tagged('post_install', '-at_install', 'dorevia_ck_product_page_note08')
class TestCkProductPageNote08Conditional(TransactionCase):
    def test_discover_only_when_ck_discover_html(self):
        product = self.env['product.template'].create({
            'name': 'Découvrir seul',
            'type': 'consu',
            'list_price': 3.0,
            'sale_ok': True,
            'ck_discover_html': '<p>Texte Découvrir.</p>',
        })
        blocks = build_ck_product_page_tabs(product)
        discover = next(block for block in blocks if block['key'] == 'discover')
        self.assertEqual(len(discover['sections']), 1)
        self.assertEqual(discover['sections'][0]['key'], 'discover')

    def test_no_empty_anchors(self):
        product = self.env['product.template'].create({
            'name': 'Produit vide note08',
            'type': 'consu',
            'list_price': 2.0,
            'sale_ok': True,
        })
        self.assertEqual(build_ck_product_page_tabs(product), [])

    def test_composition_when_any_field(self):
        product = self.env['product.template'].create({
            'name': 'Composition allergènes',
            'type': 'consu',
            'list_price': 3.5,
            'sale_ok': True,
            'ck_allergens': 'Sans allergène déclaré.',
        })
        blocks = build_ck_product_page_tabs(product)
        self.assertIn('composition', [block['key'] for block in blocks])

    def test_practical_when_packaging_only(self):
        product = self.env['product.template'].create({
            'name': 'Infos pratiques packaging',
            'type': 'consu',
            'list_price': 4.5,
            'sale_ok': True,
            'ck_packaging_label': 'Sachet 100 g',
        })
        practical = next(
            block for block in build_ck_product_page_tabs(product)
            if block['key'] == 'practical'
        )
        labels = [row['label'] for row in practical['specs']]
        self.assertIn('Conditionnement', labels)

    def test_producer_block_when_valid(self):
        producer = self.env['res.partner'].create({
            'name': 'Atelier QA',
            'ck_is_producer': True,
            'ck_producer_short_description': 'Producteur partenaire.',
        })
        product = self.env['product.template'].create({
            'name': 'Produit avec producteur',
            'type': 'consu',
            'list_price': 6.0,
            'sale_ok': True,
            'ck_producer_id': producer.id,
        })
        producer_block = next(
            block for block in build_ck_product_page_tabs(product)
            if block['key'] == 'producer'
        )
        self.assertEqual(producer_block['producer']['name'], 'Atelier QA')


@tagged('post_install', '-at_install', 'dorevia_ck_product_page_note08')
class TestCkProductPageNote08Front(HttpCase):
    def test_reassurance_v1_without_refund_promise(self):
        product = self.env['product.template'].sudo().create({
            'name': 'Réassurance QA',
            'type': 'consu',
            'list_price': 3.0,
            'sale_ok': True,
            'is_published': True,
            'ck_discover_html': '<p>Contenu.</p>',
        })
        html = self.url_open(product.website_url).text
        self.assertIn('En stock — expédié depuis Nantes', html)
        self.assertIn('Livraison suivie 2 à 3 jours ouvrables', html)
        self.assertNotIn('remboursement sous 30 jours', html.lower())

    def test_badges_and_producer_section(self):
        badge = self.env['ck.product.badge'].sudo().create({
            'name': 'Producteur identifié QA',
            'code': 'producteur_identifie_qa',
            'badge_type': 'producer',
        })
        producer = self.env['res.partner'].sudo().create({
            'name': 'Producteur Front QA',
            'ck_is_producer': True,
            'ck_producer_short_description': 'Savoir-faire local.',
            'ck_producer_location_label': 'Pointe-à-Pitre, Guadeloupe',
        })
        product = self.env['product.template'].sudo().create({
            'name': 'Fiche note08 front',
            'type': 'consu',
            'list_price': 7.0,
            'sale_ok': True,
            'is_published': True,
            'description_ecommerce': 'Accroche courte QA.',
            'ck_discover_html': '<p>Section Découvrir front.</p>',
            'ck_badge_ids': [(6, 0, badge.ids)],
            'ck_producer_id': producer.id,
        })
        html = self.url_open(product.website_url).text
        self.assertIn('ck-product-purchase__badges', html)
        self.assertIn('Producteur identifié QA', html)
        self.assertIn('id="ck-section-producer"', html)
        self.assertIn('Producteur Front QA', html)
        self.assertIn('href="#ck-section-producer"', html)
        self.assertNotIn('qty_available', html)
