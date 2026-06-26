/**
 * Recette QA — Card Shop alignée canon Homepage (67.0)
 * Critères : pas d'eyebrow origine · méta unifiée · pied desktop ligne · CTA compact
 */
import { chromium } from 'playwright';
import { mkdirSync, writeFileSync } from 'node:fs';

const DB = 'dorevia_ck_marketone_01';
const BASE = 'http://localhost:18079';
const OUT =
  '/Users/doreviateam/dorevia-saas/odoo19-addons-dorevia/dorevia_ck_marketone/docs/design/maquette_01.2/captures/card_shop_canon_home_20260626';
const headers = { 'X-Odoo-Database': DB };

const VIEWPORTS = {
  desktop1280: { width: 1280, height: 900 },
  mobile390: { width: 390, height: 900 },
};

const ROUTES = [
  { key: 'home', label: 'Home', path: '/', scope: 'home' },
  { key: 'shop', label: 'Boutique', path: '/shop', scope: 'shop' },
  { key: 'epicerie', label: 'Épicerie', path: '/shop/category/epicerie-1', scope: 'shop' },
  { key: 'soin', label: 'Soin', path: '/shop/category/soin-bien-etre-2', scope: 'shop' },
  { key: 'artisanat', label: 'Artisanat', path: '/shop/category/artisanat-3', scope: 'shop' },
];

mkdirSync(OUT, { recursive: true });

async function resolveRoute(page, path) {
  const url = `${BASE}${path}?db=${DB}`;
  const response = await page.goto(url, { waitUntil: 'networkidle', timeout: 45000 });
  return { url, httpStatus: response?.status() ?? null };
}

function extractPageData({ scope, viewportKey }) {
  const isMobile = viewportKey === 'mobile390';

  function rect(el) {
    if (!el) return null;
    const r = el.getBoundingClientRect();
    return {
      x: Math.round(r.x),
      y: Math.round(r.y),
      top: Math.round(r.top),
      left: Math.round(r.left),
      right: Math.round(r.right),
      bottom: Math.round(r.bottom),
      width: Math.round(r.width),
      height: Math.round(r.height),
    };
  }

  const html = document.documentElement;
  const body = document.body;
  const isShop = scope === 'shop';
  const overflow =
    html.scrollWidth > html.clientWidth + 1 || body.scrollWidth > body.clientWidth + 1;

  const originEyebrows = [...document.querySelectorAll('.ck-product-card__origin')];
  const shopCards = [...document.querySelectorAll('form.ck-product-card--shop')];
  const homeCards = [...document.querySelectorAll('.ck-product-card--home')];

  const cardSamples = (isShop ? shopCards : homeCards).slice(0, 4).map((card) => {
    const title = card.querySelector('.ck-product-card__title, .o_wsale_products_item_title, h3.product-card-title');
    const meta = card.querySelector('.ck-product-card__meta, .product-card-labels');
    const foot = card.querySelector('.ck-product-card__foot, .o_wsale_product_sub, .product-card-foot');
    const price = card.querySelector('.ck-product-card__price, .product_price');
    const cta = card.querySelector('.card-cart-cta, .o_wsale_product_btn_primary');
    const titleRect = rect(title);
    const metaRect = rect(meta);
    const footRect = rect(foot);
    const priceRect = rect(price);
    const ctaRect = rect(cta);
    const cardRect = rect(card);
    const footStyle = foot ? getComputedStyle(foot) : null;
    const ctaStyle = cta ? getComputedStyle(cta) : null;
    const metaText = (meta?.textContent || '').trim().replace(/\s+/g, ' ');
    const titleText = (title?.textContent || '').trim().replace(/\s+/g, ' ');

    const footColumnish =
      !!priceRect &&
      !!ctaRect &&
      ctaRect.top >= priceRect.bottom - 4;

    const sameLineDesktopish =
      !!priceRect &&
      !!ctaRect &&
      ctaRect.top <= priceRect.bottom + 6 &&
      ctaRect.bottom >= priceRect.top - 6;

    const fullWidthish = !!ctaRect && !!cardRect && ctaRect.width >= cardRect.width * 0.72;

    const ctaVisible =
      !!cta &&
      ctaStyle?.visibility !== 'hidden' &&
      ctaStyle?.display !== 'none' &&
      (ctaRect?.height ?? 0) > 0 &&
      (ctaRect?.width ?? 0) > 0;

    const hasSeparator =
      !!footStyle &&
      parseFloat(footStyle.borderTopWidth || '0') > 0 &&
      footStyle.borderTopStyle !== 'none';

    const orphanSeparator =
      /^·|·$|·\s*·/.test(metaText) || metaText === '·';

    const originBeforeTitle =
      !!metaRect &&
      !!titleRect &&
      metaRect.top < titleRect.top - 1 &&
      /^[A-ZÀÂÄÉÈÊËÏÎÔÙÛÜŸ\s-]+$/.test(metaText.split('·')[0]?.trim() || '') &&
      !metaText.includes('·');

    return {
      titleText,
      metaText,
      originEyebrowInCard: !!card.querySelector('.ck-product-card__origin'),
      metaAfterTitle: metaRect && titleRect ? metaRect.top >= titleRect.top - 1 : null,
      footColumnish,
      sameLineDesktopish,
      fullWidthish,
      ctaVisible,
      ctaHeight: ctaRect?.height ?? 0,
      ctaWidth: ctaRect?.width ?? 0,
      hasSeparator,
      orphanSeparator,
      originBeforeTitle,
      cardRect,
      priceRect,
      ctaRect,
    };
  });

  const toolbar = document.querySelector('#o_wsale_products_header, .o_wsale_products_header_is_shop');
  const toolbarRect = rect(toolbar);
  const toolbarStyle = toolbar ? getComputedStyle(toolbar) : null;

  return {
    overflow,
    originEyebrowCount: originEyebrows.length,
    shopCardCount: shopCards.length,
    homeCardCount: homeCards.length,
    cardSamples,
    toolbarVisible:
      !!toolbar &&
      toolbarStyle?.display !== 'none' &&
      (toolbarRect?.height ?? 0) > 0 &&
      toolbarStyle?.visibility !== 'hidden',
    hasHomeFeatured: !!document.querySelector('.ck-featured-products--maquette'),
    pprCss:
      document
        .querySelector('#o_wsale_products_grid')
        ?.style.getPropertyValue('--o-wsale-ppr') || '',
  };
}

function evaluateRoute(result, viewportKey) {
  const failures = [];
  const isMobile = viewportKey === 'mobile390';
  const isShop = result.scope === 'shop';
  const samples = result.cardSamples || [];

  if (result.httpStatus !== 200) failures.push(`HTTP ${result.httpStatus}`);
  if (result.overflow) failures.push('overflow horizontal');

  if (isShop) {
    if (result.originEyebrowCount > 0) {
      failures.push(`eyebrow origine présent (${result.originEyebrowCount})`);
    }
    if (samples.some((s) => s.originEyebrowInCard)) {
      failures.push('ck-product-card__origin dans une card');
    }
    if (samples.some((s) => s.orphanSeparator)) {
      failures.push('séparateur orphelin dans méta');
    }
    if (samples.some((s) => !s.ctaVisible)) {
      failures.push('CTA invisible');
    }

    if (!isMobile) {
      if (samples.some((s) => s.footColumnish)) {
        failures.push('pied en colonne sur desktop (attendu prix|CTA ligne)');
      }
      if (samples.some((s) => !s.sameLineDesktopish)) {
        failures.push('prix et CTA pas sur la même ligne');
      }
      if (samples.some((s) => s.fullWidthish)) {
        failures.push('CTA trop large (pleine largeur desktop)');
      }
      if (samples.some((s) => s.ctaWidth > 160)) {
        failures.push('CTA largeur > 160px (compact attendu)');
      }
    } else {
      if (samples.some((s) => s.ctaHeight < 44)) {
        failures.push('CTA mobile hauteur < 44px');
      }
      if (!samples.every((s) => s.footColumnish || s.sameLineDesktopish)) {
        // mobile: colonne OK
      }
    }

    if (samples.some((s) => s.metaText && !s.metaAfterTitle)) {
      failures.push('méta pas sous le titre');
    }
    if (samples.some((s) => !s.hasSeparator)) {
      failures.push('séparateur pied manquant');
    }
  }

  if (result.key === 'home') {
    if (!result.hasHomeFeatured) failures.push('section vedettes absente');
    if ((result.homeCardCount || 0) < 1) failures.push('cards home absentes');
  }

  if (result.key === 'shop' && viewportKey === 'desktop1280') {
    if (result.pprCss !== '4') failures.push(`shop_ppr=${result.pprCss || '?'}`);
    if (!result.toolbarVisible) failures.push('toolbar catégorie invisible');
  }

  return failures;
}

const browser = await chromium.launch({ headless: true, channel: 'chrome' });
const results = [];
const failures = [];

for (const route of ROUTES) {
  for (const [viewportKey, viewport] of Object.entries(VIEWPORTS)) {
    if (route.key === 'home' && viewportKey !== 'desktop1280') continue;
    if (['artisanat', 'soin'].includes(route.key) && viewportKey === 'mobile390' && route.key !== 'shop') {
      if (route.key !== 'shop') continue;
    }
    // mobile390 : shop + artisanat seulement (brief)
    if (viewportKey === 'mobile390' && !['shop', 'artisanat'].includes(route.key)) continue;

    const context = await browser.newContext({ viewport, extraHTTPHeaders: headers });
    const page = await context.newPage();
    const shotName = `${route.key}_${viewportKey}`;
    const nav = await resolveRoute(page, route.path);
    await page.screenshot({ path: `${OUT}/${shotName}.png`, fullPage: false });
    const data = await page.evaluate(extractPageData, { scope: route.scope, viewportKey });
    await context.close();

    const entry = {
      kind: 'route',
      key: route.key,
      label: route.label,
      scope: route.scope,
      viewport: viewportKey,
      path: route.path,
      screenshot: `${OUT}/${shotName}.png`,
      httpStatus: nav.httpStatus,
      ...data,
    };
    const routeFailures = evaluateRoute(entry, viewportKey);
    entry.failures = routeFailures;
    if (routeFailures.length) {
      failures.push(...routeFailures.map((f) => `${shotName}: ${f}`));
    }
    results.push(entry);
  }
}

// Fonctionnel panier
const cartContext = await browser.newContext({
  viewport: VIEWPORTS.desktop1280,
  extraHTTPHeaders: headers,
});
const cartPage = await cartContext.newPage();
await cartPage.goto(`${BASE}/shop?db=${DB}`, { waitUntil: 'networkidle', timeout: 45000 });
const beforeCart = (await cartPage.locator('.my_cart_quantity').first().textContent().catch(() => '')) || '';
const btn = cartPage
  .locator('.ck-product-card--shop .card-cart-cta, .ck-product-card--shop .a-submit')
  .first();
let cartClick = { attempted: false, ok: false, beforeCart, afterCart: beforeCart };
if (await btn.count()) {
  cartClick.attempted = true;
  await btn.click({ timeout: 10000 }).catch((e) => {
    cartClick.error = e.message;
  });
  await cartPage.waitForTimeout(2000);
  cartClick.afterCart =
    (await cartPage.locator('.my_cart_quantity').first().textContent().catch(() => '')) || '';
  cartClick.ok = cartClick.afterCart.trim() !== beforeCart.trim();
}
await cartContext.close();
await browser.close();

if (cartClick.attempted && !cartClick.ok) {
  failures.push('panier: ajout non confirmé');
}

const report = {
  date: new Date().toISOString(),
  base: BASE,
  db: DB,
  modules: {
    theme: '19.0.1.67.0',
    content: '19.0.1.47.0',
  },
  outputDir: OUT,
  technicalPass: failures.length === 0,
  failureCount: failures.length,
  failures,
  cartClick,
  results,
};

writeFileSync(`${OUT}/card_shop_canon_home_results.json`, JSON.stringify(report, null, 2));
console.log(JSON.stringify({ technicalPass: report.technicalPass, failureCount: report.failureCount, failures }, null, 2));
