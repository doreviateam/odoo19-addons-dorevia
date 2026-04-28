/** C-Kreyol — sidebar boutique /shop : facettes multi-valeurs (OU intra-groupe). */
(function () {
    "use strict";

    const SHOP_FALLBACK = "/shop";
    const COLLECTION_PARAM = "ckr_collection";
    const COLLECTION_SCOPE_PARAM = "ckr_collection_scope";
    const CATEGORY_PARAM = "ckr_category";
    const INIT_DATA_ATTR = "data-ckr-shop-sidebar-js";

    /** Préfixe boutique depuis la barre d’URL (ex. ``/fr/shop``), fiable si les nœuds QWeb porteurs de ``shop_path`` sont absents (recherche, thème). */
    function shopBaseFromPathname() {
        const p = window.location.pathname || "";
        const m = p.match(/^(.*?\/shop)(?=\/|$)/);
        if (!m) {
            return null;
        }
        const base = (m[1] || "").replace(/\/$/, "");
        return base || null;
    }

    function normSlug(s) {
        return (s || "").trim().toLowerCase();
    }

    function getCkrShopBase() {
        const fromPath = shopBaseFromPathname();
        if (fromPath) {
            return fromPath;
        }
        const nav = document.querySelector("nav.ckr-shop-shortcuts");
        let raw = nav && nav.getAttribute("data-ckr-shop-base");
        if (!raw || !raw.trim()) {
            const holder = document.querySelector(
                ".ckr-js-shop-base[data-ckr-shop-base], .ckr-shop-sidebar-ck[data-ckr-shop-base]"
            );
            raw = holder && holder.getAttribute("data-ckr-shop-base");
        }
        if (raw && raw.trim()) {
            return raw.replace(/\/$/, "");
        }
        return SHOP_FALLBACK;
    }

    function allCategoryAllInputs() {
        return document.querySelectorAll("input.ckr-sidebar-cat-all[type='checkbox']");
    }

    function allCategorySpecificInputs() {
        return document.querySelectorAll(
            "input.ckr-sidebar-cat-check:not(.ckr-sidebar-cat-all)[type='checkbox']"
        );
    }

    function categoryInputsForSlug(slug) {
        const n = normSlug(slug);
        return Array.from(allCategorySpecificInputs()).filter(
            (b) => normSlug(b.getAttribute("data-category-slug") || "") === n
        );
    }

    function allCollectionAllInputs() {
        return document.querySelectorAll("input.ckr-sidebar-collection-all[type='checkbox']");
    }

    function allCollectionSpecificInputs() {
        return document.querySelectorAll(
            "input.ckr-sidebar-collection-check:not(.ckr-sidebar-collection-all)[type='checkbox']"
        );
    }

    function collectionInputsForSlug(slug) {
        const n = normSlug(slug);
        return Array.from(allCollectionSpecificInputs()).filter(
            (b) => normSlug(b.getAttribute("data-slug") || "") === n
        );
    }

    function allOriginAllInputs() {
        return document.querySelectorAll("input.ckr-sidebar-origin-all[type='checkbox']");
    }

    function allOriginSpecificInputs() {
        return document.querySelectorAll(
            "input.ckr-sidebar-origin-check:not(.ckr-sidebar-origin-all)[type='checkbox']"
        );
    }

    function syncAllFallback(allNodes, specificNodes) {
        const allList = Array.from(allNodes || []);
        const specificList = Array.from(specificNodes || []);
        if (!allList.length) {
            return;
        }
        const anySpecific = specificList.some((b) => !!b.checked);
        allList.forEach((b) => {
            b.disabled = false;
            b.checked = !anySpecific;
        });
        specificList.forEach((b) => {
            b.disabled = false;
        });
    }

    function originInputsForSlug(slug) {
        const n = normSlug(slug);
        return Array.from(allOriginSpecificInputs()).filter(
            (b) => normSlug(b.getAttribute("data-slug") || "") === n
        );
    }

    function collectionApply() {
        const base = getCkrShopBase();
        const params = new URLSearchParams(window.location.search);
        params.delete(COLLECTION_PARAM);
        params.delete(COLLECTION_SCOPE_PARAM);
        const allBoxes = allCollectionAllInputs();
        const allBox = allBoxes[0];
        const specifics = allCollectionSpecificInputs();
        if (allBox && allBox.checked) {
            const q = params.toString();
            window.location.href = base + (q ? "?" + q : "");
            return;
        }
        const checkedSlugs = [
            ...new Set(
                Array.from(specifics)
                    .filter((b) => b.checked)
                    .map((b) => b.getAttribute("data-slug") || b.dataset.slug)
                    .filter(Boolean)
            ),
        ].sort();
        if (checkedSlugs.length === 0) {
            allBoxes.forEach((b) => {
                b.checked = true;
            });
            const q = params.toString();
            window.location.href = base + (q ? "?" + q : "");
            return;
        }
        checkedSlugs.forEach((s) => params.append(COLLECTION_PARAM, s));
        window.location.href = base + "?" + params.toString();
    }

    function collectionChange(ev) {
        if (
            ev.target.matches("input.ckr-sidebar-origin-check[type='checkbox']") ||
            ev.target.matches("input.ckr-sidebar-cat-check[type='checkbox']")
        ) {
            return;
        }
        if (!ev.target.matches("input.ckr-sidebar-collection-check[type='checkbox']")) {
            return;
        }
        const t = ev.target;
        const allBoxes = allCollectionAllInputs();
        const specifics = allCollectionSpecificInputs();
        if (t.classList.contains("ckr-sidebar-collection-all")) {
            if (t.checked) {
                specifics.forEach((b) => {
                    b.checked = false;
                });
                allBoxes.forEach((b) => {
                    b.checked = true;
                });
            } else {
                allBoxes.forEach((b) => {
                    b.checked = true;
                });
                return;
            }
        } else {
            const slug = t.getAttribute("data-slug") || "";
            const checked = t.checked;
            collectionInputsForSlug(slug).forEach((b) => {
                b.checked = checked;
            });
            if (checked) {
                allBoxes.forEach((b) => {
                    b.checked = false;
                });
            } else {
                const anySpec = Array.from(specifics).some((b) => b.checked);
                if (!anySpec) {
                    allBoxes.forEach((b) => {
                        b.checked = true;
                    });
                }
            }
        }
        collectionApply();
    }

    function originApply() {
        const base = getCkrShopBase();
        const allBoxes = allOriginAllInputs();
        const allBox = allBoxes[0];
        const specifics = allOriginSpecificInputs();
        const params = new URLSearchParams(window.location.search);
        params.delete("ckr_origin");
        const keepModes = params
            .getAll("ckr_mode")
            .filter((m) => String(m).toLowerCase() !== "origin");
        params.delete("ckr_mode");
        keepModes.forEach((m) => params.append("ckr_mode", m));
        if (allBox && allBox.checked) {
            const q = params.toString();
            window.location.href = base + (q ? "?" + q : "");
            return;
        }
        const originSlugs = [
            ...new Set(
                Array.from(specifics)
                    .filter((b) => b.checked)
                    .map((b) => b.getAttribute("data-slug") || b.dataset.slug)
                    .filter(Boolean)
            ),
        ].sort();
        if (originSlugs.length === 0) {
            allBoxes.forEach((b) => {
                b.checked = true;
            });
            const q = params.toString();
            window.location.href = base + (q ? "?" + q : "");
            return;
        }
        originSlugs.forEach((s) => params.append("ckr_origin", s));
        const q = params.toString();
        window.location.href = base + (q ? "?" + q : "");
    }

    function originChange(ev) {
        if (!ev.target.matches("input.ckr-sidebar-origin-check[type='checkbox']")) {
            return;
        }
        const t = ev.target;
        const allBoxes = allOriginAllInputs();
        const specifics = allOriginSpecificInputs();
        if (t.classList.contains("ckr-sidebar-origin-all")) {
            if (t.checked) {
                specifics.forEach((b) => {
                    b.checked = false;
                });
                allBoxes.forEach((b) => {
                    b.checked = true;
                });
            } else {
                allBoxes.forEach((b) => {
                    b.checked = true;
                });
                return;
            }
        } else {
            const slug = t.getAttribute("data-slug") || "";
            const checked = t.checked;
            originInputsForSlug(slug).forEach((b) => {
                b.checked = checked;
            });
            if (checked) {
                allBoxes.forEach((b) => {
                    b.checked = false;
                });
            } else {
                const anySpec = Array.from(specifics).some((b) => b.checked);
                if (!anySpec) {
                    allBoxes.forEach((b) => {
                        b.checked = true;
                    });
                }
            }
        }
        originApply();
    }

    function categoryApply() {
        const base = getCkrShopBase();
        const params = new URLSearchParams(window.location.search);
        params.delete(CATEGORY_PARAM);
        const allBoxes = allCategoryAllInputs();
        const allBox = allBoxes[0];
        const specifics = allCategorySpecificInputs();
        if (allBox && allBox.checked) {
            const q = params.toString();
            window.location.href = base + (q ? "?" + q : "");
            return;
        }
        const checkedSlugs = [
            ...new Set(
                Array.from(specifics)
                    .filter((b) => b.checked)
                    .map((b) => b.getAttribute("data-category-slug") || b.dataset.categorySlug)
                    .filter(Boolean)
            ),
        ].sort();
        if (checkedSlugs.length === 0) {
            allBoxes.forEach((b) => {
                b.checked = true;
            });
            const q = params.toString();
            window.location.href = base + (q ? "?" + q : "");
            return;
        }
        checkedSlugs.forEach((s) => params.append(CATEGORY_PARAM, s));
        window.location.href = base + "?" + params.toString();
    }

    function categoryChange(ev) {
        if (
            ev.target.matches("input.ckr-sidebar-collection-check[type='checkbox']") ||
            ev.target.matches("input.ckr-sidebar-origin-check[type='checkbox']")
        ) {
            return;
        }
        if (!ev.target.matches("input.ckr-sidebar-cat-check[type='checkbox']")) {
            return;
        }
        const t = ev.target;
        const allBoxes = allCategoryAllInputs();
        const specifics = allCategorySpecificInputs();
        if (t.classList.contains("ckr-sidebar-cat-all")) {
            if (t.checked) {
                specifics.forEach((b) => {
                    b.checked = false;
                });
                allBoxes.forEach((b) => {
                    b.checked = true;
                });
            } else {
                allBoxes.forEach((b) => {
                    b.checked = true;
                });
                return;
            }
        } else {
            const slug = t.getAttribute("data-category-slug") || "";
            const checked = t.checked;
            categoryInputsForSlug(slug).forEach((b) => {
                b.checked = checked;
            });
            if (checked) {
                allBoxes.forEach((b) => {
                    b.checked = false;
                });
            } else {
                const anySpec = Array.from(specifics).some((b) => b.checked);
                if (!anySpec) {
                    allBoxes.forEach((b) => {
                        b.checked = true;
                    });
                }
            }
        }
        categoryApply();
    }

    function init() {
        if (document.body.getAttribute(INIT_DATA_ATTR) === "1") {
            return;
        }
        document.body.setAttribute(INIT_DATA_ATTR, "1");
        // Régression-safe: si aucun item spécifique n'est coché, "Toutes" redevient
        // l'état visuel de base dès le chargement.
        syncAllFallback(allCategoryAllInputs(), allCategorySpecificInputs());
        syncAllFallback(allCollectionAllInputs(), allCollectionSpecificInputs());
        syncAllFallback(allOriginAllInputs(), allOriginSpecificInputs());
        document.body.addEventListener("change", categoryChange);
        document.body.addEventListener("change", collectionChange);
        document.body.addEventListener("change", originChange);
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", init);
    } else {
        init();
    }
})();
