# -*- coding: utf-8 -*-
"""Gardes S3-B1 — surface JS panier sans copie de _changeQuantity."""
from pathlib import Path

from odoo.tests import tagged
from odoo.tests.common import TransactionCase

from odoo.addons.dorevia_ck_marketone_content import __file__ as content_init


@tagged('post_install', '-at_install', 'dorevia_ck_cart_stock')
class TestCkCartStockWarningJsGuard(TransactionCase):

    def _js_source(self):
        root = Path(content_init).resolve().parent
        path = root / 'static' / 'src' / 'js' / 'ck_cart_stock_warning.js'
        self.assertTrue(path.is_file(), path)
        return path.read_text(encoding='utf-8')

    def test_js_does_not_copy_change_quantity_rpc(self):
        source = self._js_source()
        self.assertNotIn('/shop/cart/update', source)
        self.assertNotIn('redirect(', source)
        self.assertNotIn('updateCartNavBar', source)
        self.assertNotIn('async _changeQuantity', source)
        self.assertIn('patch(wSaleUtils', source)
        self.assertIn('showWarning', source)
        self.assertIn('cartNotificationService', source)

    def test_js_uses_permanent_showWarning_patch_not_await_swap(self):
        source = self._js_source()
        # F2 : pas de mutation temporaire du global pendant un await.
        self.assertNotIn('previousShowWarning', source)
        self.assertNotIn('wSaleUtils.showWarning =', source)
        self.assertIn('patch(wSaleUtils', source)
        self.assertIn('showCartStockWarningToast', source)
