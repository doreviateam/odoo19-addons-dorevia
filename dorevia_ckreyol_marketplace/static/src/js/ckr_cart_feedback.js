/** C-Kreyol : feedback léger après ajout panier (sans mini-panier). */
(function () {
    "use strict";

    var TOAST_ID = "ckr_cart_feedback_toast";
    var pendingAdd = false;
    var lastQty = null;
    var resetTimer = null;

    function parseQty() {
        var badge = document.querySelector(".ckr-header__counter-badge");
        if (!badge) {
            return null;
        }
        var raw = (badge.textContent || "").trim();
        var n = parseInt(raw, 10);
        return Number.isNaN(n) ? null : n;
    }

    function getOrCreateToast() {
        var el = document.getElementById(TOAST_ID);
        if (el) {
            return el;
        }
        el = document.createElement("div");
        el.id = TOAST_ID;
        el.className = "ckr-cart-feedback";
        el.setAttribute("role", "status");
        el.setAttribute("aria-live", "polite");
        el.innerHTML = '<span class="ckr-cart-feedback__msg">Produit ajouté au panier.</span><a class="ckr-cart-feedback__link" href="/shop/cart">Voir le panier</a>';
        document.body.appendChild(el);
        return el;
    }

    function showToast() {
        var toast = getOrCreateToast();
        toast.classList.add("is-visible");
        window.clearTimeout(toast._hideTimer);
        toast._hideTimer = window.setTimeout(function () {
            toast.classList.remove("is-visible");
        }, 2600);
    }

    function markPendingAdd() {
        pendingAdd = true;
        window.clearTimeout(resetTimer);
        resetTimer = window.setTimeout(function () {
            pendingAdd = false;
        }, 3500);
    }

    function onQtyMaybeChanged() {
        var currentQty = parseQty();
        if (!pendingAdd) {
            lastQty = currentQty;
            return;
        }
        if (currentQty !== null && currentQty !== lastQty) {
            showToast();
            pendingAdd = false;
        }
        lastQty = currentQty;
    }

    function isAddToCartTrigger(target) {
        var btn = target.closest("button, a");
        if (!btn) {
            return false;
        }
        if (btn.matches("a.ckr-product-card__cart-btn--pdp")) {
            return false;
        }
        return btn.matches(
            "button.o_wsale_product_btn_primary, button#add_to_cart, a.js_add_cart_json, button.js_add_cart_json"
        );
    }

    function initObserver() {
        var badge = document.querySelector(".ckr-header__counter-badge");
        if (!badge) {
            return;
        }
        lastQty = parseQty();
        var observer = new MutationObserver(function () {
            onQtyMaybeChanged();
        });
        observer.observe(badge, {
            childList: true,
            characterData: true,
            subtree: true,
        });
    }

    function init() {
        initObserver();
        document.addEventListener("click", function (ev) {
            if (!isAddToCartTrigger(ev.target)) {
                return;
            }
            markPendingAdd();
            // Fallback léger : si le badge n'est pas présent, on montre un feedback direct.
            if (!document.querySelector(".ckr-header__counter-badge")) {
                showToast();
                pendingAdd = false;
            }
        });
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", init);
    } else {
        init();
    }
})();
