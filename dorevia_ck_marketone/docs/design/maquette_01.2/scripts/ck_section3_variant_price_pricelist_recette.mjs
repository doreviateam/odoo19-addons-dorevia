import { chromium } from 'playwright';
import { mkdir, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const DB = 'dorevia_ck_marketone_01';
const ODOO = 'http://localhost:18079';
const SCRIPT_DIR = path.dirname(fileURLToPath(import.meta.url));
const OUT = process.env.CK_S3_PRICE_PL_RECETTE_OUT
    || path.join(SCRIPT_DIR, '..', 'captures', 'recette_section3_variant_price_pricelist');
const headers = { 'X-Odoo-Database': DB };

await mkdir(OUT, { recursive: true });

const browser = await chromium.launch({ headless: true });
const report = { checks: {}, verdict: 'KO' };

const context = await browser.newContext({ viewport: { width: 1280, height: 900 }, extraHTTPHeaders: headers });
const page = await context.newPage();

await page.goto(`${ODOO}/fr`, { waitUntil: 'networkidle', timeout: 60000 });
await page.waitForSelector('.ck-featured-products--maquette', { timeout: 30000 });

const homePrices = await page.evaluate(() => {
    const section = document.querySelector('.ck-featured-products--maquette');
    const cards = [...(section?.querySelectorAll('.ck-product-card') || [])];
    return cards.map((card) => {
        const title = card.querySelector('.product-card-title')?.textContent?.trim();
        const price = card.querySelector('.price')?.textContent?.replace(/\s+/g, ' ').trim();
        const variantId = card.querySelector('.card-cart-cta')?.dataset?.productId;
        const labels = card.querySelector('.product-card-labels')?.textContent?.replace(/\s+/g, ' ').trim();
        const priceOnly = card.querySelector('.product-card-pricing')?.textContent?.replace(/\s+/g, ' ').trim();
        return { title, price, variantId, labels, priceOnly };
    });
});

async function productPagePrice(url) {
    const p = await context.newPage();
    await p.goto(`${ODOO}${url}`, { waitUntil: 'networkidle', timeout: 60000 });
    const price = await p.evaluate(() => {
        const candidates = [
            document.querySelector('.oe_price .oe_currency_value'),
            document.querySelector('.product_price .oe_currency_value'),
            document.querySelector('[itemprop="price"]'),
        ].filter(Boolean);
        const node = candidates[0];
        return node?.textContent?.replace(/\s+/g, ' ').trim() || null;
    });
    await p.close();
    return price;
}

const saleCard = homePrices.find((c) => /sal/i.test(c.title || ''));
const sweetCard = homePrices.find((c) => /sucr/i.test(c.title || ''));

report.checks.home = homePrices;
report.checks.sale = saleCard;
report.checks.sweet = sweetCard;

if (saleCard?.variantId) {
    const saleLink = await page.locator(`[data-product-id="${saleCard.variantId}"]`)
        .locator('xpath=ancestor::article').locator('.card-cta--secondary, .card-cta').first();
    const href = await saleLink.getAttribute('href');
    report.checks.saleProductPagePrice = href ? await productPagePrice(href) : null;
}
if (sweetCard?.variantId) {
    const sweetLink = await page.locator(`[data-product-id="${sweetCard.variantId}"]`)
        .locator('xpath=ancestor::article').locator('.card-cta--secondary, .card-cta').first();
    const href = await sweetLink.getAttribute('href');
    report.checks.sweetProductPagePrice = href ? await productPagePrice(href) : null;
}

const okSale = saleCard?.price?.includes('3,60')
    && report.checks.saleProductPagePrice?.includes('3,60');
const okSweet = sweetCard?.price?.includes('3,50')
    && report.checks.sweetProductPagePrice?.includes('3,50');
const okRef = !saleCard?.labels || saleCard.labels.includes('36,00');

report.verdict = okSale && okSweet && okRef ? 'GO' : 'KO';
report.summary = { okSale, okSweet, okRef };

await page.screenshot({ path: path.join(OUT, 'section3_pricelist_home_1280.png'), fullPage: true });
await writeFile(path.join(OUT, 'recette_section3_variant_price_pricelist_report.json'), JSON.stringify(report, null, 2));
await context.close();
await browser.close();

console.log(JSON.stringify(report.summary, null, 2));
console.log('verdict:', report.verdict);
process.exit(report.verdict === 'GO' ? 0 : 1);
