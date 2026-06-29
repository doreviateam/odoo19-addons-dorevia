# -*- coding: utf-8 -*-
"""Recette-U6 — Parcours mobile 390px (SSR + tunnel achetable)."""

import json
import re
import time

from odoo.tests import tagged
from odoo.tests.common import HttpCase, JsonRpcException

from odoo.addons.dorevia_ck_marketone_content.catalog_manioc_variants import (
    MANIO_CRACKERS_PARENT_NAME,
)
from odoo.addons.dorevia_ck_marketone_content.home_featured import (
    bootstrap_home_featured_products,
)


@tagged('post_install', '-at_install', 'dorevia_ck_recette_u6')
class TestCkRecetteU6(HttpCase):
    """Garde-fous mobile : markup responsive + tunnel invité sans régression U5."""

    MOBILE_HEADERS = {
        'Accept-Language': 'fr-FR,fr;q=0.9',
        'User-Agent': (
            'Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) '
            'AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 '
            'Mobile/15E148 Safari/604.1'
        ),
    }

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls._stamp = int(time.time() * 1000)
        cls.website = cls.env['website'].get_current_website()
        cls.country_fr = cls.env.ref('base.fr')
        bootstrap_home_featured_products(cls.env)
        cls.manio = cls.env['product.template'].sudo().search([
            ('name', '=', MANIO_CRACKERS_PARENT_NAME),
            ('is_published', '=', True),
            ('website_published', '=', True),
        ], limit=1)
        if not cls.manio:
            raise cls.skipTest('Produit témoin Manio Crackers absent ou non publié.')
        cls.manio_variant = cls.manio.product_variant_id
        cls.partner_email = 'ck.recette.u6.%s@example.com' % cls._stamp

        cls.custom_provider = cls.env['payment.provider'].sudo().search([
            ('code', '=', 'custom'),
            ('state', 'in', ('enabled', 'test')),
        ], limit=1)
        if not cls.custom_provider:
            raise cls.skipTest('Provider paiement custom absent.')
        cls.custom_payment_method = cls.custom_provider.payment_method_ids[:1]

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
        self.env['product.wishlist'].sudo().search([]).unlink()

    def _open(self, path, **kwargs):
        kwargs.setdefault('headers', self.MOBILE_HEADERS)
        response = self.url_open(path, **kwargs)
        self.assertEqual(response.status_code, 200, path)
        return response

    def _jsonrpc(self, path, params, timeout=120):
        try:
            return self.make_jsonrpc_request(path, params=params, timeout=timeout)
        except JsonRpcException as exc:
            self.fail('JSON-RPC %s : %s' % (path, exc))

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

    def _wish_count(self, html):
        nav = self._header_nav(html)
        badges = re.findall(
            r'<sup[^>]*class="[^"]*my_wish_quantity[^"]*"[^>]*>(\d+)</sup>',
            nav,
        )
        visible = [
            int(v) for v in badges
            if 'd-none' not in nav[max(0, nav.find(v) - 80):nav.find(v)]
        ]
        return max(visible, default=0) if visible else 0

    def _assert_mobile_chrome(self, html, label=''):
        self.assertRegex(
            html,
            r'name="viewport"[^>]*width=device-width',
            f'{label} — meta viewport mobile absente.',
        )
        self.assertIn('o_header_mobile', html, f'{label} — header mobile absent.')
        self.assertIn('top_menu_collapse_mobile', html, f'{label} — menu offcanvas absent.')
        self.assertTrue(
            re.search(r'data-bs-toggle="offcanvas"|navbar-toggler|ck-header-mobile__menu', html),
            f'{label} — bouton hamburger absent.',
        )

    def _assert_mobile_badges(self, html, label=''):
        nav = self._header_nav(html)
        self.assertIn('my_cart_quantity', nav, f'{label} — badge panier absent.')
        self.assertIn('my_wish_quantity', nav, f'{label} — badge favoris absent.')
        self.assertRegex(
            nav,
            r'my_cart_quantity[^>]*badge[^>]*rounded-pill',
            f'{label} — badge panier mal formé.',
        )

    def _extract_csrf(self, html):
        for pattern in (
            r'<input\b[^>]*name=["\']csrf_token["\'][^>]*value=["\']([^"\']*)["\']',
            r'<input\b[^>]*value=["\']([^"\']*)["\'][^>]*name=["\']csrf_token["\']',
        ):
            match = re.search(pattern, html, flags=re.I)
            if match and match.group(1).strip():
                return match.group(1).strip()
        return None

    def _submit_guest_address(self):
        addr_get = self._open(
            '/shop/address?address_type=billing&use_delivery_as_billing=true',
        )
        token = self._extract_csrf(addr_get.text)
        self.assertTrue(token, 'R4 — jeton CSRF adresse.')
        data = {
            'csrf_token': token,
            'name': 'Client Recette U6',
            'email': self.partner_email,
            'street': '12 rue Mobile CK',
            'city': 'Nantes',
            'zip': '44000',
            'phone': '+33240102031',
            'country_id': str(self.country_fr.id),
            'address_type': 'billing',
            'use_delivery_as_billing': 'true',
        }
        submitted = self.url_open(
            '/shop/address/submit',
            data=data,
            headers=self.MOBILE_HEADERS,
            allow_redirects=False,
        )
        self.assertEqual(submitted.status_code, 200)
        feedback = json.loads(submitted.text)
        redirect_url = (feedback or {}).get('redirectUrl')
        self.assertTrue(redirect_url, 'R4 — redirectUrl adresse.')
        self.url_open(redirect_url, allow_redirects=True)

    def _payment_custom_flow(self, payment_html):
        attrs = self._parse_payment_form_attrs(payment_html)
        self.assertTrue(attrs and attrs.get('transaction_route'), 'R6 — paiement indisponible.')
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
        self.url_open(
            '/payment/custom/process',
            data={'reference': tx_vals['reference']},
            headers=self.MOBILE_HEADERS,
            allow_redirects=False,
        )
        self.url_open('/shop/payment/validate', allow_redirects=True)

    def _parse_payment_form_attrs(self, html):
        block_match = re.search(r'<form[^>]*id="o_payment_form"[^>]*>', html, flags=re.I)
        if not block_match:
            return None
        start = block_match.start()
        end = html.find('</form>', start)
        block = html[start:end] if end != -1 else ''
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

    # --- Scénario P : navigation & découverte ---

    def test_p_home_and_shop_mobile_discovery(self):
        """P1–P5 — Home hero, cards, menu mobile, shop grille, lien fiche Manio."""
        home = self._open('/?qa_ts=recette_u6_p1').text
        self._assert_mobile_chrome(home, 'P1')
        self.assertTrue(
            re.search(r'ck-home-hero|s_ck_hero|ck-hero', home, re.I),
            'P1 — bloc hero absent.',
        )
        self.assertRegex(home, r'Manio Crackers', 'P2 — Manio absent des vedettes.')
        featured_idx = home.find('ck-featured-products')
        self.assertGreater(featured_idx, 0, 'P2 — section vedettes absente.')
        featured = home[featured_idx:featured_idx + 120000]
        self.assertIn('ck-product-card--home', featured, 'P2 — cards vedettes absentes.')
        self.assertIn('ck-featured-products__grid', featured, 'P2 — grille vedettes absente.')
        self.assertIn('ck-header-mobile__search', home, 'P1 — recherche mobile absente.')

        shop = self._open('/shop?qa_ts=recette_u6_p4').text
        self._assert_mobile_chrome(shop, 'P4')
        self.assertIn('o_wsale_products_grid', shop, 'P4 — grille shop absente.')
        self.assertRegex(shop, r'g-col-6|col-6', 'P4 — colonnes mobile shop absentes.')
        self.assertTrue(
            re.search(r'o_wsale_offcanvas|data-bs-target="#o_wsale_offcanvas"', shop),
            'P4 — drawer filtres mobile absent.',
        )
        self.assertIn(MANIO_CRACKERS_PARENT_NAME, shop, 'P4 — Manio absent du shop.')
        self.assertIn(self.manio.website_url.replace('&', '&amp;'), shop, 'P5 — lien fiche Manio absent.')

    # --- Scénario Q : fiche produit mobile ---

    def test_q_product_page_mobile_add_and_wish(self):
        """Q1–Q5 — fiche Manio mobile, CTA panier/favoris, badges header."""
        html = self._open(f'{self.manio.website_url}?qa_ts=recette_u6_q1').text
        self._assert_mobile_chrome(html, 'Q1')
        self.assertRegex(html, r'oe_product_image|product_detail_img|img', 'Q1 — image produit absente.')
        self.assertIn('id="add_to_cart"', html, 'Q3 — bouton ajouter panier absent.')
        self.assertIn('o_add_wishlist', html, 'Q5 — bouton favoris absent.')
        self.assertTrue(
            re.search(r'ck-product-page|o_wsale_product_details', html),
            'Q2 — zone détails produit absente.',
        )

        self._jsonrpc('/shop/cart/add', {
            'product_template_id': self.manio.id,
            'product_id': self.manio_variant.id,
            'quantity': 1,
        })
        after_cart = self._open(f'{self.manio.website_url}?qa_ts=recette_u6_q4').text
        self.assertGreaterEqual(self._cart_count(after_cart), 1, 'Q4 — badge panier non mis à jour.')

        self._jsonrpc('/shop/wishlist/add', {'product_id': self.manio_variant.id})
        after_wish = self._open(f'{self.manio.website_url}?qa_ts=recette_u6_q5').text
        self.assertGreaterEqual(self._wish_count(after_wish), 1, 'Q5 — badge favoris non mis à jour.')

    # --- Scénario R : panier, checkout, confirmation mobile ---

    def test_r_mobile_cart_checkout_confirmation(self):
        """R1–R7 — tunnel mobile complet jusqu'à confirmation."""
        self._jsonrpc('/shop/cart/add', {
            'product_template_id': self.manio.id,
            'product_id': self.manio_variant.id,
            'quantity': 1,
        })
        cart = self._open('/shop/cart?qa_ts=recette_u6_r1').text
        self._assert_mobile_chrome(cart, 'R1')
        self.assertIn(MANIO_CRACKERS_PARENT_NAME, cart, 'R1 — produit absent du panier.')
        self.assertTrue(
            re.search(r'js_quantity|cart_lines_quantity|o_cart_product', cart),
            'R2 — contrôles quantité panier absents.',
        )

        self.url_open('/shop/checkout', allow_redirects=True)
        self._submit_guest_address()
        self._jsonrpc('/shop/set_delivery_method', {'dm_id': self.carrier.id})

        checkout = self._open('/shop/checkout?qa_ts=recette_u6_r5').text
        self._assert_mobile_chrome(checkout, 'R5')
        self.assertTrue(
            re.search(r'o_mobile_summary|o_cart_summary_offcanvas', checkout),
            'R1 — résumé mobile checkout absent.',
        )
        self.assertTrue(
            re.search(r'o_delivery_radio|delivery|Livraison', checkout, re.I),
            'R5 — livraison absente du checkout.',
        )
        self.assertTrue(
            re.search(r'terms|conditions|/terms', checkout, re.I),
            'R6 — CGV absentes.',
        )

        pay_page = self._open('/shop/payment?qa_ts=recette_u6_r6', allow_redirects=True)
        self.assertIn('o_payment_form', pay_page.text, 'R6 — page paiement inaccessible.')
        self._payment_custom_flow(pay_page.text)

        confirm = self._open('/shop/confirmation?qa_ts=recette_u6_r7', allow_redirects=True).text
        self._assert_mobile_chrome(confirm, 'R7')
        self.assertIn(MANIO_CRACKERS_PARENT_NAME, confirm, 'R7 — récap produit absent.')
        self.assertTrue(
            re.search(r'(merci|thank you|confirmation|commande)', confirm, re.I),
            'R7 — confirmation illisible.',
        )

    # --- Scénario S : header & badges mobile ---

    def test_s_mobile_badges_across_pages(self):
        """S1–S3 — badges panier/favoris visibles, qty élevée, accès panier mobile."""
        self._jsonrpc('/shop/cart/add', {
            'product_template_id': self.manio.id,
            'product_id': self.manio_variant.id,
            'quantity': 12,
        })
        self._jsonrpc('/shop/wishlist/add', {'product_id': self.manio_variant.id})

        pages = [
            '/?qa_ts=recette_u6_s1_home',
            '/shop?qa_ts=recette_u6_s1_shop',
            f'{self.manio.website_url}?qa_ts=recette_u6_s1_product',
            '/shop/cart?qa_ts=recette_u6_s1_cart',
        ]
        for path in pages:
            html = self._open(path).text
            self._assert_mobile_badges(html, path)
            self.assertGreaterEqual(self._cart_count(html), 10, f'S2 — badge panier tronqué sur {path}')
            self.assertGreaterEqual(self._wish_count(html), 1, f'S1 — favoris sur {path}')

        cart_html = self._open('/shop/cart?qa_ts=recette_u6_s3').text
        self.assertTrue(
            re.search(r'href="[^"]*shop/cart[^"]*"', self._header_nav(cart_html)),
            'S3 — lien panier header mobile absent (navigation directe mobile).',
        )
