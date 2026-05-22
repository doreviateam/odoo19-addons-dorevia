/** @odoo-module **/

import { rpc } from '@web/core/network/rpc';
import { registry } from '@web/core/registry';
import { Interaction } from '@web/public/interaction';
import wSaleUtils from '@website_sale/js/website_sale_utils';

/**
 * UX-4 Lot 2 — ajout panier depuis la grille /shop (Odoo 19 Interaction API).
 *
 * Grille : add direct via `/shop/cart/add` quand la variante est déjà connue
 * (évite le configurateur Odoo / produits optionnels sur le 1er clic).
 * Fallback service `cart` pour combos ou variantes non résolues.
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
        const card = el.closest('.oe_product_cart');
        const product = await this.waitFor(this._resolveProduct(form));
        if (!product?.productTemplateId) {
            return;
        }
        const added = await this.waitFor(this._addToCart(product));
        if (added && card) {
            this.setVisualState(card, true);
        }
    }

    /**
     * @param {HTMLFormElement} form
     */
    async _resolveProduct(form) {
        let productId = parseInt(form.querySelector('input[name="product_id"]')?.value, 10);
        const productTemplateId = parseInt(
            form.querySelector('input[name="product_template_id"]')?.value,
            10
        );
        if (!productTemplateId) {
            return null;
        }
        if (!productId) {
            productId = parseInt(
                await rpc('/sale/create_product_variant', {
                    product_template_id: productTemplateId,
                    product_template_attribute_value_ids:
                        wSaleUtils.getSelectedAttributeValues(form),
                }),
                10
            );
        }
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
     * @param {Object} product
     * @returns {Promise<boolean>}
     */
    async _addToCart(product) {
        if (product.isCombo || !product.productId) {
            await this.services.cart.add(product, {
                isBuyNow: false,
                isConfigured: Boolean(product.productId),
                showQuantity: false,
            });
            return true;
        }

        const data = await rpc('/shop/cart/add', {
            product_template_id: product.productTemplateId,
            product_id: product.productId,
            quantity: product.quantity,
        });
        wSaleUtils.updateCartNavBar(data);
        if (data.tracking_info) {
            document.querySelector('.oe_website_sale')?.dispatchEvent(
                new CustomEvent('add_to_cart_event', { detail: data.tracking_info })
            );
        }
        return Boolean(data.quantity);
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
