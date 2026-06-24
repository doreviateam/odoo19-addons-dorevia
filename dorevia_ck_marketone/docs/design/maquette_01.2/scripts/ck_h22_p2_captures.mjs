/**
 * P2 Header V2.2 — captures avant/après (desktop initial, scroll, mega, mobile).
 * Usage: node ck_h22_p2_captures.mjs
 */
import { chromium } from 'playwright';
import { mkdirSync } from 'fs';
import { dirname, join } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const DB = 'dorevia_ck_marketone_01';
const BASE = 'http://localhost:18079';
const headers = { 'X-Odoo-Database': DB };
const OUT = join(__dirname, '../captures/recette_header_v22/p2');

mkdirSync(OUT, { recursive: true });

const browser = await chromium.launch({ headless: true });
const desktop = await browser.newContext({ viewport: { width: 1280, height: 800 }, extraHTTPHeaders: headers });
const mobile = await browser.newContext({ viewport: { width: 390, height: 844 }, extraHTTPHeaders: headers });
const page = await desktop.newPage();
const mpage = await mobile.newPage();

async function openMega(label) {
  const li = page.locator('#top_menu > li.ck-nav-mega-product').filter({
    has: page.locator('.ck-nav-mega-split__link span', { hasText: label }),
  }).first();
  await li.hover({ force: true });
  // Attend la classe .show réelle (pas un simple délai fixe) — un hover qui
  // n'a pas déclenché le dropdown produirait sinon une capture "fermée"
  // silencieusement fausse (cf. before/after_mega_epicerie.png corrigés P2).
  const panel = li.locator('.o_mega_menu');
  await panel.waitFor({ state: 'visible', timeout: 5000 });
  await page.waitForFunction(
    (el) => el.classList.contains('show') && el.getBoundingClientRect().width > 100,
    await panel.elementHandle(),
    { timeout: 5000 },
  );
  await page.waitForTimeout(150);
}

await page.goto(`${BASE}/?db=${DB}&qa_ts=p2_header`, { waitUntil: 'networkidle', timeout: 60000 });
await page.screenshot({ path: join(OUT, 'after_desktop_initial.png') });

await page.evaluate(() => window.scrollTo(0, 240));
await page.waitForTimeout(400);
await page.screenshot({ path: join(OUT, 'after_desktop_scroll.png') });
await page.evaluate(() => window.scrollTo(0, 0));

await openMega('Épicerie');
await page.screenshot({ path: join(OUT, 'after_mega_epicerie.png') });

await mpage.goto(`${BASE}/?db=${DB}&qa_ts=p2_header`, { waitUntil: 'networkidle', timeout: 60000 });
await mpage.screenshot({ path: join(OUT, 'after_mobile_ferme.png') });
await mpage.locator('[aria-label="Menu"]').click();
await mpage.waitForTimeout(400);
await mpage.screenshot({ path: join(OUT, 'after_mobile_drawer.png') });

await browser.close();
console.log('P2 captures written to', OUT);
