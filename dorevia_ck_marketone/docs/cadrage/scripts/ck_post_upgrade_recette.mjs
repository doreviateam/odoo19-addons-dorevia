/**
 * Recette QA post-upgrade sandbox — Home + Nav + Univers + Mobile 390
 */
import { chromium } from 'playwright';
import { writeFile } from 'node:fs/promises';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dir = dirname(fileURLToPath(import.meta.url));
const OUT = join(__dir, '..', 'captures', 'recette_post_upgrade_20260703');
const DB = 'dorevia_ck_marketone_01';
const BASE = 'http://localhost:18079';
const headers = { 'X-Odoo-Database': DB, 'Accept-Language': 'fr-FR,fr;q=0.9' };

const UNIVERSES = [
  { key: 'epicerie', label: 'Épicerie' },
  { key: 'boissons', label: 'Boissons' },
  { key: 'soin', label: 'Soin' },
  { key: 'artisanat', label: 'Artisanat' },
];

async function visibleH1Count(page) {
  return page.evaluate(() =>
    [...document.querySelectorAll('h1')].filter((h) => {
      const c = h.className || '';
      return !c.includes('d-none') && !c.includes('visually-hidden');
    }).length
  );
}

async function auditHome(page) {
  return page.evaluate(() => {
    const doc = document.documentElement;
    const grid = document.querySelector('.ck-featured-products__grid--stable');
    const imgs = grid ? grid.querySelectorAll('.ck-product-card__img').length : 0;
    const visibleImgs = grid
      ? [...grid.querySelectorAll('.ck-product-card__img')].filter((i) => i.getBoundingClientRect().height > 0).length
      : 0;
    const disc = document.querySelector('.ck-discovery-pack');
    const discHtml = disc?.outerHTML || '';
    return {
      overflow: doc.scrollWidth > doc.clientWidth + 1,
      scrollWidth: doc.scrollWidth,
      clientWidth: doc.clientWidth,
      heroTitle: document.querySelector('#hero-title, .ck-hero--marketone-v1 h1')?.textContent?.trim() || '',
      newsletterForm: !!document.querySelector('.ck-dual-engage form.s_website_form, .ck-featured-products form.s_website_form'),
      featuredImgs: visibleImgs,
      featuredImgTotal: imgs,
      coffretNoFallback: !discHtml.includes('ck-discovery-pack__visual--editorial'),
      coffretVisual: /\/web\/image\/product\./.test(discHtml),
      ctaKits: disc?.querySelector('.ck-discovery-pack__cta')?.getAttribute('href') === '/kits',
      noStretchedLink: !discHtml.includes('stretched-link'),
      blockOrder: ['hero', 'reassurance', 'featured', 'univers', 'coffret', 'dual', 'editorial'].filter((n) => {
        const map = {
          hero: '.ck-hero--marketone-v1',
          reassurance: '.ck-reassurance--trust-bar, [data-snippet="s_ck_reassurance"]',
          featured: '.ck-featured-products',
          univers: '.ck-univers-cards, [data-snippet="s_ck_category_links"]',
          coffret: '.ck-discovery-pack',
          dual: '.ck-dual-engage, .s_ck_pro_banner',
          editorial: '.ck-home-editorial',
        };
        return !!document.querySelector(map[n]);
      }),
    };
  });
}

async function auditHeader(page, mobile) {
  return page.evaluate((isMobile) => {
    const hearts = document.querySelectorAll('#top_menu .fa-heart, header .o_wsale_my_wish, header [href*="wishlist"]');
    const carts = document.querySelectorAll('#top_menu .fa-shopping-cart, header .o_wsale_my_cart, header [href*="/shop/cart"]');
    const wishBadge = document.querySelector('.o_wsale_my_wish .my_wish_quantity, .o_wsale_my_wish .badge');
    const cartBadge = document.querySelector('.o_wsale_my_cart .my_cart_quantity, .o_wsale_my_cart .badge');
    const wishBadgeHidden = !wishBadge || wishBadge.classList.contains('d-none') || wishBadge.textContent.trim() === '0';
    const cartBadgeHidden = !cartBadge || cartBadge.classList.contains('d-none') || cartBadge.textContent.trim() === '0';
    const menu = document.querySelector('#top_menu');
    const menuText = menu?.textContent || '';
    return {
      hasHeart: hearts.length > 0,
      hasCart: carts.length > 0,
      wishBadgeHiddenAtZero: wishBadgeHidden,
      cartBadgeHiddenAtZero: cartBadgeHidden,
      menuHasBoutique: menuText.includes('Boutique'),
      menuHasEpicerie: menuText.includes('Épicerie'),
      menuHasBoissons: menuText.includes('Boissons'),
      menuHasSoin: menuText.includes('Soin'),
      menuHasArtisanat: menuText.includes('Artisanat'),
      mobileDrawer: isMobile ? !!document.querySelector('.navbar-toggler, #top_menu_collapse') : true,
    };
  }, mobile);
}

async function auditShopCategory(page, expectBanner) {
  const data = await page.evaluate(() => ({
    hasBanner: !!document.querySelector('.ck-univers-banner'),
    hasCompact: !!document.querySelector('.ck-shop-intro--title-only'),
    overflow: document.documentElement.scrollWidth > document.documentElement.clientWidth + 1,
    scrollWidth: document.documentElement.scrollWidth,
    clientWidth: document.documentElement.clientWidth,
  }));
  const h1 = await visibleH1Count(page);
  return { ...data, h1Count: h1, bannerOk: data.hasBanner === expectBanner };
}

const browser = await chromium.launch({ headless: true });
const results = { date: '2026-07-03', base: BASE, db: DB, routes: {}, viewports: {}, universes: {} };

// Routes HTTP
for (const path of ['/', '/shop', '/kits', '/shop/cart', '/producteurs']) {
  const ctx = await browser.newContext({ extraHTTPHeaders: headers });
  const p = await ctx.newPage();
  const r = path === '/kits'
    ? await p.goto(`${BASE}${path}?db=${DB}`, { waitUntil: 'domcontentloaded', timeout: 120000 })
    : await p.goto(`${BASE}${path}?db=${DB}`, { waitUntil: 'domcontentloaded', timeout: 120000 });
  results.routes[path] = { status: r?.status(), finalUrl: p.url() };
  await ctx.close();
}

// Desktop 1280 — Home + header + shop + univers sample
{
  const ctx = await browser.newContext({ viewport: { width: 1280, height: 900 }, extraHTTPHeaders: headers });
  const page = await ctx.newPage();
  await page.goto(`${BASE}/?db=${DB}`, { waitUntil: 'domcontentloaded', timeout: 120000 });
  results.viewports.desktop_1280 = {
    home: await auditHome(page),
    header: await auditHeader(page, false),
  };

  await page.goto(`${BASE}/shop?db=${DB}`, { waitUntil: 'domcontentloaded', timeout: 120000 });
  results.routes.shop_general = {
    ...(await auditShopCategory(page, false)),
    status: 200,
  };

  // Resolve epicerie link from header
  const epicerieHref = await page.evaluate(() => {
    const links = [...document.querySelectorAll('#top_menu a, header a')];
    const a = links.find((el) => (el.textContent || '').trim().startsWith('Épicerie'));
    return a?.getAttribute('href') || '';
  });
  if (epicerieHref) {
    await page.goto(epicerieHref.startsWith('http') ? epicerieHref : `${BASE}${epicerieHref}`, { waitUntil: 'domcontentloaded', timeout: 120000 });
    results.universes.epicerie_desktop = await auditShopCategory(page, true);
    results.routes.epicerie = { href: epicerieHref, finalUrl: page.url(), status: 200 };
  }

  await ctx.close();
}

// Mobile 390
{
  const ctx = await browser.newContext({ viewport: { width: 390, height: 844 }, extraHTTPHeaders: headers });
  const page = await ctx.newPage();
  await page.goto(`${BASE}/?db=${DB}`, { waitUntil: 'domcontentloaded', timeout: 120000 });
  results.viewports.mobile_390 = {
    home: await auditHome(page),
    header: await auditHeader(page, true),
  };

  if (results.routes.epicerie?.href) {
    const href = results.routes.epicerie.href;
    await page.goto(href.startsWith('http') ? href : `${BASE}${href}`, { waitUntil: 'domcontentloaded', timeout: 120000 });
    results.universes.epicerie_mobile = await auditShopCategory(page, true);
  }

  await ctx.close();
}

await browser.close();
await writeFile(join(OUT, 'recette_post_upgrade_results.json'), JSON.stringify(results, null, 2));
console.log(JSON.stringify(results, null, 2));
