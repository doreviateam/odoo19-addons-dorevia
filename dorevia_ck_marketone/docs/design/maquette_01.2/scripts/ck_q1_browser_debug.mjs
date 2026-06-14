import { chromium } from 'playwright';

const browser = await chromium.launch({ headless: true });

async function probe(label, options) {
  const context = await browser.newContext(options.context || {});
  const page = await context.newPage();
  const logs = [];
  const failed = [];
  page.on('console', (m) => logs.push({ type: m.type(), text: m.text() }));
  page.on('pageerror', (e) => logs.push({ type: 'pageerror', text: e.message }));
  page.on('requestfailed', (r) => failed.push(r.url() + ' :: ' + r.failure()?.errorText));

  await page.goto(options.url, { waitUntil: 'networkidle', timeout: 60000 });
  await page.waitForTimeout(options.wait || 5000);

  const result = await page.evaluate(() => ({
    url: location.href,
    featured: !!document.querySelector('.s_ck_featured_products'),
    dynamic: !!document.querySelector('.s_dynamic_snippet_products'),
    loading: !!document.querySelector('.o_dynamic_snippet_loading'),
    empty: !!document.querySelector('.o_dynamic_empty, .s_dynamic_empty, .o_dynamic_snippet_empty'),
    cards: document.querySelectorAll('.o_carousel_product_card, .oe_product').length,
    templateHtml: document.querySelector('.dynamic_snippet_template')?.innerHTML?.length || 0,
    filterId: document.querySelector('.s_dynamic_snippet_products')?.dataset?.filterId,
    templateKey: document.querySelector('.s_dynamic_snippet_products')?.dataset?.templateKey,
  }));

  console.log('\n===', label, '===');
  console.log(JSON.stringify({ result, failed: failed.slice(0, 5), logs: logs.filter(l => l.type !== 'log').slice(0, 10) }, null, 2));
  await context.close();
}

await probe('header-db', {
  url: 'http://localhost:18079/?db=dorevia_ck_marketone_01',
  context: { extraHTTPHeaders: { 'X-Odoo-Database': 'dorevia_ck_marketone_01' } },
});

await probe('db-param-only', {
  url: 'http://localhost:18079/?db=dorevia_ck_marketone_01',
});

// Simulate MOA: pick DB then visit /
const ctx = await browser.newContext();
const page = await ctx.newPage();
await page.goto('http://localhost:18079/web/database/selector', { waitUntil: 'networkidle', timeout: 60000 });
const dbLink = page.locator('a[href*="dorevia_ck_marketone_01"]');
if (await dbLink.count()) {
  await dbLink.first().click();
  await page.waitForLoadState('networkidle');
  await page.goto('http://localhost:18079/', { waitUntil: 'networkidle', timeout: 60000 });
  await page.waitForTimeout(5000);
  const result = await page.evaluate(() => ({
    url: location.href,
    cards: document.querySelectorAll('.o_carousel_product_card, .oe_product').length,
    loading: !!document.querySelector('.o_dynamic_snippet_loading'),
    templateHtml: document.querySelector('.dynamic_snippet_template')?.innerHTML?.length || 0,
  }));
  console.log('\n=== db-selector-then-home ===');
  console.log(JSON.stringify(result, null, 2));
}
await ctx.close();

await browser.close();
