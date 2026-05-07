/** @odoo-module **/

/** Hauteur header : voir `ckr_header_drawer.js` → `--ckr-header-measured`. */

const HERO_IMAGES = [
    "/dorevia_ckreyol_marketplace/static/src/img/hero_macro.png",
    "/dorevia_ckreyol_marketplace/static/src/img/hero_v2_immersive.png",
    "/dorevia_ckreyol_marketplace/static/src/img/hero_v3_epicerie.png",
    "/dorevia_ckreyol_marketplace/static/src/img/hero_v4_epices.png",
];

function preloadImage(url) {
    const image = new Image();
    image.src = url;
}

function setupHeroRotator(heroEl) {
    const mediaEl = heroEl.querySelector(".ckr-hero__media");
    if (!mediaEl) {
        return;
    }

    const layerA = mediaEl.querySelector(".ckr-hero__bg--layer-a");
    const layerB = mediaEl.querySelector(".ckr-hero__bg--layer-b");
    if (!layerA || !layerB) {
        return;
    }

    const interval = Number.parseInt(
        heroEl.dataset.ckrHeroRotateInterval || "60000",
        10
    );
    if (!Number.isFinite(interval) || interval < 10000) {
        return;
    }

    let currentIndex = 0;
    let activeLayer = layerA;
    let inactiveLayer = layerB;

    HERO_IMAGES.forEach(preloadImage);
    layerA.src = HERO_IMAGES[0];
    layerB.src = HERO_IMAGES[1 % HERO_IMAGES.length];

    window.setInterval(() => {
        const nextIndex = (currentIndex + 1) % HERO_IMAGES.length;
        const nextUrl = HERO_IMAGES[nextIndex];

        inactiveLayer.src = nextUrl;
        inactiveLayer.classList.add("is-active");
        activeLayer.classList.remove("is-active");

        currentIndex = nextIndex;
        const previousLayer = activeLayer;
        activeLayer = inactiveLayer;
        inactiveLayer = previousLayer;
    }, interval);
}

function initHeroRotators() {
    const heroes = document.querySelectorAll(".ckr-hero--immersive");
    heroes.forEach(setupHeroRotator);
}

if (document.readyState === "loading") {
    document.addEventListener("DOMContentLoaded", initHeroRotators, { once: true });
} else {
    initHeroRotators();
}
