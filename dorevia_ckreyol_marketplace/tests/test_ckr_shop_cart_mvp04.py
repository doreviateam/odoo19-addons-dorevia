# -*- coding: utf-8 -*-
"""Tests HTTP — panier MVP04 Palier A (header CK + page ``/shop/cart`` standard).

Ces tests verrouillent des **invariants serveur / HTML** : pas de simulation tactile,
pas de parcours checkout complet. Ils complètent la recette manuelle (P1–P6).

Pour le CTA « Payer » avec lignes panier, prévoir plus tard un tour Odoo / e2e ou des
tests contrôleur avec ``MockRequest`` (module ``website_sale``).

Exécution ciblée ::

    odoo -d <base> --test-enable --stop-after-init \\
        --test-tags=dorevia_ckr_shop_cart
"""

import re

from odoo.tests import tagged
from odoo.tests.common import HttpCase


@tagged("post_install", "-at_install", "dorevia_ckr_shop", "dorevia_ckr_shop_cart")
class TestCkrShopCartMvp04(HttpCase):
    """Non-régression structurelle panier + header C-Kreyol (Odoo 19 ``website_sale``)."""

    def test_shop_cart_returns_200(self):
        resp = self.url_open("/shop/cart", timeout=60)
        self.assertEqual(resp.status_code, 200)

    def test_shop_cart_includes_ck_header_and_cart_link(self):
        resp = self.url_open("/shop/cart", timeout=60)
        self.assertEqual(resp.status_code, 200)
        html = resp.text
        self.assertIn("ckr-header", html)
        self.assertIn("ckr-header__link-cart", html)
        self.assertIn('href="/shop/cart"', html)
        self.assertIn("ckr-header__counter-badge", html)

    def test_shop_cart_wraps_standard_checkout_layout(self):
        """Colonne panier ``#shop_cart`` + layout checkout (structure Odoo 19)."""
        resp = self.url_open("/shop/cart", timeout=60)
        self.assertEqual(resp.status_code, 200)
        html = resp.text
        self.assertIn('id="shop_cart"', html)
        self.assertIn("o_website_sale_checkout_container", html)
        self.assertIn("o_wsale_shorter_cart_summary", html)

    def test_shop_cart_empty_shows_exit_and_order_summary_heading(self):
        """Panier vide : message libre + sortie boutique + titre récapitulatif (EN ou FR).

        Odoo 19 : état vide dans ``cart_lines`` = bouton ``/shop`` libellé « Shop » /
        « Boutique », en plus du libellé « Continue shopping » éventuel dans le résumé.
        """
        resp = self.url_open("/shop/cart", timeout=60)
        self.assertEqual(resp.status_code, 200)
        html = resp.text
        self.assertTrue(
            ("Your cart is empty!" in html or "Your cart is empty." in html)
            or ("Votre panier est vide" in html),
            "Libellé panier vide attendu (traduction EN ou FR).",
        )
        has_legacy_continue = "Continue shopping" in html or "Continuer vos achats" in html
        has_odoo19_empty_cta = bool(
            re.search(
                r'<a\s+href="/shop"\s+class="[^"]*\bbtn-primary\b[^"]*"[^>]*>\s*(Shop|Boutique)\s*</a>',
                html,
                re.IGNORECASE | re.DOTALL,
            )
        )
        self.assertTrue(
            has_legacy_continue or has_odoo19_empty_cta,
            "Sortie boutique attendue : « Continue shopping » / « Continuer vos achats » "
            "ou CTA panier vide Odoo 19 (lien /shop, btn-primary, Shop ou Boutique).",
        )
        self.assertTrue(
            ("Order summary" in html or "Résumé de la commande" in html),
            "Titre bloc récap Odoo (« Order summary » / « Résumé de la commande »).",
        )
