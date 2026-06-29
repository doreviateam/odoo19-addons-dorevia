# -*- coding: utf-8 -*-
"""Polish-U3 — CTA panier mobile cards Home (parité Shop ≤575px)."""

import os

from odoo.tests import tagged
from odoo.tests.common import TransactionCase
from odoo.modules.module import get_module_path


@tagged('post_install', '-at_install', 'dorevia_ck_shop_card')
class TestCkPolishU3HomeMobileCta(TransactionCase):
    def test_home_mobile_cta_scss_canon_present(self):
        scss_path = os.path.join(
            get_module_path('dorevia_ck_theme'),
            'static/src/scss/website.scss',
        )
        with open(scss_path, encoding='utf-8') as handle:
            source = handle.read()
        self.assertIn('Polish-U3', source)
        self.assertRegex(
            source,
            r'ck-product-card--home[\s\S]{0,5000}@media \(max-width: 575\.98px\)',
        )
        mobile_chunk = source.split('Polish-U3', 1)[1][:1200]
        for needle in (
            'min-height: 44px',
            'padding: 8px 14px',
            'font-size: 12px',
            'width: 100%',
            'flex-direction: column !important',
        ):
            self.assertIn(needle, mobile_chunk, needle)
