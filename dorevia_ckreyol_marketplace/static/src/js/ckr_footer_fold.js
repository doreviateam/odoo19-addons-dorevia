/** C-Kreyol : accordéons footer — ouverts en ≥992px, repliés sur mobile ; a11y : aria-expanded, desktop non repliable. */
(function () {
    "use strict";

    var mqDesktop = window.matchMedia("(min-width: 992px)");
    var detailsSelector = ".ckr-footer__fold";

    function refreshAccordionState() {
        var desktop = mqDesktop.matches;
        document.querySelectorAll(detailsSelector).forEach(function (detail) {
            var sum = detail.querySelector(".ckr-footer__fold-summary");
            if (desktop) {
                detail.open = true;
                if (sum) {
                    sum.setAttribute("aria-expanded", "true");
                    sum.tabIndex = -1;
                }
            } else {
                if (sum) {
                    sum.tabIndex = 0;
                    sum.setAttribute("aria-expanded", detail.open ? "true" : "false");
                }
            }
        });
    }

    function initDetails(detail) {
        if (detail.dataset.ckrFooterFoldInit) {
            return;
        }
        detail.dataset.ckrFooterFoldInit = "1";

        var sum = detail.querySelector(".ckr-footer__fold-summary");
        if (!sum) {
            return;
        }

        detail.addEventListener("toggle", function () {
            if (mqDesktop.matches) {
                if (!detail.open) {
                    detail.open = true;
                }
                sum.setAttribute("aria-expanded", "true");
                return;
            }
            sum.setAttribute("aria-expanded", detail.open ? "true" : "false");
        });
    }

    function init() {
        document.querySelectorAll(detailsSelector).forEach(initDetails);

        refreshAccordionState();

        if (mqDesktop.addEventListener) {
            mqDesktop.addEventListener("change", refreshAccordionState);
        } else if (mqDesktop.addListener) {
            mqDesktop.addListener(refreshAccordionState);
        }
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", init);
    } else {
        init();
    }
})();
