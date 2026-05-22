# Rapport clôture — PR #19 — UX-4 Lot 3quater + 3quater bis

| Champ | Valeur |
|-------|--------|
| **Date** | 2026-05-22 |
| **Verdict MOA** | ☑ **GO MOA PR #19** |
| **Version** | `19.0.15.14.1` |
| **Merge commit** | `9327254` |
| **Commits fonctionnels** | `3f695b1` (Lot 3quater) · `a859c9e` (Lot 3quater bis) |
| **PR** | [#19](https://github.com/doreviateam/odoo19-addons-dorevia/pull/19) |

## Périmètre livré

| Lot | Contenu |
|-----|---------|
| **3quater** | CTA panier tuile explicite : icône + `Ajouter` · overlay bas-droit · règle **R-UX4-9** |
| **3quater bis** | Feedback « Voir le panier » contextualisé · desktop overlay hover bas-gauche · mobile inline discret |

Périmètre technique : QWeb + SCSS · exception JS défensive `marketone_shop_preview.js` uniquement · `marketone_shop_cart_add.js` inchangé.

## Recette

| Passe | Résultat |
|-------|----------|
| Recette manuelle PR #19 (V3quater + V3qB + smoke) | **30/30 OK** |
| Tests auto UX-4 | **29/29 OK** |
| Console JS bloquante | **0** |

## Réserve non bloquante

**V3q-contrast** — surveiller la lisibilité du pill `Ajouter` selon les contrastes visuels des futures images produits.

## Preuves

- [`recette_manuelle_pr19_20260522.json`](recette_manuelle_pr19_20260522.json)
- [`recette_v3qb_14_1_20260522.json`](recette_v3qb_14_1_20260522.json) + captures
- [`recette_v3quater_14_0_20260522.json`](recette_v3quater_14_0_20260522.json) + captures
- [`RAPPORT_RECETTE_SHOP_UX4_LOT3QUATER_CART_CTA_TILE_20260522.md`](RAPPORT_RECETTE_SHOP_UX4_LOT3QUATER_CART_CTA_TILE_20260522.md)
- [`RAPPORT_RECETTE_SHOP_UX4_LOT3QUATER_BIS_CART_FEEDBACK_20260522.md`](RAPPORT_RECETTE_SHOP_UX4_LOT3QUATER_BIS_CART_FEEDBACK_20260522.md)

## Version de référence UX-4

**`19.0.15.14.1`** — référence actuelle post-merge PR #19 sur `main`.
