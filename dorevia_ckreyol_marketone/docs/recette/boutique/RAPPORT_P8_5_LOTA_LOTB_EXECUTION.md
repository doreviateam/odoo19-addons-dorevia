# Rapport exécution — P8-5 — Lot A + Lot B

| Champ | Valeur |
|-------|--------|
| **Décision MOA** | GO Lot A + Lot B |
| **Date exécution** | 2026-05-20 |
| **Base** | `ckr-marketone-01` |
| **Flag** | `marketone.shop_tile_enabled = True` |

---

## 1) Lot A exécuté — 3 packshots alpha retraités

Paramètre appliqué (scope strict Lot A):

- `content_fill_ratio`: **0.78 -> 0.84**
- recette: `ck_shop_tile_v1.2-alpha`
- run: `p8_packshot_alpha_lotA_fill84_20260520`

Produits retraités:

1. Maniocookies salés La Platine (`product_id=7`)
2. Mix beignets manioc (`product_id=163`)
3. Palettes coco vanille (`default_code=CK-MO-033`)

Manifest run:

- `tools/ck_image_normalizer/reports/runs/p8_packshot_alpha_lotA_fill84_20260520/manifest_lotA_fill84.csv`

### Captures comparatives Lot A (avant/après)

- `capture_p8_lotA_compare_01_product-7_maniocookies-sales-la-platine.png`
- `capture_p8_lotA_compare_14_product-163_mix-beignets-manioc.png`
- `capture_p8_lotA_compare_33_ck-mo-033_palettes-coco-vanille.png`

### Captures /shop Lot A (après)

- `capture_p8_lotA_after_maniocookies.png`
- `capture_p8_lotA_after_mix_beignets.png`
- `capture_p8_lotA_after_palettes_coco.png`

---

## 2) Lot B exécuté — 5 lifestyle maintenus v1.1 + NEEDS_REVIEW_SOURCE

Règle appliquée:

- **pas d'alpha**
- **recette conservée**: `ck_shop_tile_v1.1`
- **statut**: `pending_review`
- note MOA: `NEEDS_REVIEW_SOURCE` (recadrage / reprise source)

Liste Lot B:

1. Biscuits banane confiture (`product_id=471`)
2. Biscuits coco vanille (`product_id=156`)
3. Pâtes de manioc Mayotte (`product_id=9`)
4. Coffret biscuits et douceurs (`product_id=188`)
5. Semoule manioc fine Mayotte (`product_id=184`)

Captures de contrôle Lot B:

- `capture_p8_lotB_v11_biscuits_coco.png`
- `capture_p8_lotB_v11_pates_manioc.png`

---

## 3) État final en base (après Lot A + Lot B)

| Indicateur | Valeur |
|-----------|--------|
| `shop_tile_recipe_version = ck_shop_tile_v1.2-alpha` | **9** |
| `shop_tile_recipe_version = ck_shop_tile_v1.1` | **34** |
| `shop_tile_status = pending_review` | **5** (Lot B) |
| `image_1920` master | **inchangé** |

Validation technique:

- répartition 9/34 conservée
- doctrine intacte
- rollback flag intact

---

## 4) Garde-fous confirmés

- aucune modification `image_1920`
- pas d'alpha sur lifestyle (Lot B)
- pas de détourage IA / rembg
- pas de cron
- pas de refonte globale
- lot X inchangé

---

## 5) Livrables associés

- `AUDIT_P8_5_VISUAL_OCCUPANCY.csv`
- `RAPPORT_P8_5_RESERVES_ACTIONS_CIBLEES.md`
- `RAPPORT_P8_5_LOTA_LOTB_EXECUTION.md` (ce document)
- captures `capture_p8_lotA_*` et `capture_p8_lotB_*`

---

## Signal Dev

```text
Lot A + Lot B exécutés conformément au GO MOA.
Verdict MOA final consigné :
GO avec réserves gouvernées — modèle hybride v1.1 + v1.2-alpha validé.
Lot B maintenu en NEEDS_REVIEW_SOURCE sous gouvernance source.
Aucun nouveau traitement technique demandé à ce stade.
```
