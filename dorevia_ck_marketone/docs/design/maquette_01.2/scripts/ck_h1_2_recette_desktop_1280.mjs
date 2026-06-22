import { chromium } from 'playwright';
import { mkdirSync, writeFileSync } from 'node:fs';

const DB = 'dorevia_ck_marketone_01';
const BASE = 'http://localhost:18079';
const QA = 'h1_2_header';
const headers = { 'X-Odoo-Database': DB };
const OUT = '/Users/doreviateam/dorevia-saas/odoo19-addons-dorevia/dorevia_ck_marketone/docs/design/maquette_01.2/captures/recette_h1_2_header';

mkdirSync(OUT, { recursive: true });

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({ viewport: { width: 1280, height: 900 }, extraHTTPHeaders: headers });
const page = await context.newPage();
const results = {};

await page.goto(`${BASE}/?db=${DB}&qa_ts=${QA}`, { waitUntil: 'networkidle', timeout: 45000 });

results.R1_threeLevels = await page.evaluate(() => ({
  serviceBar: !!document.querySelector('.ck-header-service-bar'),
  identityRow: !!document.querySelector('.ck-header__identity-row'),
  navRow: !!document.querySelector('.ck-header__nav-row'),
  searchInIdentity: !!document.querySelector('.ck-header__identity-row .ck-header__search'),
  topMenuInNavRow: !!document.querySelector('.ck-header__nav-row #top_menu'),
  extraMenuPlus: !!document.querySelector('.o_extra_menu_items .oi-plus:not([style*="display: none"])'),
  extraMenuVisible: !!document.querySelector('.o_extra_menu_items:not([style*="display: none"])'),
}));

results.R1_topMenu = await page.evaluate(() => {
  const items = [...document.querySelectorAll('#top_menu > li')]
    .filter((li) => getComputedStyle(li).display !== 'none')
    .map((li) => {
      const a = li.querySelector(':scope > a, :scope > .nav-link, :scope > .dropdown-toggle, :scope > .ck-nav-universe-split__link');
      return a ? a.textContent.trim() : null;
    })
    .filter(Boolean);
  return items;
});

await page.screenshot({ path: `${OUT}/h1_2_desktop_1280_header_closed.png`, fullPage: false });

// Dropdown L2 ouvert (première racine avec toggle split ou dropdown)
const l2Opened = await page.evaluate(async () => {
  const toggles = [
    ...document.querySelectorAll('.ck-nav-universe-split__toggle'),
    ...document.querySelectorAll('#top_menu .ck-nav-desktop-universe > .dropdown-toggle'),
  ];
  const toggle = toggles[0];
  if (!toggle) return { opened: false, reason: 'no toggle found' };
  toggle.click();
  await new Promise((r) => setTimeout(r, 350));
  const menu = document.querySelector('#top_menu .dropdown-menu.show');
  return {
    opened: !!menu,
    category: toggle.closest('.nav-item')?.querySelector('.ck-nav-universe-split__link span, .dropdown-toggle span')?.textContent?.trim(),
    items: menu ? [...menu.querySelectorAll('a')].map((a) => a.textContent.trim()).filter(Boolean) : [],
  };
});
results.R2_dropdown = l2Opened;
await page.waitForTimeout(400);
await page.screenshot({ path: `${OUT}/h1_2_desktop_1280_dropdown_open.png`, fullPage: false });

// Hover item dropdown
await page.evaluate(() => {
  const item = document.querySelector('#top_menu .dropdown-menu.show a');
  if (item) item.dispatchEvent(new MouseEvent('mouseenter', { bubbles: true }));
});
await page.waitForTimeout(200);
results.R2_hoverColor = await page.evaluate(() => {
  const item = document.querySelector('#top_menu .dropdown-menu.show a');
  return item ? getComputedStyle(item).color : null;
});
await page.screenshot({ path: `${OUT}/h1_2_desktop_1280_dropdown_hover.png`, fullPage: false });
await page.keyboard.press('Escape');

// Mobile 390
await page.setViewportSize({ width: 390, height: 844 });
await page.goto(`${BASE}/?db=${DB}&qa_ts=${QA}_mobile`, { waitUntil: 'networkidle', timeout: 45000 });
results.R4_mobile = await page.evaluate(() => ({
  mobileChrome: !!document.querySelector('.ck-header-mobile-chrome'),
  offcanvas: !!document.querySelector('#top_menu_collapse_mobile'),
  identityRowHidden: !document.querySelector('.ck-header__identity-row')?.offsetParent,
  navRowHidden: !document.querySelector('.ck-header__nav-row')?.offsetParent,
}));
await page.screenshot({ path: `${OUT}/h1_2_mobile_390_header.png`, fullPage: false });

writeFileSync(`${OUT}/h1_2_recette_results.json`, JSON.stringify(results, null, 2));
console.log(JSON.stringify(results, null, 2));
await browser.close();
