# -*- coding: utf-8 -*-
"""Tests CK-CHECKOUT-STOCK-001 / S3-B2 — sync stock CK et message panier."""
from odoo.tests import tagged
from odoo.tests.common import TransactionCase
from odoo.tools.translate import code_translations


@tagged('post_install', '-at_install', 'dorevia_ck_cart_stock')
class TestCkCheckoutStock001(TransactionCase):

    MSGID = (
        'You requested %(requested_qty)s, but only %(available_qty)s is currently available.'
    )

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        Lang = cls.env['res.lang'].with_context(active_test=False)
        lang = Lang.search([('code', '=', 'fr_FR')], limit=1)
        if lang and not lang.active:
            lang.active = True
        cls.fr_lang = lang

    def _make_line(self):
        return self.env['sale.order.line'].create({
            'order_id': self.env['sale.order'].create({
                'partner_id': self.env.ref('base.public_partner').id,
            }).id,
            'product_id': self.env['product.product'].create({
                'name': 'Warn test',
                'type': 'consu',
                'is_storable': True,
            }).id,
            'product_uom_qty': 1,
        })

    def test_ck_availability_stock_syncs_allow_out_of_stock_false(self):
        product = self.env['product.template'].create({
            'name': 'CK Stock Test',
            'type': 'consu',
            'is_storable': True,
            'sale_ok': True,
            'list_price': 1.0,
            'ck_availability_mode': 'stock',
        })
        product.write({'ck_availability_mode': 'stock'})
        self.assertFalse(product.allow_out_of_stock_order)

    def test_ck_availability_order_syncs_allow_out_of_stock_true(self):
        product = self.env['product.template'].create({
            'name': 'CK Order Test',
            'type': 'consu',
            'is_storable': True,
            'sale_ok': True,
            'list_price': 1.0,
            'ck_availability_mode': 'order',
        })
        product.write({'ck_availability_mode': 'order'})
        self.assertTrue(product.allow_out_of_stock_order)

    def test_shop_warning_stock_save_false(self):
        line = self._make_line()
        warning = line._set_shop_warning_stock(10, 2, save=False)
        self.assertFalse(line.shop_warning)
        self.assertIn('10', warning)
        self.assertIn('2', warning)
        self.assertIn('requested', warning.lower())
        self.assertNotIn('unité(s)', warning)

    def test_shop_warning_stock_save_true(self):
        line = self._make_line()
        warning = line._set_shop_warning_stock(7, 3, save=True)
        self.assertEqual(line.shop_warning, warning)
        self.assertIn('7', warning)
        self.assertIn('3', warning)

    def test_shop_warning_includes_desired_qty(self):
        line = self._make_line()
        warning = line._set_shop_warning_stock(12, 4, save=False)
        self.assertIn('12', warning)
        self.assertIn('4', warning)

    def test_shop_warning_no_hardcoded_unites(self):
        line = self._make_line()
        warning = line._set_shop_warning_stock(5, 1, save=False)
        self.assertNotIn('unité(s)', warning)
        self.assertNotIn('unite(s)', warning.lower())

    def test_shop_warning_english_locale(self):
        line = self._make_line()
        warning = line.with_context(lang='en_US')._set_shop_warning_stock(9, 2, save=False)
        self.assertIn('You requested', warning)
        self.assertIn('9', warning)
        self.assertIn('2', warning)
        self.assertNotIn('demandé', warning.lower())

    def test_python_translations_fr_loaded_with_odoo_python_marker(self):
        """F1 : sans `#. odoo-python`, Odoo 19 charge 0 entrée Python."""
        cache = code_translations.python_translations
        cache.pop(('dorevia_ck_marketone_content', 'fr_FR'), None)
        cache.pop(('dorevia_ck_marketone_content', 'fr'), None)
        translations = code_translations.get_python_translations(
            'dorevia_ck_marketone_content', 'fr_FR',
        )
        self.assertTrue(
            translations,
            msg='get_python_translations doit charger au moins une entrée (marqueur odoo-python)',
        )
        self.assertIn(self.MSGID, translations)
        self.assertIn('demandé', translations[self.MSGID].lower())
        self.assertNotIn('You requested', translations[self.MSGID])

    def test_shop_warning_french_locale(self):
        if not self.fr_lang:
            self.skipTest('Langue fr_FR absente de cette base de test')
        line = self._make_line()
        warning = line.with_context(lang='fr_FR')._set_shop_warning_stock(9, 2, save=False)
        self.assertIn('9', warning)
        self.assertIn('2', warning)
        self.assertNotIn('unité(s)', warning)
        self.assertIn('demandé', warning.lower())
        self.assertIn('disponible', warning.lower())
        self.assertNotIn('You requested', warning)
