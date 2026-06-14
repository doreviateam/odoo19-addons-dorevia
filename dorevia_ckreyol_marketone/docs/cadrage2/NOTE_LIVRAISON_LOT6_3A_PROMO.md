# NOTE_LIVRAISON — Lot 6.3a Porte Promotions · `19.0.17.0.0`

| Champ | Valeur |
|-------|--------|
| **Version** | `19.0.17.0.0` |
| **ADR** | ADR-034 |
| **Contrat** | C3.D |
| **Recette** | [`RECETTE_MANUELLE_LOT6_3A_PROMO.md`](../recette/lots/RECETTE_MANUELLE_LOT6_3A_PROMO.md) |
| **Réception MOA** | [`RECEPTION_MOA_LOT6_3A_PROMO.md`](./RECEPTION_MOA_LOT6_3A_PROMO.md) — **GO clôture MOA** (2026-06-08) |

---

## En-tête recette (cadrage2)

**ADR-034 :** [`ARBITRAGE_ARCHITECTURE_CADRAGE2.md`](../cadrage2/ARBITRAGE_ARCHITECTURE_CADRAGE2.md)

**Fonctionnalité Odoo native préservée :** Listes de prix · Promotions

**Mécanisme Odoo concerné :** `product.pricelist` · `product.pricelist.item` · règles de prix Odoo

**Non-régression référence boutique :** [`REFERENCE_RECETTE_BOUTIQUE_MOA.md`](../recette/REFERENCE_RECETTE_BOUTIQUE_MOA.md) — sections B1 · B2 · B3 · B4 · B6 · B7

---

## Phrase obligatoire

> **Aucun moteur Odoo remplacé** — les promotions s’appuient sur `product.pricelist` / `product.pricelist.item` (pricelist courante visiteur). Marketone présente et filtre la grille `/shop` uniquement.

---

## Livrables code

| Couche | Fichier |
|--------|---------|
| Résolveur promo | `models/product_pricelist.py` |
| Filtre grille | `models/product_template.py` |
| Contrôleur | `controllers/website_sale.py` — mode `promo` · alias `/promotions` |
| QWeb porte | `views/pages/shop_promo.xml` |
| Chip header | `views/layout/header.xml` |
| Styles | `static/src/scss/_shop_promo.scss` · `_header.scss` |
| Tests | `tests/test_marketone_lot6_3a_promo.py` |

---

## Limites documentées (règles Odoo complexes)

Voir docstring `models/product_pricelist.py` :

- `fixed` sur catégorie / global : inclus par prudence sans comparaison `list_price`.
- `formula` : seul `price_discount > 0` ; surcharges / arrondis non modélisés finement.
- `sale_loyalty` / coupons : hors scope — extension future au point d’union du résolveur.

---

## Hors périmètre (confirmé)

- `product_pack` · alias `/kits` · chip Kits & Coffrets
- Moteur prix / promo Marketone · recalcul front
- SEO canonical / noindex implémenté
