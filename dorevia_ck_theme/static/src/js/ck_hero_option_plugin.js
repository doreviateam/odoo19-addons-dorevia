/** @odoo-module **/

import { Plugin } from "@html_editor/plugin";
import { registry } from "@web/core/registry";

/** Slides carrousel Hero — sélection éditeur individuelle par visuel. */
export const CK_HERO_SLIDE_SELECTOR =
    ".s_ck_hero .ck-hero__visual-carousel .carousel-inner > .carousel-item";

const CK_HERO_MEDIA_SELECTOR = `${CK_HERO_SLIDE_SELECTOR} .ck-hero__slide-media`;

class CkHeroOptionPlugin extends Plugin {
    static id = "ckHeroOption";

    /** @type {import("plugins").WebsiteResources} */
    resources = {
        no_parent_containers: CK_HERO_SLIDE_SELECTOR,
        o_editable_selectors: [CK_HERO_MEDIA_SELECTOR],
        content_editable_selectors: [
            `${CK_HERO_SLIDE_SELECTOR} .o_not_editable img`,
        ],
        content_not_editable_selectors: [
            `${CK_HERO_SLIDE_SELECTOR} .o_not_editable`,
            ".s_ck_hero .ck-hero__visual-indicators",
        ],
        container_title: {
            selector: CK_HERO_SLIDE_SELECTOR,
        },
    };
}

registry.category("website-plugins").add(CkHeroOptionPlugin.id, CkHeroOptionPlugin);
