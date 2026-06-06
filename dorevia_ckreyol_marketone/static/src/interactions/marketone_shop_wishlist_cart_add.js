/** @odoo-module **/

import { rpc } from '@web/core/network/rpc';
import { registry } from '@web/core/registry';
import { Interaction } from '@web/public/interaction';
import { redirect } from '@web/core/utils/urls';
import wishlistUtils from '@website_sale_wishlist/js/website_sale_wishlist_utils';

/**
 * UX-4 — ajout panier depuis /shop/wishlist avec PTAV origine alignés grille.
 *
 * Le handler Odoo standard ne transmet que les PTAV variante (souvent vides) ;
 * les attributs no_variant (origine unique) doivent être envoyés pour consolider
 * le panier avec les ajouts tuile / preview Marketone.
 */
export class MarketoneShopWishlistCartAdd extends Interaction {
    static selector = '.marketone-shop-wishlist .o_wish_add';

    dynamicContent = {
        _root: { 't-on-click.prevent.stop': this.addToCart },
    };

    /**
     * @param {MouseEvent} ev
     */
    async addToCart(ev) {
        const button = ev.currentTarget;
        const productId = parseInt(button.dataset.productProductId, 10);
        const productTemplateId = parseInt(button.dataset.productTemplateId, 10);
        const isCombo = button.dataset.productType === 'combo';
        const ptavs = JSON.parse(button.dataset.ptavIds || '[]');
        const noVariantAttributeValues = JSON.parse(
            button.dataset.noVariantAttributeValueIds || '[]'
        );
        const showQuantity = Boolean(button.dataset.showQuantity);

        const quantity = await this.waitFor(
            this.services.cart.add(
                {
                    productTemplateId,
                    productId,
                    isCombo,
                    ptavs,
                    noVariantAttributeValues,
                },
                {
                    isConfigured: false,
                    redirectToCart: false,
                    showQuantity,
                }
            )
        );

        if (quantity > 0) {
            await this._removeProduct(button, '/shop/cart');
        }
    }

    /**
     * @param {Element} button
     * @param {string} emptyRedirectUrl
     */
    async _removeProduct(button, emptyRedirectUrl) {
        const article = button.closest('article');
        const wish = article.dataset.wishId;
        const productId = parseInt(article.dataset.productId, 10);

        await this.waitFor(rpc(`/shop/wishlist/remove/${wish}`));
        article.style.display = 'none';

        wishlistUtils.removeWishlistProduct(productId);
        wishlistUtils.updateWishlistView();
        if (!wishlistUtils.getWishlistProductIds().length && emptyRedirectUrl) {
            redirect(emptyRedirectUrl);
        }
        wishlistUtils.updateWishlistNavBar();
    }
}

registry
    .category('public.interactions')
    .add('dorevia_ckreyol_marketone.shop_wishlist_cart_add', MarketoneShopWishlistCartAdd);
