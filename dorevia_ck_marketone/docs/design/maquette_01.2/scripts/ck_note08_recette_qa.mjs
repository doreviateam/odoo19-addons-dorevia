/**
 * Recette MOA Note 08 — fiche produit CK V1.1
 * Usage: node ck_note08_recette_qa.mjs
 * Env: CK_BASE_URL, CK_DB, CK_MANIO_PATH, CK_SCREENSHOT=1
 */
import { chromium } from 'playwright';
import { mkdir, writeFile } from 'node:fs/promises';
import { join } from 'node:path';

const BASE = process.env.CK_BASE_URL || 'http://localhost:18079';
const DB = process.env.CK_DB || 'dorevia_ck_marketone_01';
const MANIO = process.env.CK_MANIO_PATH || '/shop/manio-crackers-1';
const OUT = process.env.CK_NOTE08_OUT || join(process.cwd(), '..', 'captures', 'note08_recette');
const headers = { 'X-Odoo-Database': DB };

async function auditProduct(page, width) {
    await page.setViewportSize({ width, height: 844 });
    await page.goto(`${BASE}${MANIO}?db=${DB}`, { waitUntil: 'networkidle', timeout: 90000 });
    await page.waitForSelector('.ck-product-page', { timeout: 30000 });
    return page.evaluate(() => {
        const doc = document.documentElement;
        const meta = document.querySelector('.ck-product-purchase__meta');
        const nav = document.querySelector('.ck-product-page__anchor-nav');
        const links = [...document.querySelectorAll('.ck-product-page__anchor-link')].map((a) => ({
            text: a.textContent.trim(),
            href: a.getAttribute('href'),
            active: a.classList.contains('is-active'),
        }));
        const variantPrices = [...document.querySelectorAll('.ck-product-purchase__variant-price')].map(
            (el) => el.textContent.trim(),
        );
        const deltaBadges = [...document.querySelectorAll('.variant_price_extra, .price_extra, .sign_badge_price_extra')]
            .filter((el) => el.offsetParent !== null)
            .map((el) => el.textContent.trim());
        const trust = document.querySelector('.ck-product-purchase__trust-list');
        const trustText = trust ? trust.textContent : '';
        return {
            overflow: doc.scrollWidth > doc.clientWidth + 1,
            scrollWidth: doc.scrollWidth,
            clientWidth: doc.clientWidth,
            hasCategoryChips: !!document.querySelector('.ck-product-purchase__chips'),
            hasH1: !!document.querySelector('h1.ck-product-purchase__title, .ck-product-purchase__head h1'),
            metaText: meta?.textContent?.trim() || '',
            metaHasProducerLink: !!meta?.querySelector('a[href="#ck-section-producer"]'),
            hasLead: !!document.querySelector('.ck-product-purchase__lead'),
            hasBadges: !!document.querySelector('.ck-product-purchase__badges'),
            hasAddToCart: !!document.querySelector('#add_to_cart'),
            hasWishlist: !!document.querySelector('.o_add_wishlist_dyn'),
            hasCompare: !!document.querySelector('.o_add_compare_dyn') && getComputedStyle(document.querySelector('.o_add_compare_dyn')).display !== 'none',
            trustText,
            anchorNavSticky: nav ? getComputedStyle(nav).position === 'sticky' : false,
            anchorLinks: links,
            anchorOrder: links.map((l) => l.text),
            variantPrices,
            deltaBadges,
            sections: [...document.querySelectorAll('.ck-product-page__block')].map((b) => b.id),
            producerSection: !!document.querySelector('#ck-section-producer'),
        };
    });
}

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({ extraHTTPHeaders: headers });
const page = await context.newPage();

const desktop = await auditProduct(page, 1280);
const mobile = await auditProduct(page, 390);

if (process.env.CK_SCREENSHOT === '1') {
    await mkdir(OUT, { recursive: true });
    await page.setViewportSize({ width: 1280, height: 800 });
    await page.goto(`${BASE}${MANIO}?db=${DB}`, { waitUntil: 'networkidle' });
    await page.screenshot({ path: join(OUT, 'note08_desktop1280_manio_variantes.png') });
    await page.setViewportSize({ width: 390, height: 844 });
    await page.goto(`${BASE}${MANIO}?db=${DB}`, { waitUntil: 'networkidle' });
    await page.screenshot({ path: join(OUT, 'note08_mobile390_zone_haute.png') });
    await page.locator('.ck-product-page__anchor-nav').scrollIntoViewIfNeeded().catch(() => {});
    await page.waitForTimeout(300);
    await page.screenshot({ path: join(OUT, 'note08_mobile390_ancres.png') });
}

await browser.close();

const ANCHOR_ORDER = ['Découvrir', 'Composition', 'Conservation', 'Infos pratiques', 'Producteur'];

function anchorOrderOk(order) {
    const present = ANCHOR_ORDER.filter((label) => order.includes(label));
    const indices = present.map((label) => order.indexOf(label));
    return indices.every((idx, i) => i === 0 || idx > indices[i - 1]);
}

const checks = {
    desktopNoOverflow: !desktop.overflow,
    mobileNoOverflow: !mobile.overflow,
    reassuranceOk: desktop.trustText.includes('En stock') && !/remboursement sous 30/i.test(desktop.trustText),
    compareHidden: !desktop.hasCompare,
    stickyNav: desktop.anchorNavSticky,
    noDeltaBadges: desktop.deltaBadges.length === 0,
    anchorOrderOk: anchorOrderOk(desktop.anchorOrder),
};

/** Informatif — dépend du seed contenu (réserve R3), hors gate pass/fail. */
const informational = {
    metaHasProducerLink: desktop.metaHasProducerLink,
    variantAbsolutePrices: desktop.variantPrices.length >= 1,
    producerSectionOk: desktop.producerSection,
};

const report = { desktop, mobile, checks, informational, pass: Object.values(checks).every(Boolean) };
await mkdir(OUT, { recursive: true });
await writeFile(join(OUT, 'note08_recette_results.json'), JSON.stringify(report, null, 2));
console.log(JSON.stringify(report, null, 2));
process.exit(report.pass ? 0 : 1);
