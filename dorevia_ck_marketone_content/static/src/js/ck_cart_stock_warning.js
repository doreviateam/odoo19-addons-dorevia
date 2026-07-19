/** @odoo-module **/

import { patch } from '@web/core/utils/patch';
import { CartLine } from '@website_sale/interactions/cart_line';
import wSaleUtils from '@website_sale/js/website_sale_utils';

/**
 * CK S3-B1 — avertissement stock panier en toast unique.
 *
 * Doctrine : ne pas recopier `_changeQuantity`. Intercepter uniquement
 * `wSaleUtils.showWarning` pendant l'appel standard (`super`), car c'est le
 * seul point où Odoo 19 affiche `data.warning` sur le panier.
 *
 * Pourquoi pas un `patch(wSaleUtils, { showWarning })` global ?
 * `showWarning` n'a pas accès à `cartNotificationService` (pas de `this.services`).
 * L'interception scoped sur `CartLine` conserve l'accès propre au service panier
 * sans modifier les autres appelants futurs hors de ce flux.
 *
 * Garde upgrade : si `showWarning` disparaît de l'API amont, le module échoue
 * explicitement au chargement / à l'appel (voir `assertShowWarningApi`).
 */

export function assertShowWarningApi() {
    if (typeof wSaleUtils.showWarning !== 'function') {
        throw new Error(
            'CK S3-B1: wSaleUtils.showWarning is missing — Odoo website_sale API changed'
        );
    }
}

/**
 * Affiche le warning stock via toast panier, sans bandeau legacy Odoo.
 * @param {*} cartNotificationService
 * @param {string} message
 */
export function showCartStockWarningToast(cartNotificationService, message) {
    if (!message) {
        return;
    }
    if (!cartNotificationService || typeof cartNotificationService.add !== 'function') {
        throw new Error('CK S3-B1: cartNotificationService unavailable');
    }
    cartNotificationService.add('', { warning: message });
}

assertShowWarningApi();

patch(CartLine.prototype, {
    /**
     * @override
     */
    async _changeQuantity(...args) {
        assertShowWarningApi();
        const previousShowWarning = wSaleUtils.showWarning;
        const cartNotificationService = this.services.cartNotificationService;
        wSaleUtils.showWarning = (message) => {
            // Ne pas appeler previousShowWarning : évite le doublon bandeau + toast.
            showCartStockWarningToast(cartNotificationService, message);
        };
        try {
            return await super._changeQuantity(...args);
        } finally {
            wSaleUtils.showWarning = previousShowWarning;
        }
    },
});
