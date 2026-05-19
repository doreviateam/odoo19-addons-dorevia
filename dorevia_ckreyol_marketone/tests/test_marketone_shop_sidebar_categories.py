# -*- coding: utf-8 -*-
"""Tests sidebar /shop — facette multi-catégories principales."""

from urllib.parse import parse_qs, urlparse

from odoo.tests import tagged
from odoo.tests.common import HttpCase, TransactionCase

from odoo.addons.dorevia_ckreyol_marketone.controllers.website_sale import (
    MARKETONE_CATEGORY_PARAM,
)
from odoo.addons.dorevia_ckreyol_marketone.models.marketone_shop_category import (
    MARKETONE_PRIMARY_PUBLIC_CATEGORY_NAMES,
    MARKETONE_SECONDARY_PUBLIC_CATEGORY_NAMES,
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


@tagged("post_install", "-at_install", "dorevia_marketone_shop_sidebar")
class TestMarketoneShopSidebarCategoriesModel(TransactionCase):
    """``_search_get_detail`` — facette OR multi-catégories."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.website = cls.env.ref("website.default_website")
        cls.Category = cls.env["product.public.category"].sudo()
        cls.biscuits = cls.Category.search(
            [("name", "=", "Biscuits salés"), ("website_id", "=", cls.website.id)],
            limit=1,
        )
        cls.epices = cls.Category.search(
            [("name", "=", "Épices"), ("website_id", "=", cls.website.id)],
            limit=1,
        )

    def test_search_get_detail_public_category_ids_or(self):
        if not self.biscuits or not self.epices:
            self.skipTest("Catégories recette Biscuits salés / Épices requises")
        detail = self.env["product.template"]._search_get_detail(
            self.website,
            "list_price asc",
            _website_sale_search_options(
                self.env,
                marketone_public_category_ids=[self.biscuits.id, self.epices.id],
            ),
        )
        flat = str(detail.get("base_domain"))
        self.assertIn("public_categ_ids", flat)
        self.assertIn(str(self.biscuits.id), flat)
        self.assertIn(str(self.epices.id), flat)

    def test_resolve_primary_rejects_secondary_slug(self):
        incontournables = self.Category.search(
            [("name", "=", "Incontournables"), ("website_id", "=", self.website.id)],
            limit=1,
        )
        if not incontournables:
            self.skipTest("Catégorie Incontournables absente")
        slug = self.env["ir.http"]._slug(incontournables)
        resolved = self.Category._marketone_resolve_primary_categories_from_slugs(
            [slug], website=self.website
        )
        self.assertFalse(resolved)


@tagged("post_install", "-at_install", "dorevia_marketone_shop_sidebar")
class TestMarketoneShopSidebarCategories(HttpCase):
    """Sidebar : 13 principales ; facette ``marketone_category`` multi OR."""

    def _sidebar_block(self, html):
        start = html.find('class="products_categories')
        self.assertGreater(start, -1)
        end = html.find("products_attributes_filters", start)
        self.assertGreater(end, start)
        return html[start:end]

    def test_primary_categories_helper_excludes_secondaries(self):
        primary = self.env["product.public.category"]._marketone_primary_public_categories()
        names = set(primary.mapped("name"))
        self.assertTrue(names)
        self.assertFalse(names & MARKETONE_SECONDARY_PUBLIC_CATEGORY_NAMES)
        for expected in MARKETONE_PRIMARY_PUBLIC_CATEGORY_NAMES:
            if expected in names:
                continue
            rec = self.env["product.public.category"].search(
                [("name", "=", expected), ("website_id", "!=", False)], limit=1
            )
            if rec and rec.has_published_products:
                self.assertIn(expected, names)

    def test_shop_dom_scope_wrap_not_oe_website_sale(self):
        """JS sidebar : ``marketone-shop`` sur ``#wrap``, pas sur ``.oe_website_sale``."""
        response = self.url_open("/shop")
        self.assertEqual(response.status_code, 200)
        html = response.text
        self.assertRegex(
            html,
            r'<div[^>]+id="wrap"[^>]+class="[^"]*\bmarketone-shop\b',
            "marketone-shop doit être sur #wrap (Lot 3)",
        )
        self.assertNotRegex(
            html,
            r'class="[^"]*\boe_website_sale\b[^"]*\bmarketone-shop\b[^"]*"',
            "marketone-shop ne doit pas être sur le même nœud que oe_website_sale",
        )

    def test_shop_sidebar_lists_primary_categories(self):
        response = self.url_open("/shop")
        self.assertEqual(response.status_code, 200)
        block_html = self._sidebar_block(response.text)
        self.assertIn("marketone-sidebar-cat-check", block_html)
        self.assertIn("Biscuits salés", block_html)
        self.assertIn("Miels", block_html)
        self.assertNotIn("Tous les produits", block_html)
        self.assertNotIn("All Products", block_html)

    def test_shop_no_horizontal_categories_filmstrip(self):
        """Bandeau horizontal catégories masqué — filtres = sidebar."""
        response = self.url_open("/shop")
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b"o_wsale_categories_filmstrip", response.content)
        self.assertNotIn(b"o_wsale_filmstrip", response.content)

    def test_shop_sidebar_categories_block_hides_secondaries(self):
        response = self.url_open("/shop")
        self.assertEqual(response.status_code, 200)
        block_html = self._sidebar_block(response.text)
        self.assertIn("Catégories", block_html)
        self.assertNotIn("Incontournables", block_html)
        self.assertNotIn("Apéritif créole", block_html)

    def test_shop_filter_single_category_query(self):
        cat = self.env["product.public.category"].search(
            [("name", "=", "Biscuits salés")], limit=1
        )
        self.assertTrue(cat)
        slug = self.env["ir.http"]._slug(cat)
        response = self.url_open(f"/shop?{MARKETONE_CATEGORY_PARAM}={slug}")
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"Crackers manioc", response.content)
        block_html = self._sidebar_block(response.text)
        self.assertIn("checked", block_html)

    def test_shop_category_and_origin_attribute_combined(self):
        """Catégories + attribut Origine : AND — paramètres conservés."""
        biscuits = self.env["product.public.category"].search(
            [("name", "=", "Biscuits salés")], limit=1
        )
        self.assertTrue(biscuits)
        attr_origin = self.env.ref(
            "dorevia_ckreyol_marketone.marketone_product_attribute_origin",
            raise_if_not_found=False,
        )
        if not attr_origin:
            self.skipTest("Attribut Origine non installé")
        martinique = self.env["product.attribute.value"].search(
            [
                ("attribute_id", "=", attr_origin.id),
                ("name", "=", "Martinique"),
            ],
            limit=1,
        )
        if not martinique:
            self.skipTest("Valeur Martinique absente")
        ir_http = self.env["ir.http"]
        url = (
            f"/shop?{MARKETONE_CATEGORY_PARAM}={ir_http._slug(biscuits)}"
            f"&attribute_values={attr_origin.id}-{martinique.id}"
        )
        response = self.url_open(url)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"marketone_category=", response.request.path_url.encode())
        self.assertIn(b"attribute_values=", response.request.path_url.encode())
        block_html = self._sidebar_block(response.text)
        self.assertIn("checked", block_html)

    def test_shop_filter_multi_category_or(self):
        """G11 — Biscuits salés OU Épices."""
        biscuits = self.env["product.public.category"].search(
            [("name", "=", "Biscuits salés")], limit=1
        )
        epices = self.env["product.public.category"].search(
            [("name", "=", "Épices")], limit=1
        )
        if not biscuits or not epices:
            self.skipTest("Catégories recette requises")
        ir_http = self.env["ir.http"]
        url = (
            f"/shop?{MARKETONE_CATEGORY_PARAM}={ir_http._slug(biscuits)}"
            f"&{MARKETONE_CATEGORY_PARAM}={ir_http._slug(epices)}"
        )
        response = self.url_open(url)
        self.assertEqual(response.status_code, 200)
        html = response.text
        self.assertIn(b"Crackers manioc", response.content)
        product_epice = self.env["product.template"].search(
            [
                ("sale_ok", "=", True),
                ("website_published", "=", True),
                ("public_categ_ids", "in", epices.ids),
            ],
            limit=1,
        )
        if product_epice:
            self.assertIn(
                product_epice.name.encode("utf-8"),
                response.content,
            )

    def test_shop_invalid_secondary_category_slug_empty(self):
        incontournables = self.env["product.public.category"].search(
            [("name", "=", "Incontournables")], limit=1
        )
        if not incontournables:
            self.skipTest("Incontournables absent")
        slug = self.env["ir.http"]._slug(incontournables)
        response = self.url_open(f"/shop?{MARKETONE_CATEGORY_PARAM}={slug}")
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b"Crackers manioc", response.content)

    def test_incontournables_porte_non_regression(self):
        response = self.url_open("/incontournables", allow_redirects=False)
        self.assertIn(response.status_code, (301, 302))
        location = response.headers.get("Location", "")
        self.assertIn("marketone_mode=featured", location)
        parsed = urlparse(location)
        self.assertNotIn(MARKETONE_CATEGORY_PARAM, parse_qs(parsed.query))
