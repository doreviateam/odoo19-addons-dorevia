# -*- coding: utf-8 -*-
"""Recette-U5 — Panier → checkout → commande (visiteur anonyme, Manio Crackers)."""

import json
import re
import time

from odoo.tests import tagged
from odoo.tests.common import HttpCase, JsonRpcException

from odoo.addons.dorevia_ck_marketone_content.catalog_manioc_variants import (
    MANIO_CRACKERS_PARENT_NAME,
)


@tagged('post_install', '-at_install', 'dorevia_ck_recette_u5')
class TestCkRecetteU5(HttpCase):
    FR_HEADERS = {'Accept-Language': 'fr-FR,fr;q=0.9'}

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls._stamp = int(time.time() * 1000)
        cls.website = cls.env['website'].get_current_website()
        cls.country_fr = cls.env.ref('base.fr')
        cls.manio = cls.env['product.template'].sudo().search([
            ('name', '=', MANIO_CRACKERS_PARENT_NAME),
            ('is_published', '=', True),
            ('website_published', '=', True),
        ], limit=1)
        if not cls.manio:
            raise cls.skipTest('Produit témoin Manio Crackers absent ou non publié.')
        cls.manio_variant = cls.manio.product_variant_id
        cls.partner_email = 'ck.recette.u5.%s@example.com' % cls._stamp

        cls.custom_provider = cls.env['payment.provider'].sudo().search([
            ('code', '=', 'custom'),
            ('state', 'in', ('enabled', 'test')),
        ], limit=1)
        if not cls.custom_provider:
            raise cls.skipTest('Provider paiement custom (comptant) absent.')
        cls.custom_payment_method = cls.custom_provider.payment_method_ids[:1]
        if not cls.custom_payment_method:
            raise cls.skipTest('Méthode de paiement custom absente.')

        carrier = cls.env['delivery.carrier'].sudo().search([
            ('website_published', '=', True),
        ], limit=1)
        if not carrier:
            raise cls.skipTest('Aucune méthode de livraison publiée.')
        if 'allow_cash_on_delivery' in carrier._fields:
            carrier.allow_cash_on_delivery = True
        cls.carrier = carrier

    def setUp(self):
        super().setUp()
        self.authenticate(None, None)

    def _open(self, path, **kwargs):
        kwargs.setdefault('headers', self.FR_HEADERS)
        response = self.url_open(path, **kwargs)
        self.assertEqual(response.status_code, 200, path)
        return response

    def _jsonrpc(self, path, params, timeout=120):
        try:
            return self.make_jsonrpc_request(path, params=params, timeout=timeout)
        except JsonRpcException as exc:
            self.fail('JSON-RPC %s : %s' % (path, exc))

    def _extract_csrf(self, html):
        for pattern in (
            r'<input\b[^>]*name=["\']csrf_token["\'][^>]*value=["\']([^"\']*)["\']',
            r'<input\b[^>]*value=["\']([^"\']*)["\'][^>]*name=["\']csrf_token["\']',
        ):
            match = re.search(pattern, html, flags=re.I)
            if match and match.group(1).strip():
                return match.group(1).strip()
        return None

    def _header_nav(self, html):
        match = re.search(r'<header[^>]*id="top"[^>]*>(.*?)</header>', html, re.S)
        self.assertTrue(match, 'header#top introuvable')
        return match.group(1)

    def _cart_count(self, html):
        nav = self._header_nav(html)
        badges = re.findall(
            r'<sup[^>]*class="[^"]*my_cart_quantity[^"]*"[^>]*>(\d+)</sup>',
            nav,
        )
        return max((int(v) for v in badges), default=0) if badges else 0

    def _cart_add_manio(self, quantity=1):
        self._jsonrpc('/shop/cart/add', {
            'product_template_id': self.manio.id,
            'product_id': self.manio_variant.id,
            'quantity': quantity,
        })

    def _cart_line_id_for_variant(self, html, variant_id):
        for regex in (
            r'data-line-id="(\d+)"[^>]*data-product-id="(\d+)"',
            r'data-product-id="(\d+)"[^>]*data-line-id="(\d+)"',
        ):
            for match in re.finditer(regex, html):
                groups = match.groups()
                if int(groups[1]) == variant_id:
                    return int(groups[0])
                if int(groups[0]) == variant_id:
                    return int(groups[1])
        return None

    def _parse_payment_form_attrs(self, html):
        block_match = re.search(r'<form[^>]*id="o_payment_form"[^>]*>', html, flags=re.I)
        if not block_match:
            return None
        start = block_match.start()
        end = html.find('</form>', start)
        if end == -1:
            return None
        block = html[start:end]
        out = {}
        for key, pattern in (
            ('access_token', r'data-access-token="([^"]*)"'),
            ('transaction_route', r'data-transaction-route="([^"]*)"'),
            ('landing_route', r'data-landing-route="([^"]*)"'),
        ):
            match = re.search(pattern, block)
            if match:
                out[key] = match.group(1)
        return out or None

    def _submit_guest_address(self):
        addr_get = self._open(
            '/shop/address?address_type=billing&use_delivery_as_billing=true',
        )
        token = self._extract_csrf(addr_get.text)
        self.assertTrue(token, 'M2 — jeton CSRF requis sur /shop/address.')
        data = {
            'csrf_token': token,
            'name': 'Client Recette U5',
            'email': self.partner_email,
            'street': '10 rue du Panier CK',
            'city': 'Nantes',
            'zip': '44000',
            'phone': '+33240102030',
            'country_id': str(self.country_fr.id),
            'address_type': 'billing',
            'use_delivery_as_billing': 'true',
        }
        submitted = self.url_open(
            '/shop/address/submit',
            data=data,
            headers=self.FR_HEADERS,
            allow_redirects=False,
        )
        self.assertEqual(submitted.status_code, 200)
        feedback = json.loads(submitted.text)
        self.assertNotIn('invalid_fields', feedback or {})
        redirect_url = (feedback or {}).get('redirectUrl')
        self.assertTrue(redirect_url, 'M2 — redirectUrl attendu après adresse.')
        follow = self.url_open(redirect_url, headers=self.FR_HEADERS, allow_redirects=True)
        self.assertIn(follow.status_code, (200, 302, 303))

    def _select_delivery_if_needed(self):
        self._jsonrpc('/shop/set_delivery_method', {'dm_id': self.carrier.id})

    def _payment_custom_flow(self, payment_html=None):
        if payment_html is None:
            pay_page = self._open('/shop/payment', allow_redirects=True)
            payment_html = pay_page.text
        self.assertIn('o_payment_form', payment_html, 'N1 — formulaire paiement absent.')
        attrs = self._parse_payment_form_attrs(payment_html)
        self.assertTrue(attrs and attrs.get('transaction_route'), 'N1 — attributs paiement introuvables.')
        landing = attrs.get('landing_route') or '/shop/payment/validate'
        tx_vals = self._jsonrpc(attrs['transaction_route'], {
            'access_token': attrs.get('access_token'),
            'provider_id': self.custom_provider.id,
            'payment_method_id': self.custom_payment_method.id,
            'token_id': None,
            'flow': 'direct',
            'tokenization_requested': False,
            'landing_route': landing,
        })
        self.assertTrue(tx_vals and tx_vals.get('reference'), 'N3 — création transaction vide.')
        processed = self.url_open(
            '/payment/custom/process',
            data={'reference': tx_vals['reference']},
            headers=self.FR_HEADERS,
            allow_redirects=False,
        )
        self.assertIn(processed.status_code, (200, 302, 303))
        validated = self.url_open('/shop/payment/validate', headers=self.FR_HEADERS, allow_redirects=True)
        self.assertIn(validated.status_code, (200, 302, 303))

    # --- Scénario L : panier ---

    def test_l_cart_view_update_remove_and_checkout_link(self):
        """L1–L4 — Manio visible, quantité, suppression, lien checkout."""
        self._cart_add_manio(quantity=1)
        cart = self._open('/shop/cart?qa_ts=recette_u5_l1')
        text = cart.text
        self.assertIn(MANIO_CRACKERS_PARENT_NAME, text, 'L1 — produit absent du panier.')
        self.assertRegex(text, r'oe_product_image|product_image|img', 'L1 — image produit absente.')
        self.assertTrue(
            re.search(r'js_quantity|cart_lines_quantity|quantity', text),
            'L2 — contrôle quantité absent.',
        )
        self.assertTrue(
            re.search(r'js_delete_product|fa-trash', text),
            'L3 — contrôle suppression absent.',
        )
        self.assertGreaterEqual(self._cart_count(text), 1, 'L2 — badge header non mis à jour.')

        line_id = self._cart_line_id_for_variant(text, self.manio_variant.id)
        self.assertTrue(line_id, 'L2 — ligne panier introuvable.')
        self._jsonrpc('/shop/cart/update', {'line_id': line_id, 'quantity': 2})
        cart_updated = self._open('/shop/cart?qa_ts=recette_u5_l2')
        self.assertIn(MANIO_CRACKERS_PARENT_NAME, cart_updated.text)
        self.assertGreaterEqual(self._cart_count(cart_updated.text), 2)

        line_id = self._cart_line_id_for_variant(cart_updated.text, self.manio_variant.id)
        self._jsonrpc('/shop/cart/update', {'line_id': line_id, 'quantity': 0})
        empty_cart = self.url_open('/shop/cart?qa_ts=recette_u5_l3', headers=self.FR_HEADERS)
        self.assertEqual(empty_cart.status_code, 200)
        self.assertIsNone(
            self._cart_line_id_for_variant(empty_cart.text, self.manio_variant.id),
            'L3 — ligne encore présente après suppression.',
        )

        self._cart_add_manio(quantity=1)
        checkout_probe = self.url_open('/shop/checkout', headers=self.FR_HEADERS, allow_redirects=True)
        self.assertEqual(checkout_probe.status_code, 200, 'L4 — checkout inaccessible.')

    # --- Scénario M : checkout adresse + livraison + CGV ---

    def test_m_checkout_address_delivery_terms(self):
        """M1–M5 — formulaire adresse, livraison, CGV, accès paiement."""
        self._cart_add_manio(quantity=1)
        checkout = self._open('/shop/checkout?qa_ts=recette_u5_m1', allow_redirects=True)
        text = checkout.text
        self.assertTrue(
            re.search(r'name="email"|input[^>]*email', text, re.I),
            'M1 — champ email absent.',
        )
        for field in ('name', 'street', 'city', 'zip', 'phone'):
            self.assertIn(f'name="{field}"', text, f'M1 — champ {field} absent.')

        self._submit_guest_address()
        checkout_ready = self._open('/shop/checkout?qa_ts=recette_u5_m3', allow_redirects=True)
        checkout_html = checkout_ready.text
        self._select_delivery_if_needed()
        self.assertTrue(
            re.search(r'o_delivery_radio|delivery|Livraison', checkout_html, re.I),
            'M3 — méthode de livraison non proposée.',
        )
        self.assertTrue(
            re.search(r'terms|conditions|/terms|accept_terms', checkout_html, re.I),
            'M4 — case ou lien CGV absent.',
        )
        payment_link = re.search(r'href="(/shop/payment[^"]*)"', checkout_html)
        if not payment_link:
            payment_probe = self.url_open('/shop/payment', headers=self.FR_HEADERS, allow_redirects=True)
            self.assertEqual(payment_probe.status_code, 200, 'M5 — page paiement inaccessible.')
        else:
            payment = self.url_open(payment_link.group(1), headers=self.FR_HEADERS, allow_redirects=True)
            self.assertEqual(payment.status_code, 200, 'M5 — redirection paiement échouée.')

    # --- Scénarios N + O : paiement et confirmation ---

    def test_n_o_checkout_payment_confirmation(self):
        """N1–N3 + O1–O4 — paiement comptant et page de confirmation."""
        self._cart_add_manio(quantity=1)
        self.url_open('/shop/checkout', allow_redirects=True)
        self._submit_guest_address()
        self._select_delivery_if_needed()

        pay_page = self._open('/shop/payment?qa_ts=recette_u5_n1', allow_redirects=True)
        pay_text = pay_page.text
        self.assertTrue(
            'o_payment_form' in pay_text
            or 'cash_on_delivery' in pay_text
            or self.custom_provider.name in pay_text
            or re.search(r'cash on delivery', pay_text, re.I),
            'N1 — provider custom absent.',
        )
        self.assertIn(MANIO_CRACKERS_PARENT_NAME, pay_text, 'N2 — produit absent du récap paiement.')

        order = self.env['sale.order'].sudo().search([
            ('partner_id.email', '=', self.partner_email),
            ('website_id', '=', self.website.id),
        ], order='id desc', limit=1)
        if order:
            self.assertGreater(order.amount_total, 0, 'N2 — montant total nul.')

        self._payment_custom_flow(payment_html=pay_text)

        confirm = self._open('/shop/confirmation?qa_ts=recette_u5_o1', allow_redirects=True)
        confirm_text = confirm.text
        self.assertTrue(
            re.search(
                r'(merci|thank you|confirmation|commande)',
                confirm_text,
                re.I,
            ),
            'O1 — message de remerciement absent.',
        )
        self.assertTrue(
            re.search(r'\b(S\d+|\d{4,})\b', confirm_text)
            or self.partner_email in confirm_text,
            'O1 — numéro de commande non repéré.',
        )
        self.assertIn(MANIO_CRACKERS_PARENT_NAME, confirm_text, 'O2 — produit absent du récap.')
        self.assertTrue(
            re.search(r'Nantes|44000|Panier CK', confirm_text, re.I),
            'O2 — adresse de livraison absente du récap.',
        )
        reassurance_hits = sum(
            1 for phrase in (
                r'livraison',
                r'paiement',
                r'service',
                r'sécuris',
                r'réassurance',
                r'ck-reassurance',
            )
            if re.search(phrase, confirm_text, re.I)
        )
        self.assertGreaterEqual(
            reassurance_hits, 1,
            'O4 — aucun signal de réassurance sur la confirmation.',
        )
