# Rapport MOA — Maquette CK V1.2.x · Lot 1

| Fichier | Description |
|---------|-------------|
| **[RAPPORT_MOA_MAQUETTE_CK_V1_2_X_LOT1.pdf](./RAPPORT_MOA_MAQUETTE_CK_V1_2_X_LOT1.pdf)** | **Rapport complet MOA** — synthèse · QA · visuels desktop + mobile (images embarquées) |
| **[RAPPORT_MOA_MAQUETTE_CK_V1_2_X_LOT1_SECTIONS.pdf](./RAPPORT_MOA_MAQUETTE_CK_V1_2_X_LOT1_SECTIONS.pdf)** | **Atlas visuel MOA** — une planche par section/bloc de chaque page, pour présentation et arbitrage |
| [RAPPORT_MOA_MAQUETTE_CK_V1_2_X_LOT1.html](./RAPPORT_MOA_MAQUETTE_CK_V1_2_X_LOT1.html) | Version légère — images via dossier `captures/` (ouvrir dans le navigateur, pas dans l’éditeur) |
| [RAPPORT_MOA_MAQUETTE_CK_V1_2_X_LOT1_SECTIONS.html](./RAPPORT_MOA_MAQUETTE_CK_V1_2_X_LOT1_SECTIONS.html) | Version HTML de l’atlas visuel — images via dossier `captures_sections/` |
| [captures/](./captures/) | Captures PNG Playwright (1280 px + 390 px × 3 pages) |
| [captures_sections/](./captures_sections/) | Captures PNG par section de page |

## Contenu du rapport PDF

1. **Page de garde** — verdict OK · périmètre · décision de méthode
2. **Lecture MOA** — ce que le Lot 1 prouve et ce qu’il ne décide pas encore
3. **Arbitrage recommandé** — GO Lot 2 maquette avant reprise Odoo globale
4. **Synthèse par page** — accueil · fiche produit · professionnels
5. **QA et réserves** — preuves Lot 1.1 et réserves non bloquantes
6. **Plan de suite** — décision MOA attendue
7. **Annexes visuelles** — captures desktop + mobile

## Structure du PDF

La version reprise privilégie une lecture de décision MOA : d’abord le sens, les arbitrages et la suite recommandée ; les captures sont conservées en annexes.

Le PDF est généré via serveur HTTP local (texte + images) pour garantir l’affichage complet dans Aperçu.

## Atlas visuel par sections

L’atlas `*_SECTIONS.pdf` est destiné à accompagner une présentation MOA. Il isole chaque bloc de la maquette :

- Accueil : hero, réassurance, produits, univers, coffret, signal Pro, éditorial/footer ;
- Fiche produit : achat, détails enrichis, recette, signal B2B, produits associés, footer ;
- Professionnels : hero, double cible, process, réassurance Pro, formulaire CRM, note/footer.

Chaque planche contient la capture du bloc, son rôle MOA et sa classe d’arbitrage.

## Ouvrir le rapport

- **PDF** : double-clic ou `open rapport/RAPPORT_MOA_MAQUETTE_CK_V1_2_X_LOT1.pdf` — **ne pas ouvrir dans Cursor** (fichier binaire).
- **HTML** : glisser le `.html` dans Chrome/Safari, ou `open -a "Google Chrome" rapport/RAPPORT_MOA_MAQUETTE_CK_V1_2_X_LOT1.html` — les images viennent du dossier `captures/` à côté.

## Régénérer

Prérequis : serveur maquette sur `http://127.0.0.1:8766` (ou auto-démarrage).

```bash
cd docs/design/maquette_01.2/artifact && python3 -m http.server 8766
# autre terminal :
cd docs/design/maquette_01.2/scripts && npm run rapport-lot1
# ou sans recapturer les écrans :
node generate_rapport_lot1_pdf.mjs --skip-capture
# atlas visuel par sections :
node generate_rapport_lot1_sections_pdf.mjs
```

---

*Verdict : OK MAQUETTE CK V1.2.x LOT 1 · 2026-06-13*
