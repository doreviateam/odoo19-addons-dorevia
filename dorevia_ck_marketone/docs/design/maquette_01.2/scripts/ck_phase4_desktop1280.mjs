import { chromium } from 'playwright';

const DB = 'dorevia_ck_marketone_01';
const BASE = 'http://localhost:18079';
const PRODUCT = process.env.CK_CI_PRODUCT_PATH || process.env.CK_PRODUCT_PATH || '/shop/confiture-de-goyave-3';
const headers = { 'X-Odoo-Database': DB };

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({ viewport: { width: 1280, height: 900 }, extraHTTPHeaders: headers });
const page = await context.newPage();

await page.goto(`${BASE}${PRODUCT}?db=${DB}`, { waitUntil: 'networkidle', timeout: 45000 });
await page.waitForTimeout(1500);
const product = await page.evaluate(() => ({
  url: location.pathname,
  scrollWidth: document.documentElement.scrollWidth,
  clientWidth: document.documentElement.clientWidth,
  ckProductPage: !!document.querySelector('.ck-product-page'),
  addToCart: !!document.querySelector('#add_to_cart'),
  price: !!document.querySelector('.product_price, .o_wsale_product_details_content_section_price'),
  qty: !!document.querySelector('input[name="add_qty"], .css_quantity input'),
  description: !!document.querySelector('.ck-product-enrich, #product_full_description, [itemprop="description"]'),
  proSignal: !!document.querySelector('.ck-product-pro-signal'),
  chips: document.querySelectorAll('.ck-chip').length,
  title: document.querySelector('h1, .o_wsale_product_details_content_section_title')?.textContent?.trim().slice(0, 80) || null,
}));

const regression = {};
for (const [label, path, needles] of [
  ['shop', '/shop', ['s_ck_shop_intro']],
  ['home', '/', ['ck-featured-products__grid--stable']],
  ['cart', '/shop/cart', []],
  ['professionnels', '/professionnels', []],
]) {
  const resp = await page.goto(`${BASE}${path}?db=${DB}`, { waitUntil: 'domcontentloaded', timeout: 30000 });
  regression[label] = { status: resp?.status() ?? 0, needles };
}

console.log(JSON.stringify({ product, regression }, null, 2));
await browser.close();
