# Recette manuelle — UX-3 Palier A — Grille produit `/shop`

| Champ | Valeur |
|-------|--------|
| **Ticket** | `TICKET_MARKETONE_UX3_PRODUCT_CARDS_PALIER_A` (à créer post-recette) |
| **Version cible** | **`19.0.15.0.0`** |
| **Branche** | `feat/marketone-ux3-product-cards-palier-a` |
| **URL** | http://localhost:18079/shop |
| **Base** | `ckr-marketone-01` |
| **Statut** | **Recette visuelle en cours** — avant décision PR |
| **Kit source** | `docs/Carole/ux3_palier_a.scss` → traduit en tokens Marketone |

---

## Prérequis

- Module `19.0.15.0.0` (upgrade + **restart conteneur** — bundle assets recompilé).
- Hard refresh navigateur (Ctrl+Shift+R / Cmd+Shift+R).
- Assets confirmés en bundle : `_shop_product_cards.scss` présent ✓

```bash
docker restart sandbox-odoo19-odoo-1
```

---

## V1 — Grille desktop complète

| Étape | Vérification | Attendu | ☐ |
|-------|--------------|---------|---|
| 1 | Ouvrir `/shop` desktop ≥ 992px | Cartes avec **bordure arrondie** (0.875rem) · ombre légère | |
| 2 | Images produits | Fond `#f5ece7` (beige doux) · image centrée · `object-fit: contain` | |
| 3 | Ratio image | **4/5** (légèrement portrait) · pas de rognage produit | |
| 4 | Titre carte | Hanken Grotesk semibold · taille 1rem · couleur texte token | |
| 5 | Description | 2 lignes max · tronquée proprement | |
| 6 | Prix | 1.125rem semibold · prix barré muted si promo | |
| 7 | Gap grille | Respiration **1.75rem** entre cartes | |

**Capture attendue** : `/private/tmp/marketone_ux3_desktop_before.png` (avant) · `/private/tmp/marketone_ux3_desktop_after.png` (après)

---

## V2 — Hover carte

| Étape | Vérification | Attendu | ☐ |
|-------|--------------|---------|---|
| 1 | Survoler une carte | **Lift** `-6px` · ombre plus marquée | |
| 2 | Image au hover | Zoom `scale(1.06)` · transition fluide ease-spring | |
| 3 | Layout | **Pas de saut** de grille au hover | |
| 4 | Lien titre au hover | Couleur `$marketone-primary-container` (#a65d39) | |

---

## V3 — `mix-blend-mode: multiply` — Point critique

| Étape | Vérification | Attendu | ☐ |
|-------|--------------|---------|---|
| 1 | Photo produit sur fond blanc (ex. bocal, bouteille) | Halo blanc **absent** — intégration naturelle sur fond beige | |
| 2 | Photo lifestyle / fond coloré (ex. épices, fruits) | Image **lisible** · pas ternie ni « sale » · contraste suffisant | |
| 3 | Photo produit brut sombre (ex. café, cacao) | Teinte non déformée | |
| 4 | Si effet indésirable sur ≥ 1 type d'image | → **Retirer `mix-blend-mode`** ou limiter à `.bg-white` | |

---

## V4 — Mobile 768px

| Étape | Vérification | Attendu | ☐ |
|-------|--------------|---------|---|
| 1 | Viewport 768px | Ratio image **1/1** (carré) · padding 0.75rem | |
| 2 | Grille | Gap **1rem** · 2 colonnes ou 1 selon breakpoint Odoo | |
| 3 | Titre | 0.875rem · lisible · pas de troncature trop agressive | |
| 4 | Prix | 1rem · bien visible | |

**Capture attendue** : `/private/tmp/marketone_ux3_mobile_768.png`

---

## V5 — Filtre actif (peu de produits)

| Étape | Vérification | Attendu | ☐ |
|-------|--------------|---------|---|
| 1 | Cocher 1 collection (ex. **Apéritif créole**) | Grille réduite · cartes UX-3 inchangées | |
| 2 | Chips UX-1 visibles | Barre chips au-dessus toolbar · reset visible | |
| 3 | 1 seul produit affiché | Carte isolée — pas de mise en page cassée | |

**Capture attendue** : `/private/tmp/marketone_ux3_filtre_actif.png`

---

## V6 — Produit promo (si disponible)

| Étape | Vérification | Attendu | ☐ |
|-------|--------------|---------|---|
| 1 | Produit avec prix barré | `oe_strikethrough` / `oe_default_price` en muted · taille 0.875rem | |
| 2 | Badge (si présent) | Pill terracotta (`$marketone-primary-container`) · position top-left | |

---

## V7 — Non-régression UX-2 sidebar

| Étape | Vérification | Attendu | ☐ |
|-------|--------------|---------|---|
| 1 | Sidebar desktop | Rail sticky · accordéons ouverts · rubriques intactes | |
| 2 | Offcanvas mobile | Même grammaire · pas de reset sidebar | |
| 3 | Classes UX-2 | `marketone-sidebar-rail` présent en HTML | |

---

## V8 — Non-régression chips/reset UX-1

| Étape | Vérification | Attendu | ☐ |
|-------|--------------|---------|---|
| 1 | Filtres actifs | Barre chips à gauche au-dessus toolbar | |
| 2 | Reset | Un seul « Effacer les filtres » | |
| 3 | Compteur | « N produit(s) trouvé(s) » correct | |

---

## Points de vigilance signalés (implémentation)

| Point | Détail | Décision si problème |
|-------|--------|----------------------|
| **`mix-blend-mode: multiply`** | Peut terniir images lifestyle à fond coloré | Retirer ou limiter à `.bg-white` uniquement |
| **Ratio 4/5 desktop** | Cartes plus hautes qu'attendu sur catalogue dense | Passer à `1/1` ou `4/3` si trop vertical |
| **Hover lift -6px** | Saut de layout possible dans grille tight | Réduire à `-3px` si décrochage visible |
| **Titre en corps** | `$marketone-font-body` à la place de `$marketone-font-heading` | Revenir à heading si MOA préfère le Garamond |

---

## Fiche de résultat

| Champ | Valeur |
|-------|--------|
| **Date** | |
| **Navigateur** | |
| **Module** | `19.0.15.0.0` |

| Scénario | Verdict | Note |
|----------|---------|------|
| V1 — Desktop grille | ☐ OK · ☐ réserve · ☐ KO | |
| V2 — Hover | ☐ OK · ☐ réserve · ☐ KO | |
| V3 — mix-blend-mode | ☐ OK · ☐ à retirer · ☐ KO | |
| V4 — Mobile 768px | ☐ OK · ☐ réserve · ☐ KO | |
| V5 — Filtre actif | ☐ OK · ☐ réserve · ☐ KO | |
| V6 — Promo | ☐ OK · ☐ N/A | |
| V7 — UX-2 non-régression | ☐ OK · ☐ KO | |
| V8 — UX-1 non-régression | ☐ OK · ☐ KO | |

---

---

## Corrections post-recette NO GO (commit `ff865ed`)

**Diagnostic** : la recette du cycle 1 (NO GO visuel) a révélé trois causes racines.

| Point KO | Cause racine | Correction appliquée |
|---|---|---|
| `object-fit: cover` | `o_wsale_products_opt_thumb_cover` activé sur `#o_wsale_products_grid` injectait `--o-wsale-card-thumb-fill-mode: cover` | Surcharge de la variable sur `.oe_product_cart` (DOM plus proche → héritée en priorité) |
| `transform: none` au hover | `--o-wsale-card-transform-hover` sans fallback Odoo = `none` par défaut | Définir `--o-wsale-card-transform-hover: translateY(-6px)` |
| Zoom image absent | `--o-wsale-card-img-transform-hover` indéfini | Définir `--o-wsale-card-img-transform-hover: scale(1.06)` |
| Double lift potentiel | `_shop.scss` portait `translateY(-2px)` sur `.oe_product` (parent div) | Neutraliser `transform + box-shadow` sur `.oe_product:hover` dans le scope `.marketone-shop` |
| `.oe_product_info` | Classe inexistante dans le HTML Odoo 19 | Remplacé par `.o_wsale_product_information` (classe réelle) |

**Approche finale** : toutes les surcharges visuelles passent par les CSS custom properties natives Odoo 19 (`--o-wsale-card-*`). Seul `mix-blend-mode` reste en règle directe (pas de variable Odoo).

**Bundle vérifié** (commit `ff865ed`, `ckr-marketone-01`) :
- `[OK]` `--o-wsale-card-transform-hover: translateY(-6px)` x1
- `[OK]` `--o-wsale-card-thumb-fill-mode: contain` x1
- `[OK]` `--o-wsale-card-thumb-aspect-ratio: 0.8` x2
- `[OK]` `mix-blend-mode: multiply` x1
- `[OK]` `scale(1.06)` x2
- `[OK]` easing spring x3
- `[OK]` `marketone-sidebar-rail` x2 (UX-2 non-régressé)

---

## Recette cycle 2 — grille validation

| Scénario | Verdict | Notes |
|---|---|---|
| V1 — Desktop grille | ☐ OK · ☐ réserve · ☐ KO | |
| V2 — Hover | ☐ OK · ☐ réserve · ☐ KO | |
| V3 — mix-blend-mode | ☐ OK · ☐ à retirer · ☐ KO | |
| V4 — Mobile 768px | ☐ OK · ☐ réserve · ☐ KO | |
| V5 — Filtre actif | ☐ OK · ☐ réserve · ☐ KO | |
| V6 — Promo | ☐ OK · ☐ N/A | |
| V7 — UX-2 non-régression | ☐ OK · ☐ KO | |
| V8 — UX-1 non-régression | ☐ OK · ☐ KO | |

---

## Verdict MOA UX-3 Palier A

| Verdict | ☐ |
|---------|---|
| **GO — PR UX-3 proposable** | |
| **GO avec ajustements SCSS mineurs avant PR** | |
| **Rollback partiel** (image / card) | |
| **NO GO** | |

**Ajustements identifiés (si GO avec réserves)** :
