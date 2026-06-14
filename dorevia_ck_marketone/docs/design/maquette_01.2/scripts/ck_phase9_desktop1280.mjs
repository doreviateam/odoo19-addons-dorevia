import { chromium } from 'playwright';

const DB = 'dorevia_ck_marketone_01';
const BASE = 'http://localhost:18079';
const headers = { 'X-Odoo-Database': DB };

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({ viewport: { width: 1280, height: 900 }, extraHTTPHeaders: headers });
const page = await context.newPage();

async function inspectNewsletter(path) {
  await page.goto(`${BASE}${path}?db=${DB}`, { waitUntil: 'networkidle', timeout: 45000 });
  await page.waitForTimeout(1000);
  return page.evaluate(() => ({
    url: location.pathname,
    scrollWidth: document.documentElement.scrollWidth,
    clientWidth: document.documentElement.clientWidth,
    dualCompact: !!document.querySelector('.ck-dual-engage--compact'),
    newsletterBlock: !!document.querySelector('#ck-newsletter-subscribe'),
    subscribeInput: !!document.querySelector('#ck-newsletter-subscribe input[type="email"], .s_newsletter_subscribe_form input[type="email"], .js_subscribe_email'),
    rgpdNote: document.body.textContent.includes('Désinscription possible'),
    listId: document.querySelector('[data-list-id]')?.getAttribute('data-list-id') || null,
  }));
}

const contact = await inspectNewsletter('/contactus');
const pro = await inspectNewsletter('/professionnels');

const separation = await page.evaluate(() => ({
  contactForm: !!document.getElementById('contactus_form'),
  proForm: !!document.getElementById('ck-pro-form'),
  newsletterSeparate: !!document.getElementById('ck-newsletter-subscribe'),
}));

const regression = {};
for (const [label, path] of [
  ['home', '/'],
  ['recipes', '/recettes'],
  ['shop', '/shop'],
  ['producer', '/producteur/atelier-hauts-goyaviers'],
]) {
  const resp = await page.goto(`${BASE}${path}?db=${DB}`, { waitUntil: 'domcontentloaded', timeout: 30000 });
  regression[label] = { status: resp?.status() ?? 0 };
}

console.log(JSON.stringify({ contact, pro, separation, regression }, null, 2));
await browser.close();
