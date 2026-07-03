# -*- coding: utf-8 -*-
"""CATALOG-ARCHI-001 Lot C — comportement HTTP réel des routes catégories."""

from odoo.tests import tagged
from odoo.tests.common import HttpCase


@tagged('post_install', '-at_install', 'dorevia_ck_catalog_routing_http')
class TestCkCategoryRoutesHttp(HttpCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Category = cls.env['product.public.category'].sudo()
        cls.Product = cls.env['product.template'].sudo()

    def _make_qualified_category(self, name, count=3, **vals):
        cat = self.Category.create({'name': name, **vals})
        for idx in range(count):
            self.Product.create({
                'name': f'{name} Produit {idx}',
                'sale_ok': True,
                'is_published': True,
                'website_published': True,
                'public_categ_ids': [(4, cat.id)],
            })
        return cat

    def _category_url(self, category):
        # Préfixe /en explicite : évite la redirection 303 de négociation de
        # langue (/shop/... -> 303 -> /en/shop/...) qui interférerait avec
        # allow_redirects=False sur la redirection CK elle-même.
        slug = self.env['ir.http']._slug(category)
        return f'/en/shop/category/{slug}'

    def test_active_category_returns_200(self):
        cat = self._make_qualified_category('TestCat HTTP Active', count=3)
        response = self.url_open(self._category_url(cat))
        self.assertEqual(response.status_code, 200)

    def test_promise_category_redirects_to_shop(self):
        cat = self._make_qualified_category(
            'TestCat HTTP Promise', count=3, ck_exposure_status='promise',
        )
        response = self.url_open(self._category_url(cat), allow_redirects=False)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.headers['Location'].endswith('/shop'))

    def test_hidden_category_redirects_to_shop(self):
        cat = self._make_qualified_category(
            'TestCat HTTP Hidden', count=3, ck_exposure_status='hidden',
        )
        response = self.url_open(self._category_url(cat), allow_redirects=False)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(response.headers['Location'].endswith('/shop'))

    def test_draft_category_returns_404(self):
        cat = self._make_qualified_category(
            'TestCat HTTP Draft', count=3, ck_exposure_status='draft',
        )
        response = self.url_open(self._category_url(cat))
        self.assertEqual(response.status_code, 404)

    def test_archived_with_replacement_redirects_301(self):
        replacement = self._make_qualified_category('TestCat HTTP Remplacante', count=3)
        cat = self._make_qualified_category(
            'TestCat HTTP Archived Avec Remplacante', count=3,
            ck_exposure_status='archived', ck_replacement_category_id=replacement.id,
        )
        response = self.url_open(self._category_url(cat), allow_redirects=False)
        self.assertEqual(response.status_code, 301)
        self.assertIn(str(replacement.id), response.headers['Location'])

    def test_archived_without_replacement_returns_404(self):
        cat = self._make_qualified_category(
            'TestCat HTTP Archived Sans Remplacante', count=3,
            ck_exposure_status='archived',
        )
        response = self.url_open(self._category_url(cat))
        self.assertEqual(response.status_code, 404)

    def test_shop_root_not_regressed(self):
        response = self.url_open('/en/shop')
        self.assertEqual(response.status_code, 200)
