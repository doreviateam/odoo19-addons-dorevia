/** Marketone — mesure hauteur navbar sticky (offset sidebar /shop). */
(function () {
    "use strict";

    function getHeader() {
        return document.querySelector("header#top.marketone-chrome");
    }

    function syncHeaderOffset() {
        const header = getHeader();
        if (!header) {
            return;
        }

        // Neutralise toute tentative de masquage inline résiduelle.
        header.style.transform = "none";
        header.style.opacity = "1";
        header.style.visibility = "visible";

        const offset = Math.ceil(
            header.getBoundingClientRect().height || header.offsetHeight || 0
        );
        if (offset > 0) {
            document.documentElement.style.setProperty(
                "--marketone-header-offset",
                offset + "px"
            );
        }
    }

    function initHeaderOffset() {
        const header = getHeader();
        if (!header) {
            return;
        }

        syncHeaderOffset();
        window.addEventListener("resize", syncHeaderOffset, { passive: true });
        window.addEventListener("orientationchange", syncHeaderOffset, {
            passive: true,
        });

        if (typeof ResizeObserver !== "undefined") {
            const ro = new ResizeObserver(syncHeaderOffset);
            ro.observe(header);
        }
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", initHeaderOffset);
    } else {
        initHeaderOffset();
    }
})();
