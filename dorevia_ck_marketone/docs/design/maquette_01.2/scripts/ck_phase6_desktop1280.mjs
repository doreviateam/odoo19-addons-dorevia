import { chromium } from 'playwright';

const DB = 'dorevia_ck_marketone_01';
const BASE = 'http://localhost:18079';
const PRODUCT = process.env.CK_CI_PRODUCT_PATH || process.env.CK_PRODUCT_PATH || '/shop/confiture-de-goyave-3';
const headers = { 'X-Odoo-Database': DB };

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({ viewport: { width: 1280, height: 900 }, extraHTTPHeaders: headers });
const page = await context.newPage();

await page.goto(`${BASE}/contactus?db=${DB}`, { waitUntil: 'networkidle', timeout: 45000 });
await page.waitForTimeout(1200);

const contact = await page.evaluate(() => ({
  url: location.pathname,
  scrollWidth: document.documentElement.scrollWidth,
  clientWidth: document.documentElement.clientWidth,
  ckContactPage: !!document.querySelector('.ck-contact-page'),
  form: !!document.querySelector('#contactus_form'),
  mailModel: !!document.querySelector('[data-model_name="mail.mail"]'),
  proLink: document.querySelectorAll('a[href="/professionnels"]').length,
  demoRemoved: !document.body.textContent.includes('Ma société') && !document.body.textContent.includes('Fake Buena Vista'),
  title: document.querySelector('h1')?.textContent?.trim().slice(0, 80) || null,
}));

await page.goto(`${BASE}/a-propos?db=${DB}`, { waitUntil: 'networkidle', timeout: 45000 });
await page.waitForTimeout(1200);

const about = await page.evaluate(() => ({
  url: location.pathname,
  scrollWidth: document.documentElement.scrollWidth,
  clientWidth: document.documentElement.clientWidth,
  ckAboutPage: !!document.querySelector('.ck-about-page'),
  mission: document.body.textContent.includes('Notre mission'),
  shopLink: !!document.querySelector('a[href="/shop"]'),
  proLink: !!document.querySelector('a[href="/professionnels"]'),
  contactLink: !!document.querySelector('a[href="/contactus"]'),
  title: document.querySelector('h1')?.textContent?.trim().slice(0, 80) || null,
}));

const regression = {};
for (const [label, path] of [
  ['home', '/'],
  ['shop', '/shop'],
  ['product', PRODUCT],
  ['pro', '/professionnels'],
  ['cart', '/shop/cart'],
]) {
  const resp = await page.goto(`${BASE}${path}?db=${DB}`, { waitUntil: 'domcontentloaded', timeout: 30000 });
  regression[label] = { status: resp?.status() ?? 0 };
}

console.log(JSON.stringify({ contact, about, regression }, null, 2));
await browser.close();
