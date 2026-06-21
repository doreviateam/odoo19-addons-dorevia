import { chromium } from 'playwright';

const DB = 'dorevia_ck_marketone_01';
const BASE = 'http://localhost:18079';
const QA = 'nav1';
const headers = { 'X-Odoo-Database': DB };
const OUT = '/Users/doreviateam/dorevia-saas/odoo19-addons-dorevia/dorevia_ck_marketone/docs/design/maquette_01.2/captures/recette_nav1_v2';

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({ viewport: { width: 390, height: 844 }, extraHTTPHeaders: headers });
const page = await context.newPage();

const results = {};

await page.goto(`${BASE}/?db=${DB}&qa_ts=${QA}`, { waitUntil: 'networkidle', timeout: 45000 });

// M5 — overflow on closed page
results.M5_overflow_closed = await page.evaluate(() => ({
  scrollW: document.documentElement.scrollWidth,
  clientW: document.documentElement.clientWidth,
  overflow: document.documentElement.scrollWidth > document.documentElement.clientWidth + 1,
}));

await page.screenshot({ path: `${OUT}/nav1_mobile_390_drawer.png`, fullPage: false });

// Open burger
const toggler = page.locator("header .navbar-toggler, header button[data-bs-toggle='offcanvas'], header .o_header_mobile_toggle").first();
const togglerOk = (await toggler.count()) > 0;
if (togglerOk) {
  await toggler.click();
  await page.waitForTimeout(600);
}

const offcanvas = page.locator('#top_menu_collapse_mobile.show, .offcanvas.show').first();
const offcanvasVisible = await offcanvas.isVisible().catch(() => false);
results.M1_offcanvas = { togglerOk, offcanvasVisible };

await page.screenshot({ path: `${OUT}/nav1_mobile_390_drawer.png`, fullPage: false });

// M1 — drawer top-level entries (visible only)
results.M1_entries = await page.evaluate(() => {
  const root = document.querySelector('#top_menu_collapse_mobile.show, .offcanvas.show');
  if (!root) return null;
  const items = [...root.querySelectorAll('#top_menu > li, .navbar-nav > li')];
  return items
    .map((li) => {
      const a = li.querySelector(':scope > a, :scope > .nav-link');
      const cs = a ? getComputedStyle(li) : null;
      const visible = cs ? cs.display !== 'none' && li.offsetParent !== null : false;
      return a ? { text: a.textContent.trim(), visible } : null;
    })
    .filter((x) => x && x.visible);
});

// M2 — click "Nos univers" parent, should expand without navigating
const before = page.url();
const nosUnivers = page.locator("#top_menu_collapse_mobile a:has-text('Nos univers'), .offcanvas a:has-text('Nos univers')").first();
const nosUniversCount = await nosUnivers.count();
let m2 = { found: nosUniversCount > 0 };
if (nosUniversCount > 0) {
  await nosUnivers.click({ force: true });
  await page.waitForTimeout(500);
  m2.urlUnchanged = page.url() === before;
  m2.expandedVisible = await page.evaluate(() => {
    const links = [...document.querySelectorAll('#top_menu_collapse_mobile .dropdown-menu, .offcanvas .dropdown-menu')];
    return links.some((el) => getComputedStyle(el).display !== 'none' && el.offsetParent !== null);
  });
}
results.M2_nosUnivers = m2;

await page.screenshot({ path: `${OUT}/nav1_mobile_390_nos_univers_open.png`, fullPage: false });

// M3 — children present and point to correct URLs
results.M3_children = await page.evaluate(() => {
  const root = document.querySelector('#top_menu_collapse_mobile, .offcanvas');
  if (!root) return null;
  return [...root.querySelectorAll('.dropdown-menu a')]
    .map((a) => ({ text: a.textContent.trim(), href: a.getAttribute('href') }))
    .filter((l) => l.text);
});

// M4 — Découvrir accessible, Pro+Contact
const decouvrirMobile = page.locator("#top_menu_collapse_mobile a:has-text('Découvrir'), .offcanvas a:has-text('Découvrir')").first();
const decouvrirCount = await decouvrirMobile.count();
let m4 = { found: decouvrirCount > 0 };
if (decouvrirCount > 0) {
  await decouvrirMobile.click({ force: true });
  await page.waitForTimeout(500);
  m4.megaLinks = await page.evaluate(() => {
    const root = document.querySelector('#top_menu_collapse_mobile, .offcanvas');
    if (!root) return [];
    return [...root.querySelectorAll('.o_mega_menu a, .ck-nav-decouvrir-links a')]
      .map((a) => ({ text: a.textContent.trim(), href: a.getAttribute('href') }))
      .filter((l) => l.text);
  });
}
results.M4_decouvrir = m4;

// M5 — overflow with drawer open
results.M5_overflow_open = await page.evaluate(() => ({
  scrollW: document.documentElement.scrollWidth,
  clientW: document.documentElement.clientWidth,
  overflow: document.documentElement.scrollWidth > document.documentElement.clientWidth + 1,
}));

// M6 — chrome mobile
results.M6_chrome = await page.evaluate(() => ({
  burger: !!document.querySelector("header .navbar-toggler, header button[data-bs-toggle='offcanvas']"),
  cart: !!document.querySelector('header a[href*="/shop/cart"], header .o_wsale_my_cart'),
  search: !!document.querySelector('header .fa-search, header [aria-label*="Recherche"]'),
}));

const outJson = `${OUT}/nav1_mobile_390_results.json`;
await import('node:fs').then((fs) => fs.writeFileSync(outJson, JSON.stringify(results, null, 2)));
console.log(JSON.stringify(results, null, 2));
await browser.close();
