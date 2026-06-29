# -*- coding: utf-8 -*-
from odoo.tests import tagged
from odoo.tests.common import TransactionCase

from odoo.addons.dorevia_ck_theme.product_card_ribbon import ck_product_ribbon_badge_class


@tagged('post_install', '-at_install', 'dorevia_ck_shop_card')
class TestCkProductRibbonBadgeClass(TransactionCase):
    def _ribbon(self, name):
        return self.env['product.ribbon'].create({'name': name})

    def test_mapping_nouveau(self):
        self.assertEqual(ck_product_ribbon_badge_class(self._ribbon('Nouveau !')), 'badge-new')

    def test_mapping_coups_de_coeur(self):
        self.assertEqual(
            ck_product_ribbon_badge_class(self._ribbon('Coup de cœur')),
            'badge-heart',
        )

    def test_mapping_fallback_ribbon(self):
        self.assertEqual(
            ck_product_ribbon_badge_class(self._ribbon('Agriculture Bio')),
            'badge-ribbon',
        )

    def test_ribbon_model_delegates_to_shared_mapping(self):
        ribbon = self._ribbon('Promo été')
        self.assertEqual(ribbon.get_ck_card_badge_class(), 'badge-heart')
