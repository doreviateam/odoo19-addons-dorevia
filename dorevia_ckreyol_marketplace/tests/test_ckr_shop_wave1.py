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
        self.assertIn("Mi Boutik La", resp.text)  # titre hero éditorial uniquement
        self.assertRegex(
            resp.text,
            r'class="ckr-shop-shortcuts__link[^"]*"[^>]*>\s*Toute la sélection\s*</a>',
        )  # chip reset vers /shop nu (libellé distinct du hero)
        self.assertIn("terroirs", resp.text)
        self.assertIn("créoles", resp.text)
        self.assertIn('class="ckr-shop-shortcuts', resp.text)
        self.assertNotIn('id="ckr-shop-pack-banner"', resp.text)
        self.assertNotIn('id="ckr-shop-promo-banner"', resp.text)
        self.assertNotIn('id="ckr-shop-origin-banner"', resp.text)
        self.assertNotIn('id="ckr-shop-featured-banner"', resp.text)
        self.assertNotIn('id="ckr-shop-collection-banner"', resp.text)

    def test_shop_product_tiles_expose_corner_info_action(self):
        """La tuile produit expose le rail wishlist + information à la demande."""
        resp = self.url_open("/shop", timeout=60)
        self.assertEqual(resp.status_code, 200)
        self.assertIn("ckr-product-card__corner-actions", resp.text)
        self.assertIn("ckr_shop_product_name_retail_style", resp.text)
        self.assertIn("ckr-product-card__name-link", resp.text)
        self.assertIn("ckr-product-card__info-action", resp.text)
        self.assertIn("ckr-product-card__info-icon", resp.text)
        self.assertIn("fa fa-heart", resp.text)
        self.assertIn("fa fa-info", resp.text)
        self.assertIn("Informations complémentaires sur ce produit", resp.text)
        self.assertIn('class="ckr-product-card__details-body" role="tooltip" style="display:none;"', resp.text)
        self.assertNotIn("ckr-product-card__details-summary", resp.text)

    def test_shop_search_hides_editorial_layers(self):
        """La recherche garde la toolbar native, sans hero ni shortcuts marketing."""
        resp = self.url_open("/shop?search=manioc", timeout=60)
        self.assertEqual(resp.status_code, 200)
        self.assertNotIn('class="ckr-shop-hero', resp.text)
        self.assertNotIn('class="ckr-shop-shortcuts', resp.text)

    def test_shop_promo_chip_keeps_same_retail_hero_as_root(self):
        """Chip Promotions — même bloc vitrine `/shop` (pas le variant « contexte » porte)."""
        resp = self.url_open("/shop?ckr_mode=promo", timeout=60)
        self.assertEqual(resp.status_code, 200)
        self.assertIn("ckr-shop-hero--retail", resp.text)
        self.assertNotIn("ckr-shop-hero--context", resp.text)

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
        """Alias ``/shop/category/…`` → 302→ ``/shop?ckr_category=…`` : hero vitrine + barre chips.

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
        self.assertIn("ckr-shop-hero--retail", resp.text)
        self.assertNotIn("ckr-shop-hero--context", resp.text)
        self.assertIn("Mi Boutik La", resp.text)
        self.assertIn(cat.name, resp.text)
        self.assertTrue(
            "Retrouvez la sélection" in resp.text
            or "Explorez l’excellence des terroirs créoles" in resp.text,
            "Accroche vitrine attendue sur la page catégorie (canonique ``/shop`` + facette).",
        )
        self.assertIn('class="ckr-shop-shortcuts', resp.text)

    def test_collections_general_301_shop_scope_and_shortcuts(self):
        """``/collections`` → ``/shop`` (filtre collections) ; hero vitrine + chips."""
        resp0 = self.url_open("/collections", allow_redirects=False, timeout=60)
        self.assertEqual(resp0.status_code, 301)
        loc0 = resp0.headers.get("Location", "")
        self.assertIn("/shop", loc0)
        self.assertIn("ckr_collection_scope", loc0)
        resp = self.url_open("/collections", timeout=60)
        self.assertEqual(resp.status_code, 200)
        self.assertIn('class="ckr-shop-hero', resp.text)
        self.assertIn("ckr-shop-hero--retail", resp.text)
        self.assertNotIn("ckr-shop-hero--context", resp.text)
        self.assertIn('class="ckr-shop-shortcuts', resp.text)

    def test_shop_multi_ckr_mode_combines_without_error(self):
        """Deux portes chips en query : rendu ``/shop`` 200 ; même hero vitrine."""
        resp = self.url_open("/shop?ckr_mode=promo&ckr_mode=pack", timeout=60)
        self.assertEqual(resp.status_code, 200)
        self.assertIn("ckr-shop-hero", resp.text)
        self.assertIn("ckr-shop-hero--retail", resp.text)
        self.assertNotIn("ckr-shop-hero--context", resp.text)
