/** @odoo-module **/

import { registry } from '@web/core/registry';
import { Interaction } from '@web/public/interaction';

const DESKTOP_QUERY = '(min-width: 992px)';

/** État partagé — une seule preview ouverte, listeners document uniques. */
const previewState = {
    activeCta: null,
    offcanvasEl: null,
    offcanvasBody: null,
    offcanvasCloseBtn: null,
    controller: null,
    globalListenersBound: false,
    /** true quand le pointeur est à l'intérieur du panneau offcanvas desktop. */
    pointerInPanel: false,
};

/**
 * UX-4 Lot 3 — preview « Voir » in-page depuis /shop.
 * UX-4 Lot 3bis — retrait naturel (clic / scroll hors panneau).
 * UX-4 Lot 3ter — clic image tuile (lien photo) aligné sur CTA Voir.
 *
 * Binding direct Colibri sur CTA + lien image (pattern Lot 3bis).
 * Listeners document / dismiss : instance unique via previewState.
 */
export class MarketoneShopPreview extends Interaction {
    static selector =
        '.marketone-shop .marketone-shop-card-cta, .marketone-shop .oe_product_cart[data-marketone-preview-allowed="True"] a.oe_product_image_link';

    dynamicContent = {
        _root: { 't-on-click': this.onTriggerClick },
    };

    setup() {
        super.setup();
        previewState.controller = this;
        previewState.offcanvasEl =
            previewState.offcanvasEl ||
            document.getElementById('marketone_shop_preview_offcanvas');
        previewState.offcanvasBody =
            previewState.offcanvasBody ||
            previewState.offcanvasEl?.querySelector('.marketone-shop-preview-offcanvas__body');
        previewState.offcanvasCloseBtn =
            previewState.offcanvasCloseBtn ||
            previewState.offcanvasEl?.querySelector('.marketone-shop-preview-offcanvas__close');

        if (!previewState.globalListenersBound) {
            previewState.globalListenersBound = true;
            this._bindGlobalListeners();
        }
    }

    _bindGlobalListeners() {
        previewState.offcanvasEl?.addEventListener('hidden.bs.offcanvas', () => {
            previewState.controller?._finishDesktopClose();
        });

        // Suivi de la présence du pointeur dans le panneau : tant que le curseur
        // est à l'intérieur, le scroll de la page ne doit pas fermer la preview.
        this._onPanelMouseEnter = () => {
            previewState.pointerInPanel = true;
        };
        this._onPanelMouseLeave = () => {
            previewState.pointerInPanel = false;
        };
        previewState.offcanvasEl?.addEventListener('mouseenter', this._onPanelMouseEnter);
        previewState.offcanvasEl?.addEventListener('mouseleave', this._onPanelMouseLeave);

        this._onCloseButtonClick = (ev) => {
            ev.preventDefault();
            ev.stopPropagation();
            previewState.controller?._closeAll();
        };
        previewState.offcanvasCloseBtn?.addEventListener('click', this._onCloseButtonClick);

        this._onDocumentClickCapture = (ev) => {
            if (ev.target.closest('.marketone-shop-preview__close')) {
                ev.preventDefault();
                ev.stopPropagation();
                previewState.controller?._closeAll();
            }
        };
        document.addEventListener('click', this._onDocumentClickCapture, true);

        this._onOutsideClick = (ev) => {
            if (!previewState.activeCta || this._isDismissExemptTarget(ev.target)) {
                return;
            }
            previewState.controller?._closeAll();
        };
        document.addEventListener('click', this._onOutsideClick);

        this._onOutsideScroll = (ev) => {
            if (
                !previewState.activeCta ||
                this._isScrollInsidePreview(ev.target) ||
                previewState.pointerInPanel
            ) {
                return;
            }
            previewState.controller?._closeAll();
        };
        document.addEventListener('scroll', this._onOutsideScroll, true);

        this._onKeydown = (ev) => {
            if (ev.key === 'Escape') {
                previewState.controller?._closeAll();
            }
        };
        document.addEventListener('keydown', this._onKeydown);
    }

    /**
     * @param {EventTarget|null} target
     * @returns {boolean}
     */
    _isDismissExemptTarget(target) {
        if (!(target instanceof Element)) {
            return false;
        }
        return Boolean(
            target.closest('#marketone_shop_preview_offcanvas') ||
                target.closest('.marketone-shop-preview') ||
                target.closest('.marketone-shop-card-cta') ||
                target.closest(
                    '.oe_product_image_link, .oe_product_image_img_wrapper, .oe_product_image_img'
                )
        );
    }

    /**
     * @param {EventTarget|null} target
     * @returns {boolean}
     */
    _isScrollInsidePreview(target) {
        if (!(target instanceof Element)) {
            return false;
        }
        return Boolean(
            previewState.offcanvasEl?.contains(target) ||
                target.closest('.marketone-shop-preview') ||
                target.closest('.marketone-shop-card-preview-slot--open')
        );
    }

    /**
     * @param {HTMLElement} card
     * @returns {HTMLElement|null}
     */
    _getCardPreviewCta(card) {
        return card.querySelector('.marketone-shop-card-cta');
    }

    /**
     * @param {MouseEvent} ev
     */
    async onTriggerClick(ev) {
        if (
            ev.target.closest(
                '.marketone-shop-card-cart, .marketone-shop-card-wishlist, .o_wsale_product_btn'
            )
        ) {
            return;
        }

        const trigger = ev.currentTarget;
        const card = trigger.closest('.oe_product_cart');
        if (!card || card.classList.contains('marketone-shop-preview__actions')) {
            return;
        }

        const cta =
            trigger.classList.contains('marketone-shop-card-cta')
                ? trigger
                : this._getCardPreviewCta(card);
        if (!cta || cta.dataset.marketonePreviewAllowed !== 'True') {
            return;
        }

        ev.preventDefault();
        ev.stopPropagation();

        const templateId = parseInt(cta.dataset.productTemplateId, 10);
        if (!templateId) {
            return;
        }

        if (previewState.activeCta === cta) {
            this._closeAll();
            return;
        }

        this._closeAllImmediate();
        this._showMobileLoading(card);

        const html = await this.waitFor(this._fetchPreview(templateId));
        if (!html) {
            this._hideMobileLoading(card);
            const fallbackHref = cta.getAttribute('href');
            if (fallbackHref) {
                window.location.href = fallbackHref;
            }
            return;
        }

        if (window.matchMedia(DESKTOP_QUERY).matches) {
            this._openDesktop(html, cta);
        } else {
            this._openMobile(html, card, cta);
        }
    }

    /**
     * @param {HTMLElement} card
     */
    _showMobileLoading(card) {
        if (window.matchMedia(DESKTOP_QUERY).matches) {
            return;
        }
        const slot = card.querySelector('.marketone-shop-card-preview-slot');
        if (!slot) {
            return;
        }
        this._clearPreviewContainer(slot);
        slot.innerHTML =
            '<div class="marketone-shop-preview marketone-shop-preview--loading" aria-busy="true" aria-live="polite">' +
            '<div class="marketone-shop-preview__toolbar d-lg-none">' +
            '<span class="marketone-shop-preview__toolbar-label">Découvrir le produit</span>' +
            '</div></div>';
        slot.hidden = false;
        slot.classList.add('marketone-shop-card-preview-slot--loading');
        card.classList.add('marketone-shop-card--preview-open');
    }

    /**
     * @param {HTMLElement} card
     */
    _hideMobileLoading(card) {
        const slot = card.querySelector('.marketone-shop-card-preview-slot');
        if (!slot) {
            return;
        }
        slot.classList.remove('marketone-shop-card-preview-slot--loading');
        if (!slot.querySelector('.marketone-shop-preview')) {
            slot.hidden = true;
            card.classList.remove('marketone-shop-card--preview-open');
        }
    }

    /**
     * @param {number} templateId
     * @returns {Promise<string|null>}
     */
    async _fetchPreview(templateId) {
        const response = await fetch(`/shop/product/preview/${templateId}`, {
            headers: { 'X-Requested-With': 'XMLHttpRequest' },
        });
        if (!response.ok) {
            return null;
        }
        return response.text();
    }

    /**
     * @param {string} html
     * @param {HTMLElement} cta
     */
    _openDesktop(html, cta) {
        if (!previewState.offcanvasEl || !previewState.offcanvasBody) {
            return;
        }
        this._clearPreviewContainer(previewState.offcanvasBody);
        previewState.offcanvasBody.innerHTML = html;
        this._startPreviewInteractions(previewState.offcanvasBody);
        previewState.activeCta = cta;
        this._setCtaExpanded(cta, true);
        previewState.offcanvasEl.classList.add('marketone-shop-preview-offcanvas--open');
        const Offcanvas = window.bootstrap?.Offcanvas;
        if (Offcanvas) {
            Offcanvas.getOrCreateInstance(previewState.offcanvasEl, {
                backdrop: false,
                scroll: true,
            }).show();
        } else {
            previewState.offcanvasEl.classList.add('show');
        }
    }

    /**
     * @param {string} html
     * @param {HTMLElement} card
     * @param {HTMLElement} cta
     */
    _openMobile(html, card, cta) {
        const slot = card.querySelector('.marketone-shop-card-preview-slot');
        if (!slot) {
            return;
        }
        this._clearPreviewContainer(slot);
        slot.innerHTML = html;
        this._startPreviewInteractions(slot);
        slot.hidden = false;
        slot.classList.remove('marketone-shop-card-preview-slot--loading');
        slot.classList.add('marketone-shop-card-preview-slot--open');
        card.classList.add('marketone-shop-card--preview-open');
        previewState.activeCta = cta;
        this._setCtaExpanded(cta, true);
    }

    _closeAll() {
        this._closeDesktopPanel();
        this._closeMobile();
    }

    _closeAllImmediate() {
        const Offcanvas = window.bootstrap?.Offcanvas;
        const instance =
            previewState.offcanvasEl && Offcanvas?.getInstance(previewState.offcanvasEl);
        if (instance) {
            instance.dispose();
        }
        this._finishDesktopClose();
        this._closeMobile();
    }

    _closeDesktopPanel() {
        if (!previewState.offcanvasEl) {
            return;
        }
        const isOpen =
            previewState.offcanvasEl.classList.contains('show') ||
            previewState.offcanvasEl.classList.contains('marketone-shop-preview-offcanvas--open');
        if (!isOpen) {
            return;
        }
        const Offcanvas = window.bootstrap?.Offcanvas;
        if (Offcanvas) {
            const instance = Offcanvas.getInstance(previewState.offcanvasEl);
            if (instance) {
                instance.hide();
                return;
            }
        }
        previewState.offcanvasEl.classList.remove('show');
        this._finishDesktopClose();
    }

    _finishDesktopClose() {
        previewState.pointerInPanel = false;
        if (previewState.offcanvasBody) {
            this._clearPreviewContainer(previewState.offcanvasBody);
            previewState.offcanvasBody.innerHTML = '';
        }
        if (previewState.offcanvasEl) {
            previewState.offcanvasEl.classList.remove(
                'show',
                'marketone-shop-preview-offcanvas--open'
            );
        }
        this._resetCtaState(previewState.activeCta);
        previewState.activeCta = null;
    }

    _closeMobile() {
        let closed = false;
        for (const slot of document.querySelectorAll('.marketone-shop-card-preview-slot--open, .marketone-shop-card-preview-slot--loading')) {
            const card = slot.closest('.oe_product_cart');
            this._clearPreviewContainer(slot);
            slot.innerHTML = '';
            slot.hidden = true;
            slot.classList.remove(
                'marketone-shop-card-preview-slot--open',
                'marketone-shop-card-preview-slot--loading'
            );
            closed = true;
            if (card) {
                card.classList.remove('marketone-shop-card--preview-open');
            }
        }
        if (closed) {
            this._resetCtaState(previewState.activeCta);
            previewState.activeCta = null;
        }
    }

    /**
     * @param {HTMLElement|null} cta
     */
    _resetCtaState(cta) {
        if (cta) {
            this._setCtaExpanded(cta, false);
        }
    }

    /**
     * @param {HTMLElement} cta
     * @param {boolean} expanded
     */
    _setCtaExpanded(cta, expanded) {
        cta.setAttribute('aria-expanded', expanded ? 'true' : 'false');
        cta.classList.toggle('marketone-shop-card-cta--active', expanded);
    }

    /**
     * @param {HTMLElement} container
     */
    _startPreviewInteractions(container) {
        const root = container.firstElementChild;
        if (root) {
            this.services['public.interactions'].startInteractions(root);
        }
    }

    /**
     * @param {HTMLElement} container
     */
    _clearPreviewContainer(container) {
        for (const child of container.children) {
            this.services['public.interactions'].stopInteractions(child);
        }
    }
}

registry
    .category('public.interactions')
    .add('dorevia_ckreyol_marketone.shop_preview', MarketoneShopPreview);
