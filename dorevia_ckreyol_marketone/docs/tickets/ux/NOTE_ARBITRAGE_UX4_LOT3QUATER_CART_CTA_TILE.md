# Note arbitrage MOA — UX-4 Lot 3quater · CTA panier tuile

| Champ | Valeur |
|-------|--------|
| **Date** | 2026-05-22 |
| **Lot** | UX-4 Lot 3quater |
| **Version cible** | `19.0.15.14.0` |
| **Branche** | `feat/marketone-ux4-lot3quater-cart-cta-tile` |
| **Référence UX-4** | `19.0.15.13.9` (GO global — non remis en cause) |

## Contexte MOA

La preview « Découvrir le produit » affiche un CTA panier premium pleine largeur **Ajouter au panier**.  
La tuile produit n’affichait qu’une icône panier ronde (masquage SCSS Odoo du libellé natif).  
Rupture visuelle et intention d’achat moins explicite sur la tuile.

## Décision MOA

| Sujet | Décision |
|-------|----------|
| Libellé tuile | **`Ajouter`** (court, compact) |
| Libellé preview | **`Ajouter au panier`** (inchangé) |
| Format tuile | Icône panier + libellé · overlay bas-droit · **pas** full-width |
| Périmètre | QWeb léger + SCSS scoped tuile · **zéro JS** |
| Comportement panier Lot 2 | **Inchangé** |
| Preview / wishlist / clic image | **Inchangés** |

## Règle documentée

**R-UX4-9 — CTA panier tuile explicite**

> Le CTA panier de la tuile doit rester compact mais explicite : icône panier + libellé court `Ajouter`, cohérent avec le CTA complet `Ajouter au panier` de la preview produit.

## Hors périmètre

- Modification JS, routes, interactions panier
- Changement placement overlay (reste bas-droit photo)
- Modification preview premium
- Remise en cause GO UX-4 `13.9`

## Recette

§ V3quater.1–V3quater.8 dans [`RECETTE_MANUELLE_SHOP_UX4_IN_PLACE.md`](../../recette/ux/RECETTE_MANUELLE_SHOP_UX4_IN_PLACE.md)

Smoke non-régression : L2.1–L2.5 · I5/I6 · R2-D1
