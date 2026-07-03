# -*- coding: utf-8 -*-
"""CATALOG-ARCHI-001 Lot C — ck_category_route_action / website_indexed / sitemap."""

from odoo.tests import tagged
from odoo.tests.common import TransactionCase

from odoo.addons.dorevia_ck_marketone_content.ck_category_routing import (
    ck_category_route_action,
)


@tagged('post_install', '-at_install', 'dorevia_ck_catalog_routing')
class TestCkCategoryRouteAction(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Category = cls.env['product.public.category'].sudo()

    def _make_category(self, name, **vals):
        return self.Category.create({'name': name, **vals})

    def test_active_renders(self):
        cat = self._make_category('TestCat Route Active', ck_exposure_status='active')
        self.assertEqual(ck_category_route_action(cat), {'action': 'render'})

    def test_promise_redirects_302_to_shop(self):
        cat = self._make_category('TestCat Route Promise', ck_exposure_status='promise')
        action = ck_category_route_action(cat)
        self.assertEqual(action['action'], 'redirect')
        self.assertEqual(action['url'], '/shop')
        self.assertEqual(action['code'], 302)

    def test_hidden_redirects_302_to_shop(self):
        cat = self._make_category('TestCat Route Hidden', ck_exposure_status='hidden')
        action = ck_category_route_action(cat)
        self.assertEqual(action['action'], 'redirect')
        self.assertEqual(action['url'], '/shop')
        self.assertEqual(action['code'], 302)

    def test_draft_notfound(self):
        cat = self._make_category('TestCat Route Draft', ck_exposure_status='draft')
        self.assertEqual(ck_category_route_action(cat), {'action': 'notfound'})

    def test_archived_with_replacement_redirects_301(self):
        replacement = self._make_category('TestCat Route Remplacante')
        cat = self._make_category(
            'TestCat Route Archived Avec Remplacante',
            ck_exposure_status='archived',
            ck_replacement_category_id=replacement.id,
        )
        action = ck_category_route_action(cat)
        self.assertEqual(action['action'], 'redirect')
        self.assertEqual(action['code'], 301)
        self.assertIn(str(replacement.id), action['url'])

    def test_archived_without_replacement_notfound(self):
        cat = self._make_category('TestCat Route Archived Sans Remplacante', ck_exposure_status='archived')
        self.assertEqual(ck_category_route_action(cat), {'action': 'notfound'})


@tagged('post_install', '-at_install', 'dorevia_ck_catalog_routing')
class TestCkWebsiteIndexed(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Category = cls.env['product.public.category'].sudo()
        cls.Product = cls.env['product.template'].sudo()

    def _make_qualified_category(self, name, count=3):
        cat = self.Category.create({'name': name})
        for idx in range(count):
            self.Product.create({
                'name': f'{name} Produit {idx}',
                'sale_ok': True,
                'is_published': True,
                'website_published': True,
                'public_categ_ids': [(4, cat.id)],
            })
        return cat

    def test_active_exposable_is_indexed(self):
        cat = self._make_qualified_category('TestCat Indexed Active', count=3)
        self.assertTrue(cat.website_indexed)

    def test_active_but_not_exposable_is_not_indexed(self):
        """'active' de statut mais sous le seuil produits → non indexable (§10 note_11)."""
        cat = self._make_qualified_category('TestCat Indexed Sous Seuil', count=1)
        self.assertFalse(cat.website_indexed)

    def test_non_active_status_never_indexed(self):
        cat = self._make_qualified_category('TestCat Indexed Hidden', count=5)
        cat.write({'ck_exposure_status': 'hidden'})
        self.assertFalse(cat.website_indexed)


@tagged('post_install', '-at_install', 'dorevia_ck_catalog_routing')
class TestCkSitemapEnumeratePages(TransactionCase):
    """Filtrage sitemap réel (Website._enumerate_pages), pas le sitemap_func
    de website_sale seul — cf. ck_category_routing.py sur les raisons."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.website = cls.env['website'].search([], limit=1)
        cls.Category = cls.env['product.public.category'].sudo()
        cls.Product = cls.env['product.template'].sudo()

    def _make_qualified_category(self, name, count=3):
        cat = self.Category.create({'name': name})
        for idx in range(count):
            self.Product.create({
                'name': f'{name} Produit {idx}',
                'sale_ok': True,
                'is_published': True,
                'website_published': True,
                'public_categ_ids': [(4, cat.id)],
            })
        return cat

    def _sitemap_locs(self):
        return [entry['loc'] for entry in self.website._enumerate_pages()]

    def test_exposable_category_in_sitemap(self):
        cat = self._make_qualified_category('TestCat Sitemap Exposable', count=3)
        locs = self._sitemap_locs()
        self.assertTrue(any(loc.endswith(f'-{cat.id}') for loc in locs))

    def test_hidden_category_absent_from_sitemap(self):
        cat = self._make_qualified_category('TestCat Sitemap Hidden', count=5)
        cat.write({'ck_exposure_status': 'hidden'})
        locs = self._sitemap_locs()
        self.assertFalse(any(f'-{cat.id}' in loc for loc in locs))

    def test_active_below_threshold_absent_from_sitemap(self):
        """Statut 'active' mais sous le seuil produits — website_indexed=False."""
        cat = self._make_qualified_category('TestCat Sitemap Sous Seuil', count=1)
        locs = self._sitemap_locs()
        self.assertFalse(any(f'-{cat.id}' in loc for loc in locs))

    def test_shop_root_always_in_sitemap(self):
        locs = self._sitemap_locs()
        self.assertIn('/shop', locs)
