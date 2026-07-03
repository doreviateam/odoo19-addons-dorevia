/**
 * Recette QA CATALOG-ARCHI-001 Lot C.
 *
 * Bascule temporairement Boissons (id 123) dans chaque statut de test,
 * controle HTTP + sitemap, puis restaure l'etat initial.
 */
import { execFileSync } from 'node:child_process';
import { mkdir, writeFile } from 'node:fs/promises';
import { join, dirname } from 'node:path';
import { fileURLToPath } from 'node:url';

const __dir = dirname(fileURLToPath(import.meta.url));
const OUT = join(__dir, '..', 'captures', 'recette_catalog_archi_001_abc_20260703');
const DB = 'dorevia_ck_marketone_01';
const BASE = 'http://localhost:18079';
const CATEGORY_ID = 123;
const CATEGORY_URL = '/shop/category/boissons-123';
const REPLACEMENT_ID = 1;

function psql(sql) {
  return execFileSync(
    'docker',
    ['exec', 'sandbox-odoo19-db-1', 'psql', '-U', 'odoo', '-d', DB, '-At', '-F', '\t', '-c', sql],
    { encoding: 'utf8' },
  ).trim();
}

function setCategory(status, replacementId = null) {
  const replacement = replacementId ? String(replacementId) : 'null';
  psql(`
    update product_public_category
       set ck_exposure_status = '${status}',
           ck_replacement_category_id = ${replacement},
           write_date = now()
     where id = ${CATEGORY_ID};
    delete from ir_attachment where url like '/sitemap-%';
  `);
}

async function routeProbe() {
  const response = await fetch(`${BASE}${CATEGORY_URL}?db=${DB}`, {
    redirect: 'manual',
    headers: { 'Accept-Language': 'fr-FR,fr;q=0.9' },
  });
  const text = await response.text();
  return {
    status: response.status,
    location: response.headers.get('location'),
    noindex: text.toLowerCase().includes('noindex'),
    bodyLength: text.length,
  };
}

async function sitemapProbe() {
  const response = await fetch(`${BASE}/sitemap.xml?db=${DB}`, {
    headers: { 'Accept-Language': 'fr-FR,fr;q=0.9' },
  });
  const text = await response.text();
  return {
    status: response.status,
    hasEpicerie: text.includes('epicerie-1'),
    hasBoissons: text.includes('boissons-123'),
    hasSoin: text.includes('soin-bien-etre-2'),
    hasArtisanat: text.includes('artisanat-3'),
  };
}

await mkdir(OUT, { recursive: true });

const originalRaw = psql(`
  select ck_exposure_status, coalesce(ck_replacement_category_id::text, '')
    from product_public_category
   where id = ${CATEGORY_ID};
`);
const [originalStatus, originalReplacement] = originalRaw.split('\t');

const scenarios = [
  { name: 'promise', status: 'promise', replacementId: null },
  { name: 'hidden', status: 'hidden', replacementId: null },
  { name: 'draft', status: 'draft', replacementId: null },
  { name: 'archived_with_replacement', status: 'archived', replacementId: REPLACEMENT_ID },
  { name: 'archived_without_replacement', status: 'archived', replacementId: null },
];

const results = {
  date: '2026-07-03',
  db: DB,
  categoryId: CATEGORY_ID,
  categoryUrl: CATEGORY_URL,
  original: {
    status: originalStatus,
    replacementId: originalReplacement || null,
  },
  scenarios: [],
  restored: null,
};

try {
  for (const scenario of scenarios) {
    setCategory(scenario.status, scenario.replacementId);
    results.scenarios.push({
      scenario: scenario.name,
      route: await routeProbe(),
      sitemap: await sitemapProbe(),
    });
  }
} finally {
  setCategory(originalStatus, originalReplacement || null);
}

results.restored = {
  raw: psql(`
    select ck_exposure_status, coalesce(ck_replacement_category_id::text, '')
      from product_public_category
     where id = ${CATEGORY_ID};
  `),
  route: await routeProbe(),
  sitemap: await sitemapProbe(),
};

await writeFile(join(OUT, 'recette_catalog_archi_001_lotc_switches.json'), JSON.stringify(results, null, 2));
console.log(JSON.stringify(results, null, 2));
