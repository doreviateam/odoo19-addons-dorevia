# -*- coding: utf-8 -*-
"""Tests BO — onglet Ventes produit CK (réorganisation 7 blocs)."""

from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged('post_install', '-at_install', 'dorevia_ck_product_sales_tab_bo')
class TestCkProductSalesTabBo(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.view = cls.env.ref(
            'dorevia_ck_marketone_content.product_template_form_view_ck_featured_card',
            raise_if_not_found=False,
        )
        if not cls.view:
            raise AssertionError(
                'Vue BO Ventes CK absente — -u dorevia_ck_marketone_content requis.'
            )
        cls.form_arch = cls.env['product.template'].get_views(
            [(False, 'form')],
        )['views']['form']['arch']

    def _sales_arch(self):
        from lxml import etree
        root = etree.fromstring(self.form_arch.encode())
        page = root.xpath("//page[@name='sales']")
        self.assertEqual(len(page), 1)
        return page[0]

    def _block_xml(self, group_name):
        from lxml import etree
        block = self._sales_arch().xpath(f".//group[@name='{group_name}']")
        self.assertTrue(block, group_name)
        return etree.tostring(block[0], encoding='unicode')

    def test_sales_tab_two_column_rows(self):
        sales = self._sales_arch()
        row_pairs = [
            ('ck_publication_highlight', 'ck_shop_classification'),
            ('ck_card_reference_price', 'ck_ecommerce_description'),
            ('ck_ecommerce_media', 'ck_product_recommendations'),
        ]
        for left, right in row_pairs:
            left_group = sales.xpath(f".//group[@name='{left}']")
            right_group = sales.xpath(f".//group[@name='{right}']")
            self.assertEqual(len(left_group), 1, left)
            self.assertEqual(len(right_group), 1, right)
            self.assertEqual(
                left_group[0].getparent(),
                right_group[0].getparent(),
                f'{left} et {right} doivent partager la même ligne',
            )

    def test_sales_tab_ck_blocks_order(self):
        sales = self._sales_arch()
        names = [
            node.get('name')
            for node in sales.xpath('.//group[@name]')
            if node.get('name', '').startswith('ck_')
        ]
        self.assertEqual(names, [
            'ck_publication_highlight',
            'ck_shop_classification',
            'ck_card_reference_price',
            'ck_ecommerce_description',
            'ck_ecommerce_media',
            'ck_product_recommendations',
            'ck_commercial_documents',
        ])

    def test_publication_fields(self):
        xml = self._block_xml('ck_publication_highlight')
        for field in ('is_published', 'website_ribbon_id', 'website_sequence'):
            self.assertIn(f'name="{field}"', xml)

    def test_classification_fields(self):
        xml = self._block_xml('ck_shop_classification')
        self.assertIn('name="public_categ_ids"', xml)
        self.assertIn('name="product_tag_ids"', xml)

    def test_card_reference_fields(self):
        xml = self._block_xml('ck_card_reference_price')
        for field in (
            'ck_net_quantity',
            'ck_net_quantity_uom_id',
            'ck_show_reference_price',
            'ck_reference_price_uom_id',
        ):
            self.assertIn(f'name="{field}"', xml)

    def test_recommendation_fields(self):
        xml = self._block_xml('ck_product_recommendations')
        for field in (
            'uom_ids',
            'optional_product_ids',
            'accessory_product_ids',
            'alternative_product_ids',
        ):
            self.assertIn(f'name="{field}"', xml)

    def test_commercial_documents_field(self):
        xml = self._block_xml('ck_commercial_documents')
        self.assertIn('name="description_sale"', xml)

    def test_product_still_editable(self):
        product = self.env['product.template'].create({
            'name': 'QA BO Ventes CK',
            'type': 'consu',
            'list_price': 4.5,
            'sale_ok': True,
        })
        product.write({
            'description_ecommerce': '<p>Lead e-commerce QA</p>',
            'description_sale': 'Note devis QA',
            'ck_net_quantity': 320,
            'ck_show_reference_price': True,
        })
        self.assertEqual(product.description_sale, 'Note devis QA')
        self.assertIn('Lead e-commerce', product.description_ecommerce or '')
