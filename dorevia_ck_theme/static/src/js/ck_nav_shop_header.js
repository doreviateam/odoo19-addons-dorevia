/** @odoo-module **/

import { Interaction } from '@web/public/interaction';
import { registry } from '@web/core/registry';

/**
 * Nav-Shop — menu overflow Odoo :
 * - survol pour ouvrir les sous-menus L2 (exclu par HoverableDropdown core) ;
 * - clic toggle sans fermer le menu parent.
 */
export class CkNavShopExtraMenu extends Interaction {
    static selector = 'header.ck-header';

    setup() {
        this.onExtraMenuClick = this.onExtraMenuClick.bind(this);
        this.bindExtraMenuDropdowns();
        this.extraMenuObserver = new MutationObserver(() => this.bindExtraMenuDropdowns());
        const topMenu = this.el.querySelector('#top_menu');
        if (topMenu) {
            this.extraMenuObserver.observe(topMenu, { childList: true, subtree: true });
        }
    }

    destroy() {
        this.extraMenuObserver?.disconnect();
        this._extraMenuCleanups?.forEach((fn) => fn());
        super.destroy();
    }

    _getDropdown(toggle) {
        const Dropdown = window.Dropdown ?? window.bootstrap?.Dropdown;
        return Dropdown?.getOrCreateInstance(toggle);
    }

    bindExtraMenuDropdowns() {
        this._extraMenuCleanups?.forEach((fn) => fn());
        this._extraMenuCleanups = [];
        if (window.matchMedia('(max-width: 991.98px)').matches) {
            return;
        }
        const extraRoot = this.el.querySelector('.o_extra_menu_items');
        if (!extraRoot) {
            return;
        }
        extraRoot.querySelectorAll('.dropdown-menu .dropdown').forEach((dropdownEl) => {
            const toggle = dropdownEl.querySelector('.dropdown-toggle');
            if (!toggle) {
                return;
            }
            const onEnter = () => {
                this._getDropdown(toggle)?.show();
            };
            const onLeave = () => {
                this._getDropdown(toggle)?.hide();
            };
            dropdownEl.addEventListener('mouseenter', onEnter);
            dropdownEl.addEventListener('mouseleave', onLeave);
            toggle.addEventListener('click', this.onExtraMenuClick, true);
            this._extraMenuCleanups.push(() => {
                dropdownEl.removeEventListener('mouseenter', onEnter);
                dropdownEl.removeEventListener('mouseleave', onLeave);
                toggle.removeEventListener('click', this.onExtraMenuClick, true);
            });
        });
    }

    onExtraMenuClick(ev) {
        const toggle = ev.target.closest('.o_extra_menu_items .dropdown-menu .dropdown-toggle');
        if (!toggle) {
            return;
        }
        ev.preventDefault();
        ev.stopPropagation();
        this._getDropdown(toggle)?.toggle();
    }
}

registry
    .category('public.interactions')
    .add('dorevia_ck_theme.ck_nav_shop_extra_menu', CkNavShopExtraMenu);
