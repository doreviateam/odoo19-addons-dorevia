import { chromium } from 'playwright';

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({
  viewport: { width: 1280, height: 900 },
  extraHTTPHeaders: { 'X-Odoo-Database': 'dorevia_ck_marketone_01' },
});
const page = await context.newPage();
await page.goto('http://localhost:18079/?db=dorevia_ck_marketone_01', { waitUntil: 'networkidle', timeout: 45000 });
await page.waitForTimeout(2000);

const result = await page.evaluate(() => ({
  productCards: document.querySelectorAll('.o_carousel_product_card, .oe_product').length,
  productLinks: [...new Set([...document.querySelectorAll('a[href*="/shop/"]')]
    .map((a) => a.getAttribute('href'))
    .filter((h) => h && /^\/shop\/[^/]+-\d+$/.test(h)))],
  featured: !!document.querySelector('.s_ck_featured_products'),
  dynamicLoading: !!document.querySelector('.o_dynamic_snippet_loading'),
}));

console.log(JSON.stringify(result, null, 2));
await browser.close();
