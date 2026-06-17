/** @odoo-module **/

import { browser } from "@web/core/browser/browser";
import { registry } from "@web/core/registry";
import { Interaction } from "@web/public/interaction";

/**
 * Navigation catalogue S4 — clic sur la card (hors CTA) en mode public uniquement.
 */
export class CkUniversCardNav extends Interaction {
    static selector = ".s_ck_univers_cards .ck-univers-card[data-href]";

    dynamicContent = {
        _root: { "t-on-click": this.onCardClick },
    };

    onCardClick(ev) {
        if (document.body.classList.contains("editor_enable")) {
            return;
        }
        if (ev.target.closest("a")) {
            return;
        }
        const href = this.el.dataset.href;
        if (href) {
            browser.location.assign(href);
        }
    }
}

registry.category("public.interactions").add("ck_univers_card_nav", CkUniversCardNav);
