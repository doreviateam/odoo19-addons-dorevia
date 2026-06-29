# -*- coding: utf-8 -*-
"""Wishlist-U1 — persistance session visiteur sur ajout favori."""

from odoo.addons.website_sale_wishlist.controllers.main import WebsiteSaleWishlist
from odoo.http import request, route


class CkWebsiteSaleWishlist(WebsiteSaleWishlist):
    @route('/shop/wishlist/add', type='jsonrpc', auth='public', website=True)
    def add_to_wishlist(self, product_id, **kw):
        """Odoo natif n'appelle pas session.touch() à l'ajout (contrairement au retrait).

        Sans touch, wishlist_ids peut ne pas être persisté dans le cookie de session :
        le compteur header repasse à 0 au refresh et willStart() écrase sessionStorage.
        """
        wish = super().add_to_wishlist(product_id, **kw)
        if request.website.is_public_user():
            request.session.touch()
        return wish
