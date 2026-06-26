# -*- coding: utf-8 -*-
"""Tests migration Axe C 19.0.1.43.0 — axe_c_bo_sync."""

from odoo.tests import tagged
from odoo.tests.common import TransactionCase

from odoo.addons.dorevia_ck_marketone_content.axe_c_bo_sync import (
    GALETTES_PRODUCT_NAME,
    _ensure_field_translation,
    apply_axe_c_bo_corrections,
)


@tagged('post_install', '-at_install', 'dorevia_ck_axe_c_bo_sync')
class TestCkAxeCBoSync(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.uom_g = cls.env.ref('dorevia_ck_marketone_content.ck_card_uom_g')
        cls.uom_kg = cls.env.ref('dorevia_ck_marketone_content.ck_card_uom_kg')
        cls.uom_unit = cls.env.ref('dorevia_ck_marketone_content.ck_card_uom_unit')
        cls._ensure_fr_lang()

    @classmethod
    def _ensure_fr_lang(cls):
        Lang = cls.env['res.lang'].sudo()
        lang = Lang.search([('code', '=', 'fr_FR')], limit=1)
        if not lang:
            Lang._activate_lang('fr_FR')
            lang = Lang.search([('code', '=', 'fr_FR')], limit=1)
        website = cls.env['website'].search([], limit=1)
        if website and lang not in website.language_ids:
            website.sudo().write({'language_ids': [(4, lang.id)]})

    def _make_product(self, name, **vals):
        base = {
            'name': name,
            'type': 'consu',
            'list_price': 5.0,
            'sale_ok': True,
            'is_published': True,
            'ck_net_quantity': 100,
            'ck_net_quantity_uom_id': self.uom_unit.id,
            'ck_reference_price_uom_id': self.uom_unit.id,
            'ck_show_reference_price': True,
        }
        base.update(vals)
        return self.env['product.template'].sudo().create(base)

    def test_uom_mass_products_and_panama(self):
        targets = (
            ('Confiture de goyave', 320, True),
            ('Manio Crackers', 100, True),
            (GALETTES_PRODUCT_NAME, 130, True),
            ('Savon vétiver', 125, True),
            ('Chapeau Panama', 0, True),
        )
        products = {}
        for name, qty, show_ref in targets:
            product = self.env['product.template'].sudo().search(
                [('name', '=', name)], limit=1,
            )
            if not product:
                product = self._make_product(name, ck_net_quantity=qty)
            else:
                product.write({
                    'ck_net_quantity': qty,
                    'ck_net_quantity_uom_id': self.uom_unit.id,
                    'ck_reference_price_uom_id': self.uom_unit.id,
                    'ck_show_reference_price': show_ref,
                })
            products[name] = product

        apply_axe_c_bo_corrections(self.env)

        for name in (
            'Confiture de goyave',
            'Manio Crackers',
            GALETTES_PRODUCT_NAME,
            'Savon vétiver',
        ):
            product = products[name]
            product.invalidate_recordset()
            self.assertEqual(product.ck_net_quantity_uom_id, self.uom_g)
            self.assertEqual(product.ck_reference_price_uom_id, self.uom_kg)
            self.assertTrue(product.ck_show_reference_price)

        panama = products['Chapeau Panama']
        panama.invalidate_recordset()
        self.assertFalse(panama.ck_net_quantity_uom_id)
        self.assertFalse(panama.ck_reference_price_uom_id)
        self.assertFalse(panama.ck_show_reference_price)

    def test_ensure_field_translation_idempotent(self):
        tag = self.env['product.tag'].sudo().create({'name': 'CK Translation QA'})
        tag.update_field_translations('name', {'fr_FR': 'Mauvais libellé'})
        self.assertTrue(
            _ensure_field_translation(self.env, tag, 'name', 'fr_FR', 'CK Translation QA'),
        )
        self.assertEqual(tag.with_context(lang='fr_FR').name, 'CK Translation QA')
        self.assertFalse(
            _ensure_field_translation(self.env, tag, 'name', 'fr_FR', 'CK Translation QA'),
        )
