import { chromium } from 'playwright';
import { mkdir, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const DB = 'dorevia_ck_marketone_01';
const ODOO = 'http://localhost:18079';
const SCRIPT_DIR = path.dirname(fileURLToPath(import.meta.url));
const OUT = process.env.CK_S3_CTA_RECETTE_OUT
    || path.join(SCRIPT_DIR, '..', 'captures', 'recette_section3_cta_panier');
const headers = { 'X-Odoo-Database': DB };

await mkdir(OUT, { recursive: true });

const browser = await chromium.launch({ headless: true });
const report = { captures: [], checks: {}, verdict: 'KO' };

async function runViewport(label, width, height) {
    const context = await browser.newContext({
        viewport: { width, height },
        extraHTTPHeaders: headers,
    });
    const page = await context.newPage();
    await page.goto(`${ODOO}/fr`, { waitUntil: 'networkidle', timeout: 60000 });
    await page.waitForSelector('.ck-featured-products--maquette', { timeout: 30000 });

    const section = page.locator('.ck-featured-products--maquette');
    await section.scrollIntoViewIfNeeded();

    const metrics = await page.evaluate(() => {
        const sectionEl = document.querySelector('.ck-featured-products--maquette');
        const cards = [...(sectionEl?.querySelectorAll('.ck-product-card') || [])];
        const cardMetrics = cards.map((card) => {
            const cartBtn = card.querySelector('.card-cart-cta');
            const viewLink = card.querySelector('.card-cta--secondary, .card-cta');
            const cartRect = cartBtn?.getBoundingClientRect();
            const viewRect = viewLink?.getBoundingClientRect();
            return {
                title: card.querySelector('.product-card-title')?.textContent?.trim(),
                hasCartCta: !!cartBtn,
                hasViewCta: !!viewLink,
                cartIsButton: cartBtn?.tagName === 'BUTTON',
                cartAboveView: cartRect && viewRect ? cartRect.top <= viewRect.top : null,
                stacked: cartRect && viewRect
                    ? Math.abs(cartRect.left - viewRect.left) < 8 && viewRect.top > cartRect.bottom - 4
                    : null,
            };
        });

        return {
            scrollWidth: document.documentElement.scrollWidth,
            clientWidth: document.documentElement.clientWidth,
            overflow: document.documentElement.scrollWidth > document.documentElement.clientWidth + 1,
            cartCtaCount: sectionEl?.querySelectorAll('.card-cart-cta').length ?? 0,
            viewCtaCount: sectionEl?.querySelectorAll('.card-cta--secondary, .product-card-actions .card-cta').length ?? 0,
            cards: cardMetrics,
        };
    });

    if (label === '1280') {
        const cartBefore = await page.locator('.my_cart_quantity').first().textContent().catch(() => '0');
        const firstCart = page.locator('.ck-featured-products .card-cart-cta').first();
        await firstCart.click();
        await page.waitForTimeout(1500);
        const cartAfter = await page.locator('.my_cart_quantity').first().textContent().catch(() => '0');
        const dangerToast = await page.getByText(
            'Impossible d\'ajouter ce produit au panier',
            { exact: false }
        ).count();
        metrics.cartBefore = (cartBefore || '0').trim();
        metrics.cartAfter = (cartAfter || '0').trim();
        metrics.cartIncreased = parseInt(metrics.cartAfter, 10) > parseInt(metrics.cartBefore, 10);
        metrics.noDangerToastAfterCart = dangerToast === 0;
    }

    const shot = path.join(OUT, `section3_cta_panier_${label}.png`);
    await section.screenshot({ path: shot });
    report.captures.push({ label, width, height, shot });
    report.checks[label] = metrics;
    await context.close();
}

await runViewport('1280', 1280, 800);
await runViewport('390', 390, 844);
await browser.close();

const d = report.checks['1280'];
const m = report.checks['390'];
const okDesktop = d.cartCtaCount >= 3
    && d.cards.every((c) => c.hasCartCta && c.hasViewCta && c.cartIsButton)
    && d.cartIncreased
    && d.noDangerToastAfterCart;
const okMobile = m.cartCtaCount >= 3
    && !m.overflow
    && m.cards.every((c) => c.hasCartCta && (c.stacked || c.cartAboveView));

report.verdict = okDesktop && okMobile ? 'GO' : 'KO';
report.summary = { okDesktop, okMobile };

await writeFile(path.join(OUT, 'recette_section3_cta_panier_report.json'), JSON.stringify(report, null, 2));
console.log(JSON.stringify(report.summary, null, 2));
console.log('verdict:', report.verdict);
process.exit(report.verdict === 'GO' ? 0 : 1);
