# Préparation base — Recette MOA Lot 6.3a Promo

| Champ | Valeur |
|-------|--------|
| **Base** | `ckr-marketone-01` |
| **URL** | http://localhost:18079 |
| **Version module** | `19.0.17.0.0` |
| **Script** | [`scripts/prep_recette_lot6_3a_promo.py`](../../scripts/prep_recette_lot6_3a_promo.py) |
| **Statut** | **Consommé — GO clôture MOA** (2026-06-08) · état base restauré (items 39/40 actifs · item 41 expiré) |

---

## Commande de préparation

```bash
docker exec -i sandbox-odoo19-odoo-1 odoo shell -d ckr-marketone-01 --no-http \
  < odoo19-addons-dorevia/dorevia_ckreyol_marketone/scripts/prep_recette_lot6_3a_promo.py
```

---

## Jeu de données recette (dernière exécution)

| Rôle | Produit | ID template | Item pricelist |
|------|---------|-------------|----------------|
| **Promo A** | Maniocookies salés La Platine | 7 | -15 % · item 39 |
| **Promo B** | Crackers manioc Sainte-Anne | 8 | -20 % · item 40 |
| **Hors promo** | Pâtes de manioc Mayotte | 9 | *(aucun item actif)* |
| **P6 global** *(inactif par défaut)* | Tous les produits | — | item 41 · `3_global` · -5 % · `date_end` passée |

| Paramètre | Valeur |
|-----------|--------|
| **Pricelist visiteur public** | Default · id **3** |
| **Résolveur `_marketone_get_promo_template_ids`** | `{7, 8}` |

---

## Scénarios recette

| # | Action MOA |
|---|------------|
| **P1** | `GET /promotions` → 301 → `/shop?marketone_mode=promo` |
| **N1/N2** | Header : lien **Promotions** · pas de `/kits` |
| **P2/P3** | Grille promo = produits **7** et **8** uniquement · prix Odoo natif |
| **P5/P8** | Lien « Tous les produits » · portes 6.1 / 6.2 inchangées |
| **R1–R4** | REFERENCE § B1 · B3 · B4 · smoke panier |
| **P4** | Désactiver items 39 et 40 en BO → état vide |
| **P6** | Activer item 41 (effacer `date_end`) → catalogue complet |
| **P7** | Si multi-pricelist : changer pricelist visiteur · vérifier jeu promo |

---

## Rappel doctrine

> **Aucun moteur Odoo remplacé** — promotions via `product.pricelist.item` (pricelist courante visiteur).

---

## Références

- [`RECETTE_MANUELLE_LOT6_3A_PROMO.md`](../recette/lots/RECETTE_MANUELLE_LOT6_3A_PROMO.md)
- [`RECEPTION_MOA_LOT6_3A_PROMO.md`](./RECEPTION_MOA_LOT6_3A_PROMO.md)
