/** @odoo-module **/

import { registry } from '@web/core/registry';
import { Interaction } from '@web/public/interaction';

const DESKTOP_QUERY = '(min-width: 992px)';

/**
 * UX-4 Lot 3 — preview « Voir » in-page depuis /shop.
 *
 * Desktop : offcanvas latéral droit non modal.
 * Mobile : bloc inline sous tuile (une seule preview ouverte).
 * Fallback : produits configurables → navigation fiche (href conservé).
 */
export class MarketoneShopPreview extends Interaction {
    static selector = '.marketone-shop .marketone-shop-card-cta';

    dynamicContent = {
        _root: { 't-on-click': this.onCtaClick },
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
        this._offcanvasCloseTextBtn = this._offcanvasEl?.querySelector(
            '.marketone-shop-preview-offcanvas__close-text'
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
        this._offcanvasCloseTextBtn?.addEventListener('click', this._onCloseButtonClick);

        this._onDocumentClick = (ev) => {
            if (ev.target.closest('.marketone-shop-preview__close')) {
                ev.preventDefault();
                ev.stopPropagation();
                this._closeAll();
            }
        };
        document.addEventListener('click', this._onDocumentClick, true);

        this._onKeydown = (ev) => {
            if (ev.key === 'Escape') {
                this._closeAll();
            }
        };
        document.addEventListener('keydown', this._onKeydown);
    }

    destroy() {
        document.removeEventListener('click', this._onDocumentClick, true);
        document.removeEventListener('keydown', this._onKeydown);
        this._offcanvasCloseBtn?.removeEventListener('click', this._onCloseButtonClick);
        this._offcanvasCloseTextBtn?.removeEventListener('click', this._onCloseButtonClick);
        super.destroy();
    }

    /**
     * @param {MouseEvent} ev
     */
    async onCtaClick(ev) {
        const cta = ev.currentTarget;
        const previewAllowed = cta.dataset.marketonePreviewAllowed === 'True';
        if (!previewAllowed) {
            return;
        }
        ev.preventDefault();
        ev.stopPropagation();

        const templateId = parseInt(cta.dataset.productTemplateId, 10);
        if (!templateId) {
            return;
        }

        const card = cta.closest('.oe_product_cart');
        if (!card) {
            return;
        }

        if (this._activeCta === cta) {
            this._closeAll();
            return;
        }

        this._closeAllImmediate();
        const html = await this.waitFor(this._fetchPreview(templateId));
        if (!html) {
            window.location.href = cta.getAttribute('href');
            return;
        }

        if (window.matchMedia(DESKTOP_QUERY).matches) {
            this._openDesktop(html, cta);
        } else {
            this._openMobile(html, card, cta);
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
