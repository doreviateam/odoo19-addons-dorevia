# -*- coding: utf-8 -*-
"""Garde-fous HTTP — page liste Favoris `/shop/wishlist` (charte CK minimale)."""

from odoo.tests import tagged
from odoo.tests.common import HttpCase


@tagged("post_install", "-at_install", "dorevia_ckr_shop_wishlist")
class TestCkrShopWishlist(HttpCase):
    """Lot 2 Favoris incrément minimal : wrap CK + rendu 200."""

    def test_wishlist_page_wrap_ck_and_empty_shell(self):
        """La liste expose les classes d’ancrage CK et le gabarit standard Odoo."""
        resp = self.url_open("/shop/wishlist", timeout=60)
        self.assertEqual(resp.status_code, 200)
        self.assertIn("ckr-shop-wishlist", resp.text)
        self.assertIn("ckr-root", resp.text)
        self.assertIn("ckr-page", resp.text)
        self.assertIn("wishlist-section", resp.text)
        self.assertIn("empty-wishlist-message", resp.text)
        self.assertIn("o_wishlist_table", resp.text)
