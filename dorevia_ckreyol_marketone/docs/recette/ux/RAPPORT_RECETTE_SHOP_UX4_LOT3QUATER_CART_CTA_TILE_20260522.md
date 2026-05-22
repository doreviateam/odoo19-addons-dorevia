# Rapport recette — UX-4 Lot 3quater — CTA panier tuile

| Champ | Valeur |
|-------|--------|
| **Date** | 2026-05-22 |
| **Module** | `dorevia_ckreyol_marketone` |
| **Version** | `19.0.15.14.0` |
| **Branche** | `feat/marketone-ux4-lot3quater-cart-cta-tile` |
| **Base** | `ckr-marketone-01` |
| **URL** | `http://localhost:18079/shop` |
| **Document recette** | [`RECETTE_MANUELLE_SHOP_UX4_IN_PLACE.md`](RECETTE_MANUELLE_SHOP_UX4_IN_PLACE.md) |
| **Arbitrage MOA** | [`NOTE_ARBITRAGE_UX4_LOT3QUATER_CART_CTA_TILE.md`](../../tickets/ux/NOTE_ARBITRAGE_UX4_LOT3QUATER_CART_CTA_TILE.md) |

## Préparation

| Contrôle | Résultat |
|----------|----------|
| Branche `feat/marketone-ux4-lot3quater-cart-cta-tile` depuis `main` | OK |
| Upgrade module `-u dorevia_ckreyol_marketone` | OK |
| Redémarrage Odoo long-running | OK |
| Tests automatisés UX-4 | **29/29 OK · 0 failed · 0 error(s)** |

## Implémentation (périmètre MOA)

| Zone | Changement |
|------|------------|
| QWeb `shop_product_tile_conversion.xml` | Libellé `Ajouter` · classes `marketone-shop-card-cart--tile` · `aria-label`/`title` = « Ajouter au panier » |
| SCSS `_shop_product_cards.scss` | Pill compact icône + libellé · overlay bas-droit · override `aspect-ratio` Odoo · `pointer-events` au survol uniquement (desktop) |
| JS | **Aucun changement** |
| Preview | **Inchangée** (`Ajouter au panier` pleine largeur) |

## Résultat desktop (1440 px)

| # | Scénario | Observé | Verdict |
|---|----------|---------|---------|
| V3quater.1 | CTA lisible icône + `Ajouter` | Label `Ajouter` · icône présente · ~101×39 px (pill compact) | OK |
| V3quater.2 | CTA visible au survol image | Visible après hover carte | OK |
| V3quater.4 | Clic CTA → panier seul | URL `/shop` · preview fermée · compteur +1 | OK |
| V3quater.5 | Clic image hors CTA → preview | Offcanvas preview ouverte | OK |
| V3quater.6 | Clic wishlist → wishlist seul | Wishlist +1 · preview fermée | OK |
| V3quater.7 | Feedback + compteur | « Ajouté au panier » visible sur carte | OK |
| V3quater.8 | Console | 0 erreur JS bloquante | OK |

## Résultat mobile (390 px)

| # | Scénario | Observé | Verdict |
|---|----------|---------|---------|
| V3quater.1 | CTA lisible | Label `Ajouter` · icône · ~81×36 px | OK |
| V3quater.3 | Pas de débordement horizontal | `scrollWidth <= 390` · bouton 81 px | OK |
| V3quater.4 | Clic CTA → panier seul | Pas de preview inline | OK |
| V3quater.5 | Clic image → preview inline | Preview inline ouverte | OK |
| V3quater.8 | Console | Pas de nouvelle erreur JS | OK |

## Smoke non-régression

| Critère | Référence | Résultat |
|---------|-----------|----------|
| Panier in-place | L2.1 | URL `/shop` conservée | OK |
| Retrait naturel preview | R2-D1 | Scroll panneau pendant hover — preview maintenue | OK |
| Isolation panier / wishlist | I5 · I6 (via V3quater.4 / 6) | Pas de preview parasite | OK |

## Captures et preuves

| ID | Fichier |
|----|---------|
| C-L3q-D1 | [`recette_v3quater_14_0_20260522_desktop.png`](recette_v3quater_14_0_20260522_desktop.png) |
| C-L3q-M1 | [`recette_v3quater_14_0_20260522_mobile.png`](recette_v3quater_14_0_20260522_mobile.png) |

JSON : [`recette_v3quater_14_0_20260522.json`](recette_v3quater_14_0_20260522.json)

## Correctif recette intermédiaire

- **Pointer-events desktop** : le bouton masqué (`opacity: 0`) ne doit pas intercepter le clic image — `pointer-events: none` sur `.btn` hors survol.
- **Aspect-ratio Odoo** : neutralisation explicite `aspect-ratio: auto !important` pour passer du cercle icône-seule à la pill icône + `Ajouter`.

## Verdict Lot 3quater

| Verdict | Statut |
|---------|--------|
| **GO MOA Lot 3quater** | ☐ — en attente **recette visuelle MOA** desktop + mobile |
| **NO GO** | ☐ |
| **Recette auto Codex** | ☑ **14/14 OK** sur `19.0.15.14.0` |

**Verdict : recette automatique OK — merge interdit sans validation visuelle MOA** (consigne arbitrage).

Le GO global UX-4 `19.0.15.13.9` n’est pas remis en cause ; Lot 3quater = harmonisation visuelle légère uniquement.
