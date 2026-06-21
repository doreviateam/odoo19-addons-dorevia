/**
 * Recette MOA — Fiche produit CK Lot 2 Option A · mobile 390 px
 * Usage: node ck_lot2_product_mobile390.mjs
 * Env: CK_SCREENSHOT=1 pour PNG dans ./captures/
 */
import { chromium } from 'playwright';
import { mkdir, writeFile } from 'node:fs/promises';
import { join } from 'node:path';

const DB = 'dorevia_ck_marketone_01';
const BASE = 'http://localhost:18079';
const PRODUCT = process.env.CK_PRODUCT_PATH || '/shop/confiture-de-goyave-3';
const WIDTH = 390;
const HEIGHT = 844;
const headers = { 'X-Odoo-Database': DB };

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({
    viewport: { width: WIDTH, height: HEIGHT },
    extraHTTPHeaders: headers,
});
const page = await context.newPage();
await page.goto(`${BASE}${PRODUCT}?db=${DB}`, { waitUntil: 'networkidle', timeout: 60000 });
await page.waitForSelector('.ck-product-page__long-zone', { timeout: 30000 });

const audit = await page.evaluate(() => {
    const doc = document.documentElement;
    const overflow = doc.scrollWidth > doc.clientWidth + 1;
    const anchorNav = document.querySelector('.ck-product-page__anchor-nav');
    const anchorRect = anchorNav?.getBoundingClientRect();
    const anchorLinks = [...document.querySelectorAll('.ck-product-page__anchor-link')].map((a) => ({
        text: a.textContent.trim(),
        width: a.getBoundingClientRect().width,
    }));
    const split = document.querySelector('.ck-product-page__section-split');
    const splitCols = split
        ? getComputedStyle(split).gridTemplateColumns.split(' ').filter(Boolean).length
        : 0;
    return {
        overflow,
        scrollWidth: doc.scrollWidth,
        clientWidth: doc.clientWidth,
        addToCartVisible: !!document.querySelector('#add_to_cart'),
        addToCartInViewport: (() => {
            const el = document.querySelector('#add_to_cart');
            if (!el) return false;
            const r = el.getBoundingClientRect();
            return r.top >= 0 && r.bottom <= window.innerHeight;
        })(),
        anchorNavPresent: !!anchorNav,
        anchorNavHeight: anchorRect?.height ?? 0,
        anchorLinkCount: anchorLinks.length,
        anchorLinks,
        longZonePresent: !!document.querySelector('.ck-product-page__long-zone'),
        conservationPanels: document.querySelectorAll('.ck-product-page__section-panel').length,
        conservationSingleColumn: splitCols <= 1,
        footerPresent: !!document.querySelector('footer#bottom, footer.o_footer'),
        blocks: [...document.querySelectorAll('.ck-product-page__block')].map((b) => b.id),
    };
});

if (process.env.CK_SCREENSHOT === '1') {
    const dir = join(process.cwd(), '..', 'captures', 'lot2_product_mobile390');
    await mkdir(dir, { recursive: true });
    await page.screenshot({ path: join(dir, '01_zone_haute.png') });
    await page.locator('.ck-product-page__anchor-nav').scrollIntoViewIfNeeded();
    await page.waitForTimeout(400);
    await page.screenshot({ path: join(dir, '02_bandeau_ancres.png') });
    const conservation = page.locator('#ck-section-conservation');
    if (await conservation.count()) {
        await conservation.scrollIntoViewIfNeeded();
        await page.waitForTimeout(400);
        await page.screenshot({ path: join(dir, '03_conservation.png') });
    }
    await page.evaluate(() => window.scrollTo(0, document.body.scrollHeight));
    await page.waitForTimeout(400);
    await page.screenshot({ path: join(dir, '04_footer.png') });
}

await browser.close();

const checks = {
    noOverflow: !audit.overflow,
    anchorNavOk: audit.anchorNavPresent && audit.anchorLinkCount >= 4,
    anchorNavCompact: audit.anchorNavHeight <= 120,
    longZoneOk: audit.longZonePresent,
    addToCartOk: audit.addToCartVisible,
    conservationSingleCol: audit.conservationSingleColumn,
    footerOk: audit.footerPresent,
    blocksOk: audit.blocks.length >= 4,
};

const pass = Object.values(checks).every(Boolean);

const report = { width: WIDTH, product: PRODUCT, audit, checks, pass };
console.log(JSON.stringify(report, null, 2));
process.exit(pass ? 0 : 1);
