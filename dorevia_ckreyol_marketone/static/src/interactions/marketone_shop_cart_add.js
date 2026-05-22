/** @odoo-module **/

import { registry } from '@web/core/registry';
import { Interaction } from '@web/public/interaction';
import wSaleUtils from '@website_sale/js/website_sale_utils';

/**
 * UX-4 Lot 2 — ajout panier depuis la grille /shop (Odoo 19 Interaction API).
 *
 * Délègue au service `cart` standard (`/shop/cart/add`, mode `stay`) et applique
 * le feedback local carte sans quitter `/shop`.
 */
export class MarketoneShopCartAdd extends Interaction {
    static selector = '.marketone-shop .marketone-shop-card-cart';

    dynamicContent = {
        _root: { 't-on-click.prevent': this.onAddClick },
    };

    /**
     * @param {MouseEvent} ev
     */
    async onAddClick(ev) {
        ev.stopPropagation();
        const el = ev.currentTarget;
        const form = wSaleUtils.getClosestProductForm(el);
        if (!form) {
            return;
        }
        const product = this._getProductFromForm(form);
        if (!product.productTemplateId) {
            return;
        }
        await this.waitFor(
            this.services.cart.add(product, {
                isBuyNow: false,
                isConfigured: false,
                showQuantity: el.dataset.showQuantity === 'True',
            })
        );
        const card = el.closest('.oe_product_cart');
        if (card) {
            this.setVisualState(card, true);
        }
    }

    /**
     * @param {HTMLFormElement} form
     */
    _getProductFromForm(form) {
        const productId = parseInt(form.querySelector('input[name="product_id"]')?.value, 10);
        const productTemplateId = parseInt(
            form.querySelector('input[name="product_template_id"]')?.value,
            10
        );
        const isCombo =
            form.querySelector('input[name="product_type"]')?.value === 'combo';
        return {
            ...(productId ? { productId } : {}),
            productTemplateId,
            quantity: 1,
            ...(isCombo ? { isCombo: true } : {}),
        };
    }

    /**
     * @param {HTMLElement} card
     * @param {boolean} added
     */
    setVisualState(card, added) {
        card.classList.toggle('marketone-shop-card--added-to-cart', added);
        const feedback = card.querySelector('.marketone-shop-card-cart-feedback');
        if (feedback) {
            feedback.hidden = !added;
        }
    }
}

registry
    .category('public.interactions')
    .add('dorevia_ckreyol_marketone.shop_cart_add', MarketoneShopCartAdd);
