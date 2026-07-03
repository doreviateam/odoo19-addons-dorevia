/**
 * Recette clôture CK-HOME-001B — Home desktop 1280 + mobile 390
 * Usage: node ck_home_001b_cloture_recette.mjs
 */
import { chromium } from 'playwright';
import { mkdir, writeFile } from 'node:fs/promises';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dir = dirname(fileURLToPath(import.meta.url));
const CAPTURES = join(__dir, '..', 'captures', 'recette_home_001b_cloture_20260703');
const DB = 'dorevia_ck_marketone_01';
const BASE = 'http://localhost:18079';
const headers = { 'X-Odoo-Database': DB, 'Accept-Language': 'fr-FR,fr;q=0.9' };

async function auditHome(page) {
    return page.evaluate(() => {
        const doc = document.documentElement;
        const html = document.body?.innerHTML || '';
        const featured = document.querySelector('.ck-featured-products');
        const featuredGrid = document.querySelector('.ck-featured-products__grid--stable');
        const imgs = featuredGrid
            ? [...featuredGrid.querySelectorAll('.ck-product-card__img')].map((img) => ({
                src: img.getAttribute('src') || '',
                visible: img.getBoundingClientRect().height > 0,
                height: Math.round(img.getBoundingClientRect().height),
            }))
            : [];
        const discovery = document.querySelector('.ck-discovery-pack');
        const discoveryChunk = discovery?.outerHTML || '';
        const cta = discovery?.querySelector('.ck-discovery-pack__cta');
        const ctaHref = cta?.getAttribute('href') || '';
        const blockOrder = [];
        for (const sel of [
            ['hero', '.ck-hero--marketone-v1'],
            ['reassurance', '.ck-reassurance--trust-bar, [data-snippet="s_ck_reassurance"]'],
            ['featured', '.ck-featured-products'],
            ['univers', '.ck-univers-cards, [data-snippet="s_ck_category_links"]'],
            ['coffret', '.ck-discovery-pack'],
            ['dual', '.ck-dual-engage, .s_ck_pro_banner'],
            ['editorial', '.ck-home-editorial'],
        ]) {
            const [name, q] = sel;
            const el = document.querySelector(q);
            if (el) blockOrder.push({ name, top: Math.round(el.getBoundingClientRect().top + window.scrollY) });
        }
        blockOrder.sort((a, b) => a.top - b.top);
        return {
            overflow: doc.scrollWidth > doc.clientWidth + 1,
            scrollWidth: doc.scrollWidth,
            clientWidth: doc.clientWidth,
            featuredPresent: !!featured,
            featuredImgCount: imgs.length,
            featuredImgsVisible: imgs.filter((i) => i.visible && i.height > 0).length,
            featuredImgs: imgs,
            noEditorialFallback: !html.includes('ck-discovery-pack__visual--editorial'),
            noStretchedLink: !discoveryChunk.includes('stretched-link'),
            discoveryVisualProduct: /\/web\/image\/product\./.test(discoveryChunk),
            discoveryStaticFallback: discoveryChunk.includes('ck_discovery_pack.jpg'),
            ctaHref,
            ctaPresent: !!cta,
            heroKicker: !!document.querySelector('.ck-hero--marketone-v1')?.textContent?.includes('Produits créoles'),
            heroTitle: document.querySelector('#hero-title, .ck-hero--marketone-v1 h1')?.textContent?.trim() || '',
            universCards: document.querySelectorAll('.ck-univers-card, .ck-univers-cards__grid a').length,
            universIntro: document.body.textContent.includes('Quatre univers'),
            dualPresent: !!document.querySelector('.ck-dual-engage, .s_ck_pro_banner'),
            newsletterOnHome: !!document.querySelector('.ck-dual-engage form.s_website_form') ||
                document.body.textContent.includes('Thanks for registering'),
            blockOrder: blockOrder.map((b) => b.name),
        };
    });
}

async function runViewport(browser, width, height, label) {
    const context = await browser.newContext({
        viewport: { width, height },
        extraHTTPHeaders: headers,
    });
    const page = await context.newPage();
    const url = `${BASE}/?db=${DB}`;
    const resp = await page.goto(url, { waitUntil: 'networkidle', timeout: 90000 });
    const status = resp?.status() ?? 0;

    await page.waitForSelector('.ck-featured-products', { timeout: 30000 });
    await page.waitForSelector('.ck-discovery-pack', { timeout: 30000 });

    const audit = await auditHome(page);

    await page.locator('.ck-featured-products').scrollIntoViewIfNeeded();
    await page.waitForTimeout(300);
    await page.screenshot({ path: join(CAPTURES, `home_${label}_vedettes.png`) });

    await page.locator('.ck-discovery-pack').scrollIntoViewIfNeeded();
    await page.waitForTimeout(300);
    await page.screenshot({ path: join(CAPTURES, `home_${label}_coffret.png`) });

    if (width <= 400) {
        await page.screenshot({ path: join(CAPTURES, `home_${label}_full.png`), fullPage: true });
    }

    await context.close();
    return { label, width, height, status, ...audit };
}

const browser = await chromium.launch({ headless: true });
await mkdir(CAPTURES, { recursive: true });

const kitsPage = await browser.newContext({ extraHTTPHeaders: headers });
const kitsCtx = await kitsPage.newPage();
const kitsResp = await kitsCtx.goto(`${BASE}/kits?db=${DB}`, { waitUntil: 'networkidle' });
const kitsFinal = kitsCtx.url();
await kitsPage.close();

const desktop = await runViewport(browser, 1280, 900, 'desktop_1280');
const mobile = await runViewport(browser, 390, 844, 'mobile_390');
await browser.close();

const results = {
    date: '2026-07-03',
    base: BASE,
    db: DB,
    kits: { status: kitsResp?.status(), finalUrl: kitsFinal },
    viewports: [desktop, mobile],
};
await writeFile(join(CAPTURES, 'recette_home_001b_cloture_results.json'), JSON.stringify(results, null, 2));
console.log(JSON.stringify(results, null, 2));
