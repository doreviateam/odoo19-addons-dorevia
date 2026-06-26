# -*- coding: utf-8 -*-
"""Tests Micro-lot 3A — toolbar boutique (filmstrip rayons métier)."""

import html
import re

from odoo.tests import tagged
from odoo.tests.common import HttpCase, TransactionCase

from odoo.addons.dorevia_ck_marketone_content.shop_toolbar import (
    filter_ck_toolbar_categories,
    is_ck_qa_public_category,
)


@tagged('post_install', '-at_install', 'dorevia_ck_shop_s1')
class TestCkShopToolbarHttp(HttpCase):

    EXPECTED_FILMSTRIP = (
        'Épicerie',
        'Soin & Bien-être',
        'Artisanat',
        'Boissons',
    )

    def _filmstrip_aria_labels(self, page_html):
        match = re.search(
            r'id="o_wsale_categories_filmstrip"[\s\S]*?'
            r'<ul class="o_wsale_filmstrip[^"]*"[\s\S]*?</ul>',
            page_html,
        )
        self.assertTrue(match, 'Filmstrip catégories introuvable')
        return [html.unescape(label) for label in re.findall(
            r'class="o_wsale_filmstrip_link[^"]*"[^>]*aria-label="([^"]*)"',
            match.group(0),
        )]

    def test_shop_filmstrip_rayons_metier_only(self):
        page_html = self.url_open('/shop').text
        labels = self._filmstrip_aria_labels(page_html)
        self.assertEqual(labels, list(self.EXPECTED_FILMSTRIP))
        self.assertNotIn('CK Sparse Grid QA', page_html)
        self.assertNotIn('ck-sparse-grid-qa', page_html.lower())

    def test_shop_counter_wording_en_rayon(self):
        html = self.url_open('/shop').text
        self.assertIn('produits en rayon', html)
        self.assertNotIn('produits sélectionnés', html)


@tagged('post_install', '-at_install', 'dorevia_ck_shop_s1')
class TestCkShopToolbarFilter(TransactionCase):

    def test_filter_excludes_qa_and_unknown_roots(self):
        Category = self.env['product.public.category'].sudo()
        qa = Category.create({'name': 'CK Sparse Grid QA 2'})
        extra = Category.create({'name': 'Coups de cœur'})
        epicerie = Category.search([('name', '=', 'Épicerie')], limit=1)
        if not epicerie:
            epicerie = Category.create({'name': 'Épicerie'})
        roots = Category.search([('parent_id', '=', False)])
        filtered = filter_ck_toolbar_categories(roots | qa | extra)
        self.assertTrue(is_ck_qa_public_category(qa))
        self.assertNotIn(qa, filtered)
        self.assertNotIn(extra, filtered)
        self.assertIn(epicerie, filtered)
