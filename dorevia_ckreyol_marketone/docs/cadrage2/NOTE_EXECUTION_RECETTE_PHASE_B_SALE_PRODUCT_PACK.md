# Note exécution — Recette BO Phase B `sale_product_pack`

| Champ | Valeur |
|-------|--------|
| **Date** | 2026-06-08 |
| **Base** | `ckr-marketone-01` |
| **Verdict** | **GO recette BO avec réserve perf sandbox** |
| **Activation prod** | **NO GO** |
| **Grille** | [`RECETTE_MANUELLE_PHASE_B_SALE_PRODUCT_PACK_BO.md`](../recette/maintenance/RECETTE_MANUELLE_PHASE_B_SALE_PRODUCT_PACK_BO.md) |

---

## Résultats B1–B6

| # | Scénario | Résultat |
|---|----------|----------|
| **B1** | SO pack **7** `detailed/ignored` | **6 lignes** (1 parent + 5 composants) |
| **B1b** | SO pack **8** `non_detailed` | **1 ligne** |
| **B2** | Confirmation | OK |
| **B3** | Picking / moves | OK — 6 moves |
| **B4** | Livraison | OK — picking `done` · `qty_delivered` parent = 1 |
| **B5** | Facturation | OK — **4,17 €** · pas de double comptage |
| **B6** | Smoke front | OK — `/kits` → `/shop?marketone_mode=pack` · porte Kits · packs **7** + **8** visibles |
| **B6b** | Panier pack **8** | OK — **1 ligne** `website_sale` |
| **B6c** | Pack **7** front | OK — pas de checkout **detailed** (#229 hors Phase B) |

Lot **6.3b front** : **non rouvert**.

---

## Réserve perf sandbox

Tests auto `dorevia_marketone_lot6_3b_pack` relancés **2 fois** après recette :

- **0 échec fonctionnel**
- **Timeouts HTTP 12 s** sur rendus `/shop` ou `/shop?marketone_mode=pack` pendant / après régénération assets
- Mêmes URLs en **200** ensuite

Réserve **hors décision métier Phase B** — à traiter si exigée avant prod.

---

## Statuts GO

| Niveau | Statut |
|--------|--------|
| **GO lancement recette BO** | ☑ Exécuté |
| **GO recette BO** | ☑ **Avec réserve perf sandbox** |
| **Arbitrage pilote / généralisation** | ☑ Pilote maintenu · NON généralisation |
| **GO pilote contrôlé** | ☐ Prochain verrou |
| **GO activation prod** | ☐ **NO GO** |

---

## Suite

Arbitrage MOA (2026-06-08) : **pilote 7 maintenu** · **NON généralisation catalogue** · **NO GO prod**.

**Prochain verrou** : **GO pilote contrôlé** *ou* **GO généralisation** — voir [`ARBITRAGE_MOA_POST_PHASE_B_SALE_PRODUCT_PACK.md`](./ARBITRAGE_MOA_POST_PHASE_B_SALE_PRODUCT_PACK.md).
