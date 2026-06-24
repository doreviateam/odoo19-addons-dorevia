import { chromium } from 'playwright';
import { mkdirSync, writeFileSync } from 'node:fs';

const DB = 'dorevia_ck_marketone_01';
const BASE = 'http://localhost:18079';
const OUT =
  '/Users/doreviateam/dorevia-saas/odoo19-addons-dorevia/dorevia_ck_marketone/docs/design/maquette_01.2/captures/shop_structure_s1';
const headers = { 'X-Odoo-Database': DB };

mkdirSync(OUT, { recursive: true });

const browser = await chromium.launch({
  headless: true,
  channel: 'chrome',
});

async function capture(name, url, viewport, options = {}) {
  const context = await browser.newContext({ viewport, extraHTTPHeaders: headers });
  const page = await context.newPage();
  const target = `${BASE}${url}${url.includes('?') ? '&' : '?'}db=${DB}&qa_ts=s1`;
  const response = await page.goto(target, { waitUntil: 'networkidle', timeout: 45000 });
  if (options.scrollGrid) {
    const grid = page.locator('#o_wsale_products_grid').first();
    if (await grid.count()) {
      await grid.scrollIntoViewIfNeeded();
      await page.waitForTimeout(500);
    }
  }
  await page.screenshot({ path: `${OUT}/${name}.png`, fullPage: false });

  const data = await page.evaluate(() => {
    const html = document.documentElement;
    const body = document.body;
    return {
      h1: document.querySelector('h1')?.textContent?.trim() || null,
      introLead: document.querySelector('.ck-shop-intro__lead')?.textContent?.trim() || null,
      introNote: document.querySelector('.ck-shop-intro__note')?.textContent?.trim() || null,
      sidebarTitle: document.querySelector('.ck-shop-sidebar__title')?.textContent?.trim() || null,
      toolbarCount: document.querySelectorAll('.ck-shop-toolbar__count').length,
      cardCount: document.querySelectorAll('#o_wsale_products_grid .oe_product, .ck-product-card--shop').length,
      overflow: html.scrollWidth > html.clientWidth + 1 || body.scrollWidth > body.clientWidth + 1,
      hasBudget: /Budget/i.test(document.querySelector('.ck-shop-sidebar')?.textContent || ''),
      hasAffiner: /Affiner ma sélection/i.test(document.body.textContent || ''),
    };
  });

  await context.close();
  return {
    name,
    url,
    viewport,
    httpStatus: response?.status() || null,
    ...data,
  };
}

const results = [];
results.push(await capture('shop_desktop_top', '/shop', { width: 1280, height: 900 }));
results.push(
  await capture('shop_desktop_grid', '/shop', { width: 1280, height: 900 }, { scrollGrid: true }),
);
results.push(await capture('shop_category_epicerie_desktop', '/shop/category/epicerie-1', { width: 1280, height: 900 }));
results.push(await capture('shop_tablet_800', '/shop', { width: 800, height: 900 }));
results.push(await capture('shop_mobile_390', '/shop', { width: 390, height: 900 }));

await browser.close();

const report = {
  generatedAt: new Date().toISOString(),
  base: BASE,
  db: DB,
  results,
  screenshots: OUT,
};

writeFileSync(`${OUT}/shop_structure_s1_results.json`, JSON.stringify(report, null, 2));
console.log(JSON.stringify(report, null, 2));
