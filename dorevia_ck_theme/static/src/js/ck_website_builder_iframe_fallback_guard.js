/** @odoo-module **/

/**
 * Garde-fou éditeur Website Odoo 19 — iframe fallback.
 *
 * Le noyau appelle `iframefallback.contentDocument.documentElement.replaceChildren()`
 * avant que l'iframe `/website/iframefallback` soit prête → TypeError en back-office.
 * Cf. website_builder_action.js · setIframeLoaded / cleanIframeFallback.
 */
import { patch } from "@web/core/utils/patch";
import { getScrollingElement } from "@web/core/utils/scrolling";
import { WebsiteBuilderClientAction } from "@website/client_actions/website_preview/website_builder_action";

patch(WebsiteBuilderClientAction.prototype, {
    setIframeLoaded() {
        this.iframeLoaded = new Promise((resolve) => {
            this.resolveIframeLoaded = () => {
                this.hotkeyService.registerIframe(this.websiteContent.el);
                this.websiteContent.el.contentWindow.addEventListener(
                    "beforeunload",
                    this.onPageUnload.bind(this)
                );

                this.addListeners(this.websiteContent.el.contentDocument);
                const fallbackRoot =
                    this.iframefallback.el?.contentDocument?.documentElement;
                if (fallbackRoot) {
                    fallbackRoot.replaceChildren();
                }
                resolve(this.websiteContent.el);
            };
        });
    },

    onPageUnload() {
        const websiteDoc = this.websiteContent.el?.contentDocument;
        const fallBackDoc = this.iframefallback.el?.contentDocument;
        if (
            !this.state.isEditing
            && websiteDoc?.documentElement
            && fallBackDoc?.documentElement
        ) {
            fallBackDoc.documentElement.replaceWith(
                websiteDoc.documentElement.cloneNode(true)
            );
            const currentScrollEl = getScrollingElement(websiteDoc);
            const scrollElement = getScrollingElement(fallBackDoc);
            scrollElement.scrollTop = currentScrollEl.scrollTop;
            this.cleanIframeFallback();
        }
    },

    cleanIframeFallback() {
        const fallbackDoc = this.iframefallback.el?.contentDocument;
        if (!fallbackDoc) {
            return;
        }
        const iframesEl = fallbackDoc.querySelectorAll(
            'iframe[src]:not([src=""])'
        );
        for (const iframeEl of iframesEl) {
            const url = new URL(iframeEl.src);
            url.searchParams.delete("autoplay");
            iframeEl.src = url.toString();
        }
    },
});
