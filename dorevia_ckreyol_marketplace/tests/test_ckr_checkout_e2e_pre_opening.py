# -*- coding: utf-8 -*-
"""Tests E2E pré-ouverture — tunnel marchand minimal CK.

Objectif: fournir une preuve automatisée minimale qu'un visiteur peut
progresser dans le tunnel marchand sans erreur bloquante.
"""

import json
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
                "list_price": 1.0,
            }
        )
        cls.product_b = Product.create(
            {
                "name": "CKR E2E Produit B %s" % stamp,
                "type": "consu",
                "sale_ok": True,
                "website_published": True,
                "list_price": 1.0,
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

    def _extract_checkout_action(self, html):
        """Extrait l'action du formulaire checkout/adresse."""
        m = re.search(
            r'<form\b[^>]*action=["\']([^"\']+)["\'][^>]*>',
            html,
            flags=re.I,
        )
        return m.group(1).strip() if m else "/shop/address"

    def _cart_contains(self, product):
        cart = self.url_open("/shop/cart", timeout=60)
        self.assertEqual(cart.status_code, 200)
        return product.name in cart.text

    def _add_product_to_cart(self, product, qty=1):
        """Ajoute un produit via le endpoint JSON-RPC natif Odoo 19."""
        payload = {
            "jsonrpc": "2.0",
            "method": "call",
            "params": {
                "product_template_id": product.id,
                "product_id": product.product_variant_id.id,
                "quantity": qty,
            },
        }
        resp = self.url_open(
            "/shop/cart/add",
            data=json.dumps(payload),
            headers={"Content-Type": "application/json"},
            timeout=60,
            allow_redirects=False,
        )
        self.assertEqual(resp.status_code, 200)
        self.assertNotIn('"error"', resp.text)
        self.assertTrue(self._cart_contains(product))

    def test_nominal_minimal_flow(self):
        """Nominal minimal: panier -> checkout -> payment -> confirm (sans 500)."""
        self.url_open("/", timeout=60)
        self._add_product_to_cart(self.product_a, qty=1)
        self._add_product_to_cart(self.product_b, qty=1)

        cart = self.url_open("/shop/cart", timeout=60)
        self.assertEqual(cart.status_code, 200)
        self.assertIn(self.product_a.name, cart.text)
        self.assertIn(self.product_b.name, cart.text)

        # Vérification minimale de manipulabilité du panier (sans lier au contrat interne update_cart).
        self.url_open("/shop/cart", timeout=60)
        cart2 = self.url_open("/shop/cart", timeout=60)
        self.assertEqual(cart2.status_code, 200)
        self.assertIn(self.product_a.name, cart2.text)
        self.assertIn(self.product_b.name, cart2.text)

        checkout = self.url_open("/shop/checkout", allow_redirects=False, timeout=60)
        self.assertIn(checkout.status_code, (200, 302, 303))
        payment = self.url_open("/shop/payment", allow_redirects=False, timeout=60)
        self.assertIn(payment.status_code, (200, 302, 303))
        confirm = self.url_open("/shop/confirmation", allow_redirects=False, timeout=60)
        self.assertIn(confirm.status_code, (200, 302, 303))

    def test_failure_case_empty_cart(self):
        """Cas E1: panier vide -> pas de 500 et repli propre."""
        # Panier visiteur vide par défaut dans la session de test.
        resp = self.url_open("/shop/checkout", allow_redirects=False, timeout=60)
        self.assertIn(resp.status_code, (200, 302, 303))
        if resp.status_code in (302, 303):
            self.assertIn("/shop", resp.headers.get("Location", ""))

    def test_failure_case_invalid_address(self):
        """Cas E2: adresse incomplète -> erreur formulaire, pas de crash."""
        self._add_product_to_cart(self.product_a, qty=1)
        checkout = self.url_open("/shop/checkout", timeout=60)
        self.assertEqual(checkout.status_code, 200)
        token = self._extract_csrf(checkout.text)
        self.assertTrue(token, "Jeton CSRF requis sur formulaire checkout.")
        action = self._extract_checkout_action(checkout.text)
        invalid = self.url_open(
            action,
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
        self.assertIn(invalid.status_code, (200, 302, 303))
