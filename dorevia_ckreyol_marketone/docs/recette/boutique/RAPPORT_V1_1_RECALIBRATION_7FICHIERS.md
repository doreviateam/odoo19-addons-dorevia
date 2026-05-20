# Rapport — Calibrage `ck_shop_tile_v1.1` — batch ciblé 7 fichiers

| Champ | Valeur |
|-------|--------|
| **Statut** | **Livré Dev** — **calibrage v1.1 accepté MOA** · P3 ciblé en cours |
| **Date** | 2026-05-20 |
| **Décision MOA** | GO calibrage v1.1 — pas de GO POC final |
| **Recette** | `ck_shop_tile_v1.1` |
| **Recette parente** | `ck_shop_tile_v1` |
| **Ticket** | [`TICKET_MARKETONE_CK_IMAGE_NORMALIZER_POC.md`](../../tickets/boutique/TICKET_MARKETONE_CK_IMAGE_NORMALIZER_POC.md) |

---

## Changement recette

| Ratio packshot (v1.1) | Statut |
|-----------------------|--------|
| `< 0.15` | `REJECTED` |
| `0.15 – 0.95` | `OK` / `OK_WITH_WARNINGS` |
| **`0.95 – 1.0`** | **`NEEDS_REVIEW`** *(v1 : `REJECTED`)* |

Fichier : `tools/ck_image_normalizer/recipes/ck_shop_tile_v1.1.yaml`

**Inchangé** : format 1024×1024 · fond `#F8EEDB` baked-in · WebP/JPEG · archive · previews · **aucun code Odoo**.

---

## Résultats batch ciblé (7 fichiers)

| Métrique | v1 (proxy) | v1.1 (recal) |
|----------|------------|--------------|
| Total | 7 | 7 |
| `REJECTED` | **7** | **0** |
| `NEEDS_REVIEW` | 0 | **7** |
| Rejected rate | 33 % (lot 21) | **0 %** |

---

## Tableau avant / après — statut par fichier

| Fichier | Référence | v1 | **v1.1** | `content_area_ratio` | Preview v1.1 |
|---------|-----------|-----|----------|----------------------|--------------|
| `exemple_produit_manioc_crackers_la_platine.backup_pre_retouche.png` | Crackers — avant retouche | REJECTED | **NEEDS_REVIEW** | 1.0 | `reports/runs/v1_1_recal_7/reports/previews/…` |
| `exemple_produit_manioc_crackers_la_platine.png` | Crackers — retouché | REJECTED | **NEEDS_REVIEW** | 1.0 | idem |
| `homepage_manioc_pates_mayotte_la_platine.png` | Pâtes Mayotte | REJECTED | **NEEDS_REVIEW** | 1.0 | idem |
| `mvp02_reference_coffret_gourmand_bois.png` | Coffret bois | REJECTED | **NEEDS_REVIEW** | 0.997 | idem |
| `stitch_curry_powder_pouch.png` | Pochette curry | REJECTED | **NEEDS_REVIEW** | 1.0 | idem |
| `stitch_guava_jam_jar.png` | Pot goyave | REJECTED | **NEEDS_REVIEW** | 1.0 | idem |
| `stitch_scotch_bonnet_sauce.png` | Sauce scotch bonnet | REJECTED | **NEEDS_REVIEW** | 1.0 | idem |

**Transition** : **7/7** `REJECTED` → `NEEDS_REVIEW` · tuiles produites dans les deux cas.

CSV comparatif : [`comparison_v1_vs_v1_1.csv`](../../../../tools/ck_image_normalizer/reports/runs/v1_1_recal_7/reports/comparison_v1_vs_v1_1.csv)

---

## Livrables Dev

| Livrable | Chemin |
|----------|--------|
| Recette v1.1 | `tools/ck_image_normalizer/recipes/ck_shop_tile_v1.1.yaml` |
| Manifest 7 fichiers | `tools/ck_image_normalizer/manifest.v1_1_recal_7.csv` |
| Rapport JSON | `tools/ck_image_normalizer/reports/runs/v1_1_recal_7/reports/batch_20260520T110201Z.json` |
| Rapport CSV | `tools/ck_image_normalizer/reports/runs/v1_1_recal_7/reports/batch_20260520T110201Z.csv` |
| Previews avant/après | `tools/ck_image_normalizer/reports/runs/v1_1_recal_7/reports/previews/` |
| Tuiles WebP / JPEG | `tools/ck_image_normalizer/reports/runs/v1_1_recal_7/output/` |

---

## Attendu MOA — revue visuelle P3

Pour chaque `NEEDS_REVIEW`, arbitrer :

- **Exploitable** `/shop` après normalisation ?
- **Reprise manuelle** source ou retouche ?
- **Exclure** du futur process catalogue ?

Critères G1–G6 — focus **G6** (couture `#F8EEDB` baked-in).

---

## Suite possible (après revue MOA)

1. Relancer batch **21 images** complet en v1.1 ;
2. Valider les **21 refs** comme lot officiel MOA (révision 2026-05-20) ;
3. Adopter v1.1 comme recette candidate POC officiel.

---

## Historique

| Date | Auteur | Action |
|------|--------|--------|
| 2026-05-20 | MOA | GO calibrage v1.1 + batch ciblé 7 |
| 2026-05-20 | Dev | Implémentation + batch — 7/7 NEEDS_REVIEW |
