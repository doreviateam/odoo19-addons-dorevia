import { chromium } from 'playwright';

const browser = await chromium.launch({ headless: true });

async function measureLayoutShift(viewport) {
  const ctx = await browser.newContext({
    viewport,
    extraHTTPHeaders: { 'X-Odoo-Database': 'dorevia_ck_marketone_01' },
  });
  const page = await ctx.newPage();
  let cls = 0;
  await page.addInitScript(() => {
    window.__cls = 0;
    new PerformanceObserver((list) => {
      for (const e of list.getEntries()) {
        if (!e.hadRecentInput) window.__cls += e.value;
      }
    }).observe({ type: 'layout-shift', buffered: true });
  });

  await page.goto('http://localhost:18079/', { waitUntil: 'networkidle', timeout: 60000 });
  await page.waitForTimeout(1000);

  const grid = page.locator('.ck-featured-products__grid--stable');
  await grid.scrollIntoViewIfNeeded();
  const before = await page.evaluate(() => {
    const el = document.querySelector('.ck-featured-products__grid--stable');
    const cards = [...document.querySelectorAll('.ck-featured-products__grid--stable .o_carousel_product_card')];
    return {
      gridHeight: el?.getBoundingClientRect().height,
      cardHeights: cards.map((c) => Math.round(c.getBoundingClientRect().height)),
      imageHeights: cards.map((c) => Math.round(c.querySelector('.oe_product_image')?.getBoundingClientRect().height || 0)),
    };
  });

  // Scroll page through featured block slowly
  for (let y = 0; y <= 800; y += 80) {
    await page.evaluate((yy) => window.scrollTo(0, yy), y);
    await page.waitForTimeout(120);
  }
  await page.waitForTimeout(500);

  const after = await page.evaluate(() => ({
    cls: window.__cls || 0,
    gridHeight: document.querySelector('.ck-featured-products__grid--stable')?.getBoundingClientRect().height,
    scrollWidth: document.documentElement.scrollWidth,
    clientWidth: document.documentElement.clientWidth,
  }));

  console.log(JSON.stringify({ viewport, before, after }, null, 2));
  await ctx.close();
}

await measureLayoutShift({ width: 1280, height: 900 });
await measureLayoutShift({ width: 390, height: 844 });
await browser.close();
