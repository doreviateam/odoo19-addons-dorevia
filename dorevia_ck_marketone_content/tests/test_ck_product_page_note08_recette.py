# -*- coding: utf-8 -*-
"""Recette MOA Note 08 — couverture automatisée checklist BO + logique front."""

from lxml import etree

from odoo.tests import tagged
from odoo.tests.common import HttpCase, TransactionCase

from odoo.addons.dorevia_ck_marketone_content.catalog_manioc_variants import (
    MANIO_CRACKERS_PARENT_NAME,
    bootstrap_catalog_vedettes_products,
)
from odoo.addons.dorevia_ck_marketone_content.hooks import PRODUCT_WEBSITE_DESCRIPTIONS
from odoo.addons.dorevia_ck_marketone_content.product_page_tabs import (
    build_ck_product_page_tabs,
)
from odoo.addons.dorevia_ck_marketone_content.product_page_v11 import (
    build_ck_product_page_metadata_line,
    build_ck_variant_value_prices,
)


FORBIDDEN_PRODUCT_FIELDS = {
    'ck_origin_id',
    'ck_logistics_note',
    'ck_price_per_kg',
    'ck_variant_price',
    'ck_content_validated',
    'ck_short_description',
    'ck_net_weight_label',
}

REQUIRED_PRODUCT_FIELDS = {
    'ck_producer_id',
    'ck_badge_ids',
    'ck_discover_html',
    'ck_ingredients',
    'ck_allergens',
    'ck_nutrition_html',
    'ck_conservation_before',
    'ck_conservation_after',
    'ck_packaging_label',
    'ck_net_quantity',
    'ck_net_quantity_uom_id',
}

REQUIRED_PARTNER_FIELDS = {
    'ck_is_producer',
    'ck_producer_short_description',
    'ck_producer_story_html',
    'ck_producer_location_label',
}

REQUIRED_BO_SALES_FIELDS = {
    'description_ecommerce',
    'ck_producer_id',
    'ck_badge_ids',
    'ck_discover_html',
    'ck_ingredients',
    'ck_allergens',
    'ck_nutrition_html',
    'ck_conservation_before',
    'ck_conservation_after',
    'ck_packaging_label',
    'ck_net_quantity',
    'ck_net_quantity_uom_id',
}

ANCHOR_ORDER = [
    ('discover', 'ck-section-discover', 'Découvrir'),
    ('composition', 'ck-section-composition', 'Composition'),
    ('conservation', 'ck-section-conservation', 'Conservation'),
    ('practical', 'ck-section-practical', 'Infos pratiques'),
    ('producer', 'ck-section-producer', 'Producteur'),
]

FORBIDDEN_BADGE_NAMES = {
    'Sans gluten',
    'Bio',
    'Naturel',
    'Artisanal',
    'Sans additif',
}


@tagged('post_install', '-at_install', 'dorevia_ck_product_page_note08_recette')
class TestCkProductPageNote08RecetteModels(TransactionCase):
    def test_forbidden_fields_not_created(self):
        product_fields = self.env['product.template']._fields
        for name in FORBIDDEN_PRODUCT_FIELDS:
            self.assertNotIn(
                name,
                product_fields,
                f'Le champ interdit {name} ne doit pas exister.',
            )
        for name in REQUIRED_PRODUCT_FIELDS:
            self.assertIn(name, product_fields, name)

    def test_no_x_prefixed_ck_fields_on_product(self):
        illegal = [
            name for name in self.env['product.template']._fields
            if name.startswith('x_')
        ]
        self.assertEqual(illegal, [])

    def test_partner_producer_fields(self):
        partner_fields = self.env['res.partner']._fields
        for name in REQUIRED_PARTNER_FIELDS:
            self.assertIn(name, partner_fields, name)
        self.assertTrue(self.env['ir.model']._get('ck.product.badge'))

    def test_badge_seed_records(self):
        for xml_id in (
            'dorevia_ck_marketone_content.ck_product_badge_guadeloupe',
            'dorevia_ck_marketone_content.ck_product_badge_farine_manioc',
            'dorevia_ck_marketone_content.ck_product_badge_producteur_identifie',
        ):
            badge = self.env.ref(xml_id, raise_if_not_found=False)
            self.assertTrue(badge, xml_id)
        badge_model = self.env['ck.product.badge']
        self.assertIn('requires_validation', badge_model._fields)
        self.assertIn('is_sensitive_claim', badge_model._fields)
        self.assertIn('sequence', badge_model._fields)

    def test_bo_sales_tab_fields_present(self):
        arch = self.env['product.template'].get_views([(False, 'form')])['views']['form']['arch']
        root = etree.fromstring(arch.encode())
        sales = root.xpath("//page[@name='sales']")
        self.assertEqual(len(sales), 1)
        xml = etree.tostring(sales[0], encoding='unicode')
        for field in REQUIRED_BO_SALES_FIELDS:
            self.assertIn(f'name="{field}"', xml, field)

    def test_producer_domain_on_field(self):
        domain = self.env['product.template']._fields['ck_producer_id'].domain
        self.assertEqual(domain, "[('ck_is_producer', '=', True)]")


@tagged('post_install', '-at_install', 'dorevia_ck_product_page_note08_recette')
class TestCkProductPageNote08RecetteLogic(TransactionCase):
    def test_anchor_order_fixed(self):
        producer = self.env['res.partner'].create({
            'name': 'La Platine QA',
            'ck_is_producer': True,
            'ck_producer_short_description': 'Atelier manioc.',
            'ck_producer_location_label': 'Guadeloupe',
        })
        product = self.env['product.template'].create({
            'name': 'Recette ancres QA',
            'type': 'consu',
            'list_price': 3.6,
            'sale_ok': True,
            'ck_discover_html': '<p>Découvrir.</p>',
            'ck_ingredients': 'Manioc.',
            'ck_conservation_before': 'Sec.',
            'ck_packaging_label': 'Sachet 100 g',
            'ck_producer_id': producer.id,
        })
        blocks = build_ck_product_page_tabs(product)
        self.assertEqual([block['key'] for block in blocks], [key for key, _, _ in ANCHOR_ORDER])
        for block, (_, anchor_id, nav_label) in zip(blocks, ANCHOR_ORDER):
            self.assertEqual(block['anchor_id'], anchor_id)
            self.assertEqual(block['nav_label'], nav_label)

    def test_discover_dedicated_field_overrides_website_description(self):
        product = self.env['product.template'].create({
            'name': 'Priorité Découvrir QA',
            'type': 'consu',
            'list_price': 4.0,
            'sale_ok': True,
            'ck_discover_html': '<p>Contenu dédié MOA.</p>',
            'website_description': PRODUCT_WEBSITE_DESCRIPTIONS['Confiture de goyave'],
        })
        blocks = build_ck_product_page_tabs(product)
        discover = next(block for block in blocks if block['key'] == 'discover')
        body = str(discover['sections'][0]['body'])
        self.assertIn('Contenu dédié MOA', body)
        self.assertNotIn('Origine &amp; usage', body)
        self.assertNotIn('Origine & usage', body)

    def test_fallback_website_description_when_discover_empty(self):
        product = self.env['product.template'].create({
            'name': 'Fallback seed QA',
            'type': 'consu',
            'list_price': 4.0,
            'sale_ok': True,
            'website_description': (
                '<div class="ck-product-enrich">'
                '<h3>Origine &amp; usage</h3><p>Texte seed.</p>'
                '</div>'
            ),
        })
        blocks = build_ck_product_page_tabs(product)
        self.assertIn('discover', [block['key'] for block in blocks])

    def test_metadata_includes_producer_anchor_link(self):
        producer = self.env['res.partner'].create({
            'name': 'La Platine',
            'ck_is_producer': True,
        })
        product = self.env['product.template'].create({
            'name': 'Meta producteur QA',
            'type': 'consu',
            'list_price': 3.6,
            'sale_ok': True,
            'ck_producer_id': producer.id,
        })
        variant = product.product_variant_id
        line = str(build_ck_product_page_metadata_line(self.env, product, variant))
        self.assertIn('href="#ck-section-producer"', line)
        self.assertIn('La Platine', line)

    def test_variant_absolute_prices_no_negative_delta(self):
        bootstrap_catalog_vedettes_products(self.env)
        product = self.env['product.template'].search([
            ('name', '=', MANIO_CRACKERS_PARENT_NAME),
        ], limit=1)
        if not product:
            self.skipTest('Manio Crackers absent.')
        line = product.valid_product_template_attribute_line_ids[:1]
        if not line:
            self.skipTest('Manio Crackers sans attribut.')
        prices = build_ck_variant_value_prices(self.env, product, line)
        self.assertGreaterEqual(len(prices), 2)
        for label in prices.values():
            self.assertNotRegex(label, r'^\s*[+\-−]')
            self.assertTrue(any(ch.isdigit() for ch in label))


@tagged('post_install', '-at_install', 'dorevia_ck_product_page_note08_recette')
class TestCkProductPageNote08RecetteFront(HttpCase):
    FR_HEADERS = {'Accept-Language': 'fr-FR,fr;q=0.9'}

    def _open_fr(self, url):
        return self.url_open(url, headers=self.FR_HEADERS)

    def _apply_product_rating(self, product, rate=5):
        partner = self.env['res.partner'].sudo().create({
            'name': 'Client QA Rating-U1',
            'email': 'qa-rating-u1@example.test',
        })
        rating = self.env['rating.rating'].sudo().create({
            'res_model_id': self.env['ir.model'].sudo()._get('product.template').id,
            'res_model': 'product.template',
            'res_id': product.id,
            'partner_id': partner.id,
            'rated_partner_id': self.env.company.partner_id.id,
            'publisher_id': self.env.company.partner_id.id,
        })
        product.sudo().rating_apply(
            rate,
            rating=rating,
            feedback='Avis QA Rating-U1 : produit conforme et apprécié.',
        )
        product.invalidate_recordset(['rating_count', 'rating_avg'])
        return rating

    def test_reassurance_and_compare_hidden(self):
        product = self.env['product.template'].sudo().create({
            'name': 'Recette front QA',
            'type': 'consu',
            'list_price': 3.0,
            'sale_ok': True,
            'is_published': True,
            'ck_discover_html': '<p>Section.</p>',
        })
        html = self._open_fr(product.website_url).text
        self.assertIn('En stock — expédié depuis Nantes', html)
        self.assertIn('Retour selon conditions de vente', html)
        self.assertNotIn('remboursement sous 30 jours', html.lower())
        self.assertNotIn('qty_available', html)
        self.assertNotIn('virtual_available', html)

    def test_badges_only_when_selected(self):
        badge = self.env['ck.product.badge'].sudo().create({
            'name': 'Guadeloupe QA recette',
            'code': 'guadeloupe_recette_qa',
            'badge_type': 'origin',
        })
        for forbidden_name in FORBIDDEN_BADGE_NAMES:
            self.assertFalse(
                self.env['ck.product.badge'].sudo().search([('name', '=', forbidden_name)]),
                forbidden_name,
            )
        product = self.env['product.template'].sudo().create({
            'name': 'Badges recette QA',
            'type': 'consu',
            'list_price': 3.0,
            'sale_ok': True,
            'is_published': True,
            'ck_discover_html': '<p>OK</p>',
            'ck_badge_ids': [(6, 0, badge.ids)],
        })
        html = self._open_fr(product.website_url).text
        self.assertIn('Guadeloupe QA recette', html)
        self.assertNotIn('Sans gluten', html)

    def test_shop_and_home_non_regression(self):
        shop = self._open_fr('/shop').text
        home = self._open_fr('/').text
        self.assertIn('ck-product-card--shop', shop)
        self.assertIn('ck-product-card--home', home)

    def test_rating_u1_reviews_link_section_and_dom_order(self):
        product = self.env['product.template'].sudo().create({
            'name': 'Rating U1 recette QA',
            'type': 'consu',
            'list_price': 8.0,
            'sale_ok': True,
            'is_published': True,
            'ck_packaging_label': 'Sachet QA 100 g',
        })
        self._apply_product_rating(product)

        html = self._open_fr(product.website_url).text

        self.assertIn('ck-product-purchase__title', html)
        self.assertIn('o_product_page_reviews_link', html)
        self.assertIn('(1 avis)', html)
        self.assertIn('fa-star', html)
        self.assertIn('id="o_product_page_reviews"', html)
        self.assertIn('Avis clients', html)
        self.assertIn('data-bs-target="#o_product_page_reviews_content"', html)
        self.assertLess(
            html.index('ck-product-purchase__title'),
            html.index('o_product_page_reviews_link'),
        )
        self.assertLess(
            html.index('ck-product-page__long-zone'),
            html.index('id="o_product_page_reviews"'),
        )

    def test_rating_u1_no_reviews_keeps_title_without_link(self):
        product = self.env['product.template'].sudo().create({
            'name': 'Sans avis Rating U1 QA',
            'type': 'consu',
            'list_price': 8.0,
            'sale_ok': True,
            'is_published': True,
        })

        html = self._open_fr(product.website_url).text

        self.assertIn('ck-product-purchase__title', html)
        self.assertNotIn('o_product_page_reviews_link', html)
