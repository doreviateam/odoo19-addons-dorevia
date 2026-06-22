import { chromium } from 'playwright';
import { mkdirSync, writeFileSync } from 'node:fs';

const DB = 'dorevia_ck_marketone_01';
const BASE = 'http://localhost:18079';
const QA = 'nav_shop_v2';
const headers = { 'X-Odoo-Database': DB };
const OUT = '/Users/doreviateam/dorevia-saas/odoo19-addons-dorevia/dorevia_ck_marketone/docs/design/maquette_01.2/captures/recette_nav_shop_v2';

mkdirSync(OUT, { recursive: true });

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({ viewport: { width: 1280, height: 800 }, extraHTTPHeaders: headers });
const page = await context.newPage();

const results = {};

await page.goto(`${BASE}/?db=${DB}&qa_ts=${QA}`, { waitUntil: 'networkidle', timeout: 45000 });

const topMenu = await page.evaluate(() => {
  const el = document.querySelector('#top_menu');
  if (!el) return null;
  return [...el.querySelectorAll(':scope > li')]
    .filter((li) => getComputedStyle(li).display !== 'none')
    .map((li) => {
      const a = li.querySelector(':scope > a, :scope > .nav-link, :scope > .dropdown-toggle');
      return a ? a.textContent.trim() : null;
    })
    .filter(Boolean);
});
results.D1_topMenuVisible = topMenu;

results.D2_fixedEntries = {
  tousNosProduits: topMenu?.includes('Tous nos produits') ?? false,
  decouvrir: topMenu?.includes('Découvrir') ?? false,
  decouvrirInExtraMenu: await page.evaluate(() => !!document.querySelector('.o_extra_menu_items')),
  nosUniversHidden: !topMenu?.includes('Nos univers'),
};

results.D3_boNamesFromBO = await page.evaluate(() => {
  const items = [...document.querySelectorAll('#top_menu > li.ck-nav-desktop-universe')];
  return items.map((li) => {
    const a = li.querySelector(':scope > a, :scope > .dropdown-toggle');
    return a ? a.textContent.trim() : null;
  }).filter(Boolean);
});

await page.screenshot({ path: `${OUT}/nav_shop_desktop_1280_header.png`, fullPage: false });

// Découvrir — visible direct ou menu overflow Odoo (o_extra_menu_items)
results.D4_decouvrirMega = await page.evaluate(() => {
  const openExtra = () => {
    const extra = document.querySelector('.o_extra_menu_items .dropdown-toggle');
    if (extra) extra.click();
  };
  let toggles = [...document.querySelectorAll('#top_menu .o_mega_menu_toggle, #top_menu .dropdown-toggle')]
    .filter((a) => a.textContent.includes('Découvrir') && a.getBoundingClientRect().width > 0);
  if (!toggles.length) {
    openExtra();
    toggles = [...document.querySelectorAll('.o_extra_menu_items .o_mega_menu_toggle, .o_extra_menu_items .dropdown-toggle')]
      .filter((a) => a.textContent.includes('Découvrir'));
  }
  const dec = toggles[0];
  if (!dec) return { found: false, megaVisible: false, links: [], inExtraMenu: false };
  dec.click();
  const panel = document.querySelector('.o_mega_menu.show, .dropdown-menu.show');
  const links = panel
    ? [...panel.querySelectorAll('a')].map((a) => ({ text: a.textContent.trim(), href: a.getAttribute('href') })).filter((l) => l.text)
    : [];
  return {
    found: true,
    inExtraMenu: !!dec.closest('.o_extra_menu_items'),
    megaVisible: !!panel,
    links,
    hasCommerceDuplicate: links.some((l) => (l.href || '').includes('/shop/category/')),
  };
});
await page.waitForTimeout(400);
if (results.D4_decouvrirMega.megaVisible) {
  results.D7_contrastHover = await page.evaluate(() => {
    const link = document.querySelector('.o_mega_menu.show a, .dropdown-menu.show .ck-nav-decouvrir-links a');
    return link ? getComputedStyle(link).color : null;
  });
}
await page.keyboard.press('Escape');

// H1 chrome non-régression
results.D5_h1Chrome = await page.evaluate(() => ({
  serviceBar: !!document.querySelector('.ck-header-service-bar'),
  search: !!document.querySelector('.ck-header__search'),
  brand: !!document.querySelector('.ck-header__brand'),
  cart: !!document.querySelector('header a[href*="/shop/cart"], header .o_wsale_my_cart'),
}));

// Densité / tenue visuelle (6 racines seed)
results.D6_density = await page.evaluate(() => {
  const items = [...document.querySelectorAll('#top_menu > li')]
    .filter((li) => getComputedStyle(li).display !== 'none');
  const logo = document.querySelector('header .navbar-brand, header .ck-header__brand-link');
  const cart = document.querySelector('header a[href*="/shop/cart"], header .o_wsale_my_cart');
  const out = { visibleCount: items.length, rootCategoryCount: 0 };
  items.forEach((li) => {
    if (li.classList.contains('ck-nav-desktop-universe')) out.rootCategoryCount += 1;
  });
  const lastUniverse = items.filter((li) => li.classList.contains('ck-nav-desktop-universe')).pop();
  if (logo && lastUniverse && cart) {
    const lr = logo.getBoundingClientRect();
    const ur = lastUniverse.getBoundingClientRect();
    const cr = cart.getBoundingClientRect();
    out.logoRight = lr.right;
    out.lastUniverseRight = ur.right;
    out.cartLeft = cr.left;
    out.overlapChrome = ur.right > cr.left - 8;
  }
  return out;
});


writeFileSync(`${OUT}/nav_shop_desktop_1280_results.json`, JSON.stringify(results, null, 2));
console.log(JSON.stringify(results, null, 2));
await browser.close();
