# Prompt pret a l'emploi — M-05 Premium Odoo (Open Design)

Copier tout le bloc ci-dessous dans Open Design (projet `44de8203-38b0-4405-af76-2f09c97c5f02`).

---

```text
Context: C-Kreyol Marketone — iterate existing index.html prototype.
Doctrine: "Le produit d'abord. Le recit ensuite. Le savoir en prolongement."

CRITICAL — align with LIVE Odoo premium (MOA validated):
- Line: Artisanal Terroir, premium fine grocery, warm and restrained — NOT generic marketplace, NOT tropical clichés, NOT luxury catalog ostentation.
- Colors (flat fills only, no decorative gradients):
  - body #FFFFFF
  - cards/surfaces #FFFDF8, sidebar #F3EDE5
  - product tile image zone #FDFCFA
  - text #2A1F18
  - terracotta #C4715A (price, primary commerce emphasis, hover titles)
  - sage #5A8A6E (subtle accents, card hover border)
  - borders #E2D4BC
  - reserve warm accent #F2E3D2 for chips only, NOT full-page background
- REMOVE green-forward OKLCH accent from early piste 1.
- Typography: EB Garamond (Google Fonts) for h1-h3; Hanken Grotesk for UI and body.
- Keep existing layout/sections/JS behavior; change CSS tokens and fonts only unless a small fix is needed for contrast.
- Shadows: warm rgba(42,31,24,0.07–0.09), subtle card hover translateY(-2px).
- Card radius: 12–14px on product cards (premium tenue), 8px on small controls.
- Shop tiles: full-bleed image area, conversion-first footer (price + quick add), wishlist top-right on image.

Iteration ID: M-05
Deliverable: updated index.html in project folder.
After completion: user will export to piste_1bis_artisanal_terroir/ in git.

Acceptance:
- Side-by-side with Odoo /shop screenshot would feel like same brand family
- Culture strip stays light, commerce dominates boutique grid
- Responsive unchanged or improved
- critique-panel should still score >= 4 on restraint and philosophy
```

---

Apres le run : copier vers `04_exports_open_design/piste_1bis_artisanal_terroir/` (creer le dossier) et marquer M-05 `fait` dans le backlog.
