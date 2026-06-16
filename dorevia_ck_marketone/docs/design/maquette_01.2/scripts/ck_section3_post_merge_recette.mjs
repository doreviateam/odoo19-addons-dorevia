import { chromium } from 'playwright';
import { mkdir, writeFile } from 'node:fs/promises';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const DB = 'dorevia_ck_marketone_01';
const ODOO = 'http://localhost:18079';
const SCRIPT_DIR = path.dirname(fileURLToPath(import.meta.url));
const OUT = process.env.CK_S3_RECETTE_OUT
  || path.join(SCRIPT_DIR, '..', 'captures', 'recette_section3_post_merge');
const headers = { 'X-Odoo-Database': DB };

await mkdir(OUT, { recursive: true });

const browser = await chromium.launch({ headless: true });
const report = { captures: [], checks: {}, cards: [] };

async function captureSection3(label, width, height) {
  const context = await browser.newContext({
    viewport: { width, height },
    extraHTTPHeaders: headers,
  });
  const page = await context.newPage();
  await page.goto(`${ODOO}/?db=${DB}`, { waitUntil: 'networkidle', timeout: 60000 });
  await page.waitForSelector('.ck-featured-products--maquette', { timeout: 30000 });

  const section = page.locator('.ck-featured-products--maquette');
  await section.scrollIntoViewIfNeeded();

  const metrics = await page.evaluate(() => {
    const sectionEl = document.querySelector('.ck-featured-products--maquette');
    const grid = sectionEl?.querySelector('.ck-featured-products__grid--stable');
    const cards = [...(grid?.querySelectorAll('.ck-product-card') || [])];
    const cardData = cards.map((card) => {
      const media = card.querySelector('.product-card-media');
      const mediaStyle = media ? getComputedStyle(media) : null;
      const bg = mediaStyle?.backgroundImage || '';
      const rect = media?.getBoundingClientRect();
      const title = card.querySelector('.card-title, h3, .ck-product-card__title')?.textContent?.trim()
        || card.querySelector('[class*="title"]')?.textContent?.trim();
      const cta = card.querySelector('.card-cta, a.btn');
      return {
        title: title || card.textContent?.slice(0, 80).trim(),
        href: cta?.getAttribute('href') || null,
        mediaHeight: rect?.height ?? 0,
        mediaWidth: rect?.width ?? 0,
        hasBackgroundImage: bg.includes('url(') && !bg.includes('url("")') && bg !== 'none',
        backgroundImageSnippet: bg.slice(0, 120),
      };
    });

    const hero = document.querySelector('.ck-hero--marketone-v1');
    const trust = document.querySelector('.ck-reassurance--trust-bar');
    const featured = document.querySelector('.ck-featured-products');

    return {
      scrollWidth: document.documentElement.scrollWidth,
      clientWidth: document.documentElement.clientWidth,
      overflow: document.documentElement.scrollWidth > document.documentElement.clientWidth + 1,
      sectionTitle: sectionEl?.querySelector('h2')?.textContent?.trim() || null,
      hasMaquetteClass: !!sectionEl,
      cardCount: cards.length,
      cards: cardData,
      orderHeroTrustFeatured: hero && trust && featured
        ? hero.getBoundingClientRect().top < trust.getBoundingClientRect().top
          && trust.getBoundingClientRect().top < featured.getBoundingClientRect().top
        : null,
      heroInterval: document.body.innerHTML.includes('data-bs-interval="25000"'),
      noNativeCarousel: !sectionEl?.innerHTML.includes('s_dynamic_snippet_products'),
      noProductCart: !sectionEl?.innerHTML.includes('oe_product_cart'),
    };
  });

  const sectionPath = path.join(OUT, `section3_odoo_${label}.png`);
  await section.screenshot({ path: sectionPath });

  report.captures.push({ label, width, height, sectionPath });
  report.checks[label] = metrics;
  if (label === '1280') report.cards = metrics.cards;
  await context.close();
}

for (const [label, w, h] of [['1280', 1280, 800], ['390', 390, 844]]) {
  await captureSection3(label, w, h);
}

await browser.close();
await writeFile(path.join(OUT, 'recette_section3_post_merge_report.json'), JSON.stringify(report, null, 2));
console.log(JSON.stringify(report, null, 2));
