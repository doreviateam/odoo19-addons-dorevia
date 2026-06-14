import { chromium } from 'playwright';

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({
  viewport: { width: 390, height: 844 },
  extraHTTPHeaders: { 'X-Odoo-Database': 'dorevia_ck_marketone_01' },
});
const page = await context.newPage();
await page.goto('http://localhost:18079/?db=dorevia_ck_marketone_01', { waitUntil: 'networkidle', timeout: 45000 });
await page.waitForTimeout(2000);

const result = await page.evaluate(() => {
  const metrics = {
    scrollWidth: document.documentElement.scrollWidth,
    clientWidth: document.documentElement.clientWidth,
  };
  const order = ['.s_ck_hero', '.s_ck_reassurance', '.s_ck_featured_products', '.s_ck_category_links', '.ck-dual-engage', '.s_ck_pro_banner']
    .filter((s) => document.querySelector(s))
    .map((s) => s.slice(1));
  const productLinks = [...document.querySelectorAll('a[href*="/shop/"]')]
    .map((a) => a.getAttribute('href'))
    .filter((h) => h && /^\/shop\/[^/]+-\d+$/.test(h));
  return {
    metrics,
    order,
    productLinks: [...new Set(productLinks)],
    productCards: document.querySelectorAll('.o_carousel_product_card, .oe_product').length,
    proLinks: document.querySelectorAll('a[href="/professionnels"]').length,
  };
});

console.log(JSON.stringify(result, null, 2));
await browser.close();
