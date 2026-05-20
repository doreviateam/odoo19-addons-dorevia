# TICKET — Parité visuelle grille boutique `dorevia_ckreyol_marketone`

| Champ | Valeur |
|-------|--------|
| **ID** | `TICKET_MARKETONE_BOUTIQUE_VISUAL_PARITY` |
| **Type** | Visuel / présentation Boutique |
| **Statut** | **Livré technique** `19.0.10.1.0` — validation MOA recette |
| **Version cible** | `19.0.10.1.0` |
| **Base** | `ckr-marketone-01` |
| **Prérequis** | Lots 1–3, portes 6.1 / 6.2, design system Lot 2.1 |

---

## Contexte MOA (2026-05-19)

La grille `/shop` affichait **3 produits par ligne** sur desktop (`website.shop_ppr = 3`), produisant des cartes trop larges et une boutique moins dense que l’ancien CK Marketplace.

**Objectif** : retrouver une densité retail crédible, sans copier le legacy ni modifier le moteur `website_sale`.

---

## Décision MOA

| Breakpoint | Colonnes produit |
|------------|------------------|
| Desktop large (≥ 1200 px) | **4** |
| Desktop moyen (992–1199 px) | **3** |
| Tablette (&lt; 992 px, comportement Odoo flex) | **2** |
| Mobile étroit (&lt; 576 px) | **1** |

**Périmètre inclus**

- `/shop` et portes Boutique (`marketone_mode=featured`, `marketone_mode=origin`)
- Classe scope `.marketone-shop` + paramètre site `shop_ppr = 4`
- SCSS responsive dans `_shop.scss`

**Hors périmètre**

- Moteur `website_sale` (Python, domaines, panier, checkout)
- Fiche produit, Culture, Savoirs, hub
- Copie CSS / HTML CK Marketplace

**Vigilance doctrine**

- La grille Boutique ne contient que des **produits vendables** (`product.template` publiés).
- Les recettes Savoirs (`marketone.savoir.recipe`) **n’apparaissent jamais** dans `/shop`.

---

## Livrables techniques

| Fichier | Rôle |
|---------|------|
| `data/marketone_website_shop_grid.xml` | `website.shop_ppr = 4` sur le site par défaut |
| `static/src/scss/_shop.scss` | Grille responsive 4 / 3 / 2 / 1 |
| `tests/test_marketone_lot3_shop.py` | `data-ppr="4"` sur `/shop` |

---

## Critère GO

La boutique Marketone affiche une grille **plus dense et crédible** sur desktop large (**4** cartes par ligne), reste **sobre**, **maintenable** et **standard Odoo**, avec les breakpoints MOA respectés sur `/shop` et les portes catalogue.

---

## Recette MOA rapide

| # | Vérification | Attendu |
|---|--------------|---------|
| 1 | `/shop` desktop large (≥ 1200 px) | 4 produits par ligne |
| 2 | `/shop` desktop moyen (~1100 px) | 3 produits par ligne |
| 3 | `/shop` tablette | 2 produits par ligne |
| 4 | `/shop` mobile étroit | 1 produit par ligne |
| 5 | Porte Incontournables | Même densité grille |
| 6 | Porte Origines facettée | Même densité grille |
| 7 | Aucune recette Savoirs | Pas de « Recette … » dans la grille |
| 8 | Fiche produit / panier | Inchangés |

---

## Références

- [`TICKET_MARKETONE_LOT3_SHOP.md`](../lots/TICKET_MARKETONE_LOT3_SHOP.md)
- `RECETTE_MANUELLE_SAVOIRS_V1.md` — doctrine produits vs recettes (document absent du dépôt)
- ADR-024 — trois univers
