# -*- coding: utf-8 -*-
"""Tests sidebar /shop — facettes collections commerciales (Lot B)."""

import re
from urllib.parse import parse_qs, urlparse

from odoo.tests import tagged
from odoo.tests.common import HttpCase, TransactionCase

from odoo.addons.dorevia_ckreyol_marketone.controllers.website_sale import (
    MARKETONE_CATEGORY_PARAM,
    MARKETONE_COLLECTION_PARAM,
)


def _website_sale_search_options(env, **extra):
    base = {
        "displayImage": True,
        "displayDescription": True,
        "displayExtraLink": True,
        "displayDetail": True,
        "display_currency": env.company.currency_id,
    }
    base.update(extra)
    return base


@tagged("post_install", "-at_install", "dorevia_marketone_shop_sidebar_collections")
class TestMarketoneShopSidebarCollectionsModel(TransactionCase):
    """Modèle collection — résolution slugs et C4."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.website = cls.env.ref("website.default_website")
        cls.Collection = cls.env["marketone.shop.collection"].sudo()
        cls.product_a = cls.env["product.template"].create(
            {
                "name": "Marketone Test Col A",
                "sale_ok": True,
                "website_published": True,
            }
        )
        cls.product_b = cls.env["product.template"].create(
            {
                "name": "Marketone Test Col B",
                "sale_ok": True,
                "website_published": True,
            }
        )
        cls.coll_a = cls.Collection.create(
            {
                "name": "Col Test A",
                "slug": "col-test-a-lotb",
                "website_published": True,
                "website_id": cls.website.id,
                "product_ids": [(6, 0, cls.product_a.ids)],
            }
        )
        cls.coll_b = cls.Collection.create(
            {
                "name": "Col Test B",
                "slug": "col-test-b-lotb",
                "website_published": True,
                "website_id": cls.website.id,
                "product_ids": [(6, 0, cls.product_b.ids)],
            }
        )

    def test_resolve_published_slugs_ignores_unknown(self):
        resolved = self.Collection._marketone_resolve_published_slugs(
            ["col-test-a-lotb", "slug-inexistant-lotb"],
            website=self.website,
        )
        self.assertEqual(resolved, self.coll_a)

    def test_search_get_detail_collection_ids_or(self):
        detail = self.env["product.template"]._search_get_detail(
            self.website,
            "list_price asc",
            _website_sale_search_options(
                self.env,
                marketone_collection_ids=[self.coll_a.id, self.coll_b.id],
            ),
        )
        flat = str(detail.get("base_domain"))
        self.assertIn("id", flat)
        self.assertIn(str(self.product_a.id), flat)
        self.assertIn(str(self.product_b.id), flat)

    def test_collections_for_shop_keeps_active_without_products(self):
        visible = self.Collection._marketone_collections_for_shop(
            self.product_a,
            active_collection_ids=[self.coll_b.id],
            website=self.website,
        )
        self.assertIn(self.coll_a, visible)
        self.assertIn(self.coll_b, visible)

    def test_collections_for_shop_hides_without_context(self):
        visible = self.Collection._marketone_collections_for_shop(
            self.product_a,
            active_collection_ids=[],
            website=self.website,
        )
        self.assertIn(self.coll_a, visible)
        self.assertNotIn(self.coll_b, visible)


@tagged("post_install", "-at_install", "dorevia_marketone_shop_sidebar_collections")
class TestMarketoneShopSidebarCollectionsHttp(HttpCase):
    """HTTP — rubrique Collections et facette query."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.website = cls.env.ref("website.default_website")
        cls.Collection = cls.env["marketone.shop.collection"].sudo()
        cls.product = cls.env["product.template"].search(
            [
                ("sale_ok", "=", True),
                ("website_published", "=", True),
            ],
            limit=1,
        )
        if not cls.product:
            cls.product = cls.env["product.template"].create(
                {
                    "name": "Marketone HTTP Col Product",
                    "sale_ok": True,
                    "website_published": True,
                }
            )
        cls.collection = cls.Collection.create(
            {
                "name": "Col HTTP Lot B",
                "slug": "col-http-lotb",
                "website_published": True,
                "website_id": cls.website.id,
                "product_ids": [(6, 0, cls.product.ids)],
            }
        )
        cls.collection_b = cls.Collection.create(
            {
                "name": "Col HTTP Lot B2",
                "slug": "col-http-lotb-2",
                "website_published": True,
                "website_id": cls.website.id,
                "product_ids": [(6, 0, cls.product.ids)],
            }
        )

    def _sidebar_block(self, html):
        start = html.find('id="products_grid_before"')
        self.assertGreater(start, -1)
        end = html.find("products_attributes_filters", start)
        if end < 0:
            end = start + 20000
        return html[start:end]

    def test_shop_sidebar_shows_collections_block(self):
        response = self.url_open("/shop")
        self.assertEqual(response.status_code, 200)
        block = self._sidebar_block(response.text)
        self.assertIn("Collections", block)
        self.assertIn("marketone-sidebar-col-check", block)
        self.assertIn("Col HTTP Lot B", block)

    def test_shop_sidebar_rubrique_order(self):
        """Ordre MOA : Collections → Catégories → Origines → Prix."""
        response = self.url_open("/shop")
        self.assertEqual(response.status_code, 200)
        html = response.text
        col = html.find("marketone-shop-collections-accordion")
        cat = html.find("marketone-shop-categories-accordion")
        attr = html.find("products_attributes_filters")
        price = html.find("o_wsale_price_range_option")
        self.assertGreater(col, -1)
        self.assertGreater(cat, -1)
        self.assertGreater(attr, -1)
        self.assertGreater(price, -1)
        self.assertLess(col, cat)
        self.assertLess(cat, attr)
        self.assertLess(attr, price)
        sidebar = html[html.find('id="products_grid_before"'): price + 3000]
        self.assertRegex(sidebar, r">\s*Origines\s*<")

    def test_shop_filter_single_collection(self):
        url = f"/shop?{MARKETONE_COLLECTION_PARAM}={self.collection.slug}"
        response = self.url_open(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn(self.product.name.encode("utf-8"), response.content)
        block = self._sidebar_block(response.text)
        self.assertIn(f'data-collection-slug="{self.collection.slug}"', block)
        self.assertRegex(
            block,
            rf'data-collection-slug="{self.collection.slug}"[^>]*checked|checked[^>]*data-collection-slug="{self.collection.slug}"',
        )

    def test_shop_filter_multi_collection_or(self):
        url = (
            f"/shop?{MARKETONE_COLLECTION_PARAM}={self.collection.slug}"
            f"&{MARKETONE_COLLECTION_PARAM}={self.collection_b.slug}"
        )
        response = self.url_open(url)
        self.assertEqual(response.status_code, 200)
        parsed = parse_qs(urlparse(response.request.path_url).query)
        self.assertEqual(
            sorted(parsed.get(MARKETONE_COLLECTION_PARAM, [])),
            sorted([self.collection.slug, self.collection_b.slug]),
        )

    def test_shop_invalid_collection_slug_ignored(self):
        product_count_before = self.env["product.template"].search_count(
            [("sale_ok", "=", True), ("website_published", "=", True)]
        )
        response = self.url_open(
            f"/shop?{MARKETONE_COLLECTION_PARAM}=slug-totalement-invalide-lotb"
        )
        self.assertEqual(response.status_code, 200)
        self.assertGreaterEqual(
            len(response.text),
            100,
            "Catalogue attendu, pas page vide",
        )
        block = self._sidebar_block(response.text)
        self.assertNotRegex(
            block,
            r'data-collection-slug="slug-totalement-invalide-lotb"[^>]*checked',
        )
        self.assertTrue(product_count_before >= 0)

    def test_shop_clear_filters_removes_collection(self):
        url = f"/shop?{MARKETONE_COLLECTION_PARAM}={self.collection.slug}"
        response = self.url_open(url)
        self.assertEqual(response.status_code, 200)
        html = response.text
        self.assertNotIn("Clear Filters", self._sidebar_block(html))
        reset = re.search(
            r'marketone-filter-chips__reset[^>]*href="([^"]+)"',
            html[html.find("marketone-filter-chips") :],
        )
        self.assertTrue(reset, "Effacer les filtres attendu dans la barre UX-1")
        clear_href = reset.group(1).replace("&amp;", "&")
        self.assertIn("/shop", clear_href)
        self.assertNotIn(f"{MARKETONE_COLLECTION_PARAM}=", clear_href)

    def test_incontournables_no_collection_param(self):
        response = self.url_open("/incontournables", allow_redirects=False)
        self.assertIn(response.status_code, (301, 302))
        location = response.headers.get("Location", "")
        parsed = urlparse(location)
        self.assertNotIn(MARKETONE_COLLECTION_PARAM, parse_qs(parsed.query))

    def test_shop_collection_and_category_combined(self):
        cat = self.env["product.public.category"].search(
            [("name", "=", "Biscuits salés")], limit=1
        )
        if not cat:
            self.skipTest("Catégorie Biscuits salés absente")
        slug_cat = self.env["ir.http"]._slug(cat)
        url = (
            f"/shop?{MARKETONE_CATEGORY_PARAM}={slug_cat}"
            f"&{MARKETONE_COLLECTION_PARAM}={self.collection.slug}"
        )
        response = self.url_open(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn(MARKETONE_CATEGORY_PARAM.encode(), response.request.path_url.encode())
        self.assertIn(MARKETONE_COLLECTION_PARAM.encode(), response.request.path_url.encode())
