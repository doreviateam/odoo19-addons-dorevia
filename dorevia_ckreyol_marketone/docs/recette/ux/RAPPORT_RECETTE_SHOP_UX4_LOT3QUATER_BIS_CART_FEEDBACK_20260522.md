# Rapport recette — UX-4 Lot 3quater bis — feedback « Voir le panier »

| Champ | Valeur |
|-------|--------|
| **Date** | 2026-05-22 |
| **Module** | `dorevia_ckreyol_marketone` |
| **Version** | `19.0.15.14.1` |
| **Branche / PR** | `feat/marketone-ux4-lot3quater-cart-cta-tile` · PR #19 |
| **Base** | `ckr-marketone-01` |
| **URL** | `http://localhost:18079/shop` |

## Implémentation

| Zone | Changement |
|------|------------|
| QWeb | Feedback déplacé dans zone image · label mobile `d-lg-none` |
| SCSS | Desktop : overlay bas-gauche au survol (pill « Voir le panier ») · Mobile : inline court sous image sans encart |
| JS preview | Exclusion défensive `.marketone-shop-card-cart-feedback` |
| `marketone_shop_cart_add.js` | **Aucun changement** |

## Recette auto V3qB

| Passe | Résultat |
|-------|----------|
| V3qB.1–9 desktop + mobile | **18/18 OK** |
| Smoke L2.1 · R2-D1 | OK |
| Tests auto UX-4 | **29/29 OK** |

## Points clés validés auto

- Desktop : pas de feedback dans le corps · overlay « Voir le panier » au survol après ajout
- Mobile : « Ajouté au panier » + lien inline discret · bordure sauge
- Navigation `/shop/cart` · isolation preview / panier / wishlist · compteur header

## Preuves

- JSON : [`recette_v3qb_14_1_20260522.json`](recette_v3qb_14_1_20260522.json)
- Captures : `_desktop.png` · `_mobile.png`

## Verdict

| Verdict | Statut |
|---------|--------|
| **GO MOA Lot 3quater bis** | ☐ — en attente recette visuelle MOA |
| **Recette auto Codex** | ☑ **18/18 OK** sur `19.0.15.14.1` |

**Merge interdit avant validation visuelle MOA desktop + mobile.**
