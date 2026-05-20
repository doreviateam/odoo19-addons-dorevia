/** Marketone — sidebar /shop : facettes catalogue (catégories, collections, attributs, prix). */
(function () {
    "use strict";

    const SHOP_FALLBACK = "/shop";
    const CATEGORY_PARAM = "marketone_category";
    const COLLECTION_PARAM = "marketone_collection";
    const INIT_ATTR = "data-marketone-shop-sidebar-js";

    const PRESERVE_SINGLE = [
        "search",
        "order",
        "marketone_mode",
        "min_price",
        "max_price",
        "noFuzzy",
    ];

    const PRESERVE_MULTI = [
        "marketone_category",
        "marketone_collection",
        "marketone_origin",
    ];

    /** Racine Lot 3 : `marketone-shop` sur `#wrap`, pas sur `.oe_website_sale`. */
    function getMarketoneShopRoot() {
        return (
            document.querySelector("#wrap.marketone-shop") ||
            document.querySelector(".marketone-shop")
        );
    }

    function isMarketoneShop() {
        const root = getMarketoneShopRoot();
        return !!(root && root.querySelector(".oe_website_sale"));
    }

    function shopBaseFromPathname() {
        const match = (window.location.pathname || "").match(/^(.*?\/shop)(?=\/|$)/);
        if (!match) {
            return null;
        }
        return (match[1] || "").replace(/\/$/, "") || null;
    }

    function getShopBase() {
        return shopBaseFromPathname() || SHOP_FALLBACK;
    }

    function categoryInputs() {
        const root = getMarketoneShopRoot();
        const scope = root || document;
        return scope.querySelectorAll(
            "input.marketone-sidebar-cat-check[type='checkbox']"
        );
    }

    function collectionInputs() {
        const root = getMarketoneShopRoot();
        const scope = root || document;
        return scope.querySelectorAll(
            "input.marketone-sidebar-col-check[type='checkbox']"
        );
    }

    function normSlug(value) {
        return (value || "").trim().toLowerCase();
    }

    function inputsForSlug(slug, selector, attrName) {
        const want = normSlug(slug);
        const root = getMarketoneShopRoot();
        const scope = root || document;
        return Array.from(
            scope.querySelectorAll(selector)
        ).filter((node) => normSlug(node.getAttribute(attrName)) === want);
    }

    function getCheckedCategorySlugs() {
        return [
            ...new Set(
                Array.from(categoryInputs())
                    .filter((node) => node.checked)
                    .map((node) => node.getAttribute("data-category-slug"))
                    .filter(Boolean)
            ),
        ].sort();
    }

    function getCheckedCollectionSlugs() {
        return [
            ...new Set(
                Array.from(collectionInputs())
                    .filter((node) => node.checked)
                    .map((node) => node.getAttribute("data-collection-slug"))
                    .filter(Boolean)
            ),
        ].sort();
    }

    function copyPreservedParams(source, target, options = {}) {
        const skip = new Set(options.skip || []);
        for (const key of PRESERVE_SINGLE) {
            if (skip.has(key)) {
                continue;
            }
            const value = source.get(key);
            if (value !== null && value !== "") {
                target.set(key, value);
            }
        }
        for (const key of PRESERVE_MULTI) {
            if (skip.has(key)) {
                continue;
            }
            target.delete(key);
            source.getAll(key).forEach((value) => target.append(key, value));
        }
    }

    function appendCategorySlugs(params, slugs) {
        params.delete(CATEGORY_PARAM);
        slugs.forEach((slug) => params.append(CATEGORY_PARAM, slug));
    }

    function appendCollectionSlugs(params, slugs) {
        params.delete(COLLECTION_PARAM);
        slugs.forEach((slug) => params.append(COLLECTION_PARAM, slug));
    }

    function getShopAttributesForm() {
        const root = getMarketoneShopRoot();
        return root ? root.querySelector("form.js_attributes") : null;
    }

    function mergeAttributeFacetParams(params, current) {
        const form = getShopAttributesForm();
        if (form) {
            const facetParams = buildAttributeValuesParams(form);
            for (const [key, value] of facetParams.entries()) {
                if (key === "attribute_values") {
                    params.append(key, value);
                } else {
                    params.set(key, value);
                }
            }
            return;
        }
        current.getAll("attribute_values").forEach((value) => {
            params.append("attribute_values", value);
        });
        if (current.has("tags")) {
            params.set("tags", current.get("tags"));
        }
    }

    function buildAttributeValuesParams(form) {
        const params = new URLSearchParams();
        const attributeValues = new Map();
        const tags = new Set();
        form.querySelectorAll("input:checked, select").forEach((filter) => {
            if (!filter.value) {
                return;
            }
            if (filter.name === "attribute_value") {
                const parts = filter.value.split("-");
                if (parts.length !== 2) {
                    return;
                }
                const [attributeId, attributeValueId] = parts;
                const valueIds = attributeValues.get(attributeId) || new Set();
                valueIds.add(attributeValueId);
                attributeValues.set(attributeId, valueIds);
            } else if (filter.name === "tags") {
                tags.add(filter.value);
            }
        });
        for (const [attributeId, valueIds] of attributeValues.entries()) {
            params.append(
                "attribute_values",
                `${attributeId}-${[...valueIds].join(",")}`
            );
        }
        if (tags.size) {
            params.set("tags", [...tags].join(","));
        }
        return params;
    }

    function navigateShop(params) {
        const base = getShopBase();
        const query = params.toString();
        window.location.href = base + (query ? "?" + query : "");
    }

    function buildShopParamsFromSidebarFacets() {
        const params = new URLSearchParams();
        const current = new URLSearchParams(window.location.search);
        copyPreservedParams(current, params, {
            skip: [CATEGORY_PARAM, COLLECTION_PARAM, "attribute_values", "tags"],
        });
        mergeAttributeFacetParams(params, current);
        appendCategorySlugs(params, getCheckedCategorySlugs());
        appendCollectionSlugs(params, getCheckedCollectionSlugs());
        return params;
    }

    function buildShopParamsFromAttributeForm(form) {
        const params = buildAttributeValuesParams(form);
        const current = new URLSearchParams(window.location.search);
        copyPreservedParams(current, params, {
            skip: ["attribute_values", "tags", CATEGORY_PARAM, COLLECTION_PARAM],
        });
        appendCategorySlugs(params, getCheckedCategorySlugs());
        appendCollectionSlugs(params, getCheckedCollectionSlugs());
        return params;
    }

    function syncPriceRangeDataUrl() {
        if (!isMarketoneShop()) {
            return;
        }
        const params = buildShopParamsFromSidebarFacets();
        const base = getShopBase();
        const query = params.toString();
        const href = base + (query ? "?" + query : "");
        document
            .querySelectorAll(
                '.marketone-shop #o_wsale_price_range_option input[type="range"][data-url]'
            )
            .forEach((range) => {
                range.dataset.url = href;
            });
    }

    function sidebarFacetChange(ev, selector, attrName, buildParams) {
        if (!isMarketoneShop()) {
            return;
        }
        if (!ev.target.matches(selector)) {
            return;
        }
        const root = getMarketoneShopRoot();
        if (root && !root.contains(ev.target)) {
            return;
        }
        const target = ev.target;
        const slug = target.getAttribute(attrName) || "";
        inputsForSlug(slug, selector, attrName).forEach((node) => {
            node.checked = target.checked;
        });
        navigateShop(buildParams());
    }

    function categoryChange(ev) {
        sidebarFacetChange(
            ev,
            "input.marketone-sidebar-cat-check[type='checkbox']",
            "data-category-slug",
            buildShopParamsFromSidebarFacets
        );
    }

    function collectionChange(ev) {
        sidebarFacetChange(
            ev,
            "input.marketone-sidebar-col-check[type='checkbox']",
            "data-collection-slug",
            buildShopParamsFromSidebarFacets
        );
    }

    function attributeChange(ev) {
        if (!isMarketoneShop() || !getMarketoneShopRoot().contains(ev.target)) {
            return;
        }
        if (ev.target.name !== "attribute_value") {
            return;
        }
        const form = ev.target.closest("form.js_attributes");
        if (!form) {
            return;
        }
        ev.preventDefault();
        ev.stopPropagation();
        ev.stopImmediatePropagation();

        const productGrid = document.querySelector(
            ".o_wsale_products_grid_table_wrapper"
        );
        if (productGrid) {
            productGrid.classList.add("opacity-50");
        }
        navigateShop(buildShopParamsFromAttributeForm(form));
    }

    function getSidebarScrollRail() {
        const root = getMarketoneShopRoot();
        if (!root) {
            return null;
        }
        return root.querySelector(
            "#products_grid_before .marketone-sidebar-rail"
        );
    }

    /**
     * Scrollbar overlay custom + ombres haut/bas.
     *
     * Les pseudo-éléments ::-webkit-scrollbar ne supportent pas les CSS
     * custom properties, rendant impossible tout effet de survol fiable via CSS.
     * On cache la scrollbar native et on la remplace par deux div positionnés
     * en absolu dans l'aside — la visibilité est pilotée par CSS pur (:hover sur
     * #products_grid_before), la position/hauteur du thumb par JS.
     */
    function initSidebarScrollAffordance() {
        const rail = getSidebarScrollRail();
        if (!rail || rail.getAttribute("data-marketone-scroll-hints") === "1") {
            return;
        }
        if (!window.matchMedia("(min-width: 768px)").matches) {
            return;
        }
        rail.setAttribute("data-marketone-scroll-hints", "1");

        // La track est placée dans l'aside (pas dans le rail scrollant) pour rester fixe.
        const aside = rail.closest("#products_grid_before");
        if (!aside) {
            return;
        }

        const track = document.createElement("div");
        track.className = "marketone-sidebar-scrollbar";
        const thumb = document.createElement("div");
        thumb.className = "marketone-sidebar-scrollbar__thumb";
        track.appendChild(thumb);
        aside.appendChild(track);

        // Pixels correspondant au border-radius et au padding-bottom du rail CSS.
        const RAIL_RADIUS_PX = 12;
        const RAIL_PAD_BOTTOM_PX = 16;
        const TRACK_INSET_PX = 4; // depuis le bord droit intérieur du rail

        const updateTrackGeometry = () => {
            const rightFromAside =
                aside.offsetWidth - rail.offsetLeft - rail.offsetWidth + TRACK_INSET_PX;
            track.style.right = Math.max(rightFromAside, TRACK_INSET_PX) + "px";
            track.style.top = (rail.offsetTop + RAIL_RADIUS_PX) + "px";
            track.style.height =
                Math.max(rail.clientHeight - RAIL_RADIUS_PX - RAIL_PAD_BOTTOM_PX, 20) + "px";
        };

        const updateThumb = () => {
            const { scrollTop, scrollHeight, clientHeight } = rail;
            const overflow = scrollHeight > clientHeight + 2;

            rail.classList.toggle("marketone-sidebar-rail--overflow", overflow);
            rail.classList.toggle(
                "marketone-sidebar-rail--at-top",
                !overflow || scrollTop <= 4
            );
            rail.classList.toggle(
                "marketone-sidebar-rail--at-bottom",
                !overflow || scrollTop + clientHeight >= scrollHeight - 4
            );

            if (!overflow) {
                track.style.visibility = "hidden";
                return;
            }
            track.style.visibility = "";

            updateTrackGeometry();

            const trackH = parseFloat(track.style.height) || clientHeight;
            const ratio = clientHeight / scrollHeight;
            const thumbH = Math.max(ratio * trackH, 40);
            const maxOffset = trackH - thumbH;
            const offset =
                scrollHeight > clientHeight
                    ? (scrollTop / (scrollHeight - clientHeight)) * maxOffset
                    : 0;

            thumb.style.height = thumbH + "px";
            thumb.style.transform = "translateY(" + offset + "px)";
        };

        rail.addEventListener("scroll", updateThumb, { passive: true });

        if (typeof ResizeObserver !== "undefined") {
            const ro = new ResizeObserver(updateThumb);
            ro.observe(rail);
            Array.from(rail.querySelectorAll(".accordion-collapse")).forEach(
                (node) => ro.observe(node)
            );
        }
        window.addEventListener("resize", updateThumb, { passive: true });
        rail.addEventListener("shown.bs.collapse", updateThumb);
        rail.addEventListener("hidden.bs.collapse", updateThumb);
        updateThumb();
    }

    function init() {
        if (!isMarketoneShop()) {
            return;
        }
        if (document.body.getAttribute(INIT_ATTR) === "1") {
            syncPriceRangeDataUrl();
            initSidebarScrollAffordance();
            return;
        }
        document.body.setAttribute(INIT_ATTR, "1");
        document.body.addEventListener("change", categoryChange);
        document.body.addEventListener("change", collectionChange);
        document.body.addEventListener("change", attributeChange, true);
        syncPriceRangeDataUrl();
        initSidebarScrollAffordance();
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", init);
    } else {
        init();
    }
})();
