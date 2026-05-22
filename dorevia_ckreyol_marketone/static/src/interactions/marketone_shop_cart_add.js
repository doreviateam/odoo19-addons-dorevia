/** @odoo-module **/

import { browser } from '@web/core/browser/browser';
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
        const card = this._getProductCard(form);
        const product = await this.waitFor(this._resolveProduct(form));
        if (!product?.productTemplateId) {
            return;
        }
        await this.waitFor(this._addToCart(product));
        if (card) {
            this.setVisualState(card, true);
        }
    }

    /**
     * @param {HTMLFormElement} form
     * @returns {HTMLElement|null}
     */
    _getProductCard(form) {
        if (form.classList.contains('oe_product_cart')) {
            return form;
        }
        return form.closest('.oe_product_cart');
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
     */
    async _addToCart(product) {
        if (product.isCombo || !product.productId) {
            await this.services.cart.add(product, {
                isBuyNow: false,
                isConfigured: Boolean(product.productId),
                showQuantity: false,
            });
            return;
        }

        const data = await rpc('/shop/cart/add', {
            product_template_id: product.productTemplateId,
            product_id: product.productId,
            quantity: product.quantity,
        });
        this._syncCartHeader(data.cart_quantity);
        if (data.tracking_info) {
            document.querySelector('.oe_website_sale')?.dispatchEvent(
                new CustomEvent('add_to_cart_event', { detail: data.tracking_info })
            );
        }
    }

    /**
     * Sync header cart counter only — `updateCartNavBar` throws on /shop (no `.oe_cart`).
     *
     * @param {number} cartQuantity
     */
    _syncCartHeader(cartQuantity) {
        if (cartQuantity === undefined || cartQuantity === null) {
            return;
        }
        browser.sessionStorage.setItem('website_sale_cart_quantity', cartQuantity);
        for (const cartQuantityElement of document.querySelectorAll('.my_cart_quantity')) {
            if (cartQuantity === 0) {
                cartQuantityElement.classList.add('d-none');
                continue;
            }
            const cartIconElement = document.querySelector('li.o_wsale_my_cart');
            cartIconElement?.classList.remove('d-none');
            cartQuantityElement.classList.remove('d-none');
            cartQuantityElement.classList.add('o_mycart_zoom_animation');
            setTimeout(() => {
                cartQuantityElement.textContent = cartQuantity;
                cartQuantityElement.classList.remove('o_mycart_zoom_animation');
            }, 300);
        }
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
            feedback.classList.toggle('marketone-shop-card-cart-feedback--visible', added);
        }
    }
}

registry
    .category('public.interactions')
    .add('dorevia_ckreyol_marketone.shop_cart_add', MarketoneShopCartAdd);
