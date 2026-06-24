import { chromium } from 'playwright';
import { mkdirSync, writeFileSync } from 'node:fs';

const DB = 'dorevia_ck_marketone_01';
const BASE = 'http://localhost:18079';
const OUT =
  '/Users/doreviateam/dorevia-saas/odoo19-addons-dorevia/dorevia_ck_marketone/docs/design/maquette_01.2/captures/shop_recette_current';
const headers = { 'X-Odoo-Database': DB };

mkdirSync(OUT, { recursive: true });

const browser = await chromium.launch({
  headless: true,
  channel: 'chrome',
});

async function checkPage(name, url, viewport) {
  const context = await browser.newContext({ viewport, extraHTTPHeaders: headers });
  const page = await context.newPage();
  const target = `${BASE}${url}${url.includes('?') ? '&' : '?'}db=${DB}`;
  const response = await page.goto(target, { waitUntil: 'networkidle', timeout: 45000 });
  await page.screenshot({ path: `${OUT}/${name}.png`, fullPage: false });

  const data = await page.evaluate(() => {
    const body = document.body;
    const html = document.documentElement;
    const leafTexts = [...document.querySelectorAll('body *')]
      .map((el) => (el.childElementCount === 0 ? el.textContent.trim().replace(/\s+/g, ' ') : ''))
      .filter(Boolean);

    const cardButtons = [...document.querySelectorAll('.ck-product-card__actions button, .ck-product-card__actions a, .a-submit')]
      .map((el) => {
        const rect = el.getBoundingClientRect();
        const style = getComputedStyle(el);
        const label = (el.textContent || el.getAttribute('aria-label') || el.getAttribute('title') || '')
          .trim()
          .replace(/\s+/g, ' ');
        return {
          width: Math.round(rect.width),
          height: Math.round(rect.height),
          radius: style.borderRadius,
          label,
        };
      })
      .filter((item) => item.width > 0 && item.height > 0 && /panier|cart|Ajouter/i.test(item.label))
      .slice(0, 10);

    return {
      title: document.title,
      h1: document.querySelector('h1')?.textContent.trim() || null,
      statusText: leafTexts.find((text) => /^\d+ produits?$/.test(text)) || null,
      overflow:
        html.scrollWidth > html.clientWidth + 1 ||
        body.scrollWidth > body.clientWidth + 1,
      cardCount: document.querySelectorAll('.oe_product, .ck-product-card--shop').length,
      ckShopCardCount: document.querySelectorAll('.ck-product-card--shop').length,
      productNames: [
        ...document.querySelectorAll(
          '.ck-product-card__title, .o_wsale_products_item_title, .oe_product h6, .oe_product h5'
        ),
      ]
        .map((el) => el.textContent.trim().replace(/\s+/g, ' '))
        .filter(Boolean)
        .slice(0, 8),
      eyebrowTexts: [
        ...document.querySelectorAll('.ck-product-card__eyebrow, .ck-product-card__origin, [class*="eyebrow"]'),
      ]
        .map((el) => el.textContent.trim())
        .filter(Boolean),
      addButtonCount: [...document.querySelectorAll('button, a')].filter((el) =>
        /Ajouter au panier/i.test(el.textContent || el.getAttribute('aria-label') || el.getAttribute('title') || '')
      ).length,
      cardButtons,
      categoryLabels: [...document.querySelectorAll('a, button')]
        .map((el) => el.textContent.trim().replace(/\s+/g, ' '))
        .filter((text) =>
          [
            'Épicerie',
            'Boissons',
            'Maison & Bien-être',
            'Artisanat',
            'Coups de cœur',
            'Biscuits & crackers',
            'Confitures & douceurs',
            'Farines & manioc',
          ].includes(text)
        ),
      categoryLinks: [...document.querySelectorAll('a')]
        .map((el) => ({
          text: el.textContent.trim().replace(/\s+/g, ' '),
          href: el.getAttribute('href'),
        }))
        .filter((item) =>
          [
            'Épicerie',
            'Biscuits & crackers',
            'Confitures & douceurs',
            'Farines & manioc',
          ].includes(item.text)
        ),
      hasFiltersTitle: /FILTRES/.test(document.body.textContent),
      hasPriceFilter: /FOURCHETTE DE PRIX|Prix/i.test(document.body.textContent),
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
results.push(await checkPage('shop_desktop', '/shop', { width: 1280, height: 900 }));
results.push(await checkPage('epicerie_desktop', '/shop/category/epicerie-1', { width: 1280, height: 900 }));
results.push(await checkPage('shop_tablet', '/shop', { width: 800, height: 900 }));
results.push(await checkPage('shop_mobile', '/shop', { width: 390, height: 900 }));

const urlContext = await browser.newContext({ viewport: { width: 1280, height: 900 }, extraHTTPHeaders: headers });
const urlPage = await urlContext.newPage();
const categoryCandidates = [
  ...new Set(
    results
      .flatMap((result) => result.categoryLinks || [])
      .map((link) => link.href)
      .filter((href) => href && href.startsWith('/shop/category/'))
  ),
];
const urlStatuses = [];
for (const url of categoryCandidates) {
  const response = await urlPage
    .goto(`${BASE}${url}?db=${DB}`, { waitUntil: 'domcontentloaded', timeout: 20000 })
    .catch(() => null);
  urlStatuses.push({
    url,
    httpStatus: response?.status() || null,
    finalPath: new URL(urlPage.url()).pathname,
    h1: await urlPage.locator('h1').first().textContent().catch(() => null),
  });
}
await urlContext.close();

const cartContext = await browser.newContext({ viewport: { width: 1280, height: 900 }, extraHTTPHeaders: headers });
const cartPage = await cartContext.newPage();
await cartPage.goto(`${BASE}/shop?db=${DB}`, { waitUntil: 'networkidle', timeout: 45000 });
const beforeCart = await cartPage.locator('.my_cart_quantity').first().textContent().catch(() => null);
const firstCartButton = cartPage
  .locator('.ck-product-card--shop .a-submit, .ck-product-card--shop button[type="submit"], .oe_product .a-submit')
  .first();
const cartClick = { attempted: false, ok: false, beforeCart };
if (await firstCartButton.count()) {
  cartClick.attempted = true;
  await firstCartButton.click({ timeout: 10000 }).catch((error) => {
    cartClick.error = error.message;
  });
  await cartPage.waitForTimeout(2000);
  const afterCart = await cartPage.locator('.my_cart_quantity').first().textContent().catch(() => null);
  cartClick.afterCart = afterCart;
  cartClick.ok = (afterCart || '').trim() !== (beforeCart || '').trim() || /1/.test(afterCart || '');
}
await cartContext.close();

await browser.close();

const report = {
  generatedAt: new Date().toISOString(),
  base: BASE,
  db: DB,
  results,
  urlStatuses,
  cartClick,
  screenshots: OUT,
};

writeFileSync(`${OUT}/shop_recette_current_results.json`, JSON.stringify(report, null, 2));
console.log(JSON.stringify(report, null, 2));
