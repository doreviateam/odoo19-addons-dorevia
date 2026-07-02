/**
 * CK-HOME-POLISH-001 — Addendum QA post-GO (vigilance non bloquante).
 * Usage: node ck_home_polish_postgo_qa.mjs
 */
import { chromium, firefox } from 'playwright';
import { mkdir, writeFile } from 'node:fs/promises';
import path from 'node:path';

const BASE = process.env.CK_QA_BASE || 'http://localhost:18079';
const DB = process.env.CK_QA_DB || 'dorevia_ck_marketone_01';
const OUT = process.env.CK_POSTGO_QA_OUT || '/private/tmp/ck_home_polish_postgo_qa';
const headers = { 'X-Odoo-Database': DB, 'Accept-Language': 'fr-FR,fr;q=0.9' };

await mkdir(OUT, { recursive: true });

const report = {
  base: BASE,
  timestamp: new Date().toISOString(),
  checks: {},
  captures: [],
};

function pass(id, ok, detail = {}) {
  report.checks[id] = { ok, ...detail };
  const mark = ok ? 'OK' : 'KO';
  console.log(`[${mark}] ${id}`, detail.summary || '');
}

async function headerNav(page) {
  return page.locator('header#top').innerHTML();
}

function countWishBadges(html) {
  const visible = [...html.matchAll(/<sup[^>]*my_wish_quantity[^>]*>([^<]*)<\/sup>/g)];
  return visible.map((m) => m[1].trim());
}

function countCartBadges(html) {
  const visible = [...html.matchAll(/<sup[^>]*my_cart_quantity[^>]*>([^<]*)<\/sup>/g)];
  return visible.map((m) => m[1].trim());
}

/** 1 — Cycle badge favoris */
async function checkWishlistCycle() {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    viewport: { width: 1280, height: 900 },
    extraHTTPHeaders: headers,
  });
  const page = await context.newPage();

  await page.goto(`${BASE}/shop?db=${DB}`, { waitUntil: 'networkidle', timeout: 60000 });

  const productLink = page.locator('.oe_product_cart a[href*="/shop/"]').first();
  await productLink.waitFor({ timeout: 30000 });
  const productHref = await productLink.getAttribute('href');
  await page.goto(`${BASE}${productHref}`, { waitUntil: 'networkidle' });

  let nav0 = await headerNav(page);
  const badges0 = countWishBadges(nav0);
  pass('wishlist_initial_no_zero_badge', badges0.every((b) => b !== '0') && badges0.length === 0, {
    summary: `badges initiaux: ${JSON.stringify(badges0)}`,
    badges: badges0,
  });

  const wishBtn = page.locator(
    'button.o_add_wishlist, a.o_add_wishlist, .o_add_wishlist_dyn',
  ).first();
  await wishBtn.click({ timeout: 15000 });
  await page.waitForTimeout(1200);

  await page.goto(`${BASE}/?db=${DB}`, { waitUntil: 'networkidle' });
  let nav1 = await headerNav(page);
  const badges1 = countWishBadges(nav1);
  pass('wishlist_add_shows_badge', badges1.some((b) => parseInt(b, 10) >= 1), {
    summary: `après ajout: ${JSON.stringify(badges1)}`,
    badges: badges1,
  });

  await page.goto(`${BASE}/shop/wishlist?db=${DB}`, { waitUntil: 'networkidle' });
  const removeBtn = page.locator(
    'a.o_wish_rm, button.o_wish_rm, .o_wish_rm',
  ).first();
  if (await removeBtn.count()) {
    await removeBtn.click();
    await page.waitForTimeout(1200);
  }

  await page.goto(`${BASE}/?db=${DB}`, { waitUntil: 'networkidle' });
  let nav2 = await headerNav(page);
  const badges2 = countWishBadges(nav2);
  pass('wishlist_remove_hides_badge', badges2.length === 0 || badges2.every((b) => b !== '0'), {
    summary: `après retrait: ${JSON.stringify(badges2)}`,
    badges: badges2,
  });

  await browser.close();
}

/** 2 — Viewport 375 px (iPhone SE) */
async function checkViewport375() {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({
    viewport: { width: 375, height: 667 },
    deviceScaleFactor: 2,
    isMobile: true,
    extraHTTPHeaders: headers,
  });
  const page = await context.newPage();
  await page.goto(`${BASE}/?db=${DB}`, { waitUntil: 'networkidle', timeout: 60000 });
  await page.locator('.ck-featured-products').scrollIntoViewIfNeeded();
  await page.waitForTimeout(400);

  const metrics = await page.evaluate(() => {
    const doc = document.documentElement;
    const cards = [...document.querySelectorAll('.ck-product-card--home')].slice(0, 4);
    const prices = cards.map((card) => {
      const el = card.querySelector('.ck-product-card__price-value, .price');
      const rect = el?.getBoundingClientRect();
      const cardRect = card.getBoundingClientRect();
      const style = el ? getComputedStyle(el) : null;
      return {
        text: el?.textContent?.trim() || null,
        fontSize: style?.fontSize || null,
        fontWeight: style?.fontWeight || null,
        overflowRight: rect && cardRect ? rect.right > cardRect.right + 1 : false,
        clipped: rect && cardRect ? rect.width > cardRect.width : false,
      };
    });
    return {
      scrollWidth: doc.scrollWidth,
      clientWidth: doc.clientWidth,
      horizontalOverflow: doc.scrollWidth > doc.clientWidth + 1,
      cardCount: cards.length,
      prices,
      anyPriceOverflow: prices.some((p) => p.overflowRight || p.clipped),
    };
  });

  const shot = path.join(OUT, 'home_mobile_375_featured.png');
  await page.locator('.ck-featured-products').screenshot({ path: shot });
  report.captures.push(shot);

  const priceOk = metrics.prices.every(
    (p) => p.fontSize === '15px' && (p.fontWeight === '700' || p.fontWeight === 'bold'),
  );
  pass('viewport375_no_horizontal_overflow', !metrics.horizontalOverflow, {
    summary: `${metrics.scrollWidth}/${metrics.clientWidth}px`,
    ...metrics,
  });
  pass('viewport375_price_typography', priceOk, {
    summary: metrics.prices.map((p) => `${p.fontSize}/${p.fontWeight}`).join(', '),
    prices: metrics.prices,
  });
  pass('viewport375_price_no_clip', !metrics.anyPriceOverflow, {
    summary: metrics.anyPriceOverflow ? 'débordement prix détecté' : 'prix dans les cards',
  });

  await browser.close();
}

/** 3 — Firefox desktop */
async function checkFirefoxDesktop() {
  const browser = await firefox.launch({ headless: true });
  const context = await browser.newContext({
    viewport: { width: 1280, height: 900 },
    extraHTTPHeaders: headers,
  });
  const page = await context.newPage();
  await page.goto(`${BASE}/?db=${DB}`, { waitUntil: 'networkidle', timeout: 60000 });

  const metrics = await page.evaluate(() => {
    const header = document.querySelector('header#top');
    const trust = document.querySelector('.ck-reassurance--trust-bar');
    const hero = document.querySelector('.ck-hero--marketone-v1');
    const doc = document.documentElement;
    const heart = header?.querySelector('.fa-heart, .ck-header__wish-icon');
    const cart = header?.querySelector('.fa-shopping-cart, .ck-header__cart-icon');
    const trustItems = trust ? trust.querySelectorAll('.ck-reassurance__item').length : 0;
    return {
      horizontalOverflow: doc.scrollWidth > doc.clientWidth + 1,
      headerVisible: !!header && header.offsetHeight > 0,
      heartVisible: !!heart && heart.offsetParent !== null,
      cartVisible: !!cart && cart.offsetParent !== null,
      trustItems,
      heroCtaPrimary: !!hero?.querySelector('.ck-hero__cta .btn-primary'),
      newsletterGone: !document.body.textContent.includes('Merci pour votre inscription'),
      proOnly: !!document.querySelector('.ck-dual-engage--pro-only'),
    };
  });

  const shot = path.join(OUT, 'home_firefox_1280.png');
  await page.screenshot({ path: shot, fullPage: false });
  report.captures.push(shot);

  pass('firefox_no_overflow', !metrics.horizontalOverflow, { summary: 'Gecko 1280' });
  pass('firefox_header_icons', metrics.heartVisible && metrics.cartVisible, metrics);
  pass('firefox_trust_bar', metrics.trustItems === 4, { summary: `${metrics.trustItems} items` });
  pass('firefox_polish_markers', metrics.newsletterGone && metrics.proOnly && metrics.heroCtaPrimary, metrics);

  await browser.close();
}

/** 4 — Doctrine /kits */
async function checkKitsRoute() {
  const res301 = await fetch(`${BASE}/kits`, {
    headers: { ...headers, 'X-Odoo-Database': DB },
    redirect: 'manual',
  });
  const location = res301.headers.get('location') || '';
  pass('kits_301_redirect', res301.status === 301 && location.includes('marketone_mode=pack'), {
    summary: `${res301.status} → ${location}`,
    status: res301.status,
    location,
  });

  const resFinal = await fetch(`${BASE}/kits`, {
    headers: { ...headers, 'X-Odoo-Database': DB },
    redirect: 'follow',
  });
  const finalUrl = resFinal.url;
  pass('kits_final_shop_pack', resFinal.status === 200 && finalUrl.includes('marketone_mode=pack'), {
    summary: finalUrl,
    status: resFinal.status,
  });

  const sitemap = await fetch(`${BASE}/sitemap.xml`, { headers }).then((r) => r.text()).catch(() => '');
  pass('kits_not_in_sitemap', !sitemap.includes('/kits'), {
    summary: sitemap.includes('/kits') ? '/kits présent dans sitemap' : 'absent (sitemap=False)',
  });

  const homeHtml = await fetch(`${BASE}/?db=${DB}`, { headers }).then((r) => r.text());
  const kitsLinkInCoffret = /ck-discovery-pack[\s\S]{0,4000}href="\/kits"/.test(homeHtml);
  pass('kits_link_on_home_coffret', kitsLinkInCoffret, {
    summary: 'CTA coffret pointe /kits (porte SEO-friendly)',
  });
}

await checkWishlistCycle();
await checkViewport375();
await checkFirefoxDesktop();
await checkKitsRoute();

report.allOk = Object.values(report.checks).every((c) => c.ok);
const reportPath = path.join(OUT, 'report.json');
await writeFile(reportPath, JSON.stringify(report, null, 2));

console.log('\n---');
console.log(`Rapport: ${reportPath}`);
console.log(`Verdict global: ${report.allOk ? 'GO vigilance' : 'AU MOINS UN KO'}`);
process.exit(report.allOk ? 0 : 1);
