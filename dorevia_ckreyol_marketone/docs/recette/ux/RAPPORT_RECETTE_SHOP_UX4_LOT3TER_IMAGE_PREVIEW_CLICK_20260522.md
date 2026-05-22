# Rapport recette — UX-4 Lot 3ter — clic image tuile → preview

| Champ | Valeur |
|-------|--------|
| **Date** | 2026-05-22 |
| **Module** | `dorevia_ckreyol_marketone` |
| **Version** | `19.0.15.13.5` |
| **Branche** | `feat/marketone-ux4-lot3ter-image-preview-click` |
| **Base** | `ckr-marketone-01` |
| **URL** | `http://localhost:18079/shop` |
| **Document recette** | [`RECETTE_MANUELLE_SHOP_UX4_IN_PLACE.md`](RECETTE_MANUELLE_SHOP_UX4_IN_PLACE.md) |

## Préparation

| Contrôle | Résultat |
|----------|----------|
| `git pull origin feat/marketone-ux4-lot3ter-image-preview-click` | Déjà à jour |
| Upgrade module `-u dorevia_ckreyol_marketone` | OK |
| Redémarrage Odoo long-running | OK |
| Tests automatisés élargis | **88/88 OK · 0 failed · 0 error(s)** |

## Résultat desktop

| # | Scénario | Observé | Verdict |
|---|----------|---------|---------|
| V3ter.1 | Clic centre image produit simple | URL `/shop` conservée, mais aucune preview offcanvas ouverte | **KO bloquant** |
| V3ter.2 | Clic panier overlay photo | Panier incrémenté, aucune preview ouverte | OK |
| V3ter.3 | Clic wishlist overlay photo | Wishlist togglée, aucune preview ouverte | OK |
| V3ter.4 | Clic titre produit | Navigation fiche produit complète | OK |
| V3ter.5a | Re-clic image même produit | Non validable : image n'ouvre pas la preview | **KO** |
| V3ter.5b | Image produit A → image produit B | Non validable : image A n'ouvre pas la preview | **KO** |
| V3ter.6 | Preview ouverte | Non atteint ; URL `/shop` reste conservée | Réserve liée V3ter.1 |
| V3ter.7 | Smoke fermeture V3bis.12 | Pas de régression observée sur états de retrait ; preview image non ouverte | OK hors V3ter.1 |
| V3ter.8 | Console DevTools | Aucune erreur JS bloquante observée | OK |

## Résultat mobile 390 px

| # | Scénario | Observé | Verdict |
|---|----------|---------|---------|
| V3ter.1 | Tap image | URL `/shop` conservée, aucune preview inline ouverte | **KO bloquant** |
| V3ter.2–3 | Tap panier / wishlist | Non-régression couverte par desktop + tests ; pas de preview parasite observée | OK |
| V3ter.4 | Tap titre | Comportement fiche attendu, non bloquant | OK |
| V3ter.5 | Re-tap image / bascule produit | Non validable : image n'ouvre pas la preview | **KO** |
| V3ter.6–8 | URL · fermeture · console · scroll horizontal | URL `/shop`, pas de débordement horizontal, pas d'erreur console bloquante | OK hors V3ter.1 |

## Smoke non-régression

| Critère | Référence | Résultat |
|---------|-----------|----------|
| Panier depuis preview / overlay | G3.6 · Lot 2 | OK pour overlay panier ; preview image non atteinte |
| Wishlist depuis preview / overlay | G3.7 · Lot 1 | OK pour overlay wishlist ; preview image non atteinte |
| Fermeture explicite | G3.9 | Non régressée hors scénario image |
| Mobile débordement | G3.3 | OK, `scrollWidth <= 390` |

## Captures et preuves

| ID | Fichier |
|----|---------|
| C-L3ter-D1 | [`capture_ux4_l3ter_13_5_desktop_image_preview_open_20260522.png`](capture_ux4_l3ter_13_5_desktop_image_preview_open_20260522.png) |
| C-L3ter-D2 | [`capture_ux4_l3ter_13_5_desktop_cart_no_preview_20260522.png`](capture_ux4_l3ter_13_5_desktop_cart_no_preview_20260522.png) |

JSON : [`recette_ux4_l3ter_13_5_image_click_result.json`](recette_ux4_l3ter_13_5_image_click_result.json)

## Diagnostic MOA

Le comportement demandé par l'arbitrage Lot 3ter n'est pas atteint : le clic image ne déclenche pas la preview, sur desktop comme sur mobile.

Constat technique utile pour le Dev :

- le lien image rendu est `a.oe_product_image_link` ;
- le formulaire carte porte bien `data-product-template-id` et `data-marketone-preview-allowed="True"` ;
- le clic image reste sur `/shop`, sans navigation fiche et sans preview ;
- les overlays panier / wishlist ne déclenchent pas de preview, ce qui respecte les garde-fous ;
- aucune erreur JS bloquante n'apparaît dans la console navigateur pendant la passe.

## Verdict Lot 3ter

| Verdict | Statut |
|---------|--------|
| GO MOA Lot 3ter | ☐ |
| **NO GO** | ☑ |

**Verdict : NO GO Lot 3ter.**

Blocage : **V3ter.1** échoue sur desktop et mobile. Merge PR #17 non recommandé tant que le clic image n'ouvre pas la preview comme le CTA `Voir`.

## Reprise après corrections

| Champ | Valeur |
|-------|--------|
| **Date / heure** | 2026-05-22 |
| **Commit contrôlé** | `ef99bbe` |
| **Upgrade module** | OK |
| **Restart Odoo** | OK |
| **Tests auto élargis** | **88/88 OK · 0 failed · 0 error(s)** |

### Contrôle navigateur complémentaire

| Scénario | Observé | Verdict |
|----------|---------|---------|
| Tap image produit simple, viewport mobile 390 px | URL `/shop` conservée, aucune preview inline ouverte | **KO bloquant maintenu** |
| CTA `Voir`, viewport mobile 390 px | URL `/shop` conservée, aucune preview inline ouverte | **KO complémentaire** |
| Panier overlay | Panier incrémenté, aucune preview parasite | OK |
| Wishlist overlay | Wishlist incrémentée, aucune preview parasite | OK |
| Titre produit | Navigation fiche produit complète | OK |
| Console | Aucune erreur JS bloquante observée | OK |
| Débordement mobile | `scrollWidth <= 390` | OK |

Capture reprise : [`capture_ux4_l3ter_13_5_reprise_mobile_image_click_no_preview_20260522.png`](capture_ux4_l3ter_13_5_reprise_mobile_image_click_no_preview_20260522.png)

**Verdict reprise : NO GO maintenu.**

Le correctif ne valide pas encore l'arbitrage Lot 3ter : l'ouverture de preview depuis l'image reste absente, et la passe mobile montre aussi que le CTA `Voir` ne déclenche pas la preview. Les garde-fous panier / wishlist / titre restent corrects.

## Reprise 13.6 après corrections

| Champ | Valeur |
|-------|--------|
| **Date / heure** | 2026-05-22 |
| **Version contrôlée** | `19.0.15.13.6` |
| **Commit contrôlé** | `aab2ab1` |
| **Upgrade module** | OK |
| **Restart Odoo** | OK |
| **Tests auto élargis** | **88/88 OK · 0 failed · 0 error(s)** |

### Contrôle navigateur 13.6

| Scénario | Observé | Verdict |
|----------|---------|---------|
| Tap image produit simple, viewport mobile 390 px | URL `/shop` conservée, aucune preview inline ouverte | **KO bloquant maintenu** |
| Re-tap image / image A puis B | Non validable : l'image n'ouvre pas la preview | **KO** |
| CTA `Voir`, viewport mobile 390 px | URL `/shop` conservée, aucune preview inline ouverte | **KO complémentaire maintenu** |
| Panier overlay | Action panier sans preview parasite | OK |
| Wishlist overlay | Action wishlist sans preview parasite | OK |
| Titre produit | Navigation fiche produit complète | OK |
| Console | Aucune erreur JS bloquante observée | OK |
| Débordement mobile | `scrollWidth <= 390` | OK |

Captures reprise 13.6 :

- [`capture_ux4_l3ter_13_6_image_click_preview_20260522.png`](capture_ux4_l3ter_13_6_image_click_preview_20260522.png)
- [`capture_ux4_l3ter_13_6_voir_preview_20260522.png`](capture_ux4_l3ter_13_6_voir_preview_20260522.png)
- [`capture_ux4_l3ter_13_6_cart_no_preview_20260522.png`](capture_ux4_l3ter_13_6_cart_no_preview_20260522.png)

JSON reprise 13.6 : [`recette_ux4_l3ter_13_6_image_click_result.json`](recette_ux4_l3ter_13_6_image_click_result.json)

**Verdict reprise 13.6 : NO GO maintenu.**

Le correctif `19.0.15.13.6` ne valide toujours pas l'objectif Lot 3ter : l'ouverture de preview depuis l'image ne se produit pas, et le CTA `Voir` reste également sans effet preview dans cette passe mobile. Les non-régressions panier / wishlist / titre restent favorables.

## Re-recette MOA 13.7 — V3ter.1–8

| Champ | Valeur |
|-------|--------|
| **Date / heure** | 2026-05-22 |
| **Version contrôlée** | `19.0.15.13.7` |
| **Commit contrôlé** | `132995f` |
| **Upgrade module** | OK |
| **Restart Odoo** | OK |
| **Tests auto élargis** | **88/88 OK · 0 failed · 0 error(s)** |

### Grille V3ter.1–8

| # | Scénario | Observé | Verdict |
|---|----------|---------|---------|
| V3ter.1 | Tap image produit simple | URL `/shop` conservée, aucune preview inline ouverte | **KO bloquant maintenu** |
| V3ter.2 | Tap panier overlay | Panier incrémenté, aucune preview parasite | OK |
| V3ter.3 | Tap wishlist overlay | Wishlist incrémentée, aucune preview parasite | OK |
| V3ter.4 | Tap titre produit | Navigation fiche produit complète | OK |
| V3ter.5a | Re-tap image même produit | Non validable : image n'ouvre pas la preview | **KO** |
| V3ter.5b | Image produit A → image produit B | Non validable : image A n'ouvre pas la preview | **KO** |
| V3ter.6 | URL pendant preview attendue | URL `/shop` conservée, mais preview non ouverte | Réserve liée V3ter.1 |
| V3ter.7 | ESC / clic grille / retrait naturel | Pas de modal, pas de backdrop, état fermé propre | OK hors V3ter.1 |
| V3ter.8 | Console DevTools | Aucune erreur JS bloquante observée | OK |

Contrôle complémentaire : le CTA `Voir`, qui sert de comportement de référence Lot 3, reste aussi sur `/shop` sans ouvrir la preview dans cette passe.

Captures reprise 13.7 :

- [`capture_ux4_l3ter_13_7_v3ter1_image_20260522.png`](capture_ux4_l3ter_13_7_v3ter1_image_20260522.png)
- [`capture_ux4_l3ter_13_7_voir_20260522.png`](capture_ux4_l3ter_13_7_voir_20260522.png)
- [`capture_ux4_l3ter_13_7_cart_no_preview_20260522.png`](capture_ux4_l3ter_13_7_cart_no_preview_20260522.png)

JSON reprise 13.7 : [`recette_ux4_l3ter_13_7_v3ter_1_8_result.json`](recette_ux4_l3ter_13_7_v3ter_1_8_result.json)

**Verdict re-recette MOA 13.7 : NO GO maintenu.**

Le critère central Lot 3ter n'est toujours pas atteint : le clic/tap image ne déclenche pas la preview. Les garde-fous restent bons, mais la PR ne peut pas être validée MOA tant que V3ter.1 et V3ter.5 restent KO.

## Re-recette MOA 13.8 — V3ter.1–8

| Champ | Valeur |
|-------|--------|
| **Date / heure** | 2026-05-22 |
| **Version contrôlée** | `19.0.15.13.8` |
| **Commit contrôlé** | `9e14e15` |
| **Upgrade module** | OK |
| **Restart Odoo** | OK |
| **Tests auto élargis** | **88/88 OK · 0 failed · 0 error(s)** |

### Grille V3ter.1–8

| # | Scénario | Observé | Verdict |
|---|----------|---------|---------|
| V3ter.1 | Tap image produit simple | Preview inline ouverte, URL `/shop` conservée | OK |
| V3ter.2 | Tap panier overlay | Action panier sans preview parasite | OK |
| V3ter.3 | Tap wishlist overlay | Action wishlist sans preview parasite | OK |
| V3ter.4 | Tap titre produit | Navigation fiche produit complète | OK |
| V3ter.5a | Re-tap image même produit | Preview refermée proprement | OK |
| V3ter.5b | Image produit A → image produit B | Preview bascule sur le second produit ciblé | OK |
| V3ter.6 | URL pendant preview | `/shop` conservée | OK |
| V3ter.7 | ESC / clic grille / scroll page | Retrait naturel propre, pas de modal ni backdrop | OK |
| V3ter.8 | Console DevTools | Aucune erreur JS bloquante observée | OK |

Contrôles complémentaires :

- le CTA `Voir` ouvre également la preview, cohérent avec le comportement de référence ;
- le titre produit conserve la navigation fiche ;
- le viewport mobile 390 px ne présente pas de débordement horizontal (`scrollWidth <= viewportWidth`) ;
- un premier test de bascule A→B avait ciblé le fragment preview comme seconde carte ; le contrôle complémentaire excluant les fragments preview valide bien la bascule sur une vraie tuile produit.

Captures reprise 13.8 (passe Dev signée) :

- [`capture_ux4_l3ter_13_8_v3ter1_image_preview_20260522.png`](capture_ux4_l3ter_13_8_v3ter1_image_preview_20260522.png) — V3ter.1 image A preview ouverte
- [`capture_ux4_l3ter_13_8_v3ter5b_switch_20260522.png`](capture_ux4_l3ter_13_8_v3ter5b_switch_20260522.png) — V3ter.5b bascule produit A → B
- [`capture_ux4_l3ter_13_8_voir_preview_20260522.png`](capture_ux4_l3ter_13_8_voir_preview_20260522.png) — Voir référence
- [`capture_ux4_l3ter_13_8_v3ter2_cart_no_preview_20260522.png`](capture_ux4_l3ter_13_8_v3ter2_cart_no_preview_20260522.png) — V3ter.2 panier sans preview parasite (badge +1, feedback « Ajouté au panier · Voir le panier »)
- [`capture_ux4_l3ter_13_8_v3ter3_wishlist_no_preview_20260522.png`](capture_ux4_l3ter_13_8_v3ter3_wishlist_no_preview_20260522.png) — V3ter.3 wishlist sans preview parasite

JSON reprise 13.8 : [`recette_ux4_l3ter_13_8_v3ter_1_8_result.json`](recette_ux4_l3ter_13_8_v3ter_1_8_result.json)

**Verdict re-recette MOA 13.8 : GO MOA Lot 3ter — avec réserve documentaire R1.**

Le critère central Lot 3ter est atteint : le clic/tap image ouvre la preview comme le CTA `Voir`, sans casser panier, wishlist, titre produit, fermeture naturelle, URL `/shop`, console ou mobile.

### Réserve documentaire portée 13.8

| Réf | Description | Impact | Décision |
|-----|-------------|--------|----------|
| **R1** | Libellé bouton fermeture mobile inline tronqué à « Ferme[r] » dans la toolbar étroite du fragment preview ouvert sur tuile gauche | Cosmétique mineur · fermeture fonctionnelle (ESC + clic hors panneau + croix offcanvas desktop OK) | **GO avec réserve documentaire** · polish reporté Lot 3quater ou ticket dédié |

Réserve **R1** héritée et non bloquante — déjà documentée Lot 3bis (`13.4`) avant la régression Lot 3ter. Aucune dette nouvelle introduite par `13.8`.

### Conformité pattern Lot 3bis

| Critère | État |
|---------|------|
| Binding Colibri direct (CTA + lien image) | OK (selector dual) |
| Listeners document uniques (`previewState` global) | OK |
| Placeholder synchrone `.marketone-shop-preview--loading` mobile | OK (`previewOpen: true` immédiat) |
| Garde-fous panier / wishlist / `o_wsale_product_btn` | OK |
| Pas de modal · pas de backdrop | OK |
| Re-tap → toggle ferme | OK |
| Bascule produit A → B | OK |
