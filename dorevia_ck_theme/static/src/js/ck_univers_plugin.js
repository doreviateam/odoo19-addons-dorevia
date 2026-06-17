/** @odoo-module **/

import { Plugin } from "@html_editor/plugin";
import { registry } from "@web/core/registry";
import { isMediaElement } from "@html_editor/utils/dom_info";
import { selectElements } from "@html_editor/utils/dom_traversal";

/**
 * Rend les images des cards univers éditables individuellement dans le Website Builder
 * (pattern Odoo s_company_team_basic : img dans .o_not_editable).
 */
class CkUniversPlugin extends Plugin {
    static id = "ckUnivers";

    /** @type {import("plugins").WebsiteResources} */
    resources = {
        content_editable_providers: this.getEditableEls.bind(this),
    };

    getEditableEls(rootEl) {
        const contentEditableEls = [
            ...selectElements(rootEl, ".s_ck_univers_cards .o_not_editable *"),
        ];
        return contentEditableEls.filter(
            (el) => isMediaElement(el) || el.tagName === "IMG"
        );
    }
}

registry.category("website-plugins").add(CkUniversPlugin.id, CkUniversPlugin);
