import { chromium } from 'playwright';

const browser = await chromium.launch({ headless: true });
// MOA-like : sélecteur DB puis / (/?db= seul peut rediriger vers login)
const context = await browser.newContext({ viewport: { width: 1280, height: 900 } });
const page = await context.newPage();
const logs = [];
page.on('console', (m) => logs.push(m.type() + ': ' + m.text()));
page.on('pageerror', (e) => logs.push('PAGEERROR: ' + e.message));

await page.goto('http://localhost:18079/web/database/selector', { waitUntil: 'networkidle', timeout: 60000 });
await page.locator('a[href*="dorevia_ck_marketone_01"]').first().click();
await page.waitForLoadState('networkidle');
await page.goto('http://localhost:18079/', { waitUntil: 'domcontentloaded', timeout: 60000 });
await page.waitForTimeout(2000);

const result = await page.evaluate(() => ({
  url: location.href,
  featured: !!document.querySelector('.s_ck_featured_products'),
  stableGrid: !!document.querySelector('.ck-featured-products__grid--stable'),
  dynamic: !!document.querySelector('.s_dynamic_snippet_products'),
  loading: !!document.querySelector('.o_dynamic_snippet_loading'),
  cards: document.querySelectorAll('.o_carousel_product_card, .oe_product').length,
  images: document.querySelectorAll('.ck-featured-products__grid--stable img, .ck-featured-products__grid--stable .oe_product_image_img').length,
  templateHtml: document.querySelector('.ck-featured-products__grid--stable')?.innerHTML?.length || 0,
  productLinks: [...document.querySelectorAll('.ck-featured-products__grid--stable a[href*="/shop/"]')].map(a => a.getAttribute('href')).filter(h => h && /\/shop\/[^/]+-\d+$/.test(h)),
}));

console.log(JSON.stringify({ result, logs: logs.slice(0, 15) }, null, 2));
await browser.close();
