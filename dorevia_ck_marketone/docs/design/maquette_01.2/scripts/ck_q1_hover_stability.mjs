import { chromium } from 'playwright';

const browser = await chromium.launch({ headless: true });
const ctx = await browser.newContext({
  viewport: { width: 1280, height: 900 },
  extraHTTPHeaders: { 'X-Odoo-Database': 'dorevia_ck_marketone_01' },
});
const page = await ctx.newPage();
await page.goto('http://localhost:18079/', { waitUntil: 'networkidle' });
await page.locator('.ck-featured-products__grid--stable').scrollIntoViewIfNeeded();

const heights = [];
for (const card of await page.locator('.ck-featured-products__grid--stable .o_carousel_product_card').all()) {
  await card.hover();
  await page.waitForTimeout(200);
  heights.push(await page.evaluate(() => ({
    grid: document.querySelector('.ck-featured-products__grid--stable')?.getBoundingClientRect().height,
    cards: [...document.querySelectorAll('.ck-featured-products__grid--stable .o_carousel_product_card')].map(c => c.getBoundingClientRect().height),
  })));
}

const gridStable = heights.every(h => h.grid === heights[0].grid);
const cardsStable = heights.every(h => JSON.stringify(h.cards) === JSON.stringify(heights[0].cards));
console.log(JSON.stringify({ gridStable, cardsStable, heights }, null, 2));
await browser.close();
