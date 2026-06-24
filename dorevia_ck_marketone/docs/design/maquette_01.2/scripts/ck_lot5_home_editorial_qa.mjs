import { chromium } from 'playwright';
import { mkdir, writeFile } from 'node:fs/promises';
import path from 'node:path';

const DB = 'dorevia_ck_marketone_01';
const BASE = 'http://localhost:18079';
const OUT = process.env.CK_LOT5_QA_OUT || '/private/tmp/ck_marketone_lot5_qa';
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
  await page.waitForSelector('.ck-home-editorial', { timeout: 30000 });

  const editorial = page.locator('.ck-home-editorial');
  await editorial.scrollIntoViewIfNeeded();
  await page.waitForTimeout(400);

  const metrics = await page.evaluate(() => {
    const dualEl = document.querySelector('.ck-dual-engage--compact');
    const editoEl = document.querySelector('.ck-home-editorial');
    const footerEl = document.querySelector('footer');
    const bodyText = editoEl?.textContent || '';
    const linkHrefs = editoEl
      ? [...editoEl.querySelectorAll('a')].map((a) => a.getAttribute('href'))
      : [];
    return {
      scrollWidth: document.documentElement.scrollWidth,
      clientWidth: document.documentElement.clientWidth,
      overflow: document.documentElement.scrollWidth > document.documentElement.clientWidth + 1,
      editorialVisible: !!editoEl,
      title: bodyText.includes('C-Kreyol, la boutique des saveurs créoles'),
      narrative: bodyText.includes('agro-produits transformés'),
      noTechnical: !bodyText.match(/Inspiration réf|route-hint|TODO|FIXME/i),
      linkHrefs,
      dualBeforeEditorial: dualEl && editoEl
        ? dualEl.getBoundingClientRect().top < editoEl.getBoundingClientRect().top
        : null,
      editorialBeforeFooter: editoEl && footerEl
        ? editoEl.getBoundingClientRect().top < footerEl.getBoundingClientRect().top
        : null,
      dualCompact: !!dualEl,
      discovery: !!document.querySelector('.ck-discovery-pack'),
      featured: !!document.querySelector('.ck-featured-products'),
    };
  });

  const fullPath = path.join(OUT, `lot5_home_${label}_full.png`);
  const editoPath = path.join(OUT, `lot5_home_${label}_editorial.png`);
  await page.screenshot({ path: fullPath, fullPage: true });
  await editorial.screenshot({ path: editoPath });

  report.captures.push({ label, width, height, fullPath, editoPath });
  report.checks[label] = metrics;
  await context.close();
}

await captureViewport('desktop_1280', 1280, 900);
await captureViewport('desktop_1440', 1440, 900);
await captureViewport('mobile_390', 390, 844);

const base = report.checks.desktop_1280 || {};
report.summary = {
  editorialVisibleAll: Object.values(report.checks).every((c) => c.editorialVisible && c.title),
  noOverflowMobile: !report.checks.mobile_390?.overflow,
  narrativeOk: Object.values(report.checks).every((c) => c.narrative && c.noTechnical),
  linksOk: ['/a-propos', '/producteur/atelier-hauts-goyaviers', '/recettes'].every(
    (href) => base.linkHrefs?.includes(href),
  ),
  orderOk: base.dualBeforeEditorial && base.editorialBeforeFooter,
  nonRegression: base.dualCompact && base.discovery && base.featured,
};

await writeFile(path.join(OUT, 'lot5_qa_report.json'), JSON.stringify(report, null, 2));
console.log(JSON.stringify(report.summary, null, 2));
await browser.close();
