/** @odoo-module **/

import { Interaction } from '@web/public/interaction';
import { registry } from '@web/core/registry';

/**
 * Header CK V2.2 — masque le bandeau promesses au scroll desktop.
 */
export class CkHeaderServiceBarScroll extends Interaction {
    static selector = '.ck-header-service-bar';

    setup() {
        this.onScroll = this.onScroll.bind(this);
        this.threshold = 8;
        window.addEventListener('scroll', this.onScroll, { passive: true });
        this.onScroll();
    }

    destroy() {
        window.removeEventListener('scroll', this.onScroll);
        super.destroy();
    }

    onScroll() {
        const scrolled = window.scrollY > this.threshold;
        this.el.classList.toggle('ck-header-service-bar--hidden', scrolled);
        document.body.classList.toggle('ck-header-service-bar-is-hidden', scrolled);
    }
}

registry
    .category('public.interactions')
    .add('dorevia_ck_theme.ck_header_service_bar_scroll', CkHeaderServiceBarScroll);

/**
 * Header CK V2.2 — stabilise le hover des mega-menus rayons.
 *
 * Odoo/Bootstrap ferme les dropdowns hoverables dès que le pointeur quitte
 * l'entrée N3. Or le panneau mega est positionné sous la ligne N3 : pendant
 * la descente vers un lien du panneau, un hide peut être déclenché avant que
 * le pointeur n'atteigne le contenu. On annule ce hide lorsque le pointeur se
 * trouve encore dans la zone utile entrée → panneau.
 */
export class CkHeaderMegaMenuHoverBridge extends Interaction {
    static selector = 'header#top.ck-header';

    setup() {
        this.pointer = { x: 0, y: 0 };
        this.records = [];
        this.activeRecord = null;
        this.onPointerMove = this.onPointerMove.bind(this);
        document.addEventListener('pointermove', this.onPointerMove, { passive: true });
        this.bindMegaItems();
    }

    destroy() {
        document.removeEventListener('pointermove', this.onPointerMove);
        for (const record of this.records) {
            record.item.removeEventListener('mouseenter', record.onEnter);
            record.item.removeEventListener('mouseleave', record.onLeave);
            record.toggle?.removeEventListener('hide.bs.dropdown', record.onHide);
        }
        this.records = [];
        super.destroy();
    }

    onPointerMove(ev) {
        this.pointer = { x: ev.clientX, y: ev.clientY };
    }

    bindMegaItems() {
        const items = [...this.el.querySelectorAll('#top_menu > li.ck-nav-mega-product')];
        for (const item of items) {
            const panel = item.querySelector('.o_mega_menu');
            const toggle = item.querySelector('.ck-nav-mega-split__toggle, .dropdown-toggle');
            if (!panel || !toggle) {
                continue;
            }
            const record = { item, panel, toggle, bridgeRect: null, closeTimer: null };
            record.onEnter = () => {
                this.activateRecord(record);
            };
            record.onLeave = () => {
                this.refreshBridgeRect(record);
                this.scheduleClose(record);
            };
            record.onHide = (ev) => {
                this.refreshBridgeRect(record);
                if (record === this.activeRecord && this.isPointerInside(record.bridgeRect)) {
                    ev.preventDefault();
                    this.showDropdown(toggle);
                }
            };
            item.addEventListener('mouseenter', record.onEnter);
            item.addEventListener('mouseleave', record.onLeave);
            toggle.addEventListener('hide.bs.dropdown', record.onHide);
            this.records.push(record);
        }
    }

    activateRecord(record) {
        this.activeRecord = record;
        for (const other of this.records) {
            this.clearClose(other);
            if (other !== record) {
                this.forceHideRecord(other);
            }
        }
        this.showDropdown(record.toggle);
        window.requestAnimationFrame(() => {
            for (const other of this.records) {
                if (other !== record) {
                    this.forceHideRecord(other);
                }
            }
            this.refreshBridgeRect(record);
        });
    }

    refreshBridgeRect(record) {
        const itemRect = record.item.getBoundingClientRect();
        const panelRect = record.panel.getBoundingClientRect();
        if (!panelRect.width || !panelRect.height) {
            return;
        }
        record.bridgeRect = {
            left: Math.min(itemRect.left, panelRect.left),
            right: Math.max(itemRect.right, panelRect.right),
            top: itemRect.top,
            bottom: panelRect.bottom,
        };
    }

    isPointerInside(rect) {
        if (!rect) {
            return false;
        }
        return (
            this.pointer.x >= rect.left &&
            this.pointer.x <= rect.right &&
            this.pointer.y >= rect.top &&
            this.pointer.y <= rect.bottom
        );
    }

    scheduleClose(record) {
        this.clearClose(record);
        record.closeTimer = window.setTimeout(() => {
            this.refreshBridgeRect(record);
            if (!this.isPointerInside(record.bridgeRect)) {
                if (record === this.activeRecord) {
                    this.activeRecord = null;
                }
                this.hideDropdown(record.toggle);
            }
        }, 180);
    }

    clearClose(record) {
        if (record.closeTimer) {
            window.clearTimeout(record.closeTimer);
            record.closeTimer = null;
        }
    }

    showDropdown(toggle) {
        window.bootstrap?.Dropdown?.getOrCreateInstance(toggle)?.show();
    }

    hideDropdown(toggle) {
        window.bootstrap?.Dropdown?.getOrCreateInstance(toggle)?.hide();
    }

    forceHideRecord(record) {
        this.hideDropdown(record.toggle);
        record.item.classList.remove('show');
        record.panel.classList.remove('show');
        record.toggle.classList.remove('show');
        record.toggle.setAttribute('aria-expanded', 'false');
    }
}

registry
    .category('public.interactions')
    .add('dorevia_ck_theme.ck_header_mega_menu_hover_bridge', CkHeaderMegaMenuHoverBridge);
