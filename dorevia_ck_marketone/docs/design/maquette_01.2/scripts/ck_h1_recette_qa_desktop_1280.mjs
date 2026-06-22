import { chromium } from 'playwright';

const DB = 'dorevia_ck_marketone_01';
const BASE = 'http://localhost:18079';
const QA = 'h1qa';
const headers = { 'X-Odoo-Database': DB };
const OUT = '/Users/doreviateam/dorevia-saas/odoo19-addons-dorevia/dorevia_ck_marketone/docs/design/maquette_01.2/captures/recette_h1_v2_1';

const EXPECTED_BANNER = 'Produits créoles sélectionnés · Origines identifiées · Livraison suivie';
const EXPECTED_PLACEHOLDER = 'Rechercher un produit, une saveur...';

const browser = await chromium.launch({ headless: true });
const context = await browser.newContext({ viewport: { width: 1280, height: 800 }, extraHTTPHeaders: headers });
const page = await context.newPage();
const results = {};

// R1 — bandeau on / and /shop and /contactus
for (const [key, path] of [['home', '/'], ['shop', '/shop'], ['contactus', '/contactus']]) {
  await page.goto(`${BASE}${path}?db=${DB}&qa_ts=${QA}`, { waitUntil: 'networkidle', timeout: 45000 });
  const banner = await page.evaluate(() => {
    const el = document.querySelector('.ck-header-service-bar__text, .ck-header-service-bar');
    return el ? el.textContent.replace(/\s+/g, ' ').trim() : null;
  });
  results[`R1_banner_${key}`] = banner;
}

// R2 — logo C-Kréyòl
await page.goto(`${BASE}/?db=${DB}&qa_ts=${QA}`, { waitUntil: 'networkidle', timeout: 45000 });
results.R2_logo = await page.evaluate(() => {
  const brand = document.querySelector('.ck-header__brand-link');
  const span = document.querySelector('.ck-header__brand');
  return {
    ariaLabel: brand ? brand.getAttribute('aria-label') : null,
    text: span ? span.textContent.trim() : null,
    hasO_circumflex: span ? span.textContent.includes('ò') : false,
  };
});

// R3 — recherche centrale
results.R3_search = await page.evaluate((expected) => {
  const input = document.querySelector('.ck-header__search input[type="search"], .ck-header__search input.search-query');
  return {
    found: !!input,
    placeholder: input ? input.getAttribute('placeholder') : null,
    placeholderMatches: input ? input.getAttribute('placeholder') === expected : false,
    searchType: input ? input.getAttribute('data-search-type') : null,
  };
}, EXPECTED_PLACEHOLDER);

// R4 — panier / compte presence + order
results.R4_cartAccount = await page.evaluate(() => {
  const nav = document.querySelector('header .navbar-nav.align-items-center, header ul.navbar-nav:last-of-type');
  const cart = document.querySelector('header .ck-header__cart-link, header a[href*="/shop/cart"]');
  const account = document.querySelector('header .o_header_partner_dropdown, header [t-call*="user_dropdown"], header a[href*="/web/login"]');
  let cartBeforeOrAfterAccount = null;
  if (cart && account) {
    const pos = cart.compareDocumentPosition(account);
    cartBeforeOrAfterAccount = (pos & Node.DOCUMENT_POSITION_FOLLOWING) ? 'cart_before_account' : 'cart_after_account';
  }
  return {
    cartFound: !!cart,
    accountFound: !!account,
    order: cartBeforeOrAfterAccount,
  };
});

// R5 — Nav-1 desktop menu unchanged
results.R5_nav = await page.evaluate(() => {
  const items = [...document.querySelectorAll('#top_menu.top_menu > li')];
  return items
    .map((li) => {
      const a = li.querySelector(':scope > a, :scope > .nav-link');
      const cs = getComputedStyle(li);
      return a && cs.display !== 'none' && li.offsetParent !== null ? a.textContent.trim() : null;
    })
    .filter(Boolean);
});

// R6 — mega Découvrir unchanged
const decouvrir = page.locator("header .nav-link:has-text('Découvrir'), header a:has-text('Découvrir')").first();
await decouvrir.click();
await page.waitForTimeout(600);
const megaPanel = page.locator('.o_mega_menu, .dropdown-menu.show').first();
results.R6_mega = await megaPanel.evaluate((el) => [...el.querySelectorAll('a')].map((a) => a.textContent.trim()).filter(Boolean)).catch(() => []);
await page.keyboard.press('Escape');
await page.waitForTimeout(200);

await page.screenshot({ path: `${OUT}/h1_desktop_1280_header_qa.png`, fullPage: false });

// R7 — sticky on scroll
await page.evaluate(() => window.scrollTo(0, 900));
await page.waitForTimeout(400);
results.R7_sticky = await page.evaluate(() => {
  const header = document.querySelector('header#top, header.ck-header');
  if (!header) return null;
  const cs = getComputedStyle(header);
  const r = header.getBoundingClientRect();
  return { position: cs.position, top: r.top, backgroundColor: cs.backgroundColor, opacity: cs.opacity };
});
await page.screenshot({ path: `${OUT}/h1_desktop_1280_sticky_qa.png`, fullPage: false });
await page.evaluate(() => window.scrollTo(0, 0));

// R8 — contrast banner text/bg
results.R8_contrast = await page.evaluate(() => {
  const el = document.querySelector('.ck-header-service-bar__text');
  const bar = document.querySelector('.ck-header-service-bar');
  if (!el || !bar) return null;
  return { color: getComputedStyle(el).color, background: getComputedStyle(bar).backgroundColor };
});

results.R1_bannerMatchesExpected = Object.entries(results)
  .filter(([k]) => k.startsWith('R1_banner_'))
  .every(([, v]) => v && v.replace(/\s+/g, ' ').includes(EXPECTED_BANNER.split(' · ')[0]));

const fs = await import('node:fs');
fs.writeFileSync(`${OUT}/h1_desktop_1280_qa_results.json`, JSON.stringify(results, null, 2));
console.log(JSON.stringify(results, null, 2));
await browser.close();
