/** C-Kreyol : carrousel Explorer — pas d’autoplay ; pas à pas (précédent / suivant), clavier ou rail natif. */
(function () {
    "use strict";

    function maxScrollLeft(viewport) {
        return Math.max(0, viewport.scrollWidth - viewport.clientWidth);
    }

    function pageDelta(viewport) {
        return viewport.clientWidth;
    }

    /**
     * Avance d’une « page » (largeur du viewport). En fin de rail : retour au début (instantané).
     */
    function scrollForward(viewport) {
        var w = pageDelta(viewport);
        var max = maxScrollLeft(viewport);
        if (max <= 2) {
            return;
        }
        var left = viewport.scrollLeft;
        if (left >= max - 2) {
            viewport.scrollTo({ left: 0, behavior: "auto" });
        } else {
            viewport.scrollTo({
                left: Math.min(left + w, max),
                behavior: "smooth",
            });
        }
    }

    /**
     * Recule d’une « page ». Au début du rail : saut en fin (instantané), miroir du bouton suivant.
     */
    function scrollBackward(viewport) {
        var w = pageDelta(viewport);
        var max = maxScrollLeft(viewport);
        if (max <= 2) {
            return;
        }
        var left = viewport.scrollLeft;
        if (left <= 2) {
            viewport.scrollTo({ left: max, behavior: "auto" });
        } else {
            viewport.scrollTo({
                left: Math.max(left - w, 0),
                behavior: "smooth",
            });
        }
    }

    function updateNavState(viewport, prev, next) {
        var max = maxScrollLeft(viewport);
        var stuck = max <= 2;
        if (prev) {
            prev.disabled = stuck;
            prev.setAttribute("aria-disabled", stuck ? "true" : "false");
        }
        if (next) {
            next.disabled = stuck;
            next.setAttribute("aria-disabled", stuck ? "true" : "false");
        }
    }

    function bindCarousel(wrap) {
        var viewport = wrap.querySelector(".ckr-entries__viewport");
        var prev = wrap.querySelector(".ckr-entries__nav--prev");
        var next = wrap.querySelector(".ckr-entries__nav--next");
        if (!viewport) {
            return;
        }

        if (prev) {
            prev.addEventListener("click", function () {
                scrollBackward(viewport);
            });
        }
        if (next) {
            next.addEventListener("click", function () {
                scrollForward(viewport);
            });
        }

        viewport.addEventListener("scroll", function () {
            updateNavState(viewport, prev, next);
        });

        viewport.addEventListener("keydown", function (ev) {
            if (ev.key === "ArrowLeft") {
                ev.preventDefault();
                scrollBackward(viewport);
            } else if (ev.key === "ArrowRight") {
                ev.preventDefault();
                scrollForward(viewport);
            }
        });

        window.addEventListener(
            "resize",
            function () {
                updateNavState(viewport, prev, next);
            },
            { passive: true }
        );

        window.requestAnimationFrame(function () {
            updateNavState(viewport, prev, next);
        });
    }

    function init() {
        document.querySelectorAll(".ckr-entries__carousel").forEach(bindCarousel);
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", init);
    } else {
        init();
    }
})();
