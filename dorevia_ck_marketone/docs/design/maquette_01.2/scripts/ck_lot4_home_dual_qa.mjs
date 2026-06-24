import { chromium } from 'playwright';
import { mkdir, writeFile } from 'node:fs/promises';
import path from 'node:path';

const DB = 'dorevia_ck_marketone_01';
const BASE = 'http://localhost:18079';
const OUT = process.env.CK_LOT4_QA_OUT || '/private/tmp/ck_marketone_lot4_qa';
const headers = { 'X-Odoo-Database': DB };

await mkdir(OUT, { recursive: true });

const browser = await chromium.launch({ headless: true });
const report = { captures: [], checks: {} };

async function captureViewport(label, width, height) {
  const context = await browser.newContext({
    viewport: { width, height },
    extraHTTPHeaders: headers,
  });
  const page = await context.newPage();
  await page.goto(`${BASE}/?db=${DB}`, { waitUntil: 'networkidle', timeout: 60000 });
  await page.waitForSelector('.ck-dual-engage--compact', { timeout: 30000 });

  const dual = page.locator('.ck-dual-engage--compact');
  await dual.scrollIntoViewIfNeeded();
  await page.waitForTimeout(400);

  const metrics = await page.evaluate(() => {
    const dualEl = document.querySelector('.ck-dual-engage--compact');
    const packEl = document.querySelector('.ck-discovery-pack');
    const featuredEl = document.querySelector('.ck-featured-products');
    const proBanner = document.querySelector('.s_ck_pro_banner');
    const cols = dualEl ? [...dualEl.querySelectorAll('.col-lg-6')] : [];
    const colRects = cols.map((c) => c.getBoundingClientRect());
    const stacked = colRects.length >= 2
      ? colRects[1].top >= colRects[0].bottom - 4
      : null;
    const order = [featuredEl, packEl, dualEl].map((el) => el?.getBoundingClientRect().top ?? null);
    return {
      scrollWidth: document.documentElement.scrollWidth,
      clientWidth: document.documentElement.clientWidth,
      overflow: document.documentElement.scrollWidth > document.documentElement.clientWidth + 1,
      dualCompact: !!dualEl,
      proBanner: !!proBanner,
      proTitle: dualEl?.querySelector('.ck-dual-engage__pro')?.textContent?.includes('Vous êtes professionnel'),
      newsletter: !!document.querySelector('#ck-newsletter-subscribe'),
      emailInput: !!document.querySelector('#ck-newsletter-subscribe input[type="email"], .s_newsletter_subscribe_form input[type="email"]'),
      listId: document.querySelector('[data-list-id]')?.getAttribute('data-list-id') || null,
      rgpd: document.body.textContent.includes('Désinscription possible'),
      proCtaHref: dualEl?.querySelector('.ck-dual-engage__pro a.btn')?.getAttribute('href') || null,
      colCount: cols.length,
      stackedMobile: stacked,
      blockOrderTop: order,
    };
  });

  const fullPath = path.join(OUT, `lot4_home_${label}_full.png`);
  const dualPath = path.join(OUT, `lot4_home_${label}_dual.png`);
  await page.screenshot({ path: fullPath, fullPage: true });
  await dual.screenshot({ path: dualPath });

  report.captures.push({ label, width, height, fullPath, dualPath });
  report.checks[label] = metrics;
  await context.close();
}

await captureViewport('desktop_1280', 1280, 900);
await captureViewport('desktop_1440', 1440, 900);
await captureViewport('mobile_390', 390, 844);

report.summary = {
  dualVisibleAll: Object.values(report.checks).every((c) => c.dualCompact && c.newsletter),
  noProBanner: Object.values(report.checks).every((c) => !c.proBanner),
  noOverflowMobile: !report.checks.mobile_390?.overflow,
  mobileStacked: report.checks.mobile_390?.stackedMobile === true,
  desktopTwoCols: ['desktop_1280', 'desktop_1440'].every(
    (k) => report.checks[k]?.colCount >= 2 && report.checks[k]?.stackedMobile === false,
  ),
  proCta: report.checks.desktop_1280?.proCtaHref === '/professionnels',
  newsletterFunctional: report.checks.desktop_1280?.emailInput && report.checks.desktop_1280?.listId,
};

await writeFile(path.join(OUT, 'lot4_qa_report.json'), JSON.stringify(report, null, 2));
console.log(JSON.stringify(report.summary, null, 2));
await browser.close();
