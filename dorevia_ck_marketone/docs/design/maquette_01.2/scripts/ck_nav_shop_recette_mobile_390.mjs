import { chromium } from 'playwright';
import { mkdirSync, writeFileSync } from 'node:fs';

const DB = 'dorevia_ck_marketone_01';
const BASE = 'http://localhost:18079';
const QA = 'nav_shop_v2';
const headers = { 'X-Odoo-Database': DB };
const OUT = '/Users/doreviateam/dorevia-saas/odoo19-addons-dorevia/dorevia_ck_marketone/docs/design/maquette_01.2/captures/recette_nav_shop_v2';

mkdirSync(OUT, { recursive: true });

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({ viewport: { width: 390, height: 844 }, extraHTTPHeaders: headers });
const page = await context.newPage();

const results = {};

await page.goto(`${BASE}/?db=${DB}&qa_ts=${QA}`, { waitUntil: 'networkidle', timeout: 45000 });

results.M5_overflow_closed = await page.evaluate(() => ({
  overflow: document.documentElement.scrollWidth > document.documentElement.clientWidth + 1,
}));

const toggler = page.locator("header .navbar-toggler, header button[data-bs-toggle='offcanvas']").first();
if ((await toggler.count()) > 0) {
  await toggler.click();
  await page.waitForTimeout(600);
}

await page.screenshot({ path: `${OUT}/nav_shop_mobile_390_drawer.png`, fullPage: false });

results.M1_visibleEntries = await page.evaluate(() => {
  const root = document.querySelector('#top_menu_collapse_mobile.show, .offcanvas.show, #top_menu_collapse_mobile');
  if (!root) return null;
  return [...root.querySelectorAll('li.nav-item, li.o_no_autohide_item')]
    .map((li) => {
      const a = li.querySelector(':scope > a, :scope > .nav-link, :scope > .dropdown-toggle');
      const visible = getComputedStyle(li).display !== 'none' && li.offsetParent !== null;
      return a && visible ? a.textContent.trim().split('\n')[0] : null;
    })
    .filter(Boolean);
});

const nosUnivers = page.locator("#top_menu_collapse_mobile .ck-nav-mobile-univers .dropdown-toggle, #top_menu_collapse_mobile a:has-text('Nos univers')").first();
if ((await nosUnivers.count()) > 0) {
  await nosUnivers.click({ force: true });
  await page.waitForTimeout(500);
}

await page.screenshot({ path: `${OUT}/nav_shop_mobile_390_nos_univers_open.png`, fullPage: false });

results.M2_nosUniversChildren = await page.evaluate(() => {
  const root = document.querySelector('#top_menu_collapse_mobile, .offcanvas');
  if (!root) return null;
  return [...root.querySelectorAll('li.ck-nav-mobile-universe-child > a')]
    .map((a) => ({ text: a.textContent.trim(), href: a.getAttribute('href') }))
    .filter((l) => l.text);
});

results.M3_noDuplicateRoots = await page.evaluate(() => {
  const root = document.querySelector('#top_menu_collapse_mobile, .offcanvas');
  if (!root) return null;
  const names = ['Épicerie', 'Maison & bien-être', 'Boissons', 'Coups de cœur'];
  const counts = {};
  for (const name of names) {
    const links = [...root.querySelectorAll('a, .nav-link')].filter(
      (a) => a.textContent.trim() === name && getComputedStyle(a.closest('li') || a).display !== 'none'
    );
    counts[name] = links.filter((a) => (a.closest('li') || a).offsetParent !== null).length;
  }
  return counts;
});

results.M4_h1Mobile = await page.evaluate(() => ({
  serviceBar: !!document.querySelector('.ck-header-service-bar'),
  mobileChrome: !!document.querySelector('.ck-header-mobile-chrome'),
  burger: !!document.querySelector("header button[data-bs-target='#top_menu_collapse_mobile']"),
}));

results.M5_overflow_open = await page.evaluate(() => ({
  overflow: document.documentElement.scrollWidth > document.documentElement.clientWidth + 1,
}));

writeFileSync(`${OUT}/nav_shop_mobile_390_results.json`, JSON.stringify(results, null, 2));
console.log(JSON.stringify(results, null, 2));
await browser.close();
