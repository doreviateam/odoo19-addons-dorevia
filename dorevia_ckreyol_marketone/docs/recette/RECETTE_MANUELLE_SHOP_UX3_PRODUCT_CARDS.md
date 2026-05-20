# Recette manuelle — UX-3 Palier A — Grille produit `/shop`

| Champ | Valeur |
|-------|--------|
| **Ticket** | `TICKET_MARKETONE_UX3_PRODUCT_CARDS_PALIER_A` (à créer post-recette) |
| **Version cible** | **`19.0.15.2.0`** (variante B « Tenue » — doctrine CK) |
| **Branche** | `feat/marketone-ux3-product-cards-palier-a` |
| **URL** | http://localhost:18079/shop |
| **Base** | `ckr-marketone-01` |
| **Statut** | **GO visuel proposable** — recette cycle 4 exécutée ; merge PR #9 après validation humaine MOA finale |
| **Proposition DA** | `docs/tickets/TICKET_MARKETONE_UX3_PALIER_A_PROPOSITION_DA.md` |

---

## Prérequis

- Module **`19.0.15.2.0`** (upgrade + **restart conteneur** — bundle assets recompilé).
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

**Exécution** : `ckr-marketone-01`, branche `feat/marketone-ux3-product-cards-palier-a`, module `19.0.15.0.0`, post-correction `ff865ed`.

| Scénario | Verdict | Notes |
|---|---|---|
| V1 — Desktop grille | ☑ OK | `object-fit: contain`, ratio `0.8`, fond `rgb(245,236,231)`, radius `14px`, ombre légère |
| V2 — Hover | ☑ OK | `--o-wsale-card-transform-hover: translateY(-6px)`, image `scale(1.06)` |
| V3 — mix-blend-mode | ☑ OK (réserve humaine) | `multiply` actif — valider à l'œil sur images lifestyle/colorées |
| V4 — Mobile 768px | ☐ non exécuté | CSS source présent (ratio 1/1, hover désactivé) ; capture 768 non produite |
| V5 — Filtre actif | ☑ OK | 8 produits, chip `Apéritif créole`, reset `/shop`, compteur OK |
| V6 — Promo | ☑ N/A | Pas de prix barré/badge produit détecté |
| V7 — UX-2 non-régression | ☑ OK | `marketone-sidebar-rail` présent |
| V8 — UX-1 non-régression | ☑ OK | Chips + reset confirmés via filtre actif |

**Tests auto** : `dorevia_marketone_shop_regression` · `dorevia_marketone_shop_filter_state` · `dorevia_marketone_shop_sidebar_ux2` → **21/21 OK**.

**Smokes HTTP** : `/shop` 200 · `/shop?marketone_collection=aperitif-creole` 200.

**Captures** :
- `/private/tmp/marketone_ux3_desktop_after_retest.png`
- `/private/tmp/marketone_ux3_filtre_actif_retest.png`

---

---

## Variante douce MOA (19.0.15.1.0)

**Contexte** : GO technique cycle 2 maintenu, réserve visuelle — rendu trop « card e-commerce », grille verticale, coupure image/texte forte, perte de chaleur.

**Ajustements appliqués** (`_shop_product_cards.scss`, réglages en tête de fichier) :

| Paramètre | Avant (cycle 2) | Variante douce |
|---|---|---|
| Ombre repos | `0 2px 12px` @ 4% | `0 1px 6px` @ 2.5% |
| Ombre hover | `0 16px 40px` @ 10% | `0 8px 24px` @ 6% |
| Lift hover | `-6px` | **`-4px`** |
| Zoom image hover | `1.06` | **`1.03`** |
| Ratio desktop | `0.8` (4/5) | **`1.333` (4/3)** |
| Bordure carte | `$marketone-border` plein | **`rgba(border, 0.45)`** |
| Fond image | `$marketone-surface-container` | **`$marketone-bg-soft`** (coupure adoucie) |
| `mix-blend-mode` | `multiply` | **`normal`** (désactivé) |
| Transition hover | spring | **ease-out** |

**Recette A/B ratio** — modifier `$_ux3-thumb-aspect-desktop` puis upgrade + restart :

| Valeur | Ratio | Usage |
|---|---|---|
| `0.8` | 4/5 | Palier A initial (portrait) |
| `1` | 1/1 | Carré, grille plus compacte |
| `1.333` | 4/3 | **Défaut variante douce** |

**Recette blend** — modifier `$_ux3-img-blend-mode` : `normal` (défaut) · `soft-light` · `multiply`.

### Recette cycle 3 — grille validation

| Scénario | Verdict | Notes |
|---|---|---|
| V1 — Desktop grille | ☐ OK · ☐ réserve · ☐ KO | Ratio 4/3, ombre légère, bordure discrète |
| V2 — Hover | ☐ OK · ☐ réserve · ☐ KO | Lift -4px, zoom 1.03 |
| V3 — Chaleur images | ☐ OK · ☐ réserve · ☐ KO | Sans multiply ; packshots blancs acceptables ? |
| V4 — Mobile 768px | ☐ OK · ☐ réserve · ☐ KO | |
| V5–V8 | ☐ OK | Non-régression filtres / UX-1 / UX-2 |

---

## Verdict MOA UX-3 Palier A

| Verdict | Cycle 2 | Cycle 3 |
|---------|---------|---------|
| **GO technique** | ☑ | ☐ |
| **GO visuel — PR finale** | réserve | ☐ |
| **GO avec ajustements SCSS** | | en cours |
| **NO GO** | | |

**Cycle 1** : NO GO strict visuel (`object-fit: cover`, hover absent) — corrigé via CSS custom properties Odoo 19 (`ff865ed`).

**Cycle 2** : GO technique, réserve visuelle e-commerce trop rigide.

---

## Variante B « Tenue » — doctrine CK (19.0.15.2.0)

**Arbitrage MOA** : variante B retenue · palette scope `/shop` · alias `$ck-*` locaux.

| Paramètre | Valeur cible |
|---|---|
| Fond page `/shop` | `#F5EDE0` (`$ck-bg-page`) |
| Sidebar panneau | `#EDE3D4` (`$ck-bg-sidebar`) |
| Fond image carte | `#F0E8DC` (`$ck-bg-image`) |
| Fond carte | `#ffffff` (îlot lumineux) |
| Ratio desktop | `1:1` |
| Bordure carte | `#DDD0C2` |
| Ombre repos | `0 1px 4px rgba(42,31,24,0.06)` |
| Ombre hover | `0 4px 16px rgba(42,31,24,0.08)` |
| Lift hover | `-2px` |
| Zoom image | `1.02` |
| Prix | `#C4715A` terracotta |
| Hover titre | terracotta **cartes uniquement** |
| `mix-blend-mode` | off |

### Recette cycle 4 — exécution (`ckr-marketone-01`, `19.0.15.2.0`)

**Date** : 2026-05-20 · Branche `feat/marketone-ux3-product-cards-palier-a`.

**Technique**

| Contrôle | Résultat |
|---|---|
| Upgrade module + restart | OK |
| Smoke `/shop` | `200` — 24 cartes |
| Smoke `?marketone_collection=aperitif-creole` | `200` — 8 cartes |
| Tests `dorevia_marketone_shop_regression` · `filter_state` · `sidebar_ux2` | **21/21 OK** |
| Logs (ERROR / Traceback / Undefined) | Aucun relevé |

**Validation visuelle / mesures**

| Point | Résultat |
|---|---|
| Fond `/shop` `#F5EDE0` | OK |
| Sidebar `#EDE3D4` | OK |
| Carte blanche, bordure `#DDD0C2`, radius `14px` | OK |
| Image ratio carré, `object-fit: contain`, `mix-blend-mode: normal` | OK |
| Prix terracotta `#C4715A` | OK |
| Hover variables CSS `translateY(-2px)` + `scale(1.02)` | OK |
| UX-1 chips / reset | OK |
| UX-2 `marketone-sidebar-rail` | OK |
| Scroll horizontal | Non détecté |

**Captures produites**

| Capture | Fichier | ☐ |
|---|---|---|
| Grille desktop | `/private/tmp/marketone_ux3_b_desktop.png` | ☑ |
| Filtre actif | `/private/tmp/marketone_ux3_b_filtre_actif.png` | ☑ |
| Sidebar | `/private/tmp/marketone_ux3_b_sidebar.png` | ☑ |
| Packshots fond clair | `/private/tmp/marketone_ux3_b_packshot_1.png` … `packshot_4.png` | ☑ |
| Images lifestyle / colorées | Non capturées séparément (packshots couvrent fond clair) | — |
| Mobile 768px | Non produite (viewport non contrôlable dans ce runtime) | ☐ réserve |

### Grille validation cycle 4

| Scénario | Verdict | Notes |
|---|---|---|
| V1 — Grille premium vivante | ☑ OK | Pas froide, pas SaaS |
| V2 — Îlot blanc sur fond lin | ☑ OK | Contraste doux |
| V3 — Sidebar `#EDE3D4` | ☑ OK | Distincte, pas lourde |
| V4 — Prix terracotta | ☑ OK | Guide achat sans agresser |
| V5 — Hover discret | ☑ OK | -2px / zoom 1.02 (variables CSS) |
| V6 — Images (sans multiply) | ☑ OK | Packshots fond clair OK |
| V7 — UX-2 non-régression | ☑ OK | `marketone-sidebar-rail` |
| V8 — UX-1 non-régression | ☑ OK | Chips + reset |

### Verdict recette cycle 4

| Verdict | ☑ |
|---|---|
| **GO technique** | ☑ |
| **GO visuel proposable** | ☑ |
| **GO merge PR #9** | ☐ — validation humaine MOA finale sur captures avant merge |
| **Réserve** | Capture mobile 768px non produite |

**Process** : merge PR #9 uniquement après **GO explicite MOA** post-revue des captures.
