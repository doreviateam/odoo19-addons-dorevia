import { chromium } from 'playwright';
import { mkdirSync, writeFileSync } from 'node:fs';

const DB = 'dorevia_ck_marketone_01';
const BASE = 'http://localhost:18079';
const OUT =
  '/Users/doreviateam/dorevia-saas/odoo19-addons-dorevia/dorevia_ck_marketone/docs/design/maquette_01.2/captures/micro_lot_3b';
const headers = { 'X-Odoo-Database': DB };

mkdirSync(OUT, { recursive: true });

const browser = await chromium.launch({
  headless: true,
  channel: 'chrome',
});

async function openShop(page, path = '/shop') {
  const target = `${BASE}${path}${path.includes('?') ? '&' : '?'}db=${DB}`;
  return page.goto(target, { waitUntil: 'networkidle', timeout: 60000 });
}

async function openMobileDrawer(page) {
  const mobileBtn = page.locator('button[data-bs-target="#o_wsale_offcanvas"]').first();
  await mobileBtn.waitFor({ state: 'visible', timeout: 15000 });
  await mobileBtn.click();
  await page.locator('#o_wsale_offcanvas.show, #o_wsale_offcanvas.offcanvas.show').waitFor({
    state: 'visible',
    timeout: 10000,
  });
}

async function readFilterState(page, mode) {
  return page.evaluate((scopeMode) => {
    const offcanvas = document.querySelector('#o_wsale_offcanvas');
    const sidebar = document.querySelector('.ck-shop-sidebar');
    const scope =
      scopeMode === 'mobile' && offcanvas?.classList.contains('show')
        ? offcanvas
        : sidebar || offcanvas;
    const text = scope?.textContent || '';
    return {
      hasOrigines: /Origines/.test(text),
      hasProducteurs: /Producteurs/.test(text),
      hasPreferences: /Préférences/.test(text),
      hasReset: /Réinitialiser les filtres/.test(document.body.textContent || ''),
      hasBienEtre: />Bien-être</.test(document.body.innerHTML || ''),
      productCount: document.querySelectorAll('.oe_product, .ck-product-card--shop').length,
    };
  }, mode);
}

async function captureDesktop(name, url) {
  const context = await browser.newContext({ viewport: { width: 1280, height: 900 }, extraHTTPHeaders: headers });
  const page = await context.newPage();
  const response = await openShop(page, url);
  await page.locator('.ck-shop-sidebar, #products_grid_before').first().waitFor({ state: 'attached' });
  await page.waitForTimeout(500);
  await page.screenshot({ path: `${OUT}/${name}.png`, fullPage: false });
  const data = await readFilterState(page, 'desktop');
  await context.close();
  return { name, url, viewport: { width: 1280, height: 900 }, httpStatus: response?.status() || null, ...data };
}

async function captureMobile(name, url, { openDrawer = false } = {}) {
  const context = await browser.newContext({ viewport: { width: 390, height: 844 }, extraHTTPHeaders: headers });
  const page = await context.newPage();
  const response = await openShop(page, url);
  if (openDrawer) {
    await openMobileDrawer(page);
    await page.waitForTimeout(400);
  }
  await page.screenshot({ path: `${OUT}/${name}.png`, fullPage: false });
  const data = await readFilterState(page, 'mobile');
  await context.close();
  return { name, url, viewport: { width: 390, height: 844 }, httpStatus: response?.status() || null, ...data };
}

const results = [];
results.push(await captureDesktop('shop_filtres_drawer_desktop_1280', '/shop'));
results.push(await captureMobile('shop_filtres_drawer_mobile_390', '/shop', { openDrawer: true }));

{
  const context = await browser.newContext({ viewport: { width: 390, height: 844 }, extraHTTPHeaders: headers });
  const page = await context.newPage();
  await openShop(page, '/shop');
  await openMobileDrawer(page);
  const originBtn = page.locator('[data-bs-target="#o_wsale_offcanvas_ck_tags_origin"]').first();
  if (await originBtn.count()) {
    await originBtn.click({ force: true });
    await page.waitForTimeout(300);
  }
  const guadeloupe = page.locator('#o_wsale_offcanvas_ck_tags_origin input[name="tags"]').first();
  if (await guadeloupe.count()) {
    const tagId = await guadeloupe.getAttribute('value');
    await guadeloupe.check({ force: true });
    await page.waitForTimeout(400);
    await page.screenshot({ path: `${OUT}/shop_filtres_drawer_filtre_actif_mobile_390.png`, fullPage: false });
    results.push({ name: 'shop_filtres_drawer_filtre_actif_mobile_390', tagId });

    await openShop(page, `/shop?tags=${tagId}`);
    await page.waitForTimeout(800);
    await page.screenshot({ path: `${OUT}/shop_filtres_grille_filtree_mobile_390.png`, fullPage: false });
    results.push({
      name: 'shop_filtres_grille_filtree_mobile_390',
      productCount: await page.locator('.oe_product, .ck-product-card--shop').count(),
    });
  }
  await context.close();
}

await browser.close();

const report = {
  generatedAt: new Date().toISOString(),
  base: BASE,
  db: DB,
  results,
  screenshots: OUT,
};

writeFileSync(`${OUT}/micro_lot_3b_results.json`, JSON.stringify(report, null, 2));
console.log(JSON.stringify(report, null, 2));
