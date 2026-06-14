import { chromium } from 'playwright';

const DB = 'dorevia_ck_marketone_01';
const BASE = 'http://localhost:18079';
const PRODUCT = process.env.CK_CI_PRODUCT_PATH || process.env.CK_PRODUCT_PATH || '/shop/confiture-de-goyave-3';
const headers = { 'X-Odoo-Database': DB };

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({ viewport: { width: 1280, height: 900 }, extraHTTPHeaders: headers });
const page = await context.newPage();

await page.goto(`${BASE}/professionnels?db=${DB}`, { waitUntil: 'networkidle', timeout: 45000 });
await page.waitForTimeout(1500);

const pro = await page.evaluate(() => ({
  url: location.pathname,
  scrollWidth: document.documentElement.scrollWidth,
  clientWidth: document.documentElement.clientWidth,
  ckProPage: !!document.querySelector('.ck-pro-page'),
  form: !!document.querySelector('#ck-pro-form'),
  crmModel: !!document.querySelector('[data-model_name="crm.lead"]'),
  description: !!document.querySelector('[name="description"]'),
  producteur: document.body.textContent.includes('Producteur'),
  fournisseur: document.body.textContent.includes('fournisseur'),
  distributeur: document.body.textContent.includes('distributeur'),
  boutique: /Boutiques|CHR/.test(document.body.textContent),
  title: document.querySelector('h1')?.textContent?.trim().slice(0, 80) || null,
  ctaForm: document.querySelectorAll('a[href="#ck-pro-form"]').length,
}));

const regression = {};
for (const [label, path] of [
  ['home', '/'],
  ['shop', '/shop'],
  ['product', PRODUCT],
  ['cart', '/shop/cart'],
]) {
  const resp = await page.goto(`${BASE}${path}?db=${DB}`, { waitUntil: 'domcontentloaded', timeout: 30000 });
  regression[label] = { status: resp?.status() ?? 0 };
}

console.log(JSON.stringify({ pro, regression }, null, 2));
await browser.close();
