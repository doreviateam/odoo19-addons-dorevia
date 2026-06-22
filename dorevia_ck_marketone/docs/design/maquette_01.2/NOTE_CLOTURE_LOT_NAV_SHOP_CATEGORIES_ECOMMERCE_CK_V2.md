# Clôture — Lot Nav-Shop · Catégories e-commerce dynamiques CK V2

| Champ | Valeur |
| --- | --- |
| **Lot** | Nav-Shop — navigation boutique `product.public.category` |
| **Ticket** | [`TICKET_DEV_LOT_NAV_SHOP_CATEGORIES_ECOMMERCE_CK_V2.md`](../TICKET_DEV_LOT_NAV_SHOP_CATEGORIES_ECOMMERCE_CK_V2.md) |
| **Branche Dev** | `feat/ck-nav-shop-categories-v2` |
| **PR** | [#80](https://github.com/doreviateam/odoo19-addons-dorevia/pull/80) |
| **Commit merge** | `18c04b42330c75f6bd0c51a4efc1c37746e88d9e` |
| **Commit Dev** | `ce08032` (branche `feat/ck-nav-shop-categories-v2`) |
| **Statut MOA** | **✅ GO merge · 2026-06-22** |
| **Statut QA** | **✅ GO merge · NOTE_QA §8 ter** |

## Versions livrées

| Module | Version |
| --- | --- |
| `dorevia_ck_marketone_content` | **19.0.1.28.1** |
| `dorevia_ck_theme` | **19.0.1.38.2** |

## Périmètre clos

- Navigation dynamique depuis `product.public.category` (remplacement `NAV_UNIVERSE_SPECS`)
- 2 niveaux max header · L3+ hors menu principal
- `Tous nos produits` · `Découvrir` hors catalogue · épinglage `o_no_autohide_item`
- Non-régression H1 / Nav-1
- Seed L2 recette · templates split-link / mobile L2 BO
- Corrections recette : overflow L2 · parent navigable · Découvrir pinned · doublon mobile B2

## Tests

| Tag | Résultat |
| --- | --- |
| `dorevia_ck_marketone_nav_sync` | **OK** |
| `dorevia_ck_theme_phase10` | **OK** |
| **Total** | **28/28** |

## Backlog (tickets séparés — hors lot)

- Survol L2 desktop hors overflow
- Enrichissement seed produits sous-catégories
- Arbitrage densité 7+ racines catalogue

## Documents de référence

- [`RECETTE_QA_LOT_NAV_SHOP_CATEGORIES_ECOMMERCE_CK_V2.md`](./RECETTE_QA_LOT_NAV_SHOP_CATEGORIES_ECOMMERCE_CK_V2.md)
- [`NOTE_QA_LOT_NAV_SHOP_CATEGORIES_ECOMMERCE_CK_V2.md`](./NOTE_QA_LOT_NAV_SHOP_CATEGORIES_ECOMMERCE_CK_V2.md)
- [`NOTE_NAV_SHOP_REMONTEE_DENSITE.md`](./NOTE_NAV_SHOP_REMONTEE_DENSITE.md)
