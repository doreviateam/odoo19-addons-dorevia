# -*- coding: utf-8 -*-
"""CATALOG-ARCHI-001 Lot B §10 — nom producteur dans la ligne meta card."""

from odoo.tests import tagged
from odoo.tests.common import TransactionCase

from odoo.addons.dorevia_ck_marketone_content.home_featured import (
    _get_featured_card_metadata_line,
)


@tagged('post_install', '-at_install', 'dorevia_ck_catalog_qualification')
class TestCkCardProducerMetadata(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.website = cls.env['website'].search([], limit=1)
        cls.Product = cls.env['product.template'].sudo()
        cls.Partner = cls.env['res.partner'].sudo()

    def test_producer_name_appears_in_metadata_line(self):
        producer = self.Partner.create({'name': 'La Platine', 'ck_is_producer': True})
        product = self.Product.create({
            'name': 'Test Produit Producteur',
            'sale_ok': True,
            'is_published': True,
            'website_published': True,
            'ck_producer_id': producer.id,
        })
        line = _get_featured_card_metadata_line(self.env, self.website, product.product_variant_id)
        self.assertIn('La Platine', line)

    def test_no_producer_does_not_add_empty_segment(self):
        """Additif seulement : sans producteur, pas de « ·  · » orphelin."""
        product = self.Product.create({
            'name': 'Test Produit Sans Producteur',
            'sale_ok': True,
            'is_published': True,
            'website_published': True,
        })
        line = _get_featured_card_metadata_line(self.env, self.website, product.product_variant_id)
        self.assertNotIn('·  ·', line)
        self.assertFalse(line.startswith('·'))
