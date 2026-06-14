import { chromium } from 'playwright';

const DB = 'dorevia_ck_marketone_01';
const BASE = 'http://localhost:18079';
const PRODUCER = '/producteur/atelier-hauts-goyaviers';
const PRODUCT = process.env.CK_CI_PRODUCT_PATH || process.env.CK_PRODUCT_PATH || '/shop/confiture-de-goyave-3';
const headers = { 'X-Odoo-Database': DB };

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({ viewport: { width: 1280, height: 900 }, extraHTTPHeaders: headers });
const page = await context.newPage();

await page.goto(`${BASE}${PRODUCER}?db=${DB}`, { waitUntil: 'networkidle', timeout: 45000 });
await page.waitForTimeout(1200);

const producer = await page.evaluate(() => ({
  url: location.pathname,
  scrollWidth: document.documentElement.scrollWidth,
  clientWidth: document.documentElement.clientWidth,
  ckProducerPage: !!document.querySelector('.ck-producer-page'),
  products: !!document.querySelector('#ck-producer-products'),
  criteria: document.body.textContent.includes('Pourquoi CK sélectionne'),
  shopLink: !!document.querySelector('a[href="/shop"]'),
  contactLink: !!document.querySelector('a[href="/contactus"]'),
  proLink: !!document.querySelector('a[href="/professionnels"]'),
  title: document.querySelector('h1')?.textContent?.trim().slice(0, 80) || null,
}));

const regression = {};
for (const [label, path] of [
  ['home', '/'],
  ['shop', '/shop'],
  ['product', PRODUCT],
  ['contact', '/contactus'],
  ['about', '/a-propos'],
  ['pro', '/professionnels'],
  ['cart', '/shop/cart'],
]) {
  const resp = await page.goto(`${BASE}${path}?db=${DB}`, { waitUntil: 'domcontentloaded', timeout: 30000 });
  regression[label] = { status: resp?.status() ?? 0 };
}

console.log(JSON.stringify({ producer, regression }, null, 2));
await browser.close();
