/** @odoo-module **/

import { registry } from '@web/core/registry';
import { Interaction } from '@web/public/interaction';

const DESKTOP_QUERY = '(min-width: 992px)';

/**
 * UX-4 Lot 3 — preview « Voir » in-page depuis /shop.
 * UX-4 Lot 3bis — retrait naturel (clic / scroll hors panneau).
 * UX-4 Lot 3ter — clic image tuile aligné sur CTA Voir.
 *
 * Desktop : offcanvas latéral droit non modal.
 * Mobile : bloc inline sous tuile (une seule preview ouverte).
 * Fallback : produits configurables → navigation fiche (href conservé).
 */
export class MarketoneShopPreview extends Interaction {
    static selector =
        '.marketone-shop .marketone-shop-card-cta, .marketone-shop .oe_product_image';

    dynamicContent = {
        _root: { 't-on-click': this.onPreviewTriggerClick },
    };

    setup() {
        super.setup();
        this._activeCta = null;
        this._offcanvasEl = document.getElementById('marketone_shop_preview_offcanvas');
        this._offcanvasBody = this._offcanvasEl?.querySelector(
            '.marketone-shop-preview-offcanvas__body'
        );
        this._offcanvasCloseBtn = this._offcanvasEl?.querySelector(
            '.marketone-shop-preview-offcanvas__close'
        );

        if (this._offcanvasEl) {
            this._offcanvasEl.addEventListener('hidden.bs.offcanvas', () => {
                this._finishDesktopClose();
            });
        }

        this._onCloseButtonClick = (ev) => {
            ev.preventDefault();
            ev.stopPropagation();
            this._closeAll();
        };
        this._offcanvasCloseBtn?.addEventListener('click', this._onCloseButtonClick);

        this._onDocumentClickCapture = (ev) => {
            if (ev.target.closest('.marketone-shop-preview__close')) {
                ev.preventDefault();
                ev.stopPropagation();
                this._closeAll();
            }
        };
        document.addEventListener('click', this._onDocumentClickCapture, true);

        this._onOutsideClick = (ev) => {
            if (!this._activeCta || this._isDismissExemptTarget(ev.target)) {
                return;
            }
            this._closeAll();
        };
        document.addEventListener('click', this._onOutsideClick);

        this._onOutsideScroll = (ev) => {
            if (!this._activeCta || this._isScrollInsidePreview(ev.target)) {
                return;
            }
            this._closeAll();
        };
        document.addEventListener('scroll', this._onOutsideScroll, true);

        this._onKeydown = (ev) => {
            if (ev.key === 'Escape') {
                this._closeAll();
            }
        };
        document.addEventListener('keydown', this._onKeydown);
    }

    destroy() {
        document.removeEventListener('click', this._onDocumentClickCapture, true);
        document.removeEventListener('click', this._onOutsideClick);
        document.removeEventListener('scroll', this._onOutsideScroll, true);
        document.removeEventListener('keydown', this._onKeydown);
        this._offcanvasCloseBtn?.removeEventListener('click', this._onCloseButtonClick);
        super.destroy();
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
                target.closest('.oe_product_image')
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
            this._offcanvasEl?.contains(target) ||
                target.closest('.marketone-shop-preview')
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
     * @param {HTMLElement} trigger
     * @param {HTMLElement|null} cta
     * @returns {boolean}
     */
    _isPreviewAllowed(trigger, cta) {
        const allowed = trigger.dataset.marketonePreviewAllowed ?? cta?.dataset.marketonePreviewAllowed;
        return allowed === 'True';
    }

    /**
     * @param {HTMLElement} trigger
     * @param {HTMLElement|null} cta
     * @returns {number}
     */
    _getTemplateId(trigger, cta) {
        return parseInt(trigger.dataset.productTemplateId ?? cta?.dataset.productTemplateId, 10);
    }

    /**
     * @param {HTMLElement} card
     * @returns {boolean}
     */
    _isCardPreviewAllowed(card) {
        return card?.dataset.marketonePreviewAllowed === 'True';
    }

    /**
     * @param {HTMLElement} card
     * @returns {number}
     */
    _getCardTemplateId(card) {
        return parseInt(card?.dataset.productTemplateId, 10);
    }

    /**
     * @param {MouseEvent} ev
     */
    async onPreviewTriggerClick(ev) {
        if (
            ev.target.closest(
                '.marketone-shop-card-cart, .marketone-shop-card-wishlist, .o_wsale_product_btn'
            )
        ) {
            return;
        }

        const trigger = ev.currentTarget;
        const card = trigger.closest('.oe_product_cart');
        if (!card) {
            return;
        }

        const cta = this._getCardPreviewCta(card);
        const fromImage = trigger.classList.contains('oe_product_image');
        if (fromImage && !ev.target.closest('.oe_product_image_link, .oe_product_image_img_wrapper, .oe_product_image_img')) {
            return;
        }

        const previewAllowed = fromImage
            ? this._isCardPreviewAllowed(card)
            : this._isPreviewAllowed(trigger, cta);
        if (!previewAllowed) {
            return;
        }

        ev.preventDefault();
        ev.stopPropagation();

        const templateId = fromImage
            ? this._getCardTemplateId(card)
            : this._getTemplateId(trigger, cta);
        if (!templateId) {
            return;
        }

        const stateCta = cta || trigger;
        if (this._activeCta === stateCta) {
            this._closeAll();
            return;
        }

        this._closeAllImmediate();
        const html = await this.waitFor(this._fetchPreview(templateId));
        if (!html) {
            const fallbackHref = cta?.getAttribute('href') || trigger.getAttribute('href');
            if (fallbackHref) {
                window.location.href = fallbackHref;
            }
            return;
        }

        if (window.matchMedia(DESKTOP_QUERY).matches) {
            this._openDesktop(html, stateCta);
        } else {
            this._openMobile(html, card, stateCta);
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
        if (!this._offcanvasEl || !this._offcanvasBody) {
            return;
        }
        this._clearPreviewContainer(this._offcanvasBody);
        this._offcanvasBody.innerHTML = html;
        this._startPreviewInteractions(this._offcanvasBody);
        this._activeCta = cta;
        this._setCtaExpanded(cta, true);
        this._offcanvasEl.classList.add('marketone-shop-preview-offcanvas--open');
        const Offcanvas = window.bootstrap?.Offcanvas;
        if (Offcanvas) {
            Offcanvas.getOrCreateInstance(this._offcanvasEl, {
                backdrop: false,
                scroll: true,
            }).show();
        } else {
            this._offcanvasEl.classList.add('show');
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
        slot.classList.add('marketone-shop-card-preview-slot--open');
        card.classList.add('marketone-shop-card--preview-open');
        this._activeCta = cta;
        this._setCtaExpanded(cta, true);
    }

    _closeAll() {
        this._closeDesktopPanel();
        this._closeMobile();
    }

    _closeAllImmediate() {
        const Offcanvas = window.bootstrap?.Offcanvas;
        const instance = this._offcanvasEl && Offcanvas?.getInstance(this._offcanvasEl);
        if (instance) {
            instance.dispose();
        }
        this._finishDesktopClose();
        this._closeMobile();
    }

    _closeDesktopPanel() {
        if (!this._offcanvasEl) {
            return;
        }
        const isOpen =
            this._offcanvasEl.classList.contains('show') ||
            this._offcanvasEl.classList.contains('marketone-shop-preview-offcanvas--open');
        if (!isOpen) {
            return;
        }
        const Offcanvas = window.bootstrap?.Offcanvas;
        if (Offcanvas) {
            const instance = Offcanvas.getInstance(this._offcanvasEl);
            if (instance) {
                instance.hide();
                return;
            }
        }
        this._offcanvasEl.classList.remove('show');
        this._finishDesktopClose();
    }

    _finishDesktopClose() {
        if (this._offcanvasBody) {
            this._clearPreviewContainer(this._offcanvasBody);
            this._offcanvasBody.innerHTML = '';
        }
        if (this._offcanvasEl) {
            this._offcanvasEl.classList.remove(
                'show',
                'marketone-shop-preview-offcanvas--open'
            );
        }
        this._resetCtaState(this._activeCta);
        this._activeCta = null;
    }

    _closeMobile() {
        let closed = false;
        for (const slot of document.querySelectorAll('.marketone-shop-card-preview-slot--open')) {
            this._clearPreviewContainer(slot);
            slot.innerHTML = '';
            slot.hidden = true;
            slot.classList.remove('marketone-shop-card-preview-slot--open');
            closed = true;
        }
        for (const openCard of document.querySelectorAll('.marketone-shop-card--preview-open')) {
            openCard.classList.remove('marketone-shop-card--preview-open');
        }
        if (closed) {
            this._resetCtaState(this._activeCta);
            this._activeCta = null;
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
