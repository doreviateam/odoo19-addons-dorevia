/** @odoo-module **/

import { patch } from '@web/core/utils/patch';
import { CartLine } from '@website_sale/interactions/cart_line';
import wSaleUtils from '@website_sale/js/website_sale_utils';

/**
 * CK S3-B1 — avertissement stock panier en toast unique.
 *
 * Doctrine : ne pas recopier `_changeQuantity`. Remplacer uniquement
 * `wSaleUtils.showWarning` (seul appelant Odoo 19 : CartLine), car c'est le
 * seul point où le standard affiche `data.warning` sur le panier.
 *
 * Patch **permanent** (pas de mutation scoped pendant un `await`) : le verrou
 * CartLine est par instance, donc deux lignes peuvent entrelacer des RPC et
 * polluer un swap temporaire du global — réintroduisant le bandeau legacy.
 *
 * Accès au service : `showWarning` n'a pas de `this.services`. On capture le
 * singleton `cartNotificationService` au `setup` de CartLine (même `env`),
 * puis on le résout à l'appel. Un seul appelant → pas d'effet de bord hors panier.
 *
 * Garde upgrade : si `showWarning` disparaît de l'API amont, l'appel échoue
 * explicitement (voir `assertShowWarningApi`).
 */

/** @type {*|null} */
let cartNotificationServiceRef = null;

export function assertShowWarningApi() {
    if (typeof wSaleUtils.showWarning !== 'function') {
        throw new Error(
            'CK S3-B1: wSaleUtils.showWarning is missing — Odoo website_sale API changed'
        );
    }
}

/**
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

export function resolveCartNotificationService() {
    return cartNotificationServiceRef;
}

/** @internal — tests uniquement */
export function setCartNotificationServiceForTests(service) {
    cartNotificationServiceRef = service;
}

assertShowWarningApi();

patch(CartLine.prototype, {
    setup() {
        super.setup();
        cartNotificationServiceRef = this.services.cartNotificationService;
    },
});

patch(wSaleUtils, {
    /**
     * @override Toast panier CK — ne pas appeler le bandeau `#data_warning`.
     * @param {string | null} message
     */
    showWarning(message) {
        showCartStockWarningToast(resolveCartNotificationService(), message);
    },
});
