# -*- coding: utf-8 -*-
"""Tests UX-1 — état utilisateur /shop (chips filtres, compteur)."""

import re
from urllib.parse import parse_qs, urlparse

from odoo.tests import tagged
from odoo.tests.common import HttpCase, TransactionCase

from odoo.addons.dorevia_ckreyol_marketone.controllers.website_sale import (
    MARKETONE_CATEGORY_PARAM,
    MARKETONE_COLLECTION_PARAM,
    _marketone_is_filtering_by_price,
    _marketone_should_preserve_price_in_urls,
)


@tagged("post_install", "-at_install", "dorevia_marketone_shop_filter_state")
class TestMarketoneShopFilterStatePriceHelper(TransactionCase):
    """R1 — bornes slider sans available_* ≠ filtre prix actif."""

    def test_slider_bounds_without_available_are_not_active_filter(self):
        self.assertFalse(
            _marketone_is_filtering_by_price(
                {"min_price": 5.2, "max_price": 18.5},
            )
        )

    def test_explicit_price_filter_when_bounds_differ(self):
        self.assertTrue(
            _marketone_is_filtering_by_price(
                {
                    "min_price": 10.0,
                    "max_price": 18.5,
                    "available_min_price": 5.2,
                    "available_max_price": 18.5,
                },
            )
        )

    def test_full_catalog_bounds_are_not_active_filter(self):
        self.assertFalse(
            _marketone_is_filtering_by_price(
                {
                    "min_price": 5.2,
                    "max_price": 18.5,
                    "available_min_price": 5.2,
                    "available_max_price": 18.5,
                },
            )
        )

    def test_single_product_bounds_are_not_preserved_in_urls(self):
        """Cas Sauces (1 produit à 6,80 €) — pas de filtre prix explicite."""
        self.assertFalse(
            _marketone_should_preserve_price_in_urls(
                {
                    "min_price": 6.8,
                    "max_price": 6.8,
                    "available_min_price": 6.8,
                    "available_max_price": 6.8,
                },
                {},
            )
        )


@tagged("post_install", "-at_install", "dorevia_marketone_shop_filter_state")
class TestMarketoneShopFilterState(HttpCase):
    """Barre chips + compteur global (TICKET_MARKETONE_UX1_SHOP_ETAT_UTILISATEUR)."""

    def _chip_bar_html(self, html):
        start = html.find('class="marketone-filter-state"')
        if start < 0:
            return ""
        end = html.find("o_wsale_products_main_row", start)
        if end < 0:
            end = start + 8000
        return html[start:end]

    def test_shop_counter_visible_without_filters(self):
        """MOA Q1 — compteur visible même sans filtre actif."""
        response = self.url_open("/shop")
        self.assertEqual(response.status_code, 200)
        html = response.text
        self.assertIn("marketone-filter-state__count", html)
        self.assertRegex(
            html,
            r"marketone-filter-state__count[^<]*<strong>\d+</strong>[\s\S]*?trouv",
        )
        self.assertNotIn('class="marketone-filter-state"', html)

    def test_shop_no_chips_without_filters(self):
        response = self.url_open("/shop")
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b"marketone-filter-chips__chip", response.content)

    def test_shop_no_chips_for_mode_origin_without_attribute_values(self):
        """MOA Q2 — pas de chip pour porte seule ``marketone_mode=origin``."""
        response = self.url_open("/shop?marketone_mode=origin")
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b"marketone-filter-chips__chip", response.content)

    def test_shop_filter_chips_single_category(self):
        cat = self.env["product.public.category"].search(
            [("name", "=", "Biscuits salés")], limit=1
        )
        self.assertTrue(cat)
        slug = self.env["ir.http"]._slug(cat)
        response = self.url_open(f"/shop?{MARKETONE_CATEGORY_PARAM}={slug}")
        self.assertEqual(response.status_code, 200)
        bar = self._chip_bar_html(response.text)
        self.assertIn("marketone-filter-chips__chip--category", bar)
        self.assertIn("Biscuits salés", bar)
        self.assertIn("Effacer les filtres", bar)
        self.assertNotIn(f"{MARKETONE_CATEGORY_PARAM}={slug}", bar.split("remove")[0])

    def test_shop_filter_chips_remove_category_keeps_origin(self):
        biscuits = self.env["product.public.category"].search(
            [("name", "=", "Biscuits salés")], limit=1
        )
        attr_origin = self.env.ref(
            "dorevia_ckreyol_marketone.marketone_product_attribute_origin",
            raise_if_not_found=False,
        )
        if not biscuits or not attr_origin:
            self.skipTest("Recette Biscuits salés + attribut Origine requises")
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
        bar = self._chip_bar_html(response.text)
        self.assertIn("Biscuits salés", bar)
        self.assertIn("Martinique", bar)
        remove_href = re.search(
            r'<a[^>]*href="([^"]+)"[^>]*class="[^"]*marketone-filter-chips__chip[^"]*"[^>]*>'
            r'[\s\S]*?Biscuits salés',
            bar,
        )
        if not remove_href:
            remove_href = re.search(
                r'<a[^>]*class="[^"]*marketone-filter-chips__chip[^"]*"[^>]*href="([^"]+)"[^>]*>'
                r'[\s\S]*?Biscuits salés',
                bar,
            )
        self.assertTrue(remove_href, "Lien retrait catégorie attendu")
        href = remove_href.group(1).replace("&amp;", "&")
        parsed = urlparse(href)
        qs = parse_qs(parsed.query)
        self.assertNotIn(
            MARKETONE_CATEGORY_PARAM,
            qs,
            f"La chip catégorie doit retirer {MARKETONE_CATEGORY_PARAM} : {href}",
        )
        self.assertIn(
            f"{attr_origin.id}-{martinique.id}",
            qs.get("attribute_values", []),
            href,
        )
        self.assertNotIn("min_price", qs, href)
        self.assertNotIn("max_price", qs, href)

    def test_shop_chip_remove_category_no_implicit_price(self):
        """Retrait catégorie sans filtre prix explicite — pas de min/max dans l’URL."""
        cat = self.env["product.public.category"].search(
            [("name", "=", "Biscuits salés")], limit=1
        )
        self.assertTrue(cat)
        slug = self.env["ir.http"]._slug(cat)
        response = self.url_open(f"/shop?{MARKETONE_CATEGORY_PARAM}={slug}")
        self.assertEqual(response.status_code, 200)
        bar = self._chip_bar_html(response.text)
        remove_href = re.search(
            r'<a[^>]*href="([^"]+)"[^>]*class="[^"]*marketone-filter-chips__chip[^"]*"[^>]*>'
            r'[\s\S]*?Biscuits salés',
            bar,
        )
        if not remove_href:
            remove_href = re.search(
                r'<a[^>]*class="[^"]*marketone-filter-chips__chip[^"]*"[^>]*href="([^"]+)"[^>]*>'
                r'[\s\S]*?Biscuits salés',
                bar,
            )
        self.assertTrue(remove_href)
        qs = parse_qs(urlparse(remove_href.group(1).replace("&amp;", "&")).query)
        self.assertNotIn("min_price", qs)
        self.assertNotIn("max_price", qs)

    def test_shop_filter_chips_single_collection(self):
        coll = self.env["marketone.shop.collection"].search(
            [("website_published", "=", True)], limit=1
        )
        if not coll:
            self.skipTest("Collection publiée requise")
        response = self.url_open(
            f"/shop?{MARKETONE_COLLECTION_PARAM}={coll.slug}"
        )
        self.assertEqual(response.status_code, 200)
        bar = self._chip_bar_html(response.text)
        self.assertIn("marketone-filter-chips__chip--collection", bar)
        self.assertIn(coll.name, bar)
        self.assertNotIn(
            f"{MARKETONE_COLLECTION_PARAM}={coll.slug}",
            bar.split(coll.name)[0][-200:],
        )

    def test_shop_reset_filters_url_matches_sidebar_clear(self):
        cat = self.env["product.public.category"].search(
            [("name", "=", "Biscuits salés")], limit=1
        )
        self.assertTrue(cat)
        slug = self.env["ir.http"]._slug(cat)
        response = self.url_open(f"/shop?{MARKETONE_CATEGORY_PARAM}={slug}")
        self.assertEqual(response.status_code, 200)
        html = response.text
        bar = self._chip_bar_html(html)
        chip_reset = re.search(
            r'marketone-filter-chips__reset[^>]*href="([^"]+)"', bar
        )
        self.assertTrue(chip_reset)
        sidebar_start = html.find('id="products_grid_before"')
        self.assertGreater(sidebar_start, -1)
        sidebar = html[sidebar_start : sidebar_start + 12000]
        sidebar_reset = re.search(
            r'href="(/shop[^"]*)"[^>]*>[\s\S]*?Clear Filters', sidebar
        )
        if not sidebar_reset:
            sidebar_reset = re.search(
                r'href="(/shop[^"]*)"[^>]*>[\s\S]*?Effacer', sidebar
            )
        self.assertTrue(sidebar_reset, "Reset sidebar attendu")
        chip_path = urlparse(chip_reset.group(1))
        side_path = urlparse(sidebar_reset.group(1))
        self.assertEqual(chip_path.path, side_path.path)
        for key in (
            "attribute_values",
            "tags",
            "min_price",
            "max_price",
            MARKETONE_CATEGORY_PARAM,
            MARKETONE_COLLECTION_PARAM,
        ):
            self.assertEqual(
                parse_qs(chip_path.query).get(key, []),
                parse_qs(side_path.query).get(key, []),
                key,
            )

    def test_shop_filter_chips_remove_collection_no_implicit_price(self):
        coll = self.env["marketone.shop.collection"].search(
            [("website_published", "=", True)], limit=1
        )
        if not coll:
            self.skipTest("Collection publiée requise")
        response = self.url_open(
            f"/shop?{MARKETONE_COLLECTION_PARAM}={coll.slug}"
        )
        self.assertEqual(response.status_code, 200)
        bar = self._chip_bar_html(response.text)
        remove_href = re.search(
            r'<a[^>]*href="([^"]+)"[^>]*class="[^"]*marketone-filter-chips__chip[^"]*"[^>]*>'
            rf'[\s\S]*?{re.escape(coll.name)}',
            bar,
        )
        if not remove_href:
            remove_href = re.search(
                r'<a[^>]*class="[^"]*marketone-filter-chips__chip[^"]*"[^>]*href="([^"]+)"[^>]*>'
                rf'[\s\S]*?{re.escape(coll.name)}',
                bar,
            )
        self.assertTrue(remove_href, "Lien retrait collection attendu")
        qs = parse_qs(urlparse(remove_href.group(1).replace("&amp;", "&")).query)
        self.assertNotIn("min_price", qs)
        self.assertNotIn("max_price", qs)

    def test_shop_price_chip_has_prefix(self):
        """MOA Q3 — chip prix avec préfixe « Prix »."""
        response = self.url_open("/shop?min_price=1&max_price=99999")
        self.assertEqual(response.status_code, 200)
        bar = self._chip_bar_html(response.text)
        if "marketone-filter-chips__chip--price" not in bar:
            self.skipTest("Filtre prix non actif sur cette base (bornes catalogue)")
        self.assertIn("Prix :", bar)
