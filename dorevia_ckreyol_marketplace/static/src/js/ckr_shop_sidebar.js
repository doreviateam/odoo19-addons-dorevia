/** C-Kreyol — sidebar boutique /shop : cases à cocher (maquette §4). */
(function () {
    "use strict";

    const COLLECTIONS_BASE = "/collections";

    function collectionApply() {
        const boxes = document.querySelectorAll(
            "input.ckr-sidebar-collection-check[type='checkbox']"
        );
        if (!boxes.length) {
            return;
        }
        const checked = [
            ...new Set(
                Array.from(boxes)
                    .filter((b) => b.checked)
                    .map((b) => b.dataset.slug)
                    .filter(Boolean)
            ),
        ].sort();
        if (checked.length === 0) {
            window.location.href = COLLECTIONS_BASE;
            return;
        }
        if (checked.length === 1) {
            window.location.href =
                COLLECTIONS_BASE + "/" + encodeURIComponent(checked[0]);
            return;
        }
        window.location.href =
            COLLECTIONS_BASE +
            "/union/" +
            checked.map((s) => encodeURIComponent(s)).join("/");
    }

    function originApply() {
        const boxes = document.querySelectorAll(
            "input.ckr-sidebar-origin-check[type='checkbox']"
        );
        if (!boxes.length) {
            return;
        }
        const params = new URLSearchParams(window.location.search);
        params.set("ckr_mode", "origin");
        params.delete("ckr_origin");
        Array.from(boxes)
            .filter((b) => b.checked)
            .forEach((b) => {
                if (b.dataset.slug) {
                    params.append("ckr_origin", b.dataset.slug);
                }
            });
        let path = window.location.pathname;
        if (path === "/collections" || path.startsWith("/collections/")) {
            path = "/shop";
        }
        const q = params.toString();
        window.location.href = path + (q ? "?" + q : "");
    }

    function categoryApply(ev) {
        const el = ev.target;
        if (!el.matches("input.ckr-sidebar-cat-check[type='checkbox']")) {
            return;
        }
        const allBoxes = document.querySelectorAll(
            "input.ckr-sidebar-cat-check[type='checkbox']"
        );
        const href = el.dataset.navHref;
        if (!href) {
            return;
        }
        if (el.classList.contains("ckr-sidebar-cat-all")) {
            if (el.checked) {
                allBoxes.forEach((o) => {
                    if (o !== el) {
                        o.checked = false;
                    }
                });
                window.location.href = href;
            } else {
                el.checked = true;
            }
            return;
        }
        if (el.checked) {
            allBoxes.forEach((o) => {
                if (o.classList.contains("ckr-sidebar-cat-all")) {
                    o.checked = false;
                } else if (o !== el) {
                    o.checked = false;
                }
            });
            window.location.href = href;
        } else {
            allBoxes.forEach((o) => {
                if (o.classList.contains("ckr-sidebar-cat-all")) {
                    o.checked = true;
                } else {
                    o.checked = false;
                }
            });
            const all = document.querySelector(".ckr-sidebar-cat-all");
            if (all && all.dataset.navHref) {
                window.location.href = all.dataset.navHref;
            }
        }
    }

    function collectionChange(ev) {
        if (ev.target.matches("input.ckr-sidebar-collection-check[type='checkbox']")) {
            collectionApply();
        }
    }

    function originChange(ev) {
        if (ev.target.matches("input.ckr-sidebar-origin-check[type='checkbox']")) {
            originApply();
        }
    }

    function init() {
        document.body.addEventListener("change", categoryApply);
        document.body.addEventListener("change", collectionChange);
        document.body.addEventListener("change", originChange);
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", init);
    } else {
        init();
    }
})();
