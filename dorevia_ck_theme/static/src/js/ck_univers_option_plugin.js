/** @odoo-module **/

import { Plugin } from "@html_editor/plugin";
import { registry } from "@web/core/registry";
import { BaseCardOption } from "@website/builder/plugins/options/card_option";

/** Cards S4 — sélection éditeur individuelle (pattern CARD_PARENT_HANDLERS). */
export const CK_UNIVERS_CARD_SELECTOR =
    ".s_ck_univers_cards .ck-univers-cards__grid > .ck-univers-card";

class CkUniversCardOption extends BaseCardOption {
    static selector = CK_UNIVERS_CARD_SELECTOR;
    static defaultProps = {
        disableWidth: true,
    };
}

class CkUniversOptionPlugin extends Plugin {
    static id = "ckUniversOption";

    /** @type {import("plugins").WebsiteResources} */
    resources = {
        no_parent_containers: CK_UNIVERS_CARD_SELECTOR,
        content_editable_selectors: [
            `${CK_UNIVERS_CARD_SELECTOR} .ck-univers-card__title`,
            `${CK_UNIVERS_CARD_SELECTOR} .ck-univers-card__desc`,
            `${CK_UNIVERS_CARD_SELECTOR} .o_not_editable img`,
        ],
        content_not_editable_selectors: `${CK_UNIVERS_CARD_SELECTOR} .o_not_editable`,
        builder_options: [CkUniversCardOption],
    };
}

registry.category("website-plugins").add(CkUniversOptionPlugin.id, CkUniversOptionPlugin);
