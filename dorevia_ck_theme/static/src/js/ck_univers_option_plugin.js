/** @odoo-module **/

import { Plugin } from "@html_editor/plugin";
import { registry } from "@web/core/registry";
import { BaseWebsiteBackgroundOption } from "@website/builder/plugins/options/background_option";

/** Cards S4 — sélection éditeur individuelle (pattern CARD_PARENT_HANDLERS / carousel). */
export const CK_UNIVERS_CARD_SELECTOR =
    ".s_ck_univers_cards .ck-univers-cards__grid > .ck-univers-card";

class CkUniversCardBackgroundOption extends BaseWebsiteBackgroundOption {
    static selector = CK_UNIVERS_CARD_SELECTOR;
    static applyTo = ":scope > .ck-univers-card__media";
    static defaultProps = {
        withColors: false,
        withImages: true,
        withShapes: false,
        withColorCombinations: false,
        withVideos: false,
    };
}

class CkUniversOptionPlugin extends Plugin {
    static id = "ckUniversOption";

    /** @type {import("plugins").WebsiteResources} */
    resources = {
        no_parent_containers: CK_UNIVERS_CARD_SELECTOR,
        builder_options: [CkUniversCardBackgroundOption],
    };
}

registry.category("website-plugins").add(CkUniversOptionPlugin.id, CkUniversOptionPlugin);
