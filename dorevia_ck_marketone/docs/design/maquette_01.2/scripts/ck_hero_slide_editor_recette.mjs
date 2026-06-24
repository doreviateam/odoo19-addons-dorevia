/**
 * Recette Website Builder — édition indépendante des visuels Hero carrousel.
 *
 * Usage : node ck_hero_slide_editor_recette.mjs
 */
import { chromium } from 'playwright';

const DB = process.env.CK_DB || 'dorevia_ck_marketone_01';
const BASE = process.env.CK_BASE || 'http://localhost:18079';
const SHOT = '/tmp/ck_hero_recette';

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

  const markup = await frame.evaluate(() => {
    const slides = document.querySelectorAll('.s_ck_hero .carousel-item[data-snippet="s_ck_hero_slide"]');
    const imgs = document.querySelectorAll('.s_ck_hero .ck-hero__visual-media.o_editable_media');
    return { slides: slides.length, imgs: imgs.length };
  });
  // Carrousel personnalisable par le MOA : au moins 2 visuels éditables attendus.
  step('Markup slides éditables (≥2, o_editable_media)', markup.slides >= 2 && markup.imgs === markup.slides, JSON.stringify(markup));

  const slideImgs = frame.locator('.s_ck_hero .carousel-item[data-snippet="s_ck_hero_slide"] .ck-hero__visual-media');

  // Clic visuel 1 (ciblage par index — robuste aux data-name dupliqués)
  await slideImgs.nth(0).click({ timeout: 8000 });
  await page.waitForTimeout(3500);
  const media1 = await page.evaluate(() => {
    const d = document.querySelector('.o_dialog, .modal.show');
    const containers = [...document.querySelectorAll('[data-container-title]')].map((n) => n.getAttribute('data-container-title'));
    return { open: !!d, title: d?.querySelector('.modal-title')?.innerText, containers };
  });
  step('Clic visuel 1 -> sélecteur média', media1.open && /Sélectionner un média|Select a media/i.test(media1.title || ''), media1.title || '');
  step('Sidebar cible un slide hero', media1.containers.some((c) => /Visuel hero/i.test(c || '')), JSON.stringify(media1.containers));
  await page.screenshot({ path: `${SHOT}_slide1.png` });
  await page.keyboard.press('Escape').catch(() => {});
  await page.waitForTimeout(1500);

  // Clic visuel 2 (indépendant du 1)
  await slideImgs.nth(1).click({ timeout: 8000 });
  await page.waitForTimeout(3500);
  const media2 = await page.evaluate(() => {
    const d = document.querySelector('.o_dialog, .modal.show');
    const containers = [...document.querySelectorAll('[data-container-title]')].map((n) => n.getAttribute('data-container-title'));
    return { open: !!d, containers };
  });
  step('Clic visuel 2 -> sélecteur média (indépendant)', media2.open, JSON.stringify(media2.containers));
  step('Sidebar cible un slide hero', media2.containers.some((c) => /Visuel hero/i.test(c || '')), JSON.stringify(media2.containers));

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
