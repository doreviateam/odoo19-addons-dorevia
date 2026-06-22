import { chromium } from 'playwright';
import { mkdirSync, writeFileSync } from 'fs';

const DB = 'dorevia_ck_marketone_01';
const BASE = 'http://localhost:18079';
const QA = 'h1';
const headers = { 'X-Odoo-Database': DB };
const OUT = new URL('../captures/recette_h1_v2_1/', import.meta.url).pathname;

mkdirSync(OUT, { recursive: true });

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({ viewport: { width: 1280, height: 800 }, extraHTTPHeaders: headers });
const page = await context.newPage();

const results = {};

await page.goto(`${BASE}/?db=${DB}&qa_ts=${QA}`, { waitUntil: 'networkidle', timeout: 45000 });

results.R1_serviceBar = await page.evaluate(() => {
  const bar = document.querySelector('.ck-header-service-bar');
  return {
    present: !!bar,
    text: bar?.textContent?.replace(/\s+/g, ' ').trim() || null,
  };
});

results.R2_brand = await page.evaluate(() => {
  const brand = document.querySelector('header .ck-header__brand');
  return {
    text: brand?.textContent?.trim() || null,
    ariaLabel: document.querySelector('header a[data-name="Navbar Logo"]')?.getAttribute('aria-label') || null,
  };
});

results.R3_search = await page.evaluate(() => {
  const input = document.querySelector('header .ck-header__search input[name="search"]');
  return {
    visible: !!input && input.offsetParent !== null,
    placeholder: input?.getAttribute('placeholder') || null,
    searchType: input?.getAttribute('data-search-type') || null,
  };
});

results.R4_cartAccount = await page.evaluate(() => {
  const cart = document.querySelector('header .o_wsale_my_cart');
  const login = document.querySelector('header a[href*="/web/login"]');
  const cartBox = cart?.getBoundingClientRect();
  const loginBox = login?.getBoundingClientRect();
  return {
    cartPresent: !!cart,
    loginPresent: !!login,
    cartRightOfLogin: cartBox && loginBox ? cartBox.left >= loginBox.left : null,
  };
});

results.R5_nav = await page.evaluate(() => {
  const el = document.querySelector('#top_menu');
  if (!el) return null;
  return [...el.querySelectorAll(':scope > li > a, :scope > li > .dropdown-toggle')]
    .map((a) => a.textContent.trim())
    .filter(Boolean);
});

await page.screenshot({ path: `${OUT}/h1_desktop_1280_header.png`, fullPage: false });

results.R7_sticky = await page.evaluate(() => {
  const header = document.querySelector('header#top.ck-header');
  const style = header ? getComputedStyle(header) : null;
  return { position: style?.position || null };
});

writeFileSync(`${OUT}/h1_desktop_1280_results.json`, JSON.stringify({ viewport: { width: 1280, height: 800 }, results }, null, 2));
console.log(JSON.stringify(results, null, 2));

await browser.close();
