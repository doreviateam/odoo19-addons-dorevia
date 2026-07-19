# -*- coding: utf-8 -*-
"""Exécution réelle Hoot — gardes CartLine._changeQuantity (S3-B)."""
from odoo.tests import tagged
from odoo.tests.common import HttpCase


def _hoot_hash(test_string: str) -> str:
    """Réplique HOOTCommon._generate_hash (web/tests/test_js.py)."""
    value = 0
    for char in test_string:
        value = ((value << 5) - value + ord(char)) & 0xFFFFFFFF
    return f'{value:08x}'


@tagged('post_install', '-at_install', 'dorevia_ck_cart_stock_hoot')
class TestCkCartStockWarningHoot(HttpCase):
    """Lance les tests Hoot CK via /web/tests (Chromium headless)."""

    def test_hoot_cart_stock_warning_change_quantity(self):
        """Suite Hoot CK : découverts, chargés, exécutés (dont les 2 `_changeQuantity`)."""
        # getSuitePath remplace ``../tests/`` → descripteur de suite Hoot.
        suite = '@dorevia_ck_marketone_content/ck_cart_stock_warning'
        suite_id = _hoot_hash(suite)
        url = (
            '/web/tests?headless&loglevel=2&preset=desktop&timeout=20000'
            f'&id={suite_id}'
        )
        self.browser_js(
            url,
            code='',
            ready='',
            login='admin',
            timeout=600,
            success_signal='[HOOT] Test suite succeeded',
            error_checker=lambda message: '[HOOT]' not in message,
        )
