/** @odoo-module **/

import { browser } from '@web/core/browser/browser';
import { _t } from '@web/core/l10n/translation';
import { rpc } from '@web/core/network/rpc';
import { Interaction } from '@web/public/interaction';
import { registry } from '@web/core/registry';

/**
 * Section home « Nos coups de cœur » — ajout panier via `/shop/cart/add`.
 *
 * Le service `cart` natif appelle `_trackProducts` sur `.oe_website_sale`, absent de la
 * home : l’ajout réussit mais la promesse rejette → toast danger parasite. On aligne
 * sur le pattern grille Marketone (RPC + sync header uniquement).
 */
export class CkFeaturedCartAdd extends Interaction {
    // Liens soft-launch « Voir le produit » (.card-cart-cta--view) exclus.
    static selector = '.ck-featured-products button.card-cart-cta';

    dynamicContent = {
        _root: { 't-on-click.prevent': this.onAddClick },
    };

    /**
     * @param {MouseEvent} ev
     */
    async onAddClick(ev) {
        ev.stopPropagation();
        const button = ev.currentTarget;
        const productId = parseInt(button.dataset.productId, 10);
        const productTemplateId = parseInt(button.dataset.productTemplateId, 10);
        if (!productId || !productTemplateId) {
            return;
        }
        button.disabled = true;
        try {
            const data = await this.waitFor(
                rpc('/shop/cart/add', {
                    product_template_id: productTemplateId,
                    product_id: productId,
                    quantity: 1,
                })
            );
            this._syncCartHeader(data.cart_quantity);
            this._showCartNotification(data.notification_info);
            this._trackAddToCart(data.tracking_info);
        } catch {
            this.services.notification.add(
                _t('Impossible d\'ajouter ce produit au panier. Réessayez ou consultez la fiche produit.'),
                { type: 'danger' }
            );
        } finally {
            button.disabled = false;
        }
    }

    /**
     * @param {number|undefined|null} cartQuantity
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
     * @param {Object|undefined} notificationInfo
     */
    _showCartNotification(notificationInfo) {
        if (!notificationInfo) {
            return;
        }
        const cartNotificationService = this.services.cartNotificationService;
        if (!cartNotificationService) {
            return;
        }
        if (notificationInfo.lines) {
            cartNotificationService.add('', {
                lines: notificationInfo.lines,
                currency_id: notificationInfo.currency_id,
            });
        }
        if (notificationInfo.warning) {
            cartNotificationService.add('', { warning: notificationInfo.warning });
        }
    }

    /**
     * @param {Object|undefined} trackingInfo
     */
    _trackAddToCart(trackingInfo) {
        if (!trackingInfo) {
            return;
        }
        document.querySelector('.oe_website_sale')?.dispatchEvent(
            new CustomEvent('add_to_cart_event', { detail: trackingInfo })
        );
    }
}

registry
    .category('public.interactions')
    .add('dorevia_ck_marketone_content.featured_cart_add', CkFeaturedCartAdd);
