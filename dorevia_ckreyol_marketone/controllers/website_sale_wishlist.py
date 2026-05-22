# -*- coding: utf-8 -*-
"""Extension wishlist Marketone — toggle depuis la grille /shop (UX-4 Lot 1)."""

from odoo.http import request, route
from odoo.addons.website_sale_wishlist.controllers.main import WebsiteSaleWishlist


class MarketoneWebsiteSaleWishlist(WebsiteSaleWishlist):
    @route(
        "/shop/wishlist/remove_by_product",
        type="jsonrpc",
        auth="public",
        website=True,
    )
    def rm_from_wishlist_by_product(self, product_id, **kw):
        """Retrait wishlist par ``product.product`` id — usage grille /shop (UX-4)."""
        product_id = int(product_id)
        wishes = request.env["product.wishlist"].current().filtered(
            lambda wish: wish.product_id.id == product_id
        )
        for wish in wishes:
            if request.website.is_public_user():
                wish_ids = request.session.get("wishlist_ids") or []
                if wish.id in wish_ids:
                    request.session["wishlist_ids"].remove(wish.id)
                    request.session.touch()
                wish.sudo().unlink()
            else:
                wish.unlink()
        return True
