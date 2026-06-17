/** @odoo-module **/

import { _t } from '@web/core/l10n/translation';
import { Interaction } from '@web/public/interaction';
import { registry } from '@web/core/registry';

/**
 * Section home « Nos coups de cœur » — ajout panier via le service `cart` Odoo 19.
 */
export class CkFeaturedCartAdd extends Interaction {
    static selector = '.ck-featured-products .card-cart-cta';

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
            await this.waitFor(
                this.services.cart.add(
                    {
                        productId,
                        productTemplateId,
                        quantity: 1,
                    },
                    {
                        isBuyNow: false,
                        isConfigured: true,
                        showQuantity: false,
                    }
                )
            );
        } catch {
            this.services.notification.add(
                _t('Impossible d\'ajouter ce produit au panier. Réessayez ou consultez la fiche produit.'),
                { type: 'danger' }
            );
        } finally {
            button.disabled = false;
        }
    }
}

registry
    .category('public.interactions')
    .add('dorevia_ck_marketone_content.featured_cart_add', CkFeaturedCartAdd);
