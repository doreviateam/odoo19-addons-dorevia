/** @odoo-module **/

import { Plugin } from "@html_editor/plugin";
import { closestElement } from "@html_editor/utils/dom_traversal";
import { registry } from "@web/core/registry";

const HERO_IMG_SELECTOR =
    ".s_ck_hero .ck-hero__visual-media.o_editable_media";

/**
 * Force la prise de focus Builder sur chaque slide Hero (sélecteur média par image).
 */
class CkHeroBuilderPlugin extends Plugin {
    static id = "ckHeroBuilder";
    static dependencies = ["builderOptions", "media", "operation"];

    setup() {
        const doc = this.editable.ownerDocument;
        this._onClickCapture = this._onClickCapture.bind(this);
        doc.addEventListener("click", this._onClickCapture, { capture: true });
        this._pauseCarouselsInEditor();
    }

    _pauseCarouselsInEditor() {
        if (!this._isEditorEnabled()) {
            return;
        }
        for (const carousel of this.editable.querySelectorAll(
            ".s_ck_hero .ck-hero__visual-carousel"
        )) {
            carousel.removeAttribute("data-bs-ride");
            carousel.classList.add("ck-hero__visual-carousel--editor");
        }
    }

    destroy() {
        this.editable.ownerDocument.removeEventListener("click", this._onClickCapture, {
            capture: true,
        });
        super.destroy();
    }

    _isEditorEnabled() {
        return this.editable.ownerDocument.body.classList.contains("editor_enable");
    }

    async _onClickCapture(ev) {
        if (!this._isEditorEnabled()) {
            return;
        }
        const img = ev.target.closest(HERO_IMG_SELECTOR);
        if (!img) {
            return;
        }
        ev.preventDefault();
        ev.stopPropagation();
        await this.dependencies.operation.next(async () => {
            this.dependencies.builderOptions.updateContainers(img, { forceUpdate: true });
            const editableEl =
                closestElement(img, ".o_editable") || this.editable;
            await this.dependencies.media.openMediaDialog({ node: img }, editableEl);
        });
    }
}

registry.category("website-plugins").add(CkHeroBuilderPlugin.id, CkHeroBuilderPlugin);
