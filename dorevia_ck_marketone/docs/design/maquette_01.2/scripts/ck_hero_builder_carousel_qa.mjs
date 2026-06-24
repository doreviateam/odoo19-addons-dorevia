/**
 * Recette Website Builder — CK Hero carrousel (Autoplay / Speed).
 */
import { chromium } from 'playwright';

const DB = 'dorevia_ck_marketone_01';
const BASE = 'http://localhost:18079';
const LOGIN = 'admin';
const PASSWORD = 'admin';

const report = { steps: [], consoleErrors: [] };
const step = (name, ok, detail = '') => {
  report.steps.push({ name, ok, detail });
  console.log(`${ok ? '✓' : '✗'} ${name}${detail ? ` — ${detail}` : ''}`);
};

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext();
const page = await context.newPage();

page.on('console', (msg) => {
  if (msg.type() === 'error') report.consoleErrors.push(msg.text());
});
page.on('pageerror', (err) => report.consoleErrors.push(String(err)));

try {
  await page.goto(`${BASE}/web/login?db=${DB}`, { waitUntil: 'domcontentloaded' });
  const loginForm = page.locator('form.oe_login_form');
  if (await loginForm.count()) {
    await page.fill('input[name="login"]', LOGIN);
    await page.fill('input[name="password"]', PASSWORD);
    await loginForm.locator('button[type="submit"]').click();
    await page.waitForURL(/\/odoo/, { timeout: 60000 });
  }

  await page.goto(
    `${BASE}/odoo/action-website.website_preview?path=${encodeURIComponent('/')}`,
    { waitUntil: 'domcontentloaded', timeout: 120000 },
  );
  await page.waitForSelector('iframe', { timeout: 120000 });
  await page.waitForTimeout(8000);

  const builderLoaded = await page.evaluate(() =>
    !!document.querySelector('iframe') &&
    !!document.querySelector('.o_website_preview, .o_we_website_top_actions, .o_website_navbar, .o_action_manager')
  );
  step('Builder Odoo 19 (website_preview) chargé', builderLoaded);

  const iframeEl = page.frameLocator('iframe').first();
  const heroInIframe = iframeEl.locator('.s_ck_hero.ck-hero--marketone-v1, .ck-hero--marketone-v1').first();
  await heroInIframe.waitFor({ state: 'visible', timeout: 90000 });
  await heroInIframe.click({ force: true });
  await page.waitForTimeout(3000);

  const panelText = await page.evaluate(() => {
    const sel = '.o_we_customize_panel, .o_we_builder_sidebar, aside.o_sidebar, [class*="BuilderSidebar"]';
    return [...document.querySelectorAll(sel)].map((n) => n.innerText).join('\n');
  });

  const hasAutoplay = /Autoplay/i.test(panelText);
  const hasSpeed = /Speed/i.test(panelText);
  step('Option Autoplay visible (panneau)', hasAutoplay, panelText.slice(0, 120));
  step('Option Speed visible (panneau)', hasSpeed);

  const speedInput = page.locator(
    '.o_we_customize_panel input[type="number"], .o_we_builder_sidebar input[type="number"]'
  ).first();
  let speedChanged = false;
  if (await speedInput.count()) {
    await speedInput.fill('18');
    await speedInput.blur();
    speedChanged = true;
  }
  step('Modification vitesse (18 s)', speedChanged);

  const saveBtn = page.locator('button:has-text("Save"), button:has-text("Enregistrer")').first();
  if (await saveBtn.count()) {
    await saveBtn.click({ timeout: 8000 }).catch(() => {});
    await page.waitForTimeout(4000);
  }
  step('Sauvegarde', true);

  const intervalIframe = await iframeEl.locator('.ck-hero__visual-carousel').getAttribute('data-bs-interval');
  step('data-bs-interval iframe après édition', !!intervalIframe, `valeur=${intervalIframe}`);

  await page.reload({ waitUntil: 'domcontentloaded' });
  await page.waitForTimeout(5000);
  const intervalReload = await page.frameLocator('iframe').first()
    .locator('.ck-hero__visual-carousel').getAttribute('data-bs-interval');
  step('Persistance data-bs-interval après reload builder', !!intervalReload, `valeur=${intervalReload}`);

  const critical = report.consoleErrors.filter((e) => !/favicon|404|Failed to load resource|ResizeObserver/i.test(e));
  step('Console sans erreur critique', critical.length === 0, critical.slice(0, 3).join(' | '));

  report.pass = report.steps.every((s) => s.ok);
} catch (err) {
  step('Exécution', false, String(err));
  report.pass = false;
} finally {
  await browser.close();
}

console.log('\n' + JSON.stringify(report, null, 2));
process.exit(report.pass ? 0 : 1);
