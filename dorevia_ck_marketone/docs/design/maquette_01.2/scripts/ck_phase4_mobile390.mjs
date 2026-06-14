import { chromium } from 'playwright';

const DB = 'dorevia_ck_marketone_01';
const BASE = 'http://localhost:18079';
const PRODUCT = process.env.CK_CI_PRODUCT_PATH || process.env.CK_PRODUCT_PATH || '/shop/confiture-de-goyave-3';
const headers = { 'X-Odoo-Database': DB };

async function audit(path, width) {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({ viewport: { width, height: 844 }, extraHTTPHeaders: headers });
  const page = await context.newPage();
  await page.goto(`${BASE}${path}?db=${DB}`, { waitUntil: 'networkidle', timeout: 45000 });
  await page.waitForTimeout(1500);
  const result = await page.evaluate(() => ({
    path: location.pathname,
    scrollWidth: document.documentElement.scrollWidth,
    clientWidth: document.documentElement.clientWidth,
    overflow: document.documentElement.scrollWidth > document.documentElement.clientWidth,
    addToCart: !!document.querySelector('#add_to_cart'),
    price: !!document.querySelector('.product_price, .o_wsale_product_details_content_section_price'),
    description: !!document.querySelector('.ck-product-enrich, #product_full_description'),
  }));
  await browser.close();
  return result;
}

const product = await audit(PRODUCT, 390);
const shop = await audit('/shop', 390);
const home = await audit('/', 390);

console.log(JSON.stringify({ product, shop, home }, null, 2));
