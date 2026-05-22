/** @odoo-module **/

import { rpc } from '@web/core/network/rpc';
import { registry } from '@web/core/registry';
import { Interaction } from '@web/public/interaction';
import wSaleUtils from '@website_sale/js/website_sale_utils';
import wishlistUtils from '@website_sale_wishlist/js/website_sale_wishlist_utils';

/**
 * UX-4 Lot 1 — toggle wishlist depuis la grille /shop (Odoo 19 Interaction API).
 *
 * Les boutons grille n'utilisent pas la classe `o_add_wishlist` pour éviter le handler
 * standard `AddProductToWishlistButton` (add-only + disabled).
 */
export class MarketoneShopWishlistToggle extends Interaction {
    static selector = '.marketone-shop-card-wishlist';

    dynamicContent = {
        _root: { 't-on-click.prevent': this.onToggleClick },
    };

    start() {
        super.start();
        this.syncButtonState(this.el);
    }

    /**
     * @param {MouseEvent} ev
     */
    async onToggleClick(ev) {
        ev.stopPropagation();
        const el = this.el;
        const productId = await this.waitFor(this.resolveProductId(el));
        if (!productId) {
            return;
        }
        el.dataset.productProductId = productId;
        const wishlistIds = wishlistUtils.getWishlistProductIds();
        if (wishlistIds.includes(productId)) {
            await this.waitFor(this.removeFromWishlist(el, productId));
        } else {
            await this.waitFor(this.addToWishlist(el, productId));
        }
    }

    /**
     * @param {HTMLElement} el
     * @returns {Promise<number|false>}
     */
    async resolveProductId(el) {
        let productId = parseInt(el.dataset.productProductId, 10);
        if (productId) {
            return productId;
        }
        const form = wSaleUtils.getClosestProductForm(el);
        const templateId = parseInt(el.dataset.productTemplateId, 10);
        if (!templateId) {
            return false;
        }
        return parseInt(
            await rpc('/sale/create_product_variant', {
                product_template_id: templateId,
                product_template_attribute_value_ids: wSaleUtils.getSelectedAttributeValues(form),
            }),
            10
        );
    }

    /**
     * @param {HTMLElement} el
     * @param {number} productId
     */
    async addToWishlist(el, productId) {
        await rpc('/shop/wishlist/add', { product_id: productId });
        wishlistUtils.addWishlistProduct(productId);
        wishlistUtils.updateWishlistNavBar();
        this.setVisualState(el, true);
        const wishNav = document.querySelector('.o_wsale_my_wish');
        const form = wSaleUtils.getClosestProductForm(el);
        if (wishNav && form) {
            await wSaleUtils.animateClone($(wishNav), $(form), 25, 40);
        }
    }

    /**
     * @param {HTMLElement} el
     * @param {number} productId
     */
    async removeFromWishlist(el, productId) {
        await rpc('/shop/wishlist/remove_by_product', { product_id: productId });
        wishlistUtils.removeWishlistProduct(productId);
        wishlistUtils.updateWishlistNavBar();
        this.setVisualState(el, false);
    }

    /**
     * @param {HTMLElement} el
     * @param {boolean} inWishlist
     */
    syncButtonState(el) {
        const productId = parseInt(el.dataset.productProductId, 10);
        if (!productId) {
            return;
        }
        const inWishlist = wishlistUtils.getWishlistProductIds().includes(productId);
        this.setVisualState(el, inWishlist);
    }

    /**
     * @param {HTMLElement} el
     * @param {boolean} inWishlist
     */
    setVisualState(el, inWishlist) {
        el.classList.toggle('o_in_wishlist', inWishlist);
        el.classList.toggle('is-active', inWishlist);
        el.setAttribute('aria-pressed', inWishlist ? 'true' : 'false');
        const label = inWishlist ? 'Retirer de la liste' : 'Ajouter à la liste';
        el.title = label;
        el.setAttribute('aria-label', label);
        wishlistUtils.updateDisabled(el, false);
        const iconEl = el.querySelector('.fa');
        if (iconEl) {
            iconEl.classList.toggle('fa-heart', inWishlist);
            iconEl.classList.toggle('fa-heart-o', !inWishlist);
        }
        const card = el.closest('.oe_product_cart');
        if (card) {
            card.classList.toggle('marketone-shop-card--in-wishlist', inWishlist);
        }
    }
}

registry
    .category('public.interactions')
    .add('dorevia_ckreyol_marketone.shop_wishlist_toggle', MarketoneShopWishlistToggle);
