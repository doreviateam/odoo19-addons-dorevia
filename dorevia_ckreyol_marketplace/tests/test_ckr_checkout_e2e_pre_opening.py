# -*- coding: utf-8 -*-
"""Tests E2E pré-ouverture — tunnel marchand minimal CK.

Objectif: fournir une preuve automatisée minimale qu'un visiteur peut
progresser dans le tunnel marchand sans erreur bloquante.
"""

import re
import time

from odoo.tests import tagged
from odoo.tests.common import HttpCase


@tagged("post_install", "-at_install", "dorevia_ckr_checkout_e2e")
class TestCkrCheckoutE2EPreOpening(HttpCase):
    """Lot P4: nominal minimal + échecs minimum."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.website = cls.env.ref("website.default_website")
        stamp = int(time.time() * 1000)
        Product = cls.env["product.template"].sudo()
        cls.product_a = Product.create(
            {
                "name": "CKR E2E Produit A %s" % stamp,
                "type": "consu",
                "sale_ok": True,
                "website_published": True,
                "list_price": 0.0,
            }
        )
        cls.product_b = Product.create(
            {
                "name": "CKR E2E Produit B %s" % stamp,
                "type": "consu",
                "sale_ok": True,
                "website_published": True,
                "list_price": 0.0,
            }
        )

    def _extract_csrf(self, html):
        for pattern in (
            r'<input\b[^>]*name=["\']csrf_token["\'][^>]*value=["\']([^"\']*)["\']',
            r'<input\b[^>]*value=["\']([^"\']*)["\'][^>]*name=["\']csrf_token["\']',
        ):
            m = re.search(pattern, html, flags=re.I)
            if m and m.group(1).strip():
                return m.group(1).strip()
        return None

    def _set_qty(self, product, qty):
        # Endpoint natif website_sale pour régler une quantité produit.
        self.url_open(
            "/shop/cart/update?product_id=%s&set_qty=%s"
            % (product.product_variant_id.id, qty),
            timeout=60,
        )

    def test_nominal_minimal_flow(self):
        """Nominal minimal: panier -> checkout -> payment -> confirm (sans 500)."""
        self.url_open("/", timeout=60)
        self._set_qty(self.product_a, 1)  # ajout depuis tunnel produit
        self._set_qty(self.product_b, 1)  # ajout depuis logique shop

        cart = self.url_open("/shop/cart", timeout=60)
        self.assertEqual(cart.status_code, 200)
        self.assertIn(self.product_a.name, cart.text)
        self.assertIn(self.product_b.name, cart.text)

        self._set_qty(self.product_a, 2)  # modification quantité
        self._set_qty(self.product_b, 0)  # suppression ligne
        cart2 = self.url_open("/shop/cart", timeout=60)
        self.assertEqual(cart2.status_code, 200)
        self.assertIn(self.product_a.name, cart2.text)
        self.assertNotIn(self.product_b.name, cart2.text)

        checkout = self.url_open("/shop/checkout", allow_redirects=False, timeout=60)
        self.assertIn(checkout.status_code, (200, 302))
        payment = self.url_open("/shop/payment", allow_redirects=False, timeout=60)
        self.assertIn(payment.status_code, (200, 302))
        confirm = self.url_open("/shop/confirm_order", allow_redirects=False, timeout=60)
        self.assertIn(confirm.status_code, (200, 302))

    def test_failure_case_empty_cart(self):
        """Cas E1: panier vide -> pas de 500 et repli propre."""
        self._set_qty(self.product_a, 0)
        self._set_qty(self.product_b, 0)
        resp = self.url_open("/shop/checkout", allow_redirects=False, timeout=60)
        self.assertIn(resp.status_code, (200, 302))
        if resp.status_code == 302:
            self.assertIn("/shop", resp.headers.get("Location", ""))

    def test_failure_case_invalid_address(self):
        """Cas E2: adresse incomplète -> erreur formulaire, pas de crash."""
        self._set_qty(self.product_a, 1)
        checkout = self.url_open("/shop/checkout", timeout=60)
        self.assertEqual(checkout.status_code, 200)
        token = self._extract_csrf(checkout.text)
        self.assertTrue(token, "Jeton CSRF requis sur formulaire checkout.")
        invalid = self.url_open(
            "/shop/address",
            data={
                "csrf_token": token,
                "submitted": "1",
                "name": "",
                "email": "invalid-address@example.com",
                "street": "",
                "city": "",
                "zip": "",
                "phone": "",
            },
            timeout=60,
            allow_redirects=False,
        )
        self.assertIn(invalid.status_code, (200, 302))
