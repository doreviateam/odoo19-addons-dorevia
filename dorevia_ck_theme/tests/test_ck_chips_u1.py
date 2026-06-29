# -*- coding: utf-8 -*-
"""Recette Chips-U1 — chips catégorie et ordre DOM zone achat fiche produit."""

import re

from odoo.tests import tagged
from odoo.tests.common import HttpCase


@tagged('post_install', '-at_install', 'dorevia_ck_chips_u1')
class TestCkChipsU1(HttpCase):
    FR_HEADERS = {'Accept-Language': 'fr-FR,fr;q=0.9'}

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        content = cls.env['ir.module.module'].sudo().search([
            ('name', '=', 'dorevia_ck_marketone_content'),
            ('state', '=', 'installed'),
        ], limit=1)
        if not content:
            raise cls.skipTest(
                'dorevia_ck_marketone_content non installé — recette chips non applicable'
            )

        cls.category = cls.env['product.public.category'].sudo().create({
            'name': 'Chips U1 QA Catégorie',
        })
        cls.product_with_categ = cls.env['product.template'].sudo().create({
            'name': 'Chips U1 QA Produit',
            'type': 'consu',
            'list_price': 5.0,
            'sale_ok': True,
            'is_published': True,
            'public_categ_ids': [(6, 0, [cls.category.id])],
            'description_ecommerce': '<p>Accroche courte Chips U1 QA.</p>',
        })
        cls.product_without_categ = cls.env['product.template'].sudo().create({
            'name': 'Chips U1 QA Sans catégorie',
            'type': 'consu',
            'list_price': 5.0,
            'sale_ok': True,
            'is_published': True,
        })

    def _open(self, path):
        response = self.url_open(path, headers=self.FR_HEADERS)
        self.assertEqual(response.status_code, 200, path)
        return response.text

    def _title_section(self, html):
        match = re.search(
            r'o_wsale_product_details_content_section_title[\s\S]*?'
            r'o_wsale_product_details_content_section_price',
            html,
        )
        self.assertTrue(match, 'Section titre produit introuvable.')
        return match.group(0)

    def test_chips_render_with_category_link(self):
        html = self._open(f'{self.product_with_categ.website_url}?qa_ts=chips_u1')
        zone = self._title_section(html)

        self.assertRegex(
            zone,
            r'<h1[^>]*class="[^"]*ck-product-purchase__title[^"]*"[^>]*>'
            r'[\s\S]*?Chips U1 QA Produit[\s\S]*?</h1>',
        )
        self.assertIn('ck-product-purchase__chips', zone)
        slug = self.env['ir.http'].sudo()._slug(self.category)
        self.assertRegex(
            zone,
            rf'<a[^>]*class="ck-chip"[^>]*href="/shop/category/{re.escape(slug)}"',
        )
        self.assertIn(self.category.name, zone)

    def test_chips_anchor_kept_without_category(self):
        html = self._open(f'{self.product_without_categ.website_url}?qa_ts=chips_u1')
        zone = self._title_section(html)

        self.assertIn('ck-product-purchase__chips', zone)
        self.assertNotRegex(zone, r'<a[^>]*class="ck-chip"')

    def test_buy_zone_dom_order_title_chips_lead(self):
        html = self._open(f'{self.product_with_categ.website_url}?qa_ts=chips_u1')
        zone = self._title_section(html)

        title_pos = zone.index('ck-product-purchase__title">')
        chips_pos = zone.index('ck-product-purchase__chips')
        lead_pos = zone.index('ck-product-purchase__lead')
        self.assertLess(title_pos, chips_pos)
        self.assertLess(chips_pos, lead_pos)
        self.assertIn('Accroche courte Chips U1 QA.', zone)
