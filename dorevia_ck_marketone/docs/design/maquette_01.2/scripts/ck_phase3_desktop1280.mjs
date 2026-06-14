import { chromium } from 'playwright';

const DB = 'dorevia_ck_marketone_01';
const BASE = 'http://localhost:18079';
const headers = { 'X-Odoo-Database': DB };

async function auditShop(page, path) {
  await page.goto(`${BASE}${path}?db=${DB}`, { waitUntil: 'networkidle', timeout: 45000 });
  await page.waitForTimeout(1500);
  return page.evaluate(() => {
    const grid = document.querySelector('#o_wsale_products_grid');
    const productLinks = grid
      ? [...new Set(
          [...grid.querySelectorAll('a[href*="/shop/"]')]
            .map((a) => a.getAttribute('href'))
            .filter(
              (h) =>
                h
                && !h.includes('/cart')
                && !h.includes('/wishlist')
                && !h.includes('?')
                && /\/shop\/(.+\/)?[^/]+-\d+$/.test(h),
            ),
        )]
      : [];
    const prices = [...document.querySelectorAll('.oe_product .product_price, .oe_product .o_wsale_product_sub .fw-bold')]
      .map((el) => el.textContent.trim())
      .filter(Boolean);
    const categoryHeader = document.querySelector('#o_wsale_products_header');
    const categoryDescEl = document.querySelector('#category_header.o_wsale_category_description, .o_wsale_category_description');
    return {
      url: location.pathname,
      status: document.body ? 'ok' : 'empty',
      scrollWidth: document.documentElement.scrollWidth,
      clientWidth: document.documentElement.clientWidth,
      ckShopPage: !!document.querySelector('.ck-shop-page'),
      shopIntro: !!document.querySelector('.s_ck_shop_intro'),
      reassurance: !!document.querySelector('.s_ck_reassurance'),
      proSignal: !!document.querySelector('.ck-shop-pro-signal'),
      productCards: document.querySelectorAll('#o_wsale_products_grid .oe_product, .o_wsale_products_grid .oe_product').length,
      productLinks,
      prices,
      filmstrip: document.querySelectorAll('.o_wsale_filmstrip_link').length,
      sortNative: !!document.querySelector('.o_wsale_search_order_by, [data-bs-toggle="dropdown"]'),
      categoryTitle: categoryHeader?.dataset?.categoryName?.trim()
        || categoryHeader?.querySelector('h1, .h1')?.textContent?.trim()
        || null,
      categoryDesc: !!categoryDescEl,
      categoryDescText: categoryDescEl?.textContent?.trim().slice(0, 120) || null,
    };
  });
}

async function checkLinks(page, links) {
  const broken = [];
  for (const href of links.slice(0, 8)) {
    const resp = await page.goto(`${BASE}${href}?db=${DB}`, { waitUntil: 'domcontentloaded', timeout: 30000 });
    if (!resp || resp.status() >= 400) broken.push({ href, status: resp?.status() });
  }
  return broken;
}

async function auditHome(page) {
  await page.goto(`${BASE}/?db=${DB}`, { waitUntil: 'networkidle', timeout: 45000 });
  await page.waitForTimeout(1500);
  return page.evaluate(() => ({
    featuredStable: document.querySelectorAll('.ck-featured-products__grid--stable .oe_product, .ck-featured-products__grid--stable .o_carousel_product_card').length,
    dynamicSnippet: document.querySelectorAll('.s_dynamic_snippet_products').length,
    proLinks: document.querySelectorAll('a[href="/professionnels"]').length,
    headerShop: !!document.querySelector('header a[href="/shop"]'),
  }));
}

async function auditPhase1(page) {
  const checks = {};
  for (const [label, path] of [
    ['professionnels', '/professionnels'],
    ['shop', '/shop'],
    ['category_epicerie', '/shop/category/epicerie-creole-1'],
    ['category_artisanat_404', '/shop/category/artisanat-3'],
    ['category_packs_404', '/shop/category/packs-decouvertes-4'],
  ]) {
    const resp = await page.goto(`${BASE}${path}?db=${DB}`, { waitUntil: 'domcontentloaded', timeout: 30000 });
    checks[label] = resp?.status() ?? 0;
  }
  await page.goto(`${BASE}/?db=${DB}`, { waitUntil: 'networkidle', timeout: 45000 });
  const nav = await page.evaluate(() => ({
    headerLinks: [...document.querySelectorAll('header nav a')].map((a) => a.textContent.trim()).filter(Boolean),
    footerCols: document.querySelectorAll('footer .row > div, footer .o_footer_columns > div').length,
  }));
  return { http: checks, nav };
}

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({ viewport: { width: 1280, height: 900 }, extraHTTPHeaders: headers });
const page = await context.newPage();

const shop = await auditShop(page, '/shop');
const category = await auditShop(page, '/shop/category/epicerie-creole-1');
const broken = await checkLinks(page, [...shop.productLinks, ...category.productLinks]);
const home = await auditHome(page);
const phase1 = await auditPhase1(page);

console.log(JSON.stringify({ shop, category, broken, home, phase1 }, null, 2));
await browser.close();
