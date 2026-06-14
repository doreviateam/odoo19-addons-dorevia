import { chromium } from 'playwright';

const DB = 'dorevia_ck_marketone_01';
const BASE = 'http://localhost:18079';
const RECIPES = '/recettes';
const headers = { 'X-Odoo-Database': DB };

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({ viewport: { width: 390, height: 844 }, extraHTTPHeaders: headers });
const page = await context.newPage();

const routes = [RECIPES, '/producteur/atelier-hauts-goyaviers', '/contactus', '/a-propos', '/professionnels', '/shop', '/'];

const results = {};
for (const path of routes) {
  await page.goto(`${BASE}${path}?db=${DB}`, { waitUntil: 'networkidle', timeout: 45000 });
  await page.waitForTimeout(800);
  results[path] = await page.evaluate(() => ({
    scrollWidth: document.documentElement.scrollWidth,
    clientWidth: document.documentElement.clientWidth,
    overflow: document.documentElement.scrollWidth > document.documentElement.clientWidth + 1,
  }));
}

console.log(JSON.stringify({ viewport: { width: 390, height: 844 }, results }, null, 2));
await browser.close();
