# Note exécution — Étape 1 Phase B `sale_product_pack` (merge PR #1)

| Champ | Valeur |
|-------|--------|
| **Date** | 2026-06-08 |
| **GO MOA** | Merge PR #1 · **GO lancement recette BO** uniquement |
| **PR** | https://github.com/doreviateam/odoo19-addons-oca/pull/1 — **MERGED** |
| **Merge commit** | `789fda8` |
| **Base** | `ckr-marketone-01` |
| **Marketone** | **Inchangé** — pas de `depends` ajouté |
| **Activation prod** | **NO GO** |

---

## Doctrine

```text
Odoo exécute. Marketone habille et oriente.
Aucun moteur Odoo remplacé.
```

---

## 1. Merge PR plateforme OCA

| Action | Résultat |
|--------|----------|
| Merge `dev/phase-a-oca-sale-product-pack-19` → `main` | ✓ `789fda8` |
| Branche locale `main` | Fast-forward `11ddaf4..789fda8` |
| Modules sync | `sale_product_pack` · `stock_product_pack` · `sale_stock_product_pack` |

---

## 2. Sandbox `ckr-marketone-01`

| Action | Résultat |
|--------|----------|
| Upgrade modules OCA | ✓ `-u sale_product_pack,stock_product_pack,sale_stock_product_pack` |
| État modules | **installed** `19.0.1.0.0` (×3) |
| Conteneur | `sandbox-odoo19-odoo-1` — addons OCA montés live (`/mnt/odoo19-addons-oca`) |

---

## 3. Préparation Phase B

| Produit | Template | Config |
|---------|----------|--------|
| Pack pilote | **7** | `detailed` · `pack_component_price=ignored` · 5 composants |
| Témoin pack | **8** | `non_detailed` · `ignored` |
| Témoin unitaire | **9** | `pack_ok=False` *(prep 6.3b rejouée)* |

Scripts : `prep_recette_lot6_3b_pack.py` + bascule pack **7** `detailed`.

---

## 4. Smoke automatisé Dev (pré-recette MOA)

Exécution shell — données **rollback** (non persistées).

| # | Scénario | Résultat |
|---|----------|----------|
| **B1** | SO pack **7** × 1 | **6 lignes** (1 parent + 5 composants) · composants **0 €** · parent **4,165 €** |
| **B1b** | SO pack **8** × 1 | **1 ligne** · **25 €** |
| **B2** | Confirmation SO pack **7** | `sale` ✓ |
| **B3** | Picking / moves | **6 moves** (1 pack + 5 composants) |
| **B4** | Validation picking | `done` · `qty_delivered` parent = **1** |
| **B5** | Facture | Total **4,17 €** · composants **0 €** · pas de double comptage |
| **B6** | Smoke front | **À signer MOA** navigateur — tests auto porte **13/13 OK** |

### Non-régression Marketone

```text
dorevia_marketone_lot6_3b_pack : 13/13 OK
```

---

## 5. Statuts GO (rappel MOA)

| Niveau | Statut |
|--------|--------|
| **GO lancement recette BO** | ☑ **Exécuté** (merge + sandbox + prep) |
| **GO recette BO** (B1–B6 signés MOA) | ☐ **En cours** — B6 navigateur + signature grille |
| **GO activation prod** | ☐ **NO GO** |

---

## Suite MOA

1. Exécuter recette BO **B1–B6** en navigateur — [`RECETTE_MANUELLE_PHASE_B_SALE_PRODUCT_PACK_BO.md`](../recette/maintenance/RECETTE_MANUELLE_PHASE_B_SALE_PRODUCT_PACK_BO.md)
2. **Signer ou non** le **GO recette BO**
3. Arbitrer pilote limité vs généralisation avant tout GO prod

---

## Références

- [`RECEPTION_MOA_PHASE_B_SALE_PRODUCT_PACK.md`](./RECEPTION_MOA_PHASE_B_SALE_PRODUCT_PACK.md)
- [`NOTE_PHASE_A_SALE_PRODUCT_PACK_OCA_19.md`](./NOTE_PHASE_A_SALE_PRODUCT_PACK_OCA_19.md)
- [`TICKET_MARKETONE_SALE_PRODUCT_PACK_OCA_PORT.md`](../tickets/maintenance/TICKET_MARKETONE_SALE_PRODUCT_PACK_OCA_PORT.md)
