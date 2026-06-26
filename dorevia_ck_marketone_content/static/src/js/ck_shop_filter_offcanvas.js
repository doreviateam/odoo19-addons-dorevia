/** @odoo-module **/

import { Interaction } from '@web/public/interaction';
import { registry } from '@web/core/registry';
import { redirect } from '@web/core/utils/urls';

/**
 * Drawer filtres boutique CK — sélection multiple avant application.
 *
 * Odoo natif soumet le formulaire `js_attributes` à chaque changement de case,
 * ce qui recharge la page et ferme l'offcanvas. On diffère la navigation jusqu'au
 * clic sur « Appliquer les filtres » (même agrégation URL que `WebsiteSale`).
 */
function buildShopFilterRedirectUrl(form) {
    const filters = form.querySelectorAll('input:checked, select');
    const attributeValues = new Map();
    const tags = new Set();
    for (const filter of filters) {
        if (!filter.value) {
            continue;
        }
        if (filter.name === 'attribute_value') {
            const [attributeId, attributeValueId] = filter.value.split('-');
            const valueIds = attributeValues.get(attributeId) ?? new Set();
            valueIds.add(attributeValueId);
            attributeValues.set(attributeId, valueIds);
        } else if (filter.name === 'tags') {
            tags.add(filter.value);
        }
    }
    const url = new URL(form.action, window.location.origin);
    const searchParams = url.searchParams;
    searchParams.delete('attribute_values');
    searchParams.delete('tags');
    for (const [attributeId, valueIds] of attributeValues.entries()) {
        searchParams.append(
            'attribute_values',
            `${attributeId}-${[...valueIds].join(',')}`
        );
    }
    if (tags.size) {
        searchParams.set('tags', [...tags].join(','));
    }
    return `${url.pathname}?${searchParams.toString()}`;
}

export class CkShopFilterOffcanvas extends Interaction {
    static selector = '#o_wsale_offcanvas';

    dynamicContent = {
        '.ck-shop-offcanvas__apply-btn': { 't-on-click.prevent': this.onApplyFilters },
    };

    setup() {
        this._onFormChangeCapture = (ev) => {
            const target = ev.target;
            if (!(target instanceof HTMLInputElement || target instanceof HTMLSelectElement)) {
                return;
            }
            if (target.name !== 'tags' && target.name !== 'attribute_value') {
                return;
            }
            const form = target.closest('form.js_attributes');
            if (!form || !this.el.contains(form)) {
                return;
            }
            ev.preventDefault();
            ev.stopPropagation();
            ev.stopImmediatePropagation();
        };
        this.el.addEventListener('change', this._onFormChangeCapture, true);
    }

    destroy() {
        this.el.removeEventListener('change', this._onFormChangeCapture, true);
        super.destroy();
    }

    onApplyFilters() {
        const form = this.el.querySelector('form.js_attributes');
        if (!form) {
            return;
        }
        document
            .querySelector('.o_wsale_products_grid_table_wrapper')
            ?.classList.add('opacity-50');
        redirect(buildShopFilterRedirectUrl(form));
    }
}

registry
    .category('public.interactions')
    .add('dorevia_ck_marketone_content.shop_filter_offcanvas', CkShopFilterOffcanvas);
