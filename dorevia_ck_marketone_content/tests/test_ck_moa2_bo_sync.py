# -*- coding: utf-8 -*-
"""Tests migration MOA-2 19.0.1.44.0 — axe_c_bo_sync.apply_moa2_bo_corrections."""

from odoo.tests import tagged
from odoo.tests.common import TransactionCase

from odoo.addons.dorevia_ck_marketone_content.axe_c_bo_sync import (
    GALETTES_PRODUCT_NAME,
    apply_axe_c_bo_corrections,
    apply_moa2_bo_corrections,
)


@tagged('post_install', '-at_install', 'dorevia_ck_moa2_bo_sync')
class TestCkMoa2BoSync(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.uom_g = cls.env.ref('dorevia_ck_marketone_content.ck_card_uom_g')
        cls.uom_kg = cls.env.ref('dorevia_ck_marketone_content.ck_card_uom_kg')
        cls.uom_l = cls.env.ref('dorevia_ck_marketone_content.ck_card_uom_l')
        cls.uom_unit = cls.env.ref('dorevia_ck_marketone_content.ck_card_uom_unit')

    def _make_product(self, name, **vals):
        base = {
            'name': name,
            'type': 'consu',
            'list_price': 5.0,
            'sale_ok': True,
            'is_published': True,
            'ck_net_quantity': 1,
            'ck_net_quantity_uom_id': self.uom_unit.id,
            'ck_reference_price_uom_id': self.uom_unit.id,
            'ck_show_reference_price': True,
        }
        base.update(vals)
        return self.env['product.template'].sudo().create(base)

    def _seed_product(self, name):
        product = self.env['product.template'].sudo().search(
            [('name', '=', name)], limit=1,
        )
        if not product:
            product = self._make_product(name)
        else:
            product.write({
                'ck_net_quantity_uom_id': self.uom_unit.id,
                'ck_reference_price_uom_id': self.uom_unit.id,
                'ck_show_reference_price': True,
            })
        return product

    def test_moa2_jus_and_pate_uom(self):
        jus = self._seed_product('Jus Mont-Pelé')
        pate = self._seed_product('Pâte de manioc')

        stats = apply_moa2_bo_corrections(self.env)
        self.assertEqual(stats['moa2_products_uom'], 2)

        jus.invalidate_recordset()
        pate.invalidate_recordset()
        self.assertEqual(jus.ck_net_quantity_uom_id, self.uom_l)
        self.assertEqual(jus.ck_reference_price_uom_id, self.uom_l)
        self.assertTrue(jus.ck_show_reference_price)
        self.assertEqual(pate.ck_net_quantity_uom_id, self.uom_kg)
        self.assertEqual(pate.ck_reference_price_uom_id, self.uom_kg)
        self.assertTrue(pate.ck_show_reference_price)

        stats_second = apply_moa2_bo_corrections(self.env)
        self.assertEqual(stats_second['moa2_products_uom'], 0)

    def test_moa2_does_not_alter_43_0_products(self):
        confiture = self._seed_product('Confiture de goyave')
        confiture.write({
            'ck_net_quantity': 320,
            'ck_net_quantity_uom_id': self.uom_g.id,
            'ck_reference_price_uom_id': self.uom_kg.id,
            'ck_show_reference_price': True,
        })
        galettes = self._seed_product(GALETTES_PRODUCT_NAME)
        galettes.write({
            'ck_net_quantity': 130,
            'ck_net_quantity_uom_id': self.uom_g.id,
            'ck_reference_price_uom_id': self.uom_kg.id,
            'ck_show_reference_price': True,
        })

        apply_moa2_bo_corrections(self.env)

        confiture.invalidate_recordset()
        galettes.invalidate_recordset()
        self.assertEqual(confiture.ck_net_quantity_uom_id, self.uom_g)
        self.assertEqual(confiture.ck_reference_price_uom_id, self.uom_kg)
        self.assertEqual(galettes.ck_net_quantity_uom_id, self.uom_g)
        self.assertEqual(galettes.ck_reference_price_uom_id, self.uom_kg)

        # Sanity : migration 43.0 inchangée après MOA-2
        apply_axe_c_bo_corrections(self.env)
        confiture.invalidate_recordset()
        self.assertEqual(confiture.ck_net_quantity_uom_id, self.uom_g)
        self.assertEqual(confiture.ck_reference_price_uom_id, self.uom_kg)
