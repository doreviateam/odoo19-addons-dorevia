# -*- coding: utf-8 -*-
"""Section 3 — prix vedettes avec pricelist active (cible commerciale CK)."""

import json
import re
import unittest

from odoo.tests import tagged
from odoo.tests.common import HttpCase, TransactionCase

from odoo.addons.dorevia_ck_marketone_content.home_featured import (
    _get_featured_commercial_line,
    _get_featured_price_amount,
    _get_featured_price_label,
    bootstrap_home_featured_products,
    build_featured_product_card_html,
)
from odoo.addons.dorevia_ck_marketone_content.tests.ck_home_section3_pricelist_utils import (
    enable_website_pricelists,
    ensure_ck_b2c_pricelist,
    get_manioc_cracker_variants,
    set_variant_fixed_price,
)

_TINY_PNG = (
    b'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAADElEQVR4nGP4z8AAAAMBAQDJ/pLvAAAAAElFTkSuQmCC'
)
_PRICE_RE = re.compile(r'class="price">([^<]+)')


def _normalize_price_label(text):
    return (text or '').replace('\xa0', ' ').strip()


@tagged('post_install', '-at_install', 'dorevia_ck_marketone_home_section3_pricelist')
class TestCkHomeSection3FeaturedPricelist(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        enable_website_pricelists(cls.env)
        cls.website = cls.env['website'].search([], limit=1)
        cls.pricelist = ensure_ck_b2c_pricelist(cls.env, cls.website)
        cls.parent, cls.sale, cls.sweet = get_manioc_cracker_variants(cls.env)
        if not (cls.parent and cls.sale and cls.sweet):
            raise unittest.SkipTest('Manio Crackers absent — recette pricelist non applicable.')

    def test_pricelist_available_on_website(self):
        available = self.website.sudo().get_pricelist_available()
        self.assertIn(self.pricelist, available)

    def test_get_product_price_per_variant(self):
        set_variant_fixed_price(self.env, self.pricelist, self.sale, 3.6)
        set_variant_fixed_price(self.env, self.pricelist, self.sweet, 3.5)
        self.assertAlmostEqual(self.pricelist._get_product_price(self.sale, 1.0), 3.6)
        self.assertAlmostEqual(self.pricelist._get_product_price(self.sweet, 1.0), 3.5)

    def test_featured_price_uses_pricelist_not_template(self):
        """Prix pricelist distincts du lst_price → la card suit la pricelist."""
        attr = self.env['product.attribute'].sudo().create({'name': 'Goût PL QA'})
        val_a = self.env['product.attribute.value'].sudo().create({
            'name': 'A PL', 'attribute_id': attr.id,
        })
        val_b = self.env['product.attribute.value'].sudo().create({
            'name': 'B PL', 'attribute_id': attr.id,
        })
        product = self.env['product.template'].sudo().create({
            'name': 'CK PL Distinct QA',
            'is_published': True,
            'website_published': True,
            'sale_ok': True,
            'list_price': 3.5,
            'image_1920': _TINY_PNG,
            'attribute_line_ids': [(0, 0, {
                'attribute_id': attr.id,
                'value_ids': [(6, 0, [val_a.id, val_b.id])],
            })],
        })
        variant_a = product.product_variant_ids.filtered(
            lambda v: 'A PL' in (v.display_name or '')
        )[:1]
        variant_b = product.product_variant_ids.filtered(
            lambda v: 'B PL' in (v.display_name or '')
        )[:1]
        set_variant_fixed_price(self.env, self.pricelist, variant_a, 4.2)
        set_variant_fixed_price(self.env, self.pricelist, variant_b, 2.95)
        variant_a.write({'lst_price': 9.9})
        variant_b.write({'lst_price': 8.8})
        self.assertEqual(_get_featured_price_label(self.env, self.website, variant_a), '4,20\u00a0€')
        self.assertEqual(_get_featured_price_label(self.env, self.website, variant_b), '2,95\u00a0€')

    def test_variant_rule_does_not_contaminate_sibling(self):
        set_variant_fixed_price(self.env, self.pricelist, self.sale, 3.6)
        # Pas de règle sur sucré : prix catalogue variante (lst_price).
        self.sweet.write({'lst_price': 3.5})
        self.assertAlmostEqual(
            _get_featured_price_amount(self.env, self.website, self.sale), 3.6,
        )
        self.assertAlmostEqual(
            _get_featured_price_amount(self.env, self.website, self.sweet), 3.5,
        )

    def test_simple_product_pricelist_price(self):
        product = self.env['product.template'].sudo().create({
            'name': 'CK Simple Pricelist QA',
            'type': 'consu',
            'is_published': True,
            'website_published': True,
            'sale_ok': True,
            'list_price': 5.8,
            'image_1920': _TINY_PNG,
        })
        variant = product.product_variant_id
        set_variant_fixed_price(self.env, self.pricelist, variant, 6.5)
        self.assertEqual(_get_featured_price_label(self.env, self.website, variant), '6,50\u00a0€')

    def test_reference_price_coherent_with_pricelist_amount(self):
        set_variant_fixed_price(self.env, self.pricelist, self.sale, 3.6)
        self.parent.write({
            'ck_net_quantity': 100,
            'ck_net_quantity_uom_id': self.env.ref(
                'dorevia_ck_marketone_content.ck_card_uom_g'
            ).id,
            'ck_reference_price_uom_id': self.env.ref(
                'dorevia_ck_marketone_content.ck_card_uom_kg'
            ).id,
            'ck_show_reference_price': True,
        })
        commercial = _get_featured_commercial_line(self.env, self.website, self.sale)
        self.assertIn('100 g', commercial)
        self.assertIn('36,00', commercial)
        card = build_featured_product_card_html(self.env, self.website, self.sale)
        self.assertIn('3,60', card)
        self.assertIn('36,00', card)


@tagged('post_install', '-at_install', 'dorevia_ck_marketone_home_section3_pricelist')
class TestCkHomeSection3FeaturedPricelistCompose(HttpCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        enable_website_pricelists(cls.env)
        cls.website = cls.env['website'].search([], limit=1)
        cls.pricelist = ensure_ck_b2c_pricelist(cls.env, cls.website)
        cls.parent, cls.sale, cls.sweet = get_manioc_cracker_variants(cls.env)
        if not (cls.parent and cls.sale and cls.sweet):
            raise unittest.SkipTest('Manio Crackers absent — recette pricelist HTTP non applicable.')
        set_variant_fixed_price(cls.env, cls.pricelist, cls.sale, 3.6)
        set_variant_fixed_price(cls.env, cls.pricelist, cls.sweet, 3.5)
        bootstrap_home_featured_products(cls.env)

    def setUp(self):
        super().setUp()
        set_variant_fixed_price(self.env, self.pricelist, self.sale, 3.6)
        set_variant_fixed_price(self.env, self.pricelist, self.sweet, 3.5)
        bootstrap_home_featured_products(self.env)

    def _featured_card_price(self, html, variant_id):
        marker = f'data-product-id="{variant_id}"'
        idx = html.find(marker)
        self.assertGreater(idx, -1, msg=f'Card variante {variant_id} absente')
        start = html.rfind('ck-product-card', 0, idx)
        chunk = html[start:idx + 400]
        match = _PRICE_RE.search(chunk)
        self.assertTrue(match, msg=chunk[:200])
        return _normalize_price_label(match.group(1))

    def _product_page_price(self, path):
        resp = self.url_open(path)
        self.assertEqual(resp.status_code, 200, path)
        html = resp.text
        match = re.search(
            r'class="oe_currency_value">(\d+,\d{2})</span>',
            html,
        )
        if match:
            return match.group(1)
        self.fail(f'Prix introuvable sur {path}')


    def _cart_line_price(self, variant):
        payload = {
            'jsonrpc': '2.0',
            'method': 'call',
            'params': {
                'product_template_id': variant.product_tmpl_id.id,
                'product_id': variant.id,
                'quantity': 1,
            },
        }
        resp = self.url_open(
            '/shop/cart/add',
            data=json.dumps(payload),
            headers={'Content-Type': 'application/json'},
            allow_redirects=False,
        )
        self.assertEqual(resp.status_code, 200)
        result = json.loads(resp.text).get('result') or {}
        tracking = result.get('tracking_info') or []
        if tracking:
            amount = tracking[0].get('price')
        else:
            lines = (result.get('notification_info') or {}).get('lines') or []
            amount = lines[0].get('price_total') if lines else None
        self.assertIsNotNone(amount, result)
        self.assertAlmostEqual(
            amount,
            _get_featured_price_amount(self.env, self.website, variant),
        )

    def test_home_card_product_cart_price_alignment_sale(self):
        home = self.url_open('/').text
        self.assertIn('3,60', self._featured_card_price(home, self.sale.id))
        self.assertEqual(self._product_page_price(self.sale.website_url), '3,60')
        self._cart_line_price(self.sale)

    def test_home_card_product_cart_price_alignment_sweet(self):
        home = self.url_open('/').text
        self.assertIn('3,50', self._featured_card_price(home, self.sweet.id))
        self.assertEqual(self._product_page_price(self.sweet.website_url), '3,50')
        self._cart_line_price(self.sweet)
