/** Marketone — sidebar /shop : facettes catalogue (catégories, attributs, prix). */
(function () {
    "use strict";

    const SHOP_FALLBACK = "/shop";
    const CATEGORY_PARAM = "marketone_category";
    const INIT_ATTR = "data-marketone-shop-sidebar-js";

    const PRESERVE_SINGLE = [
        "search",
        "order",
        "marketone_mode",
        "min_price",
        "max_price",
        "noFuzzy",
    ];

    const PRESERVE_MULTI = ["marketone_category", "marketone_origin"];

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

    function normSlug(value) {
        return (value || "").trim().toLowerCase();
    }

    function inputsForSlug(slug) {
        const want = normSlug(slug);
        return Array.from(categoryInputs()).filter(
            (node) => normSlug(node.getAttribute("data-category-slug")) === want
        );
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

    function buildShopParamsFromCategories() {
        const params = new URLSearchParams();
        const current = new URLSearchParams(window.location.search);
        copyPreservedParams(current, params, {
            skip: [CATEGORY_PARAM, "attribute_values", "tags"],
        });
        mergeAttributeFacetParams(params, current);
        appendCategorySlugs(params, getCheckedCategorySlugs());
        return params;
    }

    function buildShopParamsFromAttributeForm(form) {
        const params = buildAttributeValuesParams(form);
        const current = new URLSearchParams(window.location.search);
        copyPreservedParams(current, params, {
            skip: ["attribute_values", "tags", CATEGORY_PARAM],
        });
        appendCategorySlugs(params, getCheckedCategorySlugs());
        return params;
    }

    function syncPriceRangeDataUrl() {
        if (!isMarketoneShop()) {
            return;
        }
        const params = buildShopParamsFromCategories();
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

    function categoryChange(ev) {
        if (!isMarketoneShop()) {
            return;
        }
        if (!ev.target.matches("input.marketone-sidebar-cat-check[type='checkbox']")) {
            return;
        }
        const root = getMarketoneShopRoot();
        if (root && !root.contains(ev.target)) {
            return;
        }
        const target = ev.target;
        const slug = target.getAttribute("data-category-slug") || "";
        inputsForSlug(slug).forEach((node) => {
            node.checked = target.checked;
        });
        navigateShop(buildShopParamsFromCategories());
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

    function init() {
        if (!isMarketoneShop()) {
            return;
        }
        if (document.body.getAttribute(INIT_ATTR) === "1") {
            syncPriceRangeDataUrl();
            return;
        }
        document.body.setAttribute(INIT_ATTR, "1");
        document.body.addEventListener("change", categoryChange);
        document.body.addEventListener("change", attributeChange, true);
        syncPriceRangeDataUrl();
    }

    if (document.readyState === "loading") {
        document.addEventListener("DOMContentLoaded", init);
    } else {
        init();
    }
})();
