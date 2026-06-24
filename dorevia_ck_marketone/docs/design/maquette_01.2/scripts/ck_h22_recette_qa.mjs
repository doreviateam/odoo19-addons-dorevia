/**
 * Recette QA Header CK V2.2 — captures desktop + mobile.
 * Usage: node ck_h22_recette_qa.mjs
 */
import { chromium } from 'playwright';
import { mkdirSync, writeFileSync } from 'fs';
import { dirname, join } from 'path';
import { fileURLToPath } from 'url';

const __dirname = dirname(fileURLToPath(import.meta.url));
const DB = 'dorevia_ck_marketone_01';
const BASE = 'http://localhost:18079';
const QA = 'header_v22';
const headers = { 'X-Odoo-Database': DB };
const OUT = join(__dirname, '../captures/recette_header_v22');

mkdirSync(OUT, { recursive: true });

const results = {
  meta: { db: DB, base: BASE, qa: QA, capturedAt: new Date().toISOString() },
  checks: {},
};

const browser = await chromium.launch({ headless: true });
const desktop = await browser.newContext({ viewport: { width: 1280, height: 800 }, extraHTTPHeaders: headers });
const mobile = await browser.newContext({ viewport: { width: 390, height: 844 }, extraHTTPHeaders: headers });
const page = await desktop.newPage();
const mpage = await mobile.newPage();

function slugify(label) {
  return label.normalize('NFD').replace(/[^\w]+/g, '_').toLowerCase();
}

/** État visible du panneau mega pour un rayon N3 (desktop). */
function readMegaPanelState(label) {
  return page.evaluate((lbl) => {
    const item = [...document.querySelectorAll('#top_menu > li.ck-nav-mega-product')].find(
      (el) => el.querySelector('.ck-nav-mega-split__link span')?.textContent?.trim() === lbl,
    );
    const panel = item?.querySelector('.o_mega_menu');
    if (!panel) {
      return { open: false, reason: 'panel-missing', titles: [], links: [], panelHeight: 0 };
    }
    const rect = panel.getBoundingClientRect();
    const style = getComputedStyle(panel);
    const panelShow = panel.classList.contains('show');
    const visible =
      panelShow &&
      rect.height > 48 &&
      rect.width > 100 &&
      style.display !== 'none' &&
      style.visibility !== 'hidden' &&
      Number(style.opacity || 1) > 0.05;
    const titles = [...panel.querySelectorAll('.ck-mega-menu__title')].map((t) => t.textContent.trim());
    const links = [...panel.querySelectorAll('a.ck-mega-menu__link')]
      .filter((a) => {
        const r = a.getBoundingClientRect();
        return r.height > 0 && r.width > 0;
      })
      .map((a) => ({ text: a.textContent.trim(), href: a.getAttribute('href') }));
    return {
      open: visible,
      panelShow,
      panelHeight: Math.round(rect.height),
      panelWidth: Math.round(rect.width),
      titles,
      hasFamilies: titles.includes('Acheter par famille'),
      linkCount: links.length,
      links: links.slice(0, 12),
    };
  }, label);
}

/** Ouvre un mega-menu desktop (header o_hoverable_dropdown → survol). */
async function openMegaDesktop(label) {
  await page.keyboard.press('Escape');
  await page.mouse.move(0, 0);
  await page.waitForTimeout(120);
  await page.evaluate(() => window.scrollTo(0, 0));

  const li = page.locator('#top_menu > li.ck-nav-mega-product').filter({
    has: page.locator('.ck-nav-mega-split__link span', { hasText: label }),
  }).first();

  if (await li.count()) {
    await li.hover({ force: true });
    await page.waitForTimeout(450);
  }

  let state = await readMegaPanelState(label);
  if (!state.open) {
    await page.evaluate((lbl) => {
      const item = [...document.querySelectorAll('#top_menu > li.ck-nav-mega-product')].find(
        (el) => el.querySelector('.ck-nav-mega-split__link span')?.textContent?.trim() === lbl,
      );
      const toggle = item?.querySelector('.o_mega_menu_toggle, .ck-nav-mega-split__toggle');
      toggle?.dispatchEvent(new MouseEvent('mouseenter', { bubbles: true }));
      item?.dispatchEvent(new MouseEvent('mouseenter', { bubbles: true }));
      const Dropdown = window.bootstrap?.Dropdown;
      if (toggle && Dropdown?.getOrCreateInstance) {
        Dropdown.getOrCreateInstance(toggle).show();
      }
    }, label);
    await page.waitForTimeout(400);
    state = await readMegaPanelState(label);
  }
  return state;
}

async function closeMegaDesktop() {
  await page.evaluate(() => {
    for (const toggle of document.querySelectorAll('#top_menu .ck-nav-mega-split__toggle, #top_menu .dropdown-toggle')) {
      window.bootstrap?.Dropdown?.getOrCreateInstance(toggle)?.hide();
    }
    for (const panel of document.querySelectorAll('#top_menu .o_mega_menu.show, #top_menu .dropdown-menu.show')) {
      panel.classList.remove('show');
    }
    for (const item of document.querySelectorAll('#top_menu .nav-item.show')) {
      item.classList.remove('show');
    }
  });
  await page.mouse.move(0, 0);
  await page.keyboard.press('Escape');
  await page.waitForTimeout(220);
}

/** Vérifie que le mega-menu ne se ferme pas pendant la traversée N3 → panneau. */
async function checkMegaHoverBridge(label, linkText) {
  const state = await openMegaDesktop(label);
  if (!state.open) {
    return { pass: false, phase: 'open', state };
  }
  const item = page.locator('#top_menu > li.ck-nav-mega-product').filter({
    has: page.locator('.ck-nav-mega-split__link span', { hasText: label }),
  }).first();
  const linkBox = await page.evaluate((txt) => {
    const link = [...document.querySelectorAll('.o_mega_menu.show a.ck-mega-menu__link')].find(
      (a) => a.textContent.trim() === txt,
    );
    const rect = link?.getBoundingClientRect();
    return rect
      ? {
          x: rect.x,
          y: rect.y,
          width: rect.width,
          height: rect.height,
          href: link.getAttribute('href'),
        }
      : null;
  }, linkText);
  const itemBox = await item.boundingBox();
  if (!itemBox || !linkBox) {
    return { pass: false, phase: 'target', state, linkBox };
  }
  const targetX = linkBox.x + linkBox.width / 2;
  const targetY = linkBox.y + linkBox.height / 2;
  await page.mouse.move(itemBox.x + itemBox.width / 2, itemBox.y + itemBox.height / 2);
  await page.waitForTimeout(80);
  await page.mouse.move(targetX, targetY, { steps: 24 });
  await page.waitForTimeout(350);

  const after = await readMegaPanelState(label);
  const hovered = await page.evaluate(({ x, y }) => {
    const el = document.elementFromPoint(x, y);
    return {
      tag: el?.tagName,
      text: el?.textContent?.trim(),
      href: el?.closest('a')?.getAttribute('href') || null,
    };
  }, { x: targetX, y: targetY });
  return {
    pass: after.open && hovered.text === linkText,
    phase: 'traverse',
    after,
    hovered,
  };
}

/** Vérifie que le panneau actif se rafraîchit quand on balaye les rayons N3. */
async function checkMegaHoverSwitch(labels) {
  await page.keyboard.press('Escape');
  await page.mouse.move(0, 0);
  await page.waitForTimeout(120);
  await page.evaluate(() => window.scrollTo(0, 0));

  const steps = [];
  for (const label of labels) {
    const item = page.locator('#top_menu > li.ck-nav-mega-product').filter({
      has: page.locator('.ck-nav-mega-split__link span', { hasText: label }),
    }).first();
    const box = await item.boundingBox();
    if (!box) {
      steps.push({ label, pass: false, reason: 'item-missing' });
      continue;
    }
    await page.mouse.move(box.x + box.width / 2, box.y + box.height / 2, { steps: 16 });
    await page.waitForTimeout(280);

    const state = await readMegaPanelState(label);
    const openLabels = await page.evaluate(() => {
      return [...document.querySelectorAll('#top_menu > li.ck-nav-mega-product')]
        .filter((item) => {
          const panel = item.querySelector('.o_mega_menu');
          if (!panel?.classList.contains('show')) {
            return false;
          }
          const rect = panel.getBoundingClientRect();
          return rect.width > 100 && rect.height > 48;
        })
        .map((item) => item.querySelector('.ck-nav-mega-split__link span')?.textContent?.trim())
        .filter(Boolean);
    });
    steps.push({
      label,
      pass: state.open && openLabels.length === 1 && openLabels[0] === label,
      openLabels,
      panelWidth: state.panelWidth,
      linkCount: state.linkCount,
    });
  }
  return {
    pass: steps.length > 0 && steps.every((step) => step.pass),
    labels,
    steps,
  };
}

// 1 — Desktop initial
await page.goto(`${BASE}/?db=${DB}&qa_ts=${QA}`, { waitUntil: 'networkidle', timeout: 60000 });
await page.screenshot({ path: join(OUT, '01_desktop_initial.png') });
results.checks.desktop_initial = await page.evaluate(() => ({
  serviceBar: !!document.querySelector('.ck-header-service-bar'),
  serviceBarText: document.querySelector('.ck-header-service-bar')?.textContent?.replace(/\s+/g, ' ').trim(),
  baseline: document.querySelector('.ck-header__baseline')?.textContent?.trim(),
  placeholder: document.querySelector('.ck-header__search input[name="search"]')?.getAttribute('placeholder'),
  sticky: getComputedStyle(document.querySelector('header#top')).position,
  n3: [...document.querySelectorAll('#top_menu > li > a span, #top_menu > li .ck-nav-mega-split__link span')]
    .map((el) => el.textContent.trim()).filter(Boolean),
}));

// 2 — Desktop scroll (bandeau masqué)
await page.evaluate(() => window.scrollTo(0, 240));
await page.waitForTimeout(400);
await page.screenshot({ path: join(OUT, '02_desktop_scroll.png') });
results.checks.desktop_scroll = await page.evaluate(() => ({
  serviceBarHidden: document.querySelector('.ck-header-service-bar')?.classList.contains('ck-header-service-bar--hidden'),
  headerSticky: getComputedStyle(document.querySelector('header#top')).position,
  headerVisible: document.querySelector('header#top')?.getBoundingClientRect().top >= 0,
}));
await page.evaluate(() => window.scrollTo(0, 0));
await page.waitForTimeout(200);

// 3-5 — Mega-menus rayons (panneau réellement ouvert)
for (const [idx, label] of [['03', 'Épicerie'], ['04', 'Boissons'], ['05', 'Maison & Bien-être']]) {
  const megaState = await openMegaDesktop(label);
  if (!megaState.open) {
    console.warn(`[QA] Mega ${label} non visible avant capture — état:`, megaState);
  }
  await page.screenshot({ path: join(OUT, `${idx}_mega_${slugify(label)}.png`) });
  results.checks[`mega_${label}`] = megaState;
  await closeMegaDesktop();
}

results.checks.mega_hover_bridge = await checkMegaHoverBridge('Épicerie', 'Guadeloupe');
await closeMegaDesktop();
results.checks.mega_hover_switch = await checkMegaHoverSwitch([
  'Épicerie',
  'Boissons',
  'Maison & Bien-être',
  'Boissons',
  'Épicerie',
]);
await closeMegaDesktop();

// 6 — Artisanat (lien direct ou mega selon contenu)
const artisanat = page.locator('#top_menu').getByText('Artisanat', { exact: true });
results.checks.artisanat = {
  visible: await artisanat.count() > 0,
  isMega: await page.locator('#top_menu li.ck-nav-mega-product span', { hasText: 'Artisanat' }).count() > 0,
};
if (results.checks.artisanat.isMega) {
  await openMegaDesktop('Artisanat');
  await page.waitForTimeout(300);
}
await page.screenshot({ path: join(OUT, '06_artisanat.png') });
await closeMegaDesktop();

// 7 — Espace pro dropdown
await page.locator('#top_menu').getByText('Espace pro', { exact: true }).hover();
await page.waitForTimeout(300);
await page.screenshot({ path: join(OUT, '09_espace_pro_dropdown.png') });
results.checks.espace_pro = await page.evaluate(() => ({
  anchors: [...document.querySelectorAll('a[href^="/professionnels#"]')].map((a) => a.getAttribute('href')),
}));

// 8 — Nos producteurs (hover état nav)
await page.mouse.move(0, 0);
await page.waitForTimeout(150);
const producteursHref = await page.locator('#top_menu > li.ck-nav-producteurs a[href="/nos-producteurs"]').getAttribute('href');
results.checks.nos_producteurs = { href: producteursHref };
await page.screenshot({ path: join(OUT, '10_nos_producteurs_nav.png') });

// Coups de cœur — lien direct
results.checks.coups_de_coeur = await page.evaluate(() => {
  const item = [...document.querySelectorAll('#top_menu > li')].find((li) => li.textContent.includes('Coups de cœur'));
  return {
    directLink: !item?.classList.contains('dropdown'),
    href: item?.querySelector('a')?.getAttribute('href'),
    noMega: !item?.querySelector('.o_mega_menu'),
  };
});

// Coffrets — comportement seed (absence attendue si aucun tag publié)
results.checks.coffrets = await page.evaluate(() => {
  const item = [...document.querySelectorAll('#top_menu > li')].find((li) => li.textContent.includes('Coffrets'));
  if (!item) {
    return { visible: false, seedBehavior: 'absent — aucun tag coffret publié sur instance seed' };
  }
  return {
    visible: true,
    isDropdown: item.classList.contains('dropdown'),
    href: item.querySelector('a')?.getAttribute('href'),
  };
});

// Mobile fermé
await mpage.goto(`${BASE}/?db=${DB}&qa_ts=${QA}`, { waitUntil: 'networkidle', timeout: 60000 });
await mpage.screenshot({ path: join(OUT, '07_mobile_ferme.png') });
results.checks.mobile_closed = await mpage.evaluate(() => ({
  serviceBar: !!document.querySelector('.ck-header-service-bar'),
  menuBtn: !!document.querySelector('[aria-label="Menu"]'),
  brand: document.querySelector('.ck-header__brand')?.textContent?.trim(),
}));

// Mobile drawer
await mpage.locator('[aria-label="Menu"]').click();
await mpage.waitForTimeout(400);
await mpage.screenshot({ path: join(OUT, '08_mobile_drawer.png') });
results.checks.mobile_drawer = await mpage.evaluate(() => ({
  entries: [...document.querySelectorAll('#top_menu_collapse_mobile .top_menu > li')].map((li) => li.textContent.replace(/\s+/g, ' ').trim()).filter(Boolean),
  hasAccordion: !!document.querySelector('#top_menu_collapse_mobile .accordion'),
}));

/** Ouvre le mega mobile et déplie les sous-sections accordéon. */
async function openMobileMegaExpanded(label) {
  const toggle = mpage.locator('#top_menu_collapse_mobile .o_mega_menu_toggle, #top_menu_collapse_mobile .dropdown-toggle').filter({ hasText: label }).first();
  if (!(await toggle.count())) {
    await mpage.locator('#top_menu_collapse_mobile').getByText(label, { exact: true }).first().click();
  } else {
    await toggle.click({ force: true });
  }
  await mpage.waitForTimeout(500);

  await mpage.evaluate(() => {
    const panel =
      document.querySelector('#top_menu_collapse_mobile li.show .o_mega_menu') ||
      document.querySelector('#top_menu_collapse_mobile .o_mega_menu.show');
    [...(panel?.querySelectorAll('.accordion-button.collapsed') || [])].forEach((btn) => btn.click());
  });
  await mpage.waitForTimeout(400);

  return mpage.evaluate((lbl) => {
    const panel =
      document.querySelector('#top_menu_collapse_mobile li.show .o_mega_menu') ||
      document.querySelector('#top_menu_collapse_mobile .o_mega_menu.show');
    const accordion = panel?.querySelector('.ck-mega-menu__accordion');
    const expanded = [...(accordion?.querySelectorAll('.accordion-collapse.show') || [])].map((el) => {
      const btn = el.closest('.accordion-item')?.querySelector('.accordion-button');
      return btn?.textContent?.trim();
    }).filter(Boolean);
    const links = [...(accordion?.querySelectorAll('a.ck-mega-menu__link') || [])]
      .filter((a) => {
        const r = a.getBoundingClientRect();
        const collapse = a.closest('.accordion-collapse');
        return r.height > 0 && (!collapse || collapse.classList.contains('show'));
      })
      .map((a) => ({ text: a.textContent.trim(), href: a.getAttribute('href') }));
    return {
      rayon: lbl,
      panelOpen: !!panel?.classList.contains('show'),
      accordion: !!accordion,
      expandedSections: expanded,
      linkCount: links.length,
      links,
      noVisualCol: !document.querySelector('.ck-mega-menu__col--visual:not(.d-none)'),
    };
  }, label);
}

// Mega mobile — Épicerie avec accordéon déplié
if (await mpage.locator('#top_menu_collapse_mobile').getByText('Épicerie', { exact: true }).count()) {
  results.checks.mobile_mega_epicerie = await openMobileMegaExpanded('Épicerie');
  await mpage.screenshot({ path: join(OUT, '08b_mobile_mega_epicerie.png') });
}

writeFileSync(join(OUT, 'recette_header_v22_results.json'), JSON.stringify(results, null, 2));
console.log(JSON.stringify(results, null, 2));

await browser.close();
