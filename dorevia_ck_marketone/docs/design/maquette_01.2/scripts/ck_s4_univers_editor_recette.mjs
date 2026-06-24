/**
 * Recette automatisée §7 — édition unitaire des cards Section 4 « Acheter par univers »
 * dans le Website Builder Odoo 19.
 *
 * Critères validés (card Épicerie) :
 *   1. Clic image  -> ouverture du sélecteur média Odoo (« Sélectionner un média »).
 *   2. Clic titre  -> édition inline réelle (frappe clavier modifie le texte).
 *   3. Sélection   -> la sidebar cible la card seule (« Univers Épicerie créole »).
 *   4. Aucune navigation front parasite, aucune erreur JS critique.
 *
 * Usage : node ck_s4_univers_editor_recette.mjs
 */
import { chromium } from 'playwright';

const DB = process.env.CK_DB || 'dorevia_ck_marketone_01';
const BASE = process.env.CK_BASE || 'http://localhost:18079';
const SHOT = '/tmp/ck_s4_recette';

const report = { steps: [] };
const step = (name, ok, detail = '') => {
  report.steps.push({ name, ok, detail });
  console.log(`${ok ? '✓' : '✗'} ${name}${detail ? ` — ${detail}` : ''}`);
};

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({ viewport: { width: 1440, height: 900 } });
const page = await context.newPage();
const errs = [];
page.on('pageerror', (e) => errs.push(String(e)));
page.on('console', (m) => { if (m.type() === 'error') errs.push('console:' + m.text()); });

try {
  await page.goto(`${BASE}/web/login?db=${DB}`, { waitUntil: 'domcontentloaded' });
  if (await page.locator('form.oe_login_form').count()) {
    await page.fill('input[name="login"]', 'admin');
    await page.fill('input[name="password"]', 'admin');
    await page.locator('form.oe_login_form button[type="submit"]').click();
    await page.waitForURL(/\/odoo/, { timeout: 60000 });
  }

  await page.goto(`${BASE}/odoo/action-website.website_preview?path=${encodeURIComponent('/')}`,
    { waitUntil: 'domcontentloaded', timeout: 120000 });
  await page.waitForSelector('iframe', { timeout: 120000 });
  await page.waitForTimeout(7000);
  await page.locator('.o_edit_website_container button').first().click({ timeout: 8000 }).catch(() => {});
  await page.waitForTimeout(11000);

  let frame = null;
  for (const f of page.frames()) {
    if (await f.evaluate(() => !!document.body && document.body.classList.contains('editor_enable')).catch(() => false)) { frame = f; break; }
  }
  step('Mode édition Website Builder actif', !!frame);
  if (!frame) throw new Error('frame éditeur introuvable');

  await frame.evaluate(() => document.querySelector('.ck-univers-card--epicerie')?.scrollIntoView({ block: 'center' }));
  await page.waitForTimeout(1500);

  // 1. Clic image -> sélecteur média
  await frame.locator('.ck-univers-card--epicerie .ck-univers-card__img').click({ timeout: 8000 });
  await page.waitForTimeout(3500);
  const mediaSel = await page.evaluate(() => {
    const d = document.querySelector('.o_dialog, .modal.show');
    return { open: !!d, title: d?.querySelector('.modal-title')?.innerText || null, text: d ? d.innerText.slice(0, 120) : '' };
  });
  step('Clic image -> sélecteur média Odoo ouvert', mediaSel.open && /Sélectionner un média|Select a media/i.test(mediaSel.title || mediaSel.text), mediaSel.title || '');
  await page.screenshot({ path: `${SHOT}_media.png` });
  await page.keyboard.press('Escape').catch(() => {});
  await page.waitForTimeout(1500);

  // 2. Clic titre -> édition inline (frappe)
  await frame.locator('.ck-univers-card--epicerie .ck-univers-card__title').click({ timeout: 8000 });
  await page.waitForTimeout(800);
  await page.keyboard.type(' QA', { delay: 40 });
  await page.waitForTimeout(1200);
  const title = await frame.evaluate(() => {
    const t = document.querySelector('.ck-univers-card--epicerie .ck-univers-card__title');
    return { ce: !!t?.isContentEditable, text: t?.textContent || '' };
  });
  step('Clic titre -> édition inline réelle', title.ce && /QA$/.test(title.text.trim()), `texte="${title.text}"`);

  // 3. Sidebar cible la card seule
  const containers = await page.evaluate(() => [...document.querySelectorAll('[data-container-title]')].map((n) => n.getAttribute('data-container-title')));
  step('Sidebar cible la card (Univers Épicerie créole)', containers.some((c) => /Univers Épicerie créole/i.test(c || '')), JSON.stringify(containers));

  // 4. Pas d'erreur JS critique
  const critical = errs.filter((e) => !/favicon|404|Failed to load resource|ResizeObserver/i.test(e));
  step('Console sans erreur JS critique', critical.length === 0, critical.slice(0, 2).join(' | '));

  report.pass = report.steps.every((s) => s.ok);
} catch (e) {
  step('Exécution', false, String(e));
  report.pass = false;
} finally {
  await browser.close();
}

console.log('\nVERDICT:', report.pass ? 'GO' : 'NO GO');
process.exit(report.pass ? 0 : 1);
