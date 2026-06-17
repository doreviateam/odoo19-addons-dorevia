# -*- coding: utf-8 -*-
"""Tests attribut « Origine » (no_variant) — chip pays des vedettes home."""

from odoo.tests import tagged
from odoo.tests.common import TransactionCase

from odoo.addons.dorevia_ck_marketone_content.catalog_origine import (
    ORIGIN_ATTRIBUTE_NAME,
    _assign_origin,
    _ensure_origin_attribute,
)
from odoo.addons.dorevia_ck_marketone_content.home_featured import (
    _get_featured_origin_label,
)


@tagged('post_install', '-at_install', 'dorevia_ck_marketone_catalog_origine')
class TestCkCatalogOrigine(TransactionCase):
    def test_origin_attribute_is_no_variant(self):
        attribute = _ensure_origin_attribute(self.env)
        self.assertEqual(attribute.name, ORIGIN_ATTRIBUTE_NAME)
        self.assertEqual(attribute.create_variant, 'no_variant')
        self.assertTrue(attribute.value_ids)

    def test_assign_origin_drives_chip_without_new_variant(self):
        template = self.env['product.template'].sudo().create({
            'name': 'CK Origine Test',
            'sale_ok': True,
            'list_price': 1.0,
        })
        variants_before = len(template.product_variant_ids)
        _assign_origin(self.env, template, 'Réunion')
        # Le chip lit l'attribut Origine réel.
        self.assertEqual(_get_featured_origin_label(template), 'Réunion')
        # no_variant : aucune variante supplémentaire générée.
        self.assertEqual(len(template.product_variant_ids), variants_before)
