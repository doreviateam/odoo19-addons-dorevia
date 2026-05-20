# TICKET — UX-3 Palier B1 — Fonds colorés créoles premium sur `/shop`

| Champ | Valeur |
|-------|--------|
| **ID** | `TICKET_MARKETONE_UX3_PALIER_B1_CREOLE_BACKGROUNDS` |
| **Type** | **UX / DA** — réchauffement visuel SCSS uniquement |
| **Statut** | **Implémenté** — recette visuelle MOA avant merge (`19.0.15.3.0`) |
| **Jalon de référence** | ADR-031 · UX-3 Palier A « Tenue » mergé (`19.0.15.2.0`, PR #9) |
| **Version cible proposée** | `19.0.15.3.0` |
| **Branche suggérée** | `feat/marketone-ux3-b1-creole-backgrounds` |
| **Base** | `ckr-marketone-01` |
| **URL** | http://localhost:18079/shop |
| **Recette** | `docs/recette/RECETTE_MANUELLE_SHOP_UX3_B1_CREOLE_BACKGROUNDS.md` (à créer post-implémentation) |

---

## Contexte

Après le jalon UX-3 Palier A (variante B « Tenue »), la boutique `/shop` est premium et lisible, mais encore **trop neutre** visuellement.

**Intention MOA B1** (reformulation) :

> Faire vivre la page par des **fonds colorés doux** rouge / jaune / vert / blanc-crème — pas par une théorie « drapeau → rôles UX », pas par des textes ou CTA criards.

La couleur soutient image, texte, prix et achat. Elle ne les concurrence pas.

---

## 1. Ce que je propose de changer (traduction technique)

### Principe d’implémentation

| Choix | Proposition | Pourquoi |
|---|---|---|
| Scope CSS | **100 % sous `.marketone-shop`** (déjà sur `#wrap` via `shop.xml`) | Aucun effet header / footer / checkout / fiche produit |
| Fichiers | **Nouveau partial** `_shop_b1_creole_backgrounds.scss` + **mise à jour alias** `$ck-*` dans `_tokens_colors.scss` | Isole B1 du jalon A ; diff lisible en review |
| Tokens | **Remplacer les valeurs `$ck-bg-*` scope shop** (pas les `$marketone-*` globaux) | Palier A utilisait `#F5EDE0` / `#EDE3D4` / `#F0E8DC` — B1 les fait évoluer vers la palette créole pastel MOA |
| QWeb / JS / contrôleur | **Aucun** | Hors périmètre B1 |
| Prix / hover titre | **Conserver Palier A** (`#C4715A` terracotta cartes) | MOA : couleur surtout en backgrounds |

### Palette — alias proposés (`_tokens_colors.scss`, additif)

```scss
// UX-3 Palier B1 — fonds créoles pastel (scope /shop via $ck-*)
$ck-bg-white:       #FFFDF8;
$ck-bg-cream:       #F7EFE4;   // fond page B1
$ck-bg-red-soft:    #F1CFC4;
$ck-bg-yellow-soft: #F6E4A8;
$ck-bg-green-soft:  #D9E8D2;   // sidebar B1
$ck-bg-green-deep:  #6F9A78;   // usage très limité — voir § questions
$ck-border-soft:    #E2D2C3;

// Remplacements ciblés (rétrocompat alias Palier A)
$ck-bg-page:    $ck-bg-cream;      // était #F5EDE0
$ck-bg-sidebar: $ck-bg-green-soft; // était #EDE3D4
$ck-bg-image:   #FAF4E8;           // crème-jaune très léger (produit)
$ck-text:       #2A1F18;           // inchangé
$ck-border:     $ck-border-soft;   // était #DDD0C2 — proche
```

**Cartes** : `--o-wsale-card-bg: #FFFDF8` · bordure `$ck-border-soft` · ombres chaudes inchangées (Palier A).

---

## 2. Travail par zone — mapping fichier / sélecteur

| Zone MOA | Fichier | Sélecteur (réel) | Proposition |
|---|---|---|---|
| **6.1 Fond page** | `_shop.scss` | `.marketone-shop { background-color }` | `$ck-bg-cream` `#F7EFE4` |
| **6.2 Sidebar** | `_shop_sidebar.scss` | `.marketone-sidebar-rail` | `background: $ck-bg-green-soft` ; accordéons `background: rgba(#FFFDF8, 0.72)` ; texte `$ck-text` |
| **6.3 Chips** | `_shop_filter_state.scss` | `.marketone-filter-chips__chip` | **Voir § alerte** — pas de chips « Tout / Promo / Kits » aujourd’hui |
| **6.4 Cartes** | `_shop_product_cards.scss` | `--o-wsale-card-*` | fond `#FFFDF8` · bordure `$ck-border-soft` |
| **6.5 Zone image** | `_shop_product_cards.scss` | `--o-wsale-card-thumb-background` | `#FAF4E8` (crème chaud léger) |
| **6.6 Zone haute** | `_shop.scss` + `_shop_featured.scss` + `_shop_origin.scss` | `.o_wsale_products_shop_title`, `.marketone-shop-featured-intro`, `.marketone-shop-origin-intro` | fond léger `$ck-bg-green-soft` ou `$ck-bg-yellow-soft` en **padding bandeau** — SCSS only, sans refonte hero |

**Sélecteurs interdits** (conformité MOA §8) : aucun `[class*="…"]` — uniquement classes Marketone / Odoo ciblées sous `.marketone-shop`.

---

## 3. Point d’alerte — chips « Tout / Promotions / Incontournables / Kits »

**Constat code** : sur `/shop` aujourd’hui, les chips visibles sont les **chips UX-1 filtres actifs** (`.marketone-filter-chips__chip`), générées dynamiquement avec des classes :

- `marketone-filter-chips__chip--collection`
- `marketone-filter-chips__chip--category`
- `marketone-filter-chips__chip--origin`
- `marketone-filter-chips__chip--price` (si actif)

Il n’existe **pas** de barre de navigation rapide fixe « Tout · Promotions · Incontournables · Kits/Packs » dans le module Marketone actuel.

**Proposition B1 (sans QWeb)** :

| Option | Description | Recommandation |
|---|---|---|
| **A** | Remplacer la **rotation pastel 5 tons** actuelle par une palette créole (rouge / jaune / vert / crème / blanc) en `nth-child` | Rythme visuel immédiat, sans logique sémantique |
| **B** | Mapper par **type de chip** : `collection` → jaune · `category` → crème · `origin` → vert · `price` → rouge | Plus lisible, reste UX-1 |
| **C** | Reporter chips sémantiques « Tout/Promo/… » au **Palier B2** (QWeb + routes) | Si l’intention MOA exige ces libellés fixes |

**Recommandation Dev** : **Option B** pour B1 (SCSS seul, cohérent avec UX-1).

---

## 4. Ce que je propose de conserver (jalon A + UX-1/2)

- Scope `.marketone-shop` · variables Odoo 19 cartes · `object-fit: contain` · ratio 1:1 · hover -2px / zoom 1.02
- `mix-blend-mode` off · prix terracotta cartes · hover titre terracotta cartes uniquement
- Logique filtres, sidebar sticky, accordéons UX-2, tests `21/21`

---

## 5. Ce que je propose de ne pas faire (B1)

- Header / footer / panier / checkout / fiche produit / home / culture
- Refonte hero complète (→ B2 si besoin)
- Chips navigation « Tout/Promo/… » sans ticket QWeb dédié
- `$ck-bg-green-deep` en grand aplats (risque saturation)
- Sélecteurs génériques `[class*="chip"]` etc.
- Modification JS, contrôleur, comportement filtres

---

## 6. Fichiers impactés (estimation)

| Fichier | Action |
|---|---|
| `static/src/scss/_tokens_colors.scss` | Alias B1 + remap `$ck-bg-page` / `$ck-bg-sidebar` / `$ck-bg-image` |
| `static/src/scss/_shop_b1_creole_backgrounds.scss` | **Nouveau** — overrides B1 centralisés (optionnel si tout dans partials existants) |
| `static/src/scss/_shop.scss` | Fond page |
| `static/src/scss/_shop_sidebar.scss` | Panneau vert pastel + blocs internes crème |
| `static/src/scss/_shop_filter_state.scss` | Tons chips créoles (option B) |
| `static/src/scss/_shop_product_cards.scss` | Fond carte + fond image |
| `static/src/scss/_shop_featured.scss` / `_shop_origin.scss` | Bandeau zone haute léger |
| `__manifest__.py` | Version `19.0.15.3.0` + asset partial |
| `docs/recette/RECETTE_MANUELLE_SHOP_UX3_B1_*.md` | Grille recette + captures |
| `docs/cadrage/DECISIONS.md` | Note courte post-GO (optionnel, pas ADR bloquant) |

**Alternative plus minimaliste** : pas de fichier B1 dédié — uniquement mise à jour des 4 partials shop + tokens. **Recommandation** : partial B1 pour review MOA lisible.

---

## 7. Risques visuels / techniques

| Risque | Mitigation |
|---|---|
| Patchwork rouge/jaune/vert | Dominante crème/blanc · couleurs en **grandes surfaces** limitées (sidebar + chips + bandeau) |
| Sidebar trop verte | `$ck-bg-green-soft` + blocs accordéon blancs — pas `$ck-bg-green-deep` en plein panneau |
| Régression UX-1 chips | Conserver structure HTML · ne toucher qu’aux couleurs SCSS |
| Effet de bord hors `/shop` | Tests : home, `/shop/product`, panier, checkout sans `.marketone-shop` |
| Perte « Tenue » Palier A | Captures avant/après obligatoires en recette |

---

## 8. Recette et captures (post-implémentation)

| Capture | URL / état |
|---|---|
| Avant (main `19.0.15.2.0`) | `/shop` neutre Tenue |
| Après B1 | `/shop` desktop grille |
| Sidebar | `/shop` panneau vert visible |
| Chips | `/shop?marketone_collection=…` (chips actifs) |
| Promo | Si produit/badge promo disponible |
| Filtre actif | Chip + compteur UX-1 |
| Mobile | ≤768px (ou réserve documentée) |
| Hors scope | Home + checkout — smoke visuel |

**Tests auto** : `dorevia_marketone_shop_regression` · `filter_state` · `sidebar_ux2` → **21/21** attendu.

**Verdict** : recette visuelle MOA — **pas de merge automatique** (process ADR-031).

---

## 9. Arbitrages MOA (validés — 2026-05-20)

| # | Sujet | Décision MOA |
|---|---|---|
| 1 | Chips | **Option B** — mapping par type UX-1 |
| 2 | Chips fixes | **Report B2** |
| 3 | `$ck-bg-green-deep` | Pas de grand aplat |
| 4 | Fonds Palier A | Remplacés sur `/shop` |
| 5 | Zone haute | Bandeau SCSS léger |
| 6 | Prix terracotta | Inchangé |

---

## 10. Implémentation (`19.0.15.3.0`)

Fichiers : `_tokens_colors.scss` · `_shop.scss` · `_shop_sidebar.scss` · `_shop_filter_state.scss` · `_shop_product_cards.scss` · `_shop_featured.scss` · `_shop_origin.scss`.

Recette : `docs/recette/RECETTE_MANUELLE_SHOP_UX3_B1_CREOLE_BACKGROUNDS.md`

---

## 11. Synthèse

**B1 livré** — fonds créoles sur `/shop`. Merge après GO visuel MOA uniquement.
