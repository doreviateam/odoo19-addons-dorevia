/** @odoo-module **/

import { patch } from '@web/core/utils/patch';
import { browser } from '@web/core/browser/browser';
import { rpc } from '@web/core/network/rpc';
import { redirect } from '@web/core/utils/urls';
import { CartLine } from '@website_sale/interactions/cart_line';
import wSaleUtils from '@website_sale/js/website_sale_utils';

/**
 * CK-CHECKOUT-STOCK-001 — warning stock panier : toast unique via cartNotificationService.
 * Le bandeau legacy showWarning est volontairement omis (évite doublon persistant + toast).
 */
patch(CartLine.prototype, {
    async _changeQuantity(input) {
        let quantity = parseInt(input.value || 0, 10);
        if (Number.isNaN(quantity)) {
            quantity = 1;
        }
        const lineId = parseInt(input.dataset.lineId, 10);
        const data = await this.waitFor(
            rpc('/shop/cart/update', {
                line_id: lineId,
                product_id: parseInt(input.dataset.productId, 10),
                quantity,
            })
        );

        if (!data.cart_quantity) {
            browser.sessionStorage.setItem('website_sale_cart_quantity', 0);
            return redirect('/shop/cart');
        }
        input.value = data.quantity;
        this.el.querySelectorAll(`.js_quantity[data-line-id="${lineId}"]`).forEach(
            (qtyInput) => {
                qtyInput.value = data.quantity;
            }
        );

        const cart = this.el.closest('#shop_cart');
        this.services['public.interactions'].stopInteractions(cart);
        wSaleUtils.updateCartNavBar(data);
        wSaleUtils.updateQuickReorderSidebar(data);
        this.services['public.interactions'].startInteractions(cart);

        if (data.warning) {
            this.services.cartNotificationService?.add('', { warning: data.warning });
        }
        this.env.bus.trigger('cart_amount_changed', [data.amount, data.minor_amount]);
    },
});
