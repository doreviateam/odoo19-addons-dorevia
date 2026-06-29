# -*- coding: utf-8 -*-
"""Recette Breadcrumb-U1 — icône racine shop dans le fil d'Ariane."""

import re

from odoo.tests import tagged
from odoo.tests.common import HttpCase


@tagged('post_install', '-at_install', 'dorevia_ck_breadcrumb_u1')
class TestCkBreadcrumbU1(HttpCase):
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
                'dorevia_ck_marketone_content non installé — recette breadcrumb non applicable'
            )

        cls.product = cls.env['product.template'].sudo().search([
            ('is_published', '=', True),
            ('public_categ_ids', '!=', False),
        ], limit=1)
        if not cls.product:
            raise cls.skipTest('Aucun produit publié avec catégorie publique.')
        cls.category = cls.product.public_categ_ids[:1]

    def _open(self, path):
        response = self.url_open(path, headers=self.FR_HEADERS)
        self.assertEqual(response.status_code, 200, path)
        return response.text

    def _breadcrumbs(self, html):
        return re.findall(r'<ol[^>]*breadcrumb[^>]*>[\s\S]*?</ol>', html)

    def _assert_shop_root_icon(self, breadcrumb):
        self.assertIn('class="ck-breadcrumb-root"', breadcrumb)
        self.assertRegex(breadcrumb, r'href="(?:/[a-z]{2}(?:-[A-Z]{2})?)?/shop"')
        self.assertIn('aria-label="Tous les produits"', breadcrumb)
        self.assertIn('title="Tous les produits"', breadcrumb)
        self.assertRegex(
            breadcrumb,
            r'<i[^>]*class="fa fa-home"[^>]*aria-hidden="true"',
        )
        self.assertIn('<span class="visually-hidden">Tous les produits</span>', breadcrumb)
        self.assertNotRegex(breadcrumb, r'>\s*(Products|All Products)\s*<')

    def test_shop_without_category_has_no_breadcrumb(self):
        html = self._open('/shop?qa_ts=breadcrumb_u1')
        self.assertFalse(self._breadcrumbs(html))

    def test_category_breadcrumb_root_is_home_icon(self):
        slug = self.env['ir.http'].sudo()._slug(self.category)
        html = self._open(f'/shop/category/{slug}?qa_ts=breadcrumb_u1')
        breadcrumbs = self._breadcrumbs(html)
        self.assertEqual(len(breadcrumbs), 1)
        self._assert_shop_root_icon(breadcrumbs[0])
        self.assertIn(self.category.name, breadcrumbs[0])

    def test_product_breadcrumb_root_is_home_icon(self):
        html = self._open(f'{self.product.website_url}?qa_ts=breadcrumb_u1')
        breadcrumbs = self._breadcrumbs(html)
        self.assertEqual(len(breadcrumbs), 1)
        self._assert_shop_root_icon(breadcrumbs[0])
        self.assertIn(self.product.name, breadcrumbs[0])
