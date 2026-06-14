#!/usr/bin/env node
/**
 * Génère un atlas visuel MOA par section — Maquette CK V1.2.x Lot 1.1
 * Usage: node generate_rapport_lot1_sections_pdf.mjs [--base-url=http://127.0.0.1:8766] [--skip-capture]
 */
import { chromium } from 'playwright';
import { mkdir, writeFile, readFile, access } from 'fs/promises';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
import { spawn } from 'child_process';

const __dirname = dirname(fileURLToPath(import.meta.url));
const ROOT = join(__dirname, '..');
const RAPPORT_DIR = join(ROOT, 'rapport');
const CAPTURES_DIR = join(RAPPORT_DIR, 'captures_sections');
const RAPPORT_HTTP_PORT = 8768;

const baseUrlArg = process.argv.find((a) => a.startsWith('--base-url='));
const BASE_URL = baseUrlArg ? baseUrlArg.split('=')[1] : 'http://127.0.0.1:8766';
const SKIP_CAPTURE = process.argv.includes('--skip-capture');

const PAGES = [
  {
    id: 'accueil',
    title: 'Accueil',
    file: 'index.html',
    intent: 'Prouver que CK est une boutique élégante orientée achat, pas une vitrine contemplative.',
    sections: [
      {
        id: 'hero',
        title: 'Hero court',
        selectors: ['.hero'],
        role: 'Installer immédiatement la promesse marchande : saveurs créoles, produits commandables, entrée boutique et entrée Pro.',
        arbitration: 'V1 prioritaire',
      },
      {
        id: 'reassurance',
        title: 'Réassurance',
        selectors: ['.trust-bar'],
        role: 'Donner les preuves nécessaires avant exposition produit : livraison, paiement, sélection, service.',
        arbitration: 'V1 prioritaire',
      },
      {
        id: 'produits',
        title: 'Produits vedettes',
        selectors: ['#produits'],
        role: 'Faire vendre vite : produits visibles, prix TTC, origine, famille produit et CTA court.',
        arbitration: 'V1 prioritaire',
      },
      {
        id: 'univers',
        title: 'Univers / catégories',
        selectors: ['#univers'],
        role: 'Préparer le Lot 2 : structurer la découverte par familles sans surcharger la home.',
        arbitration: 'V1 différée vers Lot 2',
      },
      {
        id: 'coffret',
        title: 'Coffret découverte',
        selectors: ['.packs-strip'],
        role: 'Introduire une offre simple à comprendre, utile pour cadeau, panier moyen et première commande.',
        arbitration: 'V1 possible',
      },
      {
        id: 'pro-home',
        title: 'Signal professionnel',
        selectors: ['#espace-pro'],
        role: 'Rendre visible la double cible sans transformer la home en portail B2B.',
        arbitration: 'V1 prioritaire',
      },
      {
        id: 'editorial-footer',
        title: 'Éditorial bas + footer',
        selectors: ['.editorial', '.site-footer'],
        role: 'Fermer avec la mission CK, les liens utiles et un footer propre sans effet template.',
        arbitration: 'V1 possible / V1 prioritaire footer',
      },
    ],
  },
  {
    id: 'fiche-produit',
    title: 'Fiche produit type',
    file: 'fiche-produit.html',
    intent: 'Montrer comment vendre avec élégance : valeur d’usage, origine, achat simple et signal Pro.',
    sections: [
      {
        id: 'achat',
        title: 'Zone achat',
        selectors: ['.breadcrumb', '.product-layout'],
        role: 'Fiche produit native : image, badges, prix, quantité, panier, achat immédiat et preuves courtes.',
        arbitration: 'V1 prioritaire',
      },
      {
        id: 'details',
        title: 'Détails enrichis',
        selectors: ['section[aria-labelledby="enrich-title"]'],
        role: 'Créer de la valeur : origine, terroir, producteur, conservation et associations.',
        arbitration: 'V1 prioritaire + V1 possible + V1 différée',
      },
      {
        id: 'recette',
        title: 'Idée recette',
        selectors: ['section[aria-labelledby="recipe-title"]'],
        role: 'Faire vivre le produit au-delà de la fiche technique ; bon levier éditorial, non obligatoire V1.',
        arbitration: 'V1 différée',
      },
      {
        id: 'signal-pro',
        title: 'Signal B2B fiche',
        selectors: ['.pro-strip'],
        role: 'Orienter les professionnels vers la qualification sans afficher de conditions B2B publiques.',
        arbitration: 'V1 prioritaire',
      },
      {
        id: 'cross-sell',
        title: 'Produits associés',
        selectors: ['section[aria-labelledby="related-title"]'],
        role: 'Préparer le cross-sell et les associations de panier, à arbitrer avec les capacités Odoo.',
        arbitration: 'V1 différée',
      },
      {
        id: 'footer',
        title: 'Footer fiche',
        selectors: ['.site-footer'],
        role: 'Maintenir une sortie propre et cohérente avec la boutique.',
        arbitration: 'V1 prioritaire',
      },
    ],
  },
  {
    id: 'professionnels',
    title: 'Professionnels',
    file: 'professionnels.html',
    intent: 'Clarifier la cible Pro : producteurs et distributeurs, avec qualification CRM et sans portail B2B.',
    sections: [
      {
        id: 'hero',
        title: 'Hero professionnel',
        selectors: ['.pro-page-hero'],
        role: 'Positionner la page : double cible, conditions sur qualification, pas de commande pro immédiate.',
        arbitration: 'V1 prioritaire',
      },
      {
        id: 'double-cible',
        title: 'Double cible',
        selectors: ['section[aria-labelledby="dual-title"]'],
        role: 'Séparer producteurs / transformateurs et distributeurs / CHR avec des critères lisibles.',
        arbitration: 'V1 prioritaire',
      },
      {
        id: 'process',
        title: 'Process qualification',
        selectors: ['section[aria-labelledby="process-title"]'],
        role: 'Rassurer sans promettre un workflow custom : demande, contact, conditions sur mesure.',
        arbitration: 'V1 possible',
      },
      {
        id: 'reassurance-pro',
        title: 'Réassurance Pro',
        selectors: ['.trust-bar'],
        role: 'Montrer logistique, relation, sélection et réseau de distribution.',
        arbitration: 'V1 possible',
      },
      {
        id: 'formulaire',
        title: 'Formulaire CRM',
        selectors: ['section[aria-labelledby="form-title"]'],
        role: 'Transformer l’intérêt Pro en lead qualifié via un formulaire Odoo cible.',
        arbitration: 'V1 prioritaire',
      },
      {
        id: 'note-footer',
        title: 'Note qualification + footer',
        selectors: ['section[aria-labelledby="note-qualif"]', '.site-footer'],
        role: 'Rappeler la règle : prix publics B2C, relation B2B étudiée après dossier.',
        arbitration: 'V1 prioritaire',
      },
    ],
  },
];

const REPORT_CSS = `
  @page { size: A4 landscape; margin: 10mm; }
  * { box-sizing: border-box; -webkit-print-color-adjust: exact; print-color-adjust: exact; }
  body { margin:0; color:#211813; background:#fff; font-family:Arial, Helvetica, sans-serif; font-size:9.6pt; line-height:1.42; }
  .sheet { page-break-after:always; padding:2mm 0 5mm; }
  .sheet:last-child { page-break-after:auto; }
  .cover { min-height:185mm; display:flex; flex-direction:column; justify-content:space-between; background:#fff8f1; border-top:7px solid #8f3f5f; padding:13mm 14mm; }
  .eyebrow { margin:0 0 7px; color:#8f3f5f; font-size:9pt; font-weight:700; text-transform:uppercase; letter-spacing:.04em; }
  h1 { margin:0 0 10px; font-size:28pt; line-height:1.05; }
  h1 span, h2 { color:#8f3f5f; }
  h2 { margin:0 0 8px; font-size:15pt; line-height:1.16; }
  h3 { margin:0 0 6px; font-size:11pt; color:#211813; }
  p { margin:0 0 8px; }
  .lead { max-width:190mm; color:#574a42; font-size:12pt; line-height:1.38; }
  .verdict { display:inline-block; width:fit-content; padding:7px 12px; background:#2d6b4f; color:#fff; border-radius:5px; font-weight:700; margin-bottom:13px; }
  .grid3 { display:grid; grid-template-columns:repeat(3, 1fr); gap:9px; margin-top:18px; }
  .card { border:1px solid #e3d7ca; background:#fff; border-radius:6px; padding:10px 11px; }
  .card strong { display:block; margin-bottom:3px; color:#211813; }
  .card span { color:#675c55; font-size:9pt; }
  table { width:100%; border-collapse:collapse; margin:8px 0 12px; font-size:8.7pt; }
  th, td { border:1px solid #ded3c8; padding:5px 7px; text-align:left; vertical-align:top; }
  th { background:#f4ede5; }
  .ok { color:#2d6b4f; font-weight:700; }
  .reserve { color:#a15c13; font-weight:700; }
  .section-sheet { display:grid; grid-template-columns:72mm 1fr; gap:10mm; align-items:start; }
  .section-meta { border-left:4px solid #8f3f5f; padding-left:9px; }
  .page-label { display:inline-block; color:#8f3f5f; font-weight:700; margin-bottom:7px; text-transform:uppercase; letter-spacing:.035em; font-size:8.5pt; }
  .pill { display:inline-block; padding:4px 7px; border-radius:999px; background:#f4ede5; color:#5f5148; font-size:8.2pt; font-weight:700; }
  figure { margin:0; }
  figure img { width:100%; height:auto; display:block; border:1px solid #d9d0c8; border-radius:5px; }
  .summary-list { margin:0; padding-left:17px; }
  .summary-list li { margin-bottom:4px; }
  .footer-note { margin-top:12px; padding-top:8px; border-top:1px solid #e3d7ca; color:#756a62; font-size:8.3pt; }
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
  for (let i = 0; i < 25; i++) {
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
  const res = await fetch(`${BASE_URL}/index.html`);
  if (!res.ok) throw new Error(`Maquette indisponible sur ${BASE_URL}`);
}

function cssEscape(value) {
  return value.replace(/[^a-z0-9_-]/gi, '-').toLowerCase();
}

async function captureSection(page, section, targetPath) {
  const clip = await page.evaluate((selectors) => {
    const rects = selectors.flatMap((selector) =>
      Array.from(document.querySelectorAll(selector)).map((el) => {
        const rect = el.getBoundingClientRect();
        return {
          left: rect.left + window.scrollX,
          top: rect.top + window.scrollY,
          right: rect.right + window.scrollX,
          bottom: rect.bottom + window.scrollY,
        };
      })
    );
    if (!rects.length) return null;
    const left = Math.max(0, Math.min(...rects.map((r) => r.left)) - 12);
    const top = Math.max(0, Math.min(...rects.map((r) => r.top)) - 12);
    const right = Math.min(document.documentElement.scrollWidth, Math.max(...rects.map((r) => r.right)) + 12);
    const bottom = Math.min(document.documentElement.scrollHeight, Math.max(...rects.map((r) => r.bottom)) + 12);
    const width = Math.max(1, Math.ceil(right - left));
    const height = Math.max(1, Math.ceil(bottom - top));
    return {
      x: Math.floor(left),
      y: Math.floor(top),
      width,
      height,
    };
  }, section.selectors);
  if (!clip) throw new Error(`Section introuvable: ${section.title}`);
  console.log('Capture section :', section.title, clip);
  await page.screenshot({ path: targetPath, clip, fullPage: true });
  return clip;
}

async function captureSections(browser) {
  const shots = [];
  for (const pageSpec of PAGES) {
    const context = await browser.newContext({ viewport: { width: 1280, height: 900 }, deviceScaleFactor: 1 });
    const page = await context.newPage();
    await page.goto(`${BASE_URL}/${pageSpec.file}`, { waitUntil: 'networkidle', timeout: 60000 });
    await page.waitForTimeout(500);
    for (const section of pageSpec.sections) {
      const filename = `${pageSpec.id}-${cssEscape(section.id)}.png`;
      const filepath = join(CAPTURES_DIR, filename);
      const clip = await captureSection(page, section, filepath);
      shots.push({ page: pageSpec, section, filename, clip });
    }
    await context.close();
  }
  return shots;
}

async function loadExistingShots() {
  const shots = [];
  for (const pageSpec of PAGES) {
    for (const section of pageSpec.sections) {
      const filename = `${pageSpec.id}-${cssEscape(section.id)}.png`;
      await access(join(CAPTURES_DIR, filename));
      shots.push({ page: pageSpec, section, filename });
    }
  }
  return shots;
}

function buildReportHtml(shots) {
  const sectionPages = shots.map((shot, index) => `
  <section class="sheet section-sheet">
    <div class="section-meta">
      <span class="page-label">${shot.page.title}</span>
      <h2>${index + 1}. ${shot.section.title}</h2>
      <p>${shot.section.role}</p>
      <p><span class="pill">${shot.section.arbitration}</span></p>
      <h3>Lecture MOA</h3>
      <p>Cette planche sert de référence visuelle pour arbitrer la traduction Odoo : ce bloc doit-il être repris tel quel, simplifié, différé ou transformé en contenu éditorial ?</p>
      <h3>Page source</h3>
      <p><code>artifact/${shot.page.file}</code></p>
    </div>
    <figure><img src="captures_sections/${shot.filename}" alt="${shot.page.title} — ${shot.section.title}" /></figure>
  </section>`).join('\n');

  const summaryRows = PAGES.map((pageSpec) => `
        <tr>
          <td>${pageSpec.title}</td>
          <td>${pageSpec.sections.length}</td>
          <td>${pageSpec.intent}</td>
        </tr>`).join('');

  return `<!DOCTYPE html>
<html lang="fr">
<head>
  <meta charset="UTF-8" />
  <title>Atlas visuel MOA — Maquette CK V1.2.x Lot 1.1</title>
  <style>${REPORT_CSS}</style>
</head>
<body>
  <section class="sheet cover">
    <div>
      <p class="eyebrow">Support de présentation MOA · Références visuelles par section</p>
      <p class="verdict">OK MAQUETTE CK V1.2.x LOT 1 · Atlas sections</p>
      <h1>C-<span>Kreyol</span><br/>Planches visuelles par bloc</h1>
      <p class="lead">Ce document accompagne la présentation MOA : chaque section de chaque page Lot 1.1 est isolée en capture, avec son rôle et sa classe d’arbitrage. Il sert à décider ce qui doit être traduit dans Odoo, différé ou ajusté au Lot 2.</p>
      <div class="grid3">
        <div class="card"><strong>Accueil</strong><span>Hero, réassurance, produits, univers, coffret, Pro, éditorial/footer.</span></div>
        <div class="card"><strong>Fiche produit</strong><span>Achat, détails enrichis, recette, signal Pro, cross-sell, footer.</span></div>
        <div class="card"><strong>Professionnels</strong><span>Hero Pro, double cible, process, réassurance, formulaire, note/footer.</span></div>
      </div>
    </div>
    <div class="footer-note">
      Source : maquette HTML Lot 1.1 · Captures desktop 1280 px · Odoo en pause · Généré le 2026-06-13.
    </div>
  </section>

  <section class="sheet">
    <h2>Mode d’emploi MOA</h2>
    <p>Le rapport de décision garde le verdict global. Cet atlas sert au travail en réunion : on regarde chaque bloc, on arbitre son statut, puis on alimente le Lot 2 ou la traduction Odoo.</p>
    <table>
      <thead><tr><th>Page</th><th>Planches</th><th>Intention</th></tr></thead>
      <tbody>${summaryRows}
      </tbody>
    </table>
    <h3>Questions à poser bloc par bloc</h3>
    <ul class="summary-list">
      <li>Ce bloc favorise-t-il réellement la vente avec élégance ?</li>
      <li>Est-il prioritaire pour la V1 Odoo ou peut-il rester en maquette / Lot 2 ?</li>
      <li>La promesse affichée est-elle opérationnellement tenable ?</li>
      <li>La traduction Odoo est-elle native, CMS, ou doit-elle être simplifiée ?</li>
    </ul>
  </section>

${sectionPages}
</body>
</html>`;
}

async function waitForImages(page) {
  await page.evaluate(async () => {
    await Promise.all(Array.from(document.images).map((img) =>
      img.complete && img.naturalWidth > 0
        ? Promise.resolve()
        : new Promise((resolve, reject) => {
            img.onload = () => resolve();
            img.onerror = () => reject(new Error(`Image failed: ${img.src}`));
          })
    ));
  });
}

async function main() {
  await mkdir(CAPTURES_DIR, { recursive: true });
  const browser = await chromium.launch({ headless: true });
  let shots;
  if (SKIP_CAPTURE) {
    console.log('Reprise captures sections existantes…');
    shots = await loadExistingShots();
  } else {
    await ensureMaquetteServer();
    console.log('Capture des sections maquette…');
    shots = await captureSections(browser);
  }

  const html = buildReportHtml(shots);
  const htmlPath = join(RAPPORT_DIR, 'RAPPORT_MOA_MAQUETTE_CK_V1_2_X_LOT1_SECTIONS.html');
  await writeFile(htmlPath, html, 'utf8');
  console.log('HTML atlas sections :', htmlPath);

  await startHttpServer(RAPPORT_DIR, RAPPORT_HTTP_PORT);
  const reportUrl = `http://127.0.0.1:${RAPPORT_HTTP_PORT}/RAPPORT_MOA_MAQUETTE_CK_V1_2_X_LOT1_SECTIONS.html`;
  const pdfPage = await browser.newPage();
  await pdfPage.goto(reportUrl, { waitUntil: 'networkidle', timeout: 120000 });
  await waitForImages(pdfPage);
  await pdfPage.emulateMedia({ media: 'print' });
  const check = await pdfPage.evaluate(() => ({
    textLength: document.body.innerText.length,
    images: document.images.length,
    imagesOk: Array.from(document.images).filter((i) => i.naturalWidth > 0).length,
    sheets: document.querySelectorAll('.sheet').length,
    hasAtlasTitle: document.body.innerText.includes('Planches visuelles par bloc'),
  }));
  console.log('Vérification rendu atlas :', check);
  if (check.images !== check.imagesOk) throw new Error('Certaines captures ne sont pas chargées');
  if (!check.hasAtlasTitle) throw new Error('Titre atlas absent');

  const pdfPath = join(RAPPORT_DIR, 'RAPPORT_MOA_MAQUETTE_CK_V1_2_X_LOT1_SECTIONS.pdf');
  await pdfPage.pdf({
    path: pdfPath,
    format: 'A4',
    landscape: true,
    printBackground: true,
    preferCSSPageSize: true,
    margin: { top: '8mm', bottom: '8mm', left: '8mm', right: '8mm' },
  });
  await browser.close();

  const stat = await readFile(pdfPath).then((b) => b.length);
  console.log('PDF atlas sections :', pdfPath, `(${(stat / 1024 / 1024).toFixed(2)} Mo)`);
}

main().catch((err) => {
  console.error(err);
  process.exit(1);
});
