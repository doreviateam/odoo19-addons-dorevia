import { chromium } from 'playwright';

const DB = 'dorevia_ck_marketone_01';
const BASE = 'http://localhost:18079';
const headers = { 'X-Odoo-Database': DB };

async function audit(path) {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    viewport: { width: 390, height: 844 },
    extraHTTPHeaders: headers,
  });
  const page = await context.newPage();
  await page.goto(`${BASE}${path}?db=${DB}`, { waitUntil: 'networkidle', timeout: 45000 });
  await page.waitForTimeout(1500);
  const result = await page.evaluate(() => {
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
    const categoryHeader = document.querySelector('#o_wsale_products_header');
    const categoryDescEl = document.querySelector('#category_header.o_wsale_category_description, .o_wsale_category_description');
    return {
      path: location.pathname,
      scrollWidth: document.documentElement.scrollWidth,
      clientWidth: document.documentElement.clientWidth,
      overflow: document.documentElement.scrollWidth > document.documentElement.clientWidth,
      shopIntro: !!document.querySelector('.s_ck_shop_intro'),
      productCards: document.querySelectorAll('#o_wsale_products_grid .oe_product').length,
      productLinks: productLinks.length,
      categoryTitle: categoryHeader?.dataset?.categoryName?.trim() || null,
      categoryDesc: !!categoryDescEl,
      cartBtn: !!document.querySelector('a[href="/shop/cart"], .o_wsale_my_cart, .my_cart'),
    };
  });
  await browser.close();
  return result;
}

const shop = await audit('/shop');
const category = await audit('/shop/category/epicerie-creole-1');

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({ viewport: { width: 390, height: 844 }, extraHTTPHeaders: headers });
const page = await context.newPage();
await page.goto(`${BASE}/?db=${DB}`, { waitUntil: 'networkidle', timeout: 45000 });
await page.waitForTimeout(1500);
const home = await page.evaluate(() => ({
  scrollWidth: document.documentElement.scrollWidth,
  clientWidth: document.documentElement.clientWidth,
  overflow: document.documentElement.scrollWidth > document.documentElement.clientWidth,
  featuredStable: document.querySelectorAll('.ck-featured-products__grid--stable .oe_product, .ck-featured-products__grid--stable .o_carousel_product_card').length,
}));
await browser.close();

console.log(JSON.stringify({ shop, category, home }, null, 2));
