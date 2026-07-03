/**
 * Recette QA CATALOG-ARCHI-001 A+B+C.
 *
 * Controle le rendu public observable sans manipulation BO :
 * routes, header/footer, Home univers, cards, robots/noindex, overflow et erreurs JS.
 */
import { chromium } from 'playwright';
import { mkdir, writeFile } from 'node:fs/promises';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dir = dirname(fileURLToPath(import.meta.url));
const OUT = join(__dir, '..', 'captures', 'recette_catalog_archi_001_abc_20260703');
const DB = 'dorevia_ck_marketone_01';
const BASE = 'http://localhost:18079';
const headers = { 'Accept-Language': 'fr-FR,fr;q=0.9' };

const routes = [
  '/',
  '/shop',
  '/shop/category/epicerie-1',
  '/shop/category/boissons-123',
  '/shop/category/soin-bien-etre-2',
  '/shop/category/artisanat-3',
];

const viewports = {
  desktop_1280: { width: 1280, height: 900 },
  mobile_390: { width: 390, height: 844 },
};

function urlFor(path) {
  const sep = path.includes('?') ? '&' : '?';
  return `${BASE}${path}${sep}db=${DB}`;
}

async function visibleTextList(page, selector) {
  return page.evaluate((sel) => {
    const visible = (el) => {
      const style = window.getComputedStyle(el);
      const rect = el.getBoundingClientRect();
      return style.display !== 'none' && style.visibility !== 'hidden' && rect.width > 0 && rect.height > 0;
    };
    return [...document.querySelectorAll(sel)]
      .filter(visible)
      .map((el) => (el.textContent || '').replace(/\s+/g, ' ').trim())
      .filter(Boolean);
  }, selector);
}

async function auditPage(page, path) {
  const jsErrors = [];
  page.on('pageerror', (err) => jsErrors.push(err.message));
  page.on('console', (msg) => {
    if (msg.type() === 'error') {
      jsErrors.push(msg.text());
    }
  });

  const response = await page.goto(urlFor(path), { waitUntil: 'domcontentloaded', timeout: 120000 });
  await page.waitForTimeout(250);

  const base = await page.evaluate(() => {
    const doc = document.documentElement;
    const robots = document.querySelector('meta[name="robots"]')?.getAttribute('content') || '';
    const footer = document.querySelector('footer, #footer');
    const boutiqueTitle = [...document.querySelectorAll('footer h1, footer h2, footer h3, footer h4, #footer h1, #footer h2, #footer h3, #footer h4')]
      .find((el) => (el.textContent || '').trim().toLowerCase().includes('boutique'));
    const boutiqueColumn = boutiqueTitle?.closest('.col, [class*="col-"], div') || footer;
    const footerLinks = boutiqueColumn
      ? [...boutiqueColumn.querySelectorAll('a')].map((a) => ({
          text: (a.textContent || '').replace(/\s+/g, ' ').trim(),
          href: a.getAttribute('href') || '',
        })).filter((a) => a.text)
      : [];
    const headerLinks = [...document.querySelectorAll('header a, #top_menu a')]
      .filter((a) => {
        const style = window.getComputedStyle(a);
        const rect = a.getBoundingClientRect();
        return style.display !== 'none' && style.visibility !== 'hidden' && rect.width > 0 && rect.height > 0;
      })
      .map((a) => ({
        text: (a.textContent || '').replace(/\s+/g, ' ').trim(),
        href: a.getAttribute('href') || '',
      }))
      .filter((a) => a.text);
    return {
      title: document.title,
      h1: [...document.querySelectorAll('h1')]
        .filter((h) => {
          const style = window.getComputedStyle(h);
          const rect = h.getBoundingClientRect();
          return style.display !== 'none' && style.visibility !== 'hidden' && rect.width > 0 && rect.height > 0;
        })
        .map((h) => (h.textContent || '').replace(/\s+/g, ' ').trim()),
      robots,
      noindex: robots.toLowerCase().includes('noindex'),
      overflow: doc.scrollWidth > doc.clientWidth + 1,
      scrollWidth: doc.scrollWidth,
      clientWidth: doc.clientWidth,
      headerLinks,
      footerLinks,
    };
  });

  let mobileDrawer = null;
  const viewport = page.viewportSize();
  if (viewport && viewport.width <= 600) {
    const toggler = page.locator('header .navbar-toggler, .navbar-toggler').first();
    if (await toggler.isVisible().catch(() => false)) {
      await toggler.click();
      await page.waitForTimeout(250);
      mobileDrawer = {
        opened: true,
        links: await visibleTextList(page, 'header a, #top_menu a, .navbar-collapse a, .offcanvas a'),
      };
    } else {
      mobileDrawer = { opened: false, links: [] };
    }
  }

  let home = null;
  if (path === '/') {
    home = await page.evaluate(() => ({
      universCards: [...document.querySelectorAll('.ck-univers-card')].map((card) => ({
        title: (card.querySelector('.ck-univers-card__title')?.textContent || '').replace(/\s+/g, ' ').trim(),
        coverHref: card.querySelector('.ck-univers-card__cover')?.getAttribute('href') || '',
        ctaHref: card.querySelector('.ck-univers-card__cta')?.getAttribute('href') || '',
      })),
      featuredProducts: [...document.querySelectorAll('.ck-featured-products .ck-product-card, .ck-featured-products article, .ck-featured-products .card')]
        .map((card) => ({
          text: (card.textContent || '').replace(/\s+/g, ' ').trim(),
          href: card.querySelector('a[href*="/shop/"]')?.getAttribute('href') || '',
        }))
        .filter((card) => card.text),
    }));
  }

  let shop = null;
  if (path.startsWith('/shop')) {
    shop = await page.evaluate(() => ({
      productCards: [...document.querySelectorAll('.oe_product, .o_wsale_product_grid_wrapper, .ck-product-card, article')]
        .map((card) => ({
          text: (card.textContent || '').replace(/\s+/g, ' ').trim(),
          href: card.querySelector('a[href*="/shop/"]')?.getAttribute('href') || '',
        }))
        .filter((card) => card.text && card.href),
    }));
  }

  return {
    status: response?.status() || null,
    finalUrl: page.url(),
    ...base,
    mobileDrawer,
    jsErrors,
    home,
    shop,
  };
}

await mkdir(OUT, { recursive: true });

const browser = await chromium.launch({ headless: true });
const results = { date: '2026-07-03', base: BASE, db: DB, viewports: {}, sitemap: null };

for (const [name, viewport] of Object.entries(viewports)) {
  const ctx = await browser.newContext({ viewport, extraHTTPHeaders: headers });
  results.viewports[name] = {};
  for (const path of routes) {
    const page = await ctx.newPage();
    results.viewports[name][path] = await auditPage(page, path);
    await page.close();
  }
  await ctx.close();
}

{
  const ctx = await browser.newContext({ extraHTTPHeaders: headers });
  const page = await ctx.newPage();
  const response = await page.goto(urlFor('/sitemap.xml'), { waitUntil: 'domcontentloaded', timeout: 120000 });
  const text = await page.locator('body').textContent();
  results.sitemap = {
    status: response?.status() || null,
    hasEpicerie: text.includes('epicerie-1'),
    hasBoissons: text.includes('boissons-123'),
    hasSoin: text.includes('soin-bien-etre-2'),
    hasArtisanat: text.includes('artisanat-3'),
  };
  await ctx.close();
}

await browser.close();

await writeFile(join(OUT, 'recette_catalog_archi_001_abc_results.json'), JSON.stringify(results, null, 2));
console.log(JSON.stringify(results, null, 2));
