import { chromium } from 'playwright';

const browser = await chromium.launch({ headless: true });

async function check(label, contextOpts, url, waitMs = 2000) {
  const ctx = await browser.newContext(contextOpts);
  const page = await ctx.newPage();
  await page.goto(url, { waitUntil: 'domcontentloaded', timeout: 60000 });
  await page.waitForTimeout(waitMs);
  const htmlCards = await page.content();
  const result = await page.evaluate(() => ({
    url: location.href,
    featured: !!document.querySelector('.s_ck_featured_products'),
    stableGrid: !!document.querySelector('.ck-featured-products__grid--stable'),
    dynamicJs: !!document.querySelector('.s_dynamic_snippet_products'),
    cards: document.querySelectorAll('.o_carousel_product_card').length,
    images: document.querySelectorAll('.ck-featured-products__grid--stable img, .ck-featured-products__grid--stable .oe_product_image_img').length,
    links: [...new Set([...document.querySelectorAll('.ck-featured-products__grid--stable a[href*="/shop/"]')].map(a => a.getAttribute('href')))],
  }));
  result.htmlCardCount = (htmlCards.match(/o_carousel_product_card/g) || []).length;
  console.log(label, JSON.stringify(result));
  await ctx.close();
}

// SSR visible sans attendre hydratation JS
await check('header-immediate', {
  extraHTTPHeaders: { 'X-Odoo-Database': 'dorevia_ck_marketone_01' },
  viewport: { width: 1280, height: 900 },
}, 'http://localhost:18079/', 500);

const ctx = await browser.newContext();
const page = await ctx.newPage();
await page.goto('http://localhost:18079/web/database/selector', { waitUntil: 'networkidle' });
await page.locator('a[href*="dorevia_ck_marketone_01"]').first().click();
await page.waitForLoadState('networkidle');
await page.goto('http://localhost:18079/', { waitUntil: 'domcontentloaded' });
await page.waitForTimeout(500);
const moa = await page.evaluate(() => ({
  cards: document.querySelectorAll('.o_carousel_product_card').length,
  stableGrid: !!document.querySelector('.ck-featured-products__grid--stable'),
  title: document.querySelector('.s_ck_featured_products h2')?.textContent?.trim(),
}));
console.log('moa-db-selector-500ms', JSON.stringify(moa));
await ctx.close();

await browser.close();
