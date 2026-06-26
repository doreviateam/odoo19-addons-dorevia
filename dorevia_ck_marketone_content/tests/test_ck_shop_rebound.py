# -*- coding: utf-8 -*-
"""Tests Note 07 Lot C — shop_rebound.ck_should_show_rebound / ck_shop_has_active_filters."""

from odoo.tests import tagged
from odoo.tests.common import TransactionCase

from odoo.addons.dorevia_ck_marketone_content.shop_rebound import (
    CK_REBOUND_MESSAGE,
    ck_shop_has_active_filters,
    ck_should_show_rebound,
)


def _values(category=None, search_count=0, search='', original_search=False,
            tags='', attrib_set=None,
            min_price=None, available_min_price=None,
            max_price=None, available_max_price=None):
    v = {
        'category': category,
        'search_count': search_count,
        'search': search,
        'original_search': original_search,
        'tags': tags,
        'attrib_set': attrib_set if attrib_set is not None else set(),
    }
    if min_price is not None:
        v['min_price'] = min_price
        v['available_min_price'] = min_price if available_min_price is None else available_min_price
    if max_price is not None:
        v['max_price'] = max_price
        v['available_max_price'] = max_price if available_max_price is None else available_max_price
    return v


@tagged('post_install', '-at_install', 'dorevia_ck_shop_note07_rebound')
class TestCkShopRebound(TransactionCase):

    def _make_cat(self, name='Boissons'):
        return self.env['product.public.category'].sudo().create({'name': name})

    # ---- ck_should_show_rebound ----

    def test_show_when_1_product(self):
        self.assertTrue(ck_should_show_rebound(_values(self._make_cat(), search_count=1), {}))

    def test_rebound_message_v1_copy(self):
        self.assertIn("s'enrichit progressivement", CK_REBOUND_MESSAGE)
        self.assertIn("origine, au producteur et à la qualité", CK_REBOUND_MESSAGE)
        self.assertNotIn("Découvrez d'autres produits créoles", CK_REBOUND_MESSAGE)

    def test_show_when_2_products(self):
        self.assertTrue(ck_should_show_rebound(_values(self._make_cat(), search_count=2), {}))

    def test_no_show_when_0_products(self):
        self.assertFalse(ck_should_show_rebound(_values(self._make_cat(), search_count=0), {}))

    def test_no_show_when_3_products(self):
        self.assertFalse(ck_should_show_rebound(_values(self._make_cat(), search_count=3), {}))

    def test_no_show_when_more_products(self):
        for n in (4, 10, 100):
            self.assertFalse(ck_should_show_rebound(_values(self._make_cat(), search_count=n), {}))

    def test_no_show_without_category(self):
        self.assertFalse(ck_should_show_rebound(_values(None, search_count=1), {}))

    def test_no_show_when_search(self):
        self.assertFalse(ck_should_show_rebound(_values(self._make_cat(), search_count=1, search='coco'), {}))

    def test_no_show_when_original_search(self):
        self.assertFalse(ck_should_show_rebound(
            _values(self._make_cat(), search_count=1, original_search='cocoo'), {}))

    def test_no_show_when_attrib_filter(self):
        self.assertFalse(ck_should_show_rebound(
            _values(self._make_cat(), search_count=1, attrib_set={42}), {}))

    def test_no_show_when_tags(self):
        self.assertFalse(ck_should_show_rebound(
            _values(self._make_cat(), search_count=1, tags='5'), {}))

    def test_no_show_when_price_filtered(self):
        self.assertFalse(ck_should_show_rebound(
            _values(self._make_cat(), search_count=1,
                    min_price=5.0, available_min_price=0.0,
                    max_price=50.0, available_max_price=50.0), {}))

    # ---- ck_shop_has_active_filters ----

    def test_no_filter_empty(self):
        self.assertFalse(ck_shop_has_active_filters(_values(), {}))

    def test_attrib_set_active(self):
        self.assertTrue(ck_shop_has_active_filters(_values(attrib_set={1, 2}), {}))

    def test_tags_active(self):
        self.assertTrue(ck_shop_has_active_filters(_values(tags='5,7'), {}))

    def test_price_min_filtered(self):
        self.assertTrue(ck_shop_has_active_filters(
            _values(min_price=10.0, available_min_price=0.0,
                    max_price=100.0, available_max_price=100.0), {}))

    def test_price_max_filtered(self):
        self.assertTrue(ck_shop_has_active_filters(
            _values(min_price=0.0, available_min_price=0.0,
                    max_price=30.0, available_max_price=100.0), {}))

    def test_price_no_filter_same_range(self):
        self.assertFalse(ck_shop_has_active_filters(
            _values(min_price=0.0, available_min_price=0.0,
                    max_price=100.0, available_max_price=100.0), {}))
