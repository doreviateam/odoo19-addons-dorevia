import { chromium } from 'playwright';

const DB = 'dorevia_ck_marketone_01';
const BASE = 'http://localhost:18079';
const headers = { 'X-Odoo-Database': DB };

async function audit(path, width) {
  const browser = await chromium.launch({ headless: true });
  const context = await browser.newContext({ viewport: { width, height: 844 }, extraHTTPHeaders: headers });
  const page = await context.newPage();
  await page.goto(`${BASE}${path}?db=${DB}`, { waitUntil: 'networkidle', timeout: 45000 });
  await page.waitForTimeout(1200);
  const metrics = await page.evaluate(() => ({
    scrollWidth: document.documentElement.scrollWidth,
    clientWidth: document.documentElement.clientWidth,
    formVisible: !!document.querySelector('#ck-pro-form'),
    submitVisible: !!document.querySelector('.s_website_form_send'),
  }));
  await browser.close();
  return { path, width, ...metrics, overflow: metrics.scrollWidth > metrics.clientWidth };
}

const pro = await audit('/professionnels', 390);
const home = await audit('/', 390);

console.log(JSON.stringify({ pro, home }, null, 2));
