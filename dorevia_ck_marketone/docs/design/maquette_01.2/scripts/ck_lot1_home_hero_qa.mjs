import { chromium } from 'playwright';
import { mkdir, writeFile } from 'node:fs/promises';
import path from 'node:path';

const DB = 'dorevia_ck_marketone_01';
const ODOO = 'http://localhost:18079';
const MAQUETTE = 'http://127.0.0.1:8766/index.html';
const OUT = process.env.CK_LOT1_QA_OUT || '/private/tmp/ck_marketone_lot1_qa';
const headers = { 'X-Odoo-Database': DB };

await mkdir(OUT, { recursive: true });

const browser = await chromium.launch({ headless: true });
const report = { captures: [], checks: {}, maquette: {} };

async function captureOdoo(label, width, height) {
  const context = await browser.newContext({
    viewport: { width, height },
    extraHTTPHeaders: headers,
  });
  const page = await context.newPage();
  await page.goto(`${ODOO}/?db=${DB}`, { waitUntil: 'networkidle', timeout: 60000 });
  await page.waitForSelector('.ck-hero--marketone-v1', { timeout: 30000 });

  const hero = page.locator('.ck-hero--marketone-v1');
  const metrics = await page.evaluate(() => {
    const heroEl = document.querySelector('.ck-hero--marketone-v1');
    const rect = heroEl?.getBoundingClientRect();
    const title = heroEl?.querySelector('.ck-hero__title')?.textContent?.trim();
    const kicker = heroEl?.querySelector('.ck-hero__kicker')?.textContent?.trim();
    const visual = heroEl?.querySelector('.ck-hero__visual');
    const grid = heroEl?.querySelector('.ck-hero__grid');
    const gridStyle = grid ? getComputedStyle(grid) : null;
    const imgSrc = heroEl?.querySelector('.ck-hero__visual img')?.getAttribute('src') || null;
    const titleEl = heroEl?.querySelector('.ck-hero__title');
    const titleStyle = titleEl ? getComputedStyle(titleEl) : null;
    const primaryBtn = heroEl?.querySelector('.ck-hero__cta .btn-primary');
    const secondaryBtn = heroEl?.querySelector('.ck-hero__cta .btn-secondary');
    const primaryStyle = primaryBtn ? getComputedStyle(primaryBtn) : null;
    const secondaryStyle = secondaryBtn ? getComputedStyle(secondaryBtn) : null;
    return {
      scrollWidth: document.documentElement.scrollWidth,
      clientWidth: document.documentElement.clientWidth,
      overflow: document.documentElement.scrollWidth > document.documentElement.clientWidth + 1,
      heroHeight: rect?.height ?? null,
      gridColumns: gridStyle?.gridTemplateColumns ?? null,
      gridGap: gridStyle?.gap ?? null,
      title,
      titleLines: titleEl ? Math.round(titleEl.getBoundingClientRect().height / parseFloat(titleStyle?.lineHeight || '1')) : null,
      titleWhiteSpace: titleStyle?.whiteSpace ?? null,
      titleScrollWidth: titleEl?.scrollWidth ?? null,
      titleClientWidth: titleEl?.clientWidth ?? null,
      titleOverflow: titleEl ? titleEl.scrollWidth > titleEl.clientWidth + 1 : null,
      titleOverlapsVisual: (() => {
        const visualCol = heroEl?.querySelector('.ck-hero__visual-col');
        if (!titleEl || !visualCol) return null;
        return titleEl.getBoundingClientRect().right > visualCol.getBoundingClientRect().left + 1;
      })(),
      contentWidth: heroEl?.querySelector('.ck-hero__content')?.getBoundingClientRect().width ?? null,
      kicker,
      shopCta: !!heroEl?.querySelector('a[href="/shop"]'),
      proCta: !!heroEl?.querySelector('a[href="/professionnels"]'),
      noCoverDefault: !document.body.innerHTML.includes('website.s_cover_default_image'),
      visualHeight: visual?.getBoundingClientRect().height ?? null,
      visualMedia: !!heroEl?.querySelector('.ck-hero__visual-media, .ck-hero__visual--editorial'),
      visualVisible: (visual?.getBoundingClientRect().height ?? 0) >= 100,
      imgSrc,
      heroStaticAsset: imgSrc?.includes('ck_hero_home_v1') ?? false,
      carouselInVisual: !!heroEl?.querySelector('.ck-hero__visual .ck-hero__visual-carousel'),
      carouselSlideCount: heroEl?.querySelectorAll('.ck-hero__visual .carousel-item').length ?? 0,
      carouselInContent: !!heroEl?.querySelector('.ck-hero__content [data-bs-ride="carousel"]'),
      primaryBg: primaryStyle?.backgroundColor ?? null,
      secondaryBg: secondaryStyle?.backgroundColor ?? null,
      secondaryBorder: secondaryStyle?.borderColor ?? null,
      featuredAfter: (() => {
        const h = document.querySelector('.ck-hero--marketone-v1');
        const f = document.querySelector('.ck-featured-products');
        return h && f ? h.getBoundingClientRect().top < f.getBoundingClientRect().top : null;
      })(),
    };
  });

  const fullPath = path.join(OUT, `lot1_odoo_${label}_full.png`);
  const heroPath = path.join(OUT, `lot1_odoo_${label}_hero.png`);
  await page.screenshot({ path: fullPath, fullPage: false });
  await hero.screenshot({ path: heroPath });

  report.captures.push({ source: 'odoo', label, width, height, fullPath, heroPath });
  report.checks[label] = metrics;
  await context.close();
}

async function captureMaquette(label, width, height) {
  const context = await browser.newContext({ viewport: { width, height } });
  const page = await context.newPage();
  await page.goto(MAQUETTE, { waitUntil: 'networkidle', timeout: 60000 });
  await page.waitForSelector('.hero', { timeout: 30000 });
  const hero = page.locator('.hero');
  const metrics = await page.evaluate(() => {
    const heroEl = document.querySelector('.hero');
    const rect = heroEl?.getBoundingClientRect();
    const grid = heroEl?.querySelector('.hero-grid');
    const gridStyle = grid ? getComputedStyle(grid) : null;
    const visual = heroEl?.querySelector('.hero-visual');
    return {
      heroHeight: rect?.height ?? null,
      gridColumns: gridStyle?.gridTemplateColumns ?? null,
      gridGap: gridStyle?.gap ?? null,
      visualHeight: visual?.getBoundingClientRect().height ?? null,
      title: document.getElementById('hero-title')?.textContent?.trim(),
    };
  });
  const heroPath = path.join(OUT, `lot1_maquette_${label}_hero.png`);
  await hero.screenshot({ path: heroPath });
  report.maquette[label] = metrics;
  report.captures.push({ source: 'maquette', label, width, height, heroPath });
  await context.close();
}

for (const [label, w, h] of [
  ['desktop_1280', 1280, 900],
  ['desktop_1440', 1440, 900],
  ['mobile_390', 390, 844],
]) {
  await captureOdoo(label, w, h);
  await captureMaquette(label, w, h);
}

const odoo1280 = report.checks.desktop_1280 || {};
report.summary = {
  titleMaquette: odoo1280.title === 'Les saveurs créoles, prêtes à commander.',
  kickerPresent: !!odoo1280.kicker?.includes('Boutique créole'),
  dualCta: odoo1280.shopCta && odoo1280.proCta,
  noCoverDefault: odoo1280.noCoverDefault,
  noOverflowMobile: !report.checks.mobile_390?.overflow,
  featuredOrder: odoo1280.featuredAfter === true,
  heroCompactDesktop: odoo1280.heroHeight != null && odoo1280.heroHeight < 520,
  h1SingleLineDesktop:
    (report.checks.desktop_1440?.titleLines ?? 2) <= 1
    && (report.checks.desktop_1280?.titleLines ?? 2) <= 1,
  h1FullyVisibleDesktop:
    report.checks.desktop_1440?.titleOverflow === false
    && report.checks.desktop_1280?.titleOverflow === false
    && report.checks.desktop_1440?.titleOverlapsVisual === false
    && report.checks.desktop_1280?.titleOverlapsVisual === false,
  heroStaticAsset: odoo1280.heroStaticAsset === true,
  carouselImageOnly: odoo1280.carouselInVisual === true && odoo1280.carouselInContent === false,
  carouselSlideBounded: (odoo1280.carouselSlideCount ?? 0) >= 1 && (odoo1280.carouselSlideCount ?? 0) <= 3,
  visualBounded: (odoo1280.visualHeight ?? 0) >= 140 && (odoo1280.visualHeight ?? 0) <= 240,
  visualVisible: odoo1280.visualVisible === true,
};

await writeFile(path.join(OUT, 'lot1_qa_report.json'), JSON.stringify(report, null, 2));
console.log(JSON.stringify(report.summary, null, 2));
await browser.close();
