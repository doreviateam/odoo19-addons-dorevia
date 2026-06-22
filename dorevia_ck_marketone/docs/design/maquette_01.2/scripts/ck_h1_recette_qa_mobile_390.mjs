import { chromium } from 'playwright';

const DB = 'dorevia_ck_marketone_01';
const BASE = 'http://localhost:18079';
const QA = 'h1qa';
const headers = { 'X-Odoo-Database': DB };
const OUT = '/Users/doreviateam/dorevia-saas/odoo19-addons-dorevia/dorevia_ck_marketone/docs/design/maquette_01.2/captures/recette_h1_v2_1';

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({ viewport: { width: 390, height: 844 }, extraHTTPHeaders: headers });
const page = await context.newPage();
const results = {};

await page.goto(`${BASE}/?db=${DB}&qa_ts=${QA}`, { waitUntil: 'networkidle', timeout: 45000 });

// M1 — chrome line 1: Menu, C-Kréyòl, Recherche, Panier (no account)
results.M1_chrome = await page.evaluate(() => {
  const burger = document.querySelector("header .navbar-toggler, header button[data-bs-toggle='offcanvas']");
  const logo = document.querySelector('.ck-header__brand-link, .ck-header__brand');
  const search = document.querySelector('header .ck-header-mobile__search, header [data-bs-toggle="modal"][aria-label*="Rechercher"], header .fa-search');
  const cart = document.querySelector('header .ck-header__cart-link, header a[href*="/shop/cart"]');
  const accountInChrome = [...document.querySelectorAll('header .o_main_nav a, header .o_main_nav button')]
    .find((el) => /se connecter|mon compte/i.test(el.textContent) && el.offsetParent !== null);
  return {
    burgerFound: !!burger,
    burgerAriaLabel: burger ? burger.getAttribute('aria-label') : null,
    logoFound: !!logo,
    searchFound: !!search,
    cartFound: !!cart,
    accountVisibleInChrome: !!accountInChrome,
  };
});

results.M4_overflow_closed = await page.evaluate(() => ({
  scrollW: document.documentElement.scrollWidth,
  clientW: document.documentElement.clientWidth,
  overflow: document.documentElement.scrollWidth > document.documentElement.clientWidth + 1,
}));

await page.screenshot({ path: `${OUT}/h1_mobile_390_chrome_qa.png` });

// M5 — logo legibility (text content + width check, no tofu)
results.M5_logo = await page.evaluate(() => {
  const span = document.querySelector('.ck-header__brand');
  if (!span) return null;
  const r = span.getBoundingClientRect();
  return { text: span.textContent.trim(), width: r.width, height: r.height, hasOMacron: span.textContent.includes('ò') };
});

// M1 bis — banner overflow check (M4 in doc)
results.M4_banner = await page.evaluate(() => {
  const bar = document.querySelector('.ck-header-service-bar');
  if (!bar) return null;
  const r = bar.getBoundingClientRect();
  return { width: r.width, scrollWidth: bar.scrollWidth, text: bar.textContent.replace(/\s+/g, ' ').trim() };
});

// Open burger -> M2 drawer
const toggler = page.locator("header .navbar-toggler, header button[data-bs-toggle='offcanvas']").first();
await toggler.click();
await page.waitForTimeout(600);
await page.screenshot({ path: `${OUT}/h1_mobile_390_drawer_qa.png` });

results.M2_drawer = await page.evaluate(() => {
  const offcanvas = document.querySelector('#top_menu_collapse_mobile');
  if (!offcanvas) return null;
  const searchInDrawer = offcanvas.querySelector('input[type="search"], .oe_search_box');
  const searchVisible = searchInDrawer ? getComputedStyle(searchInDrawer.closest('li') || searchInDrawer).display !== 'none' && searchInDrawer.offsetParent !== null : false;
  const topItems = [...offcanvas.querySelectorAll('ul.top_menu > li')]
    .map((li) => {
      const a = li.querySelector(':scope > a, :scope > .nav-link');
      const cs = getComputedStyle(li);
      return a && cs.display !== 'none' && li.offsetParent !== null ? a.textContent.trim() : null;
    })
    .filter(Boolean);
  return { topItems, searchVisibleInDrawer: searchVisible };
});

// M3 — account link in drawer
results.M3_account = await page.evaluate(() => {
  const offcanvas = document.querySelector('#top_menu_collapse_mobile');
  const link = [...offcanvas.querySelectorAll('a')].find((a) => /se connecter/i.test(a.textContent));
  return link ? { found: true, href: link.getAttribute('href'), text: link.textContent.trim() } : { found: false };
});

const fs = await import('node:fs');
fs.writeFileSync(`${OUT}/h1_mobile_390_qa_results.json`, JSON.stringify(results, null, 2));
console.log(JSON.stringify(results, null, 2));
await browser.close();
