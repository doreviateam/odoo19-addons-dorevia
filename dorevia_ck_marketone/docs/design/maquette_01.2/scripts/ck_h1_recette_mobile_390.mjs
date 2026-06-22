import { chromium } from 'playwright';
import { mkdirSync, writeFileSync } from 'fs';

const DB = 'dorevia_ck_marketone_01';
const BASE = 'http://localhost:18079';
const QA = 'h1';
const headers = { 'X-Odoo-Database': DB };
const OUT = new URL('../captures/recette_h1_v2_1/', import.meta.url).pathname;

mkdirSync(OUT, { recursive: true });

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({ viewport: { width: 390, height: 844 }, extraHTTPHeaders: headers });
const page = await context.newPage();

const results = {};

await page.goto(`${BASE}/?db=${DB}&qa_ts=${QA}`, { waitUntil: 'networkidle', timeout: 45000 });

results.M1_chrome = await page.evaluate(() => ({
  menuLabel: document.querySelector('button[data-bs-target="#top_menu_collapse_mobile"]')?.getAttribute('aria-label') || null,
  brand: document.querySelector('header .ck-header__brand')?.textContent?.trim() || null,
  searchBtn: !!document.querySelector('header .ck-header-mobile__search'),
  cart: !!document.querySelector('header .o_wsale_my_cart'),
  chromeClass: !!document.querySelector('.ck-header-mobile-chrome'),
}));

await page.screenshot({ path: `${OUT}/h1_mobile_390_chrome.png`, fullPage: false });

await page.click('button[data-bs-target="#top_menu_collapse_mobile"]');
await page.waitForTimeout(500);

results.M2_drawer = await page.evaluate(() => {
  const drawer = document.querySelector('#top_menu_collapse_mobile');
  const items = drawer ? [...drawer.querySelectorAll('.top_menu > li > a, .top_menu > li > .accordion-button')].map((a) => a.textContent.trim()) : [];
  return { items, searchInDrawer: !!drawer?.querySelector('input[name="search"]') };
});

results.M3_account = await page.evaluate(() => ({
  loginInDrawer: !!document.querySelector('#top_menu_collapse_mobile a[href*="/web/login"]'),
  loginInChrome: !!document.querySelector('header.o_header_mobile a[href*="/web/login"]'),
}));

await page.screenshot({ path: `${OUT}/h1_mobile_390_drawer.png`, fullPage: false });

results.M4_overflow = await page.evaluate(() => ({
  docWidth: document.documentElement.scrollWidth,
  viewWidth: window.innerWidth,
}));

results.M6_homeCoexistence = await page.evaluate(() => {
  const bar = document.querySelector('.ck-header-service-bar')?.textContent?.replace(/\s+/g, ' ').trim() || '';
  const trust = document.querySelector('.ck-reassurance--trust-bar')?.textContent?.replace(/\s+/g, ' ').trim() || '';
  return { serviceBar: bar, trustBar: trust };
});

writeFileSync(`${OUT}/h1_mobile_390_results.json`, JSON.stringify({ viewport: { width: 390, height: 844 }, results }, null, 2));
console.log(JSON.stringify(results, null, 2));

await browser.close();
