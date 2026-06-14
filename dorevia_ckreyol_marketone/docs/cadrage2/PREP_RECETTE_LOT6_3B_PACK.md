# Préparation base — Recette MOA Lot 6.3b Kits & Coffrets

| Champ | Valeur |
|-------|--------|
| **Base** | `ckr-marketone-01` |
| **URL** | http://localhost:18079 |
| **Version module** | `19.0.18.0.0` |
| **Script** | [`scripts/prep_recette_lot6_3b_pack.py`](../../scripts/prep_recette_lot6_3b_pack.py) |
| **Statut** | **Consommé — GO clôture MOA** (2026-06-08) · état base restauré (`pack_ok` sur **7**/**8**) |

---

## Commande de préparation

```bash
docker exec -i sandbox-odoo19-odoo-1 odoo shell -d ckr-marketone-01 --no-http \
  < odoo19-addons-dorevia/dorevia_ckreyol_marketone/scripts/prep_recette_lot6_3b_pack.py
```

---

## Jeu de données recette (dernière exécution)

| Rôle | Produit | ID template | Attendu porte pack |
|------|---------|-------------|--------------------|
| **Pack A** | Maniocookies salés La Platine | 7 | Visible · `pack_ok=True` |
| **Pack B** | Crackers manioc Sainte-Anne | 8 | Visible · `pack_ok=True` |
| **Témoin unitaire** | Pâtes de manioc Mayotte | 9 | **Absent** · `pack_ok=False` |

| Paramètre | Valeur |
|-----------|--------|
| **Packs publiés `pack_ok=True`** | 2 (templates **7**, **8**) |
| **Contrôle catalogue complet** | template **9** visible sur `/shop` · absent de `/shop?marketone_mode=pack` |

**URLs recette** :

- `GET /kits` → 301 → `/shop?marketone_mode=pack`
- Chip header **Kits & Coffrets**

> **Sandbox multi-base** : sur http://localhost:18079, sélectionner la base **`ckr-marketone-01`** via `/web/login` avant d’ouvrir `/shop` ou `/kits` (sinon 404 « No database is selected »).

---

## Scénarios recette

| # | Action MOA |
|---|------------|
| **K1** | `GET /kits` → 301 → `/shop?marketone_mode=pack` |
| **N1/N2** | Header : lien **Kits & Coffrets** · **Promotions** conservé |
| **K2/K3** | Grille pack = produits **7** et **8** uniquement · **9** absent |
| **K4/K5** | Prix Odoo natif · lien « Tous les produits » |
| **R1–R4** | REFERENCE § B1 · B3 · B4 · smoke panier (pack = 1 ligne) |
| **K6** | Désactiver `pack_ok` sur **7** et **8** en BO → état vide → restaurer |
| **K7/K8** | Priorité `pack > promo` · portes 6.3a / 6.1 / 6.2 inchangées |

---

## Documents liés

- [`RECETTE_MANUELLE_LOT6_3B_PACK.md`](../recette/lots/RECETTE_MANUELLE_LOT6_3B_PACK.md)
- [`RECEPTION_MOA_LOT6_3B_PACK.md`](./RECEPTION_MOA_LOT6_3B_PACK.md)
- [`NOTE_LIVRAISON_LOT6_3B_PACK.md`](./NOTE_LIVRAISON_LOT6_3B_PACK.md)
