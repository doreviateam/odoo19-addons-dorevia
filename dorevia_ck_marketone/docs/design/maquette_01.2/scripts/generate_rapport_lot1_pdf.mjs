#!/usr/bin/env node
/**
 * Génère le rapport MOA PDF — Maquette CK V1.2.x Lot 1
 * Usage: node generate_rapport_lot1_pdf.mjs [--base-url=http://127.0.0.1:8766] [--skip-capture]
 */
import { chromium } from 'playwright';
import { mkdir, writeFile, readFile, access } from 'fs/promises';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
import { spawn } from 'child_process';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = join(__dirname, '..');
const RAPPORT_DIR = join(ROOT, 'rapport');
const CAPTURES_DIR = join(RAPPORT_DIR, 'captures');
const RAPPORT_HTTP_PORT = 8767;

const baseUrlArg = process.argv.find((a) => a.startsWith('--base-url='));
const BASE_URL = baseUrlArg ? baseUrlArg.split('=')[1] : 'http://127.0.0.1:8766';
const SKIP_CAPTURE = process.argv.includes('--skip-capture');

const PAGES = [
  {
    id: 'accueil',
    file: 'index.html',
    title: 'Accueil enrichie',
    route: '/',
    role: 'Promesse CK · réassurance · produits · coffret · signal B2B',
    blocs: [
      'Header marchand',
      'Hero court + CTA boutique / Pro',
      'Réassurance (4 preuves)',
      'Produits vedettes ×6',
      'Catégories / univers',
      'Coffret découverte',
      'Espace Pro home',
      'Éditorial + footer',
    ],
  },
  {
    id: 'fiche-produit',
    file: 'fiche-produit.html',
    title: 'Fiche produit type',
    route: '/shop/confiture-goyavier-123',
    role: 'Valeur CK : origine · usage · producteur · conservation · association · signal pro',
    blocs: [
      'Galerie + achat (prix · panier)',
      'Origine & usage',
      'Producteur',
      'Conservation',
      'Associations',
      'Idée recette',
      'Signal B2B',
      'Cross-sell',
    ],
  },
  {
    id: 'professionnels',
    file: 'professionnels.html',
    title: 'Page Professionnels',
    route: '/professionnels',
    role: 'Double cible producteurs / distributeurs · qualification · pas portail B2B',
    blocs: [
      'Hero double entrée',
      'Cartes producteurs / distributeurs',
      'Process qualification ×3',
      'Réassurance pro',
      'Formulaire CRM mock',
      'Note qualification',
    ],
  },
];

const REPORT_CSS = `
  @page { size: A4; margin: 14mm 12mm; }
  * { box-sizing: border-box; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
  body {
    font-family: Arial, Helvetica, sans-serif;
    font-size: 10.5pt;
    line-height: 1.5;
    color: #1c1917;
    margin: 0;
    padding: 0;
    background: #fff;
  }
  .sheet { page-break-after: always; padding: 4mm 0 8mm; }
  .sheet:last-child { page-break-after: auto; }

  .cover { background: #fffbf7; border-bottom: 4px solid #d84315; padding: 18mm 0 14mm; }
  .cover h1 { font-size: 26pt; margin: 0 0 8px; font-weight: 700; }
  .cover h1 span { color: #d84315; }
  .cover .subtitle { font-size: 13pt; color: #57534e; margin: 0 0 24px; line-height: 1.4; }
  .cover .verdict {
    display: inline-block; background: #2e7d4f; color: #fff; font-weight: 700;
    padding: 8px 16px; border-radius: 6px; font-size: 10.5pt; margin: 0 0 20px;
  }
  .cover table { border-collapse: collapse; font-size: 10pt; width: 100%; max-width: 520px; }
  .cover td { padding: 5px 12px 5px 0; vertical-align: top; color: #44403c; }
  .cover td:first-child { font-weight: 700; color: #1c1917; width: 130px; }

  h2 { font-size: 15pt; color: #d84315; margin: 0 0 10px; font-weight: 700; }
  h3 { font-size: 11pt; margin: 16px 0 8px; font-weight: 700; color: #1c1917; }
  p { margin: 0 0 10px; }
  .meta { font-size: 9.5pt; color: #57534e; margin-bottom: 12px; line-height: 1.55; }
  code { font-size: 8.5pt; background: #f5f0e8; padding: 1px 5px; border-radius: 3px; font-family: Menlo, Consolas, monospace; }

  table.data { width: 100%; border-collapse: collapse; font-size: 9pt; margin: 10px 0 14px; }
  table.data th, table.data td { border: 1px solid #d6d3d1; padding: 6px 8px; text-align: left; vertical-align: top; }
  table.data th { background: #f5f0e8; font-weight: 700; }
  .ok { color: #2e7d4f; font-weight: 700; }
  .reserve { color: #b45309; font-weight: 600; }

  .doctrine {
    background: #f5f0e8; padding: 10px 12px; border-radius: 6px; font-size: 9.5pt;
    margin: 10px 0 14px; border-left: 4px solid #d84315; line-height: 1.5;
  }
  ul.blocs { margin: 0 0 12px; padding-left: 20px; font-size: 9.5pt; }
  ul.blocs li { margin-bottom: 4px; }

  .visual-sheet h3 { margin-top: 0; color: #d84315; }
  figure { margin: 0; }
  figure img {
    width: 100%; height: auto; display: block;
    border: 1px solid #d6d3d1; border-radius: 4px;
  }
  figure.mobile img { width: 42%; min-width: 140px; max-width: 200px; margin: 0 auto; }

  .footer-note {
    margin-top: 16px; padding-top: 10px; border-top: 1px solid #e7e0d5;
    font-size: 8.5pt; color: #78716c; line-height: 1.45;
  }
`;

async function startHttpServer(cwd, port) {
  try {
    const res = await fetch(`http://127.0.0.1:${port}/`);
    if (res.ok) return;
  } catch { /* start */ }
  const proc = spawn('python3', ['-m', 'http.server', String(port)], {
    cwd,
    detached: true,
    stdio: 'ignore',
  });
  proc.unref();
  for (let i = 0; i < 20; i++) {
    await new Promise((r) => setTimeout(r, 200));
    try {
      const res = await fetch(`http://127.0.0.1:${port}/`);
      if (res.ok) return;
    } catch { /* retry */ }
  }
  throw new Error(`Serveur HTTP indisponible sur le port ${port}`);
}

async function ensureMaquetteServer() {
  await startHttpServer(join(ROOT, 'artifact'), 8766);
  try {
    const res = await fetch(`${BASE_URL}/index.html`);
    if (!res.ok) throw new Error('maquette down');
  } catch {
    throw new Error(`Maquette indisponible sur ${BASE_URL}`);
  }
}

async function captureScreenshots(browser) {
  const shots = [];
  for (const page of PAGES) {
    for (const vp of [
      { label: 'desktop', width: 1280, height: 800 },
      { label: 'mobile', width: 390, height: 844 },
    ]) {
      const filename = `${page.id}-${vp.label}.png`;
      const filepath = join(CAPTURES_DIR, filename);
      const ctx = await browser.newContext({
        viewport: { width: vp.width, height: vp.height },
        deviceScaleFactor: vp.label === 'mobile' ? 2 : 1,
      });
      const tab = await ctx.newPage();
      await tab.goto(`${BASE_URL}/${page.file}`, { waitUntil: 'networkidle', timeout: 60000 });
      await tab.waitForTimeout(800);
      await tab.screenshot({ path: filepath, fullPage: true });
      shots.push({ page, vp, filename, filepath });
      await ctx.close();
    }
  }
  return shots;
}

async function loadExistingShots() {
  const shots = [];
  for (const page of PAGES) {
    for (const label of ['desktop', 'mobile']) {
      const filename = `${page.id}-${label}.png`;
      const filepath = join(CAPTURES_DIR, filename);
      await access(filepath);
      shots.push({ page, vp: { label }, filename, filepath });
    }
  }
  return shots;
}

function buildReportHtml(shots, date) {
  const pageSections = PAGES.map((p) => {
    const desktop = shots.find((s) => s.page.id === p.id && s.vp.label === 'desktop');
    const mobile = shots.find((s) => s.page.id === p.id && s.vp.label === 'mobile');
    const blocsList = p.blocs.map((b) => `<li>${b}</li>`).join('');
    return `
<section class="sheet text-sheet">
  <h2>${p.title}</h2>
  <p class="meta"><strong>Rôle :</strong> ${p.role}<br/>
  <strong>Route Odoo cible :</strong> <code>${p.route}</code><br/>
  <strong>Fichier artifact :</strong> <code>artifact/${p.file}</code></p>
  <h3>Blocs matérialisés</h3>
  <ul class="blocs">${blocsList}</ul>
</section>
<section class="sheet visual-sheet">
  <h3>${p.title} — Desktop 1280 px</h3>
  <figure><img src="captures/${desktop.filename}" alt="${p.title} desktop" /></figure>
</section>
<section class="sheet visual-sheet">
  <h3>${p.title} — Mobile 390 px</h3>
  <figure class="mobile"><img src="captures/${mobile.filename}" alt="${p.title} mobile" /></figure>
</section>`;
  }).join('\n');

  return `<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8" />
  <title>Rapport MOA — Maquette CK V1.2.x Lot 1</title>
  <style>${REPORT_CSS}</style>
</head>
<body>

<section class="sheet cover">
  <p class="verdict">OK MAQUETTE CK V1.2.x LOT 1</p>
  <h1>C-<span>Kreyol</span></h1>
  <p class="subtitle">Rapport MOA — Maquette HTML V1.2.x · Lot 1 recetté<br/>Vision matérialisée · Odoo en pause</p>
  <table>
    <tr><td>Projet</td><td>dorevia_ck_marketone · thème dorevia_ck_theme</td></tr>
    <tr><td>Date rapport</td><td>${date}</td></tr>
    <tr><td>Verdict QA</td><td>OK MAQUETTE CK V1.2.x LOT 1 (Lot 1.1 validé)</td></tr>
    <tr><td>Périmètre</td><td>Accueil enrichie · Fiche produit type · Page Professionnels</td></tr>
    <tr><td>Artifact</td><td>docs/design/maquette_01.2/artifact/</td></tr>
    <tr><td>Preview maquette</td><td>${BASE_URL}/</td></tr>
    <tr><td>Odoo</td><td>EN PAUSE — aucune traduction demandée</td></tr>
    <tr><td>Suite</td><td>Lot 2 maquette (Shop · Catégorie)</td></tr>
  </table>
</section>

<section class="sheet">
  <h2>1. Synthèse exécutive</h2>
  <div class="doctrine">
    Doctrine MOA : la maquette est le terrain de décision ; Odoo reste figé comme preuve de faisabilité jusqu’à arbitrage de traduction.
  </div>
  <p>Le Lot 1 matérialise la promesse CK, la valeur produit enrichie et la double cible B2C/B2B. La recette QA (desktop 1280 px · mobile 390 px) confirme : visuels chargés (10/10 URLs), absence d’overflow horizontal, démonstration propre (tags arbitrage masqués).</p>
  <h3>Pages livrées</h3>
  <table class="data">
    <thead><tr><th>Page</th><th>Statut QA</th><th>Rôle expérience</th></tr></thead>
    <tbody>
      <tr><td>Accueil enrichie</td><td class="ok">OK</td><td>Boutique élégante · conversion · réassurance · signal Pro</td></tr>
      <tr><td>Fiche produit type</td><td class="ok">OK</td><td>Produit enrichi CK — origine · usage · producteur · B2B</td></tr>
      <tr><td>Professionnels</td><td class="ok">OK</td><td>Double cible · qualification · formulaire CRM</td></tr>
    </tbody>
  </table>
</section>

<section class="sheet">
  <h2>2. Classes d’arbitrage &amp; contrôles QA</h2>
  <h3>Concepts — synthèse</h3>
  <table class="data">
    <thead><tr><th>Classe</th><th>Éléments Lot 1</th></tr></thead>
    <tbody>
      <tr><td class="ok">V1 prioritaire</td><td>Home marchande · réassurance · produits prix/origine · achat fiche · signal Pro · page Pro + CRM</td></tr>
      <tr><td>V1 possible</td><td>Bloc producteur fiche · process Pro · coffret · badges · réassurance pro</td></tr>
      <tr><td class="reserve">V1 différée</td><td>Shop · catégorie · associations fiche · recette/blog · cross-sell avancé</td></tr>
      <tr><td class="reserve">Réserves non bloquantes</td><td>Routes Odoo à mapper · promesses logistiques à confirmer · fiche fournisseur à arbitrer</td></tr>
      <tr><td>Hors scope</td><td>Portail B2B · checkout pro · catalogue parallèle</td></tr>
    </tbody>
  </table>
  <h3>Contrôles QA Lot 1.1</h3>
  <table class="data">
    <thead><tr><th>Contrôle</th><th>Résultat</th></tr></thead>
    <tbody>
      <tr><td>Image fiche produit</td><td class="ok">OK — desktop + mobile</td></tr>
      <tr><td>URLs visuelles Unsplash</td><td class="ok">OK — 10/10 HTTP 200</td></tr>
      <tr><td>Tags .arbitrage-tag</td><td class="ok">OK — masqués au rendu</td></tr>
      <tr><td>Mobile 390 px</td><td class="ok">OK — 3 pages sans overflow</td></tr>
      <tr><td>Desktop 1280 px</td><td class="ok">OK — 3 pages sans overflow</td></tr>
    </tbody>
  </table>
</section>

<section class="sheet">
  <h2>3. Parcours maquette</h2>
  <p><strong>B2C :</strong> Accueil → Confiture goyavier (fiche) → panier</p>
  <p><strong>B2B :</strong> Accueil / fiche → Espace Pro → formulaire qualification</p>
  <p><strong>Liens relatifs Lot 1 :</strong> index.html ↔ fiche-produit.html ↔ professionnels.html</p>
  <h3>Visuels des pages</h3>
  <p>Les sections suivantes reprennent pour chaque page : une fiche texte (rôle · blocs), puis les captures desktop et mobile.</p>
</section>

${pageSections}

<section class="sheet">
  <h2>4. Suite MOA</h2>
  <table class="data">
    <thead><tr><th>Étape</th><th>Statut</th></tr></thead>
    <tbody>
      <tr><td>GO Lot 1 · production artifact</td><td class="ok">✅</td></tr>
      <tr><td>Recette QA Lot 1.1</td><td class="ok">✅ OK</td></tr>
      <tr><td>Rapport MOA PDF</td><td class="ok">✅</td></tr>
      <tr><td>GO Lot 2 — Shop · Catégorie</td><td>À acter MOA</td></tr>
      <tr><td>Reprise Odoo traduction</td><td>En pause</td></tr>
    </tbody>
  </table>
  <p class="footer-note">
    Références : recette_qa_maquette_v1_2_x.md · CADRAGE_MAQUETTE_CK_V1_2_X.md · LIVRAISON_V1_2_X_LOT1.md<br/>
    Généré par scripts/generate_rapport_lot1_pdf.mjs · C-Kreyol / Dorevia · ${date}
  </p>
</section>

</body>
</html>`;
}

async function waitForImages(page) {
  await page.evaluate(async () => {
    await Promise.all(
      Array.from(document.images).map((img) =>
        img.complete && img.naturalWidth > 0
          ? Promise.resolve()
          : new Promise((resolve, reject) => {
              img.onload = () => resolve();
              img.onerror = () => reject(new Error(`Image failed: ${img.src}`));
            })
      )
    );
  });
}

async function main() {
  await mkdir(CAPTURES_DIR, { recursive: true });
  const date = new Date().toISOString().slice(0, 10);

  const browser = await chromium.launch({ headless: true });

  let shots;
  if (SKIP_CAPTURE) {
    console.log('Reprise captures existantes…');
    shots = await loadExistingShots();
  } else {
    await ensureMaquetteServer();
    console.log('Capture des écrans maquette…');
    shots = await captureScreenshots(browser);
  }

  const htmlPath = join(RAPPORT_DIR, 'RAPPORT_MOA_MAQUETTE_CK_V1_2_X_LOT1.html');
  let html;
  try {
    html = await readFile(htmlPath, 'utf8');
    console.log('HTML rapport repris :', htmlPath);
  } catch {
    html = buildReportHtml(shots, date);
    await writeFile(htmlPath, html, 'utf8');
    console.log('HTML rapport généré :', htmlPath);
  }

  await startHttpServer(RAPPORT_DIR, RAPPORT_HTTP_PORT);
  const reportUrl = `http://127.0.0.1:${RAPPORT_HTTP_PORT}/RAPPORT_MOA_MAQUETTE_CK_V1_2_X_LOT1.html`;

  const pdfPage = await browser.newPage();
  await pdfPage.goto(reportUrl, { waitUntil: 'networkidle', timeout: 120000 });
  await waitForImages(pdfPage);
  await pdfPage.emulateMedia({ media: 'print' });

  const check = await pdfPage.evaluate(() => ({
    textLength: (document.body.innerText || '').trim().length,
    images: document.images.length,
    imagesOk: Array.from(document.images).filter((i) => i.naturalWidth > 0).length,
    hasCover: !!document.querySelector('.cover h1'),
    hasDecisionReading: (document.body.innerText || '').includes('Lecture MOA'),
  }));
  console.log('Vérification rendu :', check);
  if (check.textLength < 500) throw new Error('Texte insuffisant dans le DOM avant export PDF');

  const pdfPath = join(RAPPORT_DIR, 'RAPPORT_MOA_MAQUETTE_CK_V1_2_X_LOT1.pdf');
  await pdfPage.pdf({
    path: pdfPath,
    format: 'A4',
    printBackground: true,
    preferCSSPageSize: true,
    margin: { top: '12mm', bottom: '12mm', left: '10mm', right: '10mm' },
  });
  await browser.close();

  const stat = await readFile(pdfPath).then((b) => b.length);
  console.log('PDF rapport :', pdfPath, `(${(stat / 1024 / 1024).toFixed(2)} Mo)`);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
