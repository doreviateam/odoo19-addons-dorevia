# -*- coding: utf-8 -*-
"""Garde-fous régressions /shop — UX-1 (R1/R2) + C4 sidebar.

Tag unique pour CI / recette rapide :

    --test-tags=dorevia_marketone_shop_regression
"""

import re
from urllib.parse import parse_qs, urlparse

from odoo.tests import tagged
from odoo.tests.common import HttpCase

from odoo.addons.dorevia_ckreyol_marketone.controllers.website_sale import (
    MARKETONE_CATEGORY_PARAM,
)


@tagged("post_install", "-at_install", "dorevia_marketone_shop_regression")
class TestMarketoneShopRegression(HttpCase):
    """Détection ciblée des régressions connues (prix implicite, sidebar C4)."""

    def _sidebar_categories_block(self, html):
        start = html.find("marketone-shop-categories-accordion")
        self.assertGreater(start, -1)
        end = html.find("marketone-shop-collections-accordion", start)
        if end < 0:
            end = html.find("products_attributes_filters", start)
        self.assertGreater(end, start)
        return html[start:end]

    def _chip_bar(self, html):
        start = html.find("marketone-filter-chips")
        if start < 0:
            return ""
        end = html.find("products_header btn-toolbar", start)
        if end < 0:
            end = html.find("o_wsale_products_grid_table_wrapper", start)
        return html[start : end if end > start else start + 4000]

    def test_ux1_chip_bar_after_toolbar_above_grid(self):
        """Barre chips sous la ligne recherche / résultat / tri."""
        cat = self.env["product.public.category"].search(
            [("name", "=", "Condiments")], limit=1
        )
        self.assertTrue(cat, "Catégorie Condiments requise")
        slug = self.env["ir.http"]._slug(cat)
        response = self.url_open(f"/shop?{MARKETONE_CATEGORY_PARAM}={slug}")
        self.assertEqual(response.status_code, 200)
        html = response.text
        grid_start = html.find('id="products_grid"')
        self.assertGreater(grid_start, -1)
        header_start = html.find('id="o_wsale_products_header"', grid_start)
        self.assertGreater(header_start, -1)
        header_end = html.find("</header>", header_start)
        header_html = html[header_start:header_end]
        bar_pos = header_html.find('aria-label="Filtres actifs"')
        toolbar_pos = header_html.find("marketone-shop-catalog-toolbar")
        self.assertGreater(bar_pos, -1)
        self.assertGreater(toolbar_pos, -1)
        self.assertGreater(bar_pos, toolbar_pos)
        grid_pos = html.find("o_wsale_products_grid_table_wrapper", header_end)
        self.assertGreater(grid_pos, header_end)
        bar = self._chip_bar(html)
        self.assertIn("marketone-filter-chips__group", bar)
        reset_pos = bar.find("marketone-filter-chips__reset")
        first_chip_pos = bar.find("marketone-filter-chips__chip")
        self.assertGreater(reset_pos, -1)
        self.assertGreater(first_chip_pos, reset_pos)
        self.assertIn("marketone-filter-chips__chip--", bar)

    def test_r1_chip_remove_category_no_implicit_price(self):
        """R1 — retrait chip catégorie sans min_price/max_price dans l’URL."""
        cat = self.env["product.public.category"].search(
            [("name", "=", "Condiments")], limit=1
        )
        if not cat:
            cat = self.env["product.public.category"].search(
                [("name", "=", "Sauces")], limit=1
            )
        self.assertTrue(cat, "Catégorie Condiments ou Sauces requise")
        slug = self.env["ir.http"]._slug(cat)
        response = self.url_open(f"/shop?{MARKETONE_CATEGORY_PARAM}={slug}")
        self.assertEqual(response.status_code, 200)
        bar = self._chip_bar(response.text)
        if "marketone-filter-chips__chip" not in bar:
            self.skipTest("Barre chips absente — UX-1 non déployé sur cette base")
        remove = re.search(
            rf'<a[^>]*href="([^"]+)"[^>]*>[\s\S]*?{re.escape(cat.name)}',
            bar,
        )
        if not remove:
            remove = re.search(
                rf'<a[^>]*class="[^"]*marketone-filter-chips__chip[^"]*"[^>]*href="([^"]+)"[^>]*>[\s\S]*?{re.escape(cat.name)}',
                bar,
            )
        self.assertTrue(remove, "Lien retrait chip catégorie attendu")
        qs = parse_qs(urlparse(remove.group(1).replace("&amp;", "&")).query)
        self.assertNotIn("min_price", qs, remove.group(1))
        self.assertNotIn("max_price", qs, remove.group(1))

    def test_c4_sidebar_keeps_primaries_when_category_active(self):
        """C4 — une catégorie active ne réduit pas la sidebar à 2 entrées."""
        condiments = self.env["product.public.category"].search(
            [("name", "=", "Condiments")], limit=1
        )
        if not condiments:
            self.skipTest("Condiments absent")
        slug = self.env["ir.http"]._slug(condiments)
        baseline = self.url_open("/shop")
        base_slugs = set(
            re.findall(
                r'data-category-slug="([^"]+)"',
                self._sidebar_categories_block(baseline.text),
            )
        )
        filtered = self.url_open(f"/shop?{MARKETONE_CATEGORY_PARAM}={slug}")
        filt_slugs = set(
            re.findall(
                r'data-category-slug="([^"]+)"',
                self._sidebar_categories_block(filtered.text),
            )
        )
        self.assertGreaterEqual(len(base_slugs), 10)
        self.assertGreaterEqual(
            len(filt_slugs),
            len(base_slugs) - 1,
            f"Sidebar réduite après filtre catégorie : {sorted(filt_slugs)}",
        )

    def test_no_sidebar_clear_filters_when_chips_visible(self):
        """Reset unique — pas de Clear Filters dans la sidebar."""
        cat = self.env["product.public.category"].search(
            [("name", "=", "Condiments")], limit=1
        )
        if not cat:
            self.skipTest("Condiments absent")
        slug = self.env["ir.http"]._slug(cat)
        response = self.url_open(f"/shop?{MARKETONE_CATEGORY_PARAM}={slug}")
        self.assertEqual(response.status_code, 200)
        html = response.text
        self.assertIn("marketone-filter-chips__reset", html)
        sidebar_start = html.find('id="products_grid_before"')
        sidebar = html[sidebar_start : sidebar_start + 12000]
        self.assertNotIn("Clear Filters", sidebar)

    def test_r2_grid_title_in_header_not_toolbar(self):
        """R2 — compteur discret en ligne résultat, absent de la toolbar tri."""
        response = self.url_open("/shop")
        self.assertEqual(response.status_code, 200)
        html = response.text
        self.assertIn('id="products_grid_content_title"', html)
        self.assertIn("marketone-shop-grid-result", html)
        self.assertIn("produits disponibles", html)
        self.assertNotIn("marketone-filter-state__count", html)
