import { chromium } from 'playwright';

const DB = 'dorevia_ck_marketone_01';
const BASE = 'http://localhost:18079';
const QA = 'nav1';
const headers = { 'X-Odoo-Database': DB };
const OUT = '/Users/doreviateam/dorevia-saas/odoo19-addons-dorevia/dorevia_ck_marketone/docs/design/maquette_01.2/captures/recette_nav1_v2';

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({ viewport: { width: 1280, height: 800 }, extraHTTPHeaders: headers });
const page = await context.newPage();

const results = {};

await page.goto(`${BASE}/?db=${DB}&qa_ts=${QA}`, { waitUntil: 'networkidle', timeout: 45000 });

// D1 + D2 — top-level menu entries
const topMenu = await page.evaluate(() => {
  const el = document.querySelector('#top_menu');
  if (!el) return null;
  return [...el.querySelectorAll(':scope > li > a, :scope > li > .nav-link')]
    .map((a) => a.textContent.trim())
    .filter(Boolean);
});
results.D1_D2_topMenu = topMenu;

// D3 — no CTA button
results.D3_ctaContact = await page.evaluate(() => ({
  btnCtaCount: document.querySelectorAll('header .btn_cta').length,
  contactTextInHeaderTop: !!document.querySelector('#top_menu')?.textContent.match(/Contactez-nous/),
}));

await page.screenshot({ path: `${OUT}/nav1_desktop_1280_header.png`, fullPage: false });

// D4 — Tous nos produits -> /shop
let resp = await page.goto(`${BASE}/shop?db=${DB}&qa_ts=${QA}`, { waitUntil: 'networkidle', timeout: 45000 });
results.D4_shop = {
  status: resp.status(),
  productCount: await page.evaluate(() => document.querySelectorAll('#o_wsale_products_grid .oe_product, .o_wsale_products_grid .oe_product').length),
};

// D5 — Épicerie
resp = await page.goto(`${BASE}/shop/category/epicerie-1?db=${DB}&qa_ts=${QA}`, { waitUntil: 'networkidle', timeout: 45000 });
results.D5_epicerie = {
  status: resp.status(),
  productCount: await page.evaluate(() => document.querySelectorAll('#o_wsale_products_grid .oe_product, .o_wsale_products_grid .oe_product').length),
};

// D6 — Soin & Bien-être
resp = await page.goto(`${BASE}/shop/category/maison-bien-etre-2?db=${DB}&qa_ts=${QA}`, { waitUntil: 'networkidle', timeout: 45000 });
results.D6_soinBienEtre = {
  status: resp.status(),
  productCount: await page.evaluate(() => document.querySelectorAll('#o_wsale_products_grid .oe_product, .o_wsale_products_grid .oe_product').length),
  menuLabel: topMenu?.find((t) => t.includes('Soin')) || null,
};

// D7, D8 — Mega Découvrir
await page.goto(`${BASE}/?db=${DB}&qa_ts=${QA}`, { waitUntil: 'networkidle', timeout: 45000 });
const decouvrir = page.locator("header .nav-link:has-text('Découvrir'), header a:has-text('Découvrir')").first();
await decouvrir.click();
await page.waitForTimeout(600);
const megaPanel = page.locator('.o_mega_menu, .dropdown-menu.show').first();
const megaVisible = await megaPanel.isVisible().catch(() => false);
const megaLinks = megaVisible
  ? await megaPanel.evaluate((el) => [...el.querySelectorAll('a')].map((a) => ({ text: a.textContent.trim(), href: a.getAttribute('href') })).filter((l) => l.text))
  : [];
results.D7_D8_mega = { megaVisible, megaLinks };
await page.screenshot({ path: `${OUT}/nav1_desktop_1280_header.png`, fullPage: false });

// D9 — chrome header
results.D9_chrome = await page.evaluate(() => ({
  logo: !!document.querySelector('header .navbar-brand, header .ck-header__brand'),
  search: !!document.querySelector('header .o_wsale_products_search, header .oe_search_box, header [aria-label*="Recherche"], header .fa-search'),
  account: !!document.querySelector('header a[href*="/web/login"], header .o_header_partner_dropdown, header .fa-user'),
  cart: !!document.querySelector('header a[href*="/shop/cart"], header .o_wsale_my_cart'),
}));

// D10 — contrast hover/focus on mega links (CSS computed color)
if (megaVisible) {
  const firstLink = megaPanel.locator('a').first();
  await firstLink.hover();
  await page.waitForTimeout(150);
  results.D10_contrast = await firstLink.evaluate((el) => getComputedStyle(el).color);
}

// Close mega
await page.keyboard.press('Escape');
await page.waitForTimeout(200);

// §10 bis — visual tenue checks: bounding boxes for overlap / wrap detection
await page.goto(`${BASE}/?db=${DB}&qa_ts=${QA}`, { waitUntil: 'networkidle', timeout: 45000 });
results.V1_V2_V3 = await page.evaluate(() => {
  const items = [...document.querySelectorAll('#top_menu > li > a, #top_menu > li > .nav-link')];
  const soin = items.find((a) => a.textContent.includes('Soin'));
  const logo = document.querySelector('header .navbar-brand, header .ck-header__brand-link');
  const rightChrome = document.querySelector('header .o_wsale_my_cart, header a[href*="/shop/cart"]');
  const out = { soinFound: !!soin };
  if (soin) {
    const r = soin.getBoundingClientRect();
    out.soinHeight = r.height;
    out.soinText = soin.textContent.trim();
    out.soinLineWrap = r.height > 30; // heuristic: single-line nav link ~20-26px
  }
  if (logo && soin) {
    const lr = logo.getBoundingClientRect();
    const sr = soin.getBoundingClientRect();
    out.logoOverlapsSoin = !(lr.right < sr.left || sr.right < lr.left);
  }
  if (rightChrome && soin) {
    const cr = rightChrome.getBoundingClientRect();
    const sr = soin.getBoundingClientRect();
    out.chromeOverlapsSoin = !(cr.left > sr.right + 8);
  }
  return out;
});

const outJson = `${OUT}/nav1_desktop_1280_results.json`;
await import('node:fs').then((fs) => fs.writeFileSync(outJson, JSON.stringify(results, null, 2)));

console.log(JSON.stringify(results, null, 2));
await browser.close();
