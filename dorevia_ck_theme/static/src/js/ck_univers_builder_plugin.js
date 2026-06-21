/** @odoo-module **/

import { Plugin } from "@html_editor/plugin";
import { closestElement } from "@html_editor/utils/dom_traversal";
import { registry } from "@web/core/registry";

const UNIVERS_IMG_SELECTOR =
    ".s_ck_univers_cards .ck-univers-card__img.o_editable_media";
const UNIVERS_TEXT_SELECTOR =
    ".s_ck_univers_cards .ck-univers-card__title.o_editable, .s_ck_univers_cards .ck-univers-card__desc.o_editable";

/**
 * Force la prise de focus Builder sur les cards S4 (média + textes inline).
 * Complète o_editable_selectors / layout éditeur — seul le CSS ne suffit pas
 * avec l'overlay empilé en mode public.
 */
class CkUniversBuilderPlugin extends Plugin {
    static id = "ckUniversBuilder";
    static dependencies = ["builderOptions", "media", "operation"];

    setup() {
        const doc = this.editable.ownerDocument;
        this._onClickCapture = this._onClickCapture.bind(this);
        doc.addEventListener("click", this._onClickCapture, { capture: true });
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
        const img = ev.target.closest(UNIVERS_IMG_SELECTOR);
        if (img) {
            ev.preventDefault();
            ev.stopPropagation();
            await this.dependencies.operation.next(async () => {
                this.dependencies.builderOptions.updateContainers(img, { forceUpdate: true });
                const editableEl =
                    closestElement(img, ".o_editable") || this.editable;
                await this.dependencies.media.openMediaDialog({ node: img }, editableEl);
            });
            return;
        }
        const text = ev.target.closest(UNIVERS_TEXT_SELECTOR);
        if (text) {
            ev.preventDefault();
            ev.stopPropagation();
            this.dependencies.builderOptions.updateContainers(text, { forceUpdate: true });
            if (text.isContentEditable) {
                text.focus();
                const selection = text.ownerDocument.getSelection();
                const range = text.ownerDocument.createRange();
                range.selectNodeContents(text);
                range.collapse(false);
                selection.removeAllRanges();
                selection.addRange(range);
            }
        }
    }
}

registry.category("website-plugins").add(CkUniversBuilderPlugin.id, CkUniversBuilderPlugin);
