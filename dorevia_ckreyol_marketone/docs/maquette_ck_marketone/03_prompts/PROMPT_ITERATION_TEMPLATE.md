# Prompt iteration Open Design — CK Marketone

Copier-coller dans Open Design (projet existant `44de8203-38b0-4405-af76-2f09c97c5f02`, skill **prototype**).

Remplacer les blocs `{{...}}`.

---

## En-tete (toujours inclure)

```text
Context: C-Kreyol Marketone — marketplace produits territoires creolophones.
Doctrine: "Le produit d'abord. Le recit ensuite. Le savoir en prolongement."
Mondes: Boutique (achat), Culture (origines), Savoirs (transmission).
Direction active: Artisanal Terroir PREMIUM (aligned with live Odoo MOA) — warm, restrained, fine grocery, product-first.
Colors (flat only): body #FFFFFF, cards #FFFDF8, tile image zone #FDFCFA, text #2A1F18, terracotta #C4715A, sage #5A8A6E, borders #E2D4BC. NO green-forward marketplace accent. NO decorative gradients/blobs.
Typography: EB Garamond headings, Hanken Grotesk body (Google Fonts link OK).
Constraints: no generic tropical/exotic shop; card radius 8–14px; culture never dominates shop grid; match Odoo shop tile behavior (full-bleed photo, warm shadow, conversion-first).
Audience: acheteurs, MOA C-Kreyol, equipe Dorevia, integrateurs Odoo Website Sale.
Reference: docs/maquette_ck_marketone/00_brief/CADRAGE_PREMIUM_MAQUETTE_ODOO.md

Task: ITERATION on the existing index.html prototype — do not restart from blank unless asked.
Iteration ID: {{M-01}}
Focus scope: {{ex. mobile navigation drawer for Boutique / Culture / Savoirs}}
```

## Corps iteration

```text
Keep unchanged unless required for consistency:
- Overall visual direction and OKLCH palette structure
- Sections already validated: {{ex. hero, shop grid, product detail, culture strip, checkout}}
- French UI copy tone

Implement in this iteration:
{{description detaillee — 3 à 8 bullet points max}}

Acceptance criteria:
- {{critere 1}}
- {{critere 2}}
- Responsive: desktop + <= 1020px + <= 680px
- Accessible: aria-labels on icon buttons, focus visible
- Stable product card dimensions, no overlapping text

Deliverable: update the single self-contained index.html in the project folder.
```

## Exemple rempli — M-01 drawer mobile

```text
Iteration ID: M-01
Focus scope: mobile navigation

Implement:
- Wire the existing mobile-menu button to open a drawer or full-screen panel
- Links: Boutique (#boutique), Culture (#culture), Savoirs (placeholder #savoirs)
- Close on link click and overlay click
- Keep search visible on mobile below brand row
- Do not remove desktop nav

Acceptance criteria:
- Drawer works at <= 1020px where navlinks are hidden
- No scroll lock bugs
- Keyboard Esc closes drawer
```

## Exemple rempli — M-05 piste 1 bis tokens MOA

```text
Iteration ID: M-05
Focus scope: global tokens only

Implement:
- Replace green-forward accent with MOA terracotta/sauge/cream chain:
  - text #2A1F18, terracotta CTA #C4715A, sauge #5A8A6E, borders #E2D4BC
  - body/surfaces: #FFFFFF, cards #FFFDF8, tile image zone #FDFCFA
- Headings: EB Garamond; body: Hanken Grotesk (Google fonts link if needed)
- Keep layout and components identical to current prototype

Acceptance criteria:
- Same HTML structure, only CSS/token changes
- Still product-first hierarchy
- No saturated full-page green background
```

---

Apres le run : sync export (voir `01_workflow/WORKFLOW_MAQUETTE_ITERATIVE.md`) et mettre a jour `02_backlog/BACKLOG_MAQUETTE.md`.
