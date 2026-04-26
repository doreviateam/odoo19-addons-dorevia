# -*- coding: utf-8 -*-
"""Garde-fous HTTP pour l'orchestration visuelle de la boutique Vague 1."""

from odoo.tests import tagged
from odoo.tests.common import HttpCase


@tagged("post_install", "-at_install", "dorevia_ckr_shop", "dorevia_ckr_shop_wave1")
class TestCkrShopWave1(HttpCase):
    """Verrouille les invariants d'orchestration issus de ``docs/mvp_02``."""

    def test_shop_root_uses_hero_and_shortcuts(self):
        """Le shop retail expose le hero principal et la barre commerciale."""
        resp = self.url_open("/shop", timeout=60)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('class="ckr-shop-hero', resp.text)
        self.assertIn("ckr-shop-hero--retail", resp.text)
        self.assertIn("Toute la Boutique", resp.text)  # hero + chip (maquette / 2_SHOP.md §5)
        self.assertIn("terroirs", resp.text)
        self.assertIn("créoles", resp.text)
        self.assertIn('class="ckr-shop-shortcuts', resp.text)
        self.assertNotIn('id="ckr-shop-pack-banner"', resp.text)
        self.assertNotIn('id="ckr-shop-promo-banner"', resp.text)
        self.assertNotIn('id="ckr-shop-origin-banner"', resp.text)
        self.assertNotIn('id="ckr-shop-featured-banner"', resp.text)
        self.assertNotIn('id="ckr-shop-collection-banner"', resp.text)

    def test_shop_search_hides_editorial_layers(self):
        """La recherche garde la toolbar native, sans hero ni shortcuts marketing."""
        resp = self.url_open("/shop?search=manioc", timeout=60)
        self.assertEqual(resp.status_code, 200)
        self.assertNotIn('class="ckr-shop-hero', resp.text)
        self.assertNotIn('class="ckr-shop-shortcuts', resp.text)

    def test_origin_mode_uses_hero_without_legacy_banner(self):
        """Une porte contextuelle garde le hero, mais plus l'ancien bandeau dédié."""
        resp = self.url_open("/shop?ckr_mode=origin", timeout=60)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('class="ckr-shop-hero', resp.text)
        self.assertIn("ckr-shop-hero--context", resp.text)
        self.assertIn("Origines", resp.text)
        self.assertIn('class="ckr-shop-shortcuts', resp.text)
        self.assertNotIn('id="ckr-shop-origin-banner"', resp.text)

    def test_category_page_uses_hero_with_shortcuts(self):
        """Une catégorie garde le hero et la barre commerciale (2_SHOP.md §5).

        HttpCase Odoo 19 n'autorise pas ``commit()`` : on réutilise une
        ``product.public.category`` déjà persistée (données module / recette),
        sans créer de record dans la transaction du test.
        """
        website = self.env.ref("website.default_website")
        cat = self.env["product.public.category"].search(
            [
                "|",
                ("website_id", "=", False),
                ("website_id", "=", website.id),
            ],
            limit=1,
        )
        if not cat:
            self.skipTest(
                "Aucune catégorie e-commerce publique en base — impossible "
                "de tester /shop/category sans commit HttpCase."
            )
        category_path = "/shop/category/%s" % self.env["ir.http"].sudo()._slug(
            cat
        )
        resp = self.url_open(category_path, timeout=60)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('class="ckr-shop-hero', resp.text)
        self.assertIn("ckr-shop-hero--context", resp.text)
        self.assertIn(cat.name, resp.text)
        desc = (cat.website_description or "").strip()
        if not desc:
            self.assertIn("Retrouvez la sélection", resp.text)
        else:
            self.assertIn("ckr-shop-hero__category-desc", resp.text)
        self.assertIn('class="ckr-shop-shortcuts', resp.text)

    def test_collections_general_hides_retail_shortcuts(self):
        """La porte noble ``/collections`` garde le hero sans barre retail."""
        resp = self.url_open("/collections", timeout=60)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('class="ckr-shop-hero', resp.text)
        self.assertIn("ckr-shop-hero--context", resp.text)
        self.assertNotIn('class="ckr-shop-shortcuts', resp.text)
