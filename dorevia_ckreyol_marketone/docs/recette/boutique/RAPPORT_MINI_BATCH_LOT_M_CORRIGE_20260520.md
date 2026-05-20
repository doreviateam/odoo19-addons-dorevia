# Rapport mini-batch — lot M corrigé — pilote média

| Champ | Valeur |
|-------|--------|
| **Date** | 2026-05-20 |
| **Signal amont** | [`RAPPORT_P4_LOTS_M_X_QUALITE_SOURCE.md`](./RAPPORT_P4_LOTS_M_X_QUALITE_SOURCE.md) — GO mini-batch ciblé lot M corrigé |
| **Run** | `tools/ck_image_normalizer/reports/runs/pilote_20260520_lot_m_corrige/` |
| **Input** | `tools/ck_image_normalizer/input/pilote_lot_m_corrige/` |
| **Manifest** | `tools/ck_image_normalizer/manifest.pilote_lot_m_corrige.csv` |
| **Recette** | `ck_shop_tile_v1.1` |
| **Volume** | 7 images (reprises manuelles P4) |
| **Garde-fous** | Aucun code Odoo · aucun remplacement `image_1920` · sources pilote originales intactes |

---

## 1. Résultat automatique

| Statut moteur | Nombre | Taux |
|---------------|-------:|-----:|
| `OK` | 5 | 71 % |
| `OK_WITH_WARNINGS` | 0 | 0 % |
| `NEEDS_REVIEW` | 0 | 0 % |
| `REJECTED` | 2 | 29 % |

Synthèse :

```text
OK + OK_WITH_WARNINGS : 5 / 7 = 71 %
REJECTED              : 2 / 7 = 29 %
NEEDS_REVIEW          : 0 / 7 = 0 %
GO candidate auto     : non (seuil REJECTED ≤ 10 %)
```

---

## 2. Détail par fichier

| Fichier | Référence | Statut | `content_area_ratio` | Alerte |
|---------|-----------|--------|---------------------:|--------|
| `07_product-156_biscuits-coco-vanille_corrige.jpg` | Biscuits coco vanille | **OK** | 0,1881 | — |
| `10_product-159_rougail-epices-reunion_corrige.jpg` | Rougail épices Réunion | **OK** | 0,3431 | — |
| `11_product-160_chutney-mangue-verte_corrige.jpg` | Chutney mangue verte | **OK** | 0,3951 | — |
| `19_product-180_tartinade-coco-citron-vert_corrige.jpg` | Tartinade coco citron vert | **OK** | 0,4059 | — |
| `27_product-188_coffret-biscuits-et-douceurs_corrige.jpg` | Coffret biscuits et douceurs | **OK** | 0,2077 | — |
| `03_product-9_pates-de-manioc-mayotte_corrige.jpg` | Pâtes de manioc Mayotte | **REJECTED** | 0,1013 | produit petit dans la source |
| `23_product-184_semoule-manioc-fine-mayotte_corrige.jpg` | Semoule manioc fine Mayotte | **REJECTED** | 0,1013 | produit petit dans la source |

Livrables run :

| Type | Chemin |
|------|--------|
| Rapport CSV | `…/reports/batch_20260520T122805Z.csv` |
| Rapport JSON | `…/reports/batch_20260520T122805Z.json` |
| Previews | `…/reports/previews/` |
| WebP / JPEG | `…/output/webp/` · `…/output/jpeg/` |

---

## 3. Lecture MOA / Dev

### Gains

- **5 / 7** reprises manuelles passent en **`OK`** auto — amélioration nette vs statut `M` initial.
- **0 `NEEDS_REVIEW`** sur ce mini-batch — charge revue réduite sur les corrections réussies.
- La reprise source locale **fonctionne** quand le produit occupe suffisamment la frame (`content_area_ratio` ≥ 0,15).

### Blocages restants (2 manioc)

Les deux fichiers **REJECTED** partagent le **même checksum MD5** — il s’agit du **même visuel** dupliqué pour deux SKU distincts (pâtes vs semoule manioc).

Cause technique :

```text
content_area_ratio = 0,1013 (< seuil packshot 0,15)
→ statut REJECTED · « produit petit dans la source »
```

Décision recommandée :

```text
Pas de correction recette — reprendre deux packshots dédiés par SKU, recadrés plus serrés sur le sachet.
```

---

## 4. Impact sur le bilan pilote 50 SKU

| Catégorie | Avant mini-batch | Après mini-batch |
|-----------|-----------------:|-----------------:|
| Exploitable cumulé | 36 / 50 (72 %) | **41 / 50 (82 %)** sous réserve contrôle visuel MOA |
| Hors flux sans action | 14 / 50 (28 %) | **9 / 50 (18 %)** — 2 manioc redemande source + 7 lot X |

Les **5 OK** restent soumis à **contrôle visuel MOA** avant exploitation (pas de publication auto).

Les **7 lot X** restent en **demande fournisseur / exclusion** — inchangé.

---

## 5. Validation visuelle MOA (2026-05-20)

Signal reçu :

```text
GO réintégration pilote — 5 images lot M corrigé validées visuellement — bilan exploitable porté à 41 / 50.
```

| Image | Statut moteur | Décision MOA finale | Note MOA |
|-------|:-------------:|:-------------------:|----------|
| Biscuits coco vanille | `OK` | **OK avec réserve** ✅ | Cadrage horizontal · proximité visuelle coffret |
| Rougail épices Réunion | `OK` | **OK visuel** ✅ | Composition lisible · poids visuel correct |
| Chutney mangue verte | `OK` | **OK avec réserve** ✅ | Réserve identification SKU en mobile |
| Tartinade coco citron vert | `OK` | **OK avec réserve** ✅ | Réserve scène lifestyle dense |
| Coffret biscuits et douceurs | `OK` | **OK avec réserve** ✅ | Réserve proximité visuelle avec biscuits coco |
| Pâtes de manioc Mayotte | `REJECTED` | **Redemande source distincte** | `content_area_ratio` 0,1013 · source dupliquée |
| Semoule manioc fine Mayotte | `REJECTED` | **Redemande source distincte** | `content_area_ratio` 0,1013 · source dupliquée |

Lot X (7) : **demande fournisseur / exclusion temporaire** maintenu — voir `lot_x_arbitrage_moa.csv`.

Règle catalogue actée : [`REGLE_CATALOGUE_IMAGES_SOURCE.md`](../../cadrage/REGLE_CATALOGUE_IMAGES_SOURCE.md)

---

## 6. Bilan consolidé après mini-batch lot M

| Catégorie | Nombre |
|-----------|-------:|
| `OK` moteur | 18 |
| `OK_WITH_WARNINGS` moteur | 3 |
| `NEEDS_REVIEW` validés `E` (P4) | 3 |
| `NEEDS_REVIEW` validés `R` (P4) | 12 |
| Lot M mini-batch validés MOA | 5 |
| **Total exploitable** | **41 / 50** |
| Hors flux — 2 manioc redemande source | 2 |
| Hors flux — lot X demande fournisseur | 7 |
| **Total hors flux** | **9 / 50** |

```text
Taux exploitable après lot M : 41 / 50 = 82 %
Taux hors flux         : 9 / 50 = 18 %
REJECTED définitif     : 0 / 50 auto (2 manioc en attente source)
```

Addendum : les deux SKU manioc ont ensuite reçu des sources distinctes et ont été réintégrés.

```text
Bilan consolidé final : 43 / 50 = 86 %
Hors flux final        : 7 / 50 = 14 % (lot X)
```

→ [`REPONSE_MOA_REINTEGRATION_2_MANIOC_SOURCES_DISTINCTES.md`](./REPONSE_MOA_REINTEGRATION_2_MANIOC_SOURCES_DISTINCTES.md)

---

## 7. Suite opérationnelle

| Qui | Action | Statut |
|-----|--------|--------|
| **MOA** | Fournir **2 packshots manioc distincts** — [`lot_manioc_redemande_source.csv`](../../../../tools/ck_image_normalizer/reports/runs/pilote_20260520/lot_manioc_redemande_source.csv) | ✅ Réalisé |
| **Dev** | Mini-batch ciblé **2 manioc** — **sur signal MOA** uniquement | ✅ Exécuté |
| **MOA** | Lot **X** (7) — charte source fournisseur | ☐ [`lot_x_arbitrage_moa.csv`](../../../../tools/ck_image_normalizer/reports/runs/pilote_20260520/lot_x_arbitrage_moa.csv) |

---

## 8. Signal de clôture mini-batch

```text
Mini-batch lot M clôturé — 5 / 7 validés MOA — bilan pilote 41 / 50 (82 %) — 2 manioc redemande source — lot X exclu temporairement.
```

Signal consolidé après mini-batch manioc :

```text
GO réintégration pilote — 2 SKU manioc validés sur sources distinctes — bilan exploitable porté à 43 / 50 — lot X maintenu en demande fournisseur / exclusion temporaire.
```

**Commande exécutée** :

```bash
cd tools/ck_image_normalizer
.venv/bin/python -m ck_image_normalizer run \
  --input input/pilote_lot_m_corrige \
  --manifest manifest.pilote_lot_m_corrige.csv \
  --recipe recipes/ck_shop_tile_v1.1.yaml \
  --output-dir reports/runs/pilote_20260520_lot_m_corrige
```

---

## Références

| Document | Rôle |
|----------|------|
| [`REPONSE_MOA_REINTEGRATION_5_LOT_M_CORRIGE.md`](./REPONSE_MOA_REINTEGRATION_5_LOT_M_CORRIGE.md) | Validation visuelle MOA · signal GO |
| [`REGLE_CATALOGUE_IMAGES_SOURCE.md`](../../cadrage/REGLE_CATALOGUE_IMAGES_SOURCE.md) | Règle catalogue source — actée MOA |
| [`RAPPORT_P4_LOTS_M_X_QUALITE_SOURCE.md`](./RAPPORT_P4_LOTS_M_X_QUALITE_SOURCE.md) | Préparation lots M/X |
| [`RECETTE_MANUELLE_CK_IMAGE_NORMALIZER_PILOTE_MEDIA.md`](./RECETTE_MANUELLE_CK_IMAGE_NORMALIZER_PILOTE_MEDIA.md) | Clôture P5 pilote |
| [`lot_m_reprise_manuelle.csv`](../../../../tools/ck_image_normalizer/reports/runs/pilote_20260520/lot_m_reprise_manuelle.csv) | Lot M initial (7) |
| [`lot_manioc_redemande_source.csv`](../../../../tools/ck_image_normalizer/reports/runs/pilote_20260520/lot_manioc_redemande_source.csv) | 2 manioc — redemande source distincte |
| [`lot_x_arbitrage_moa.csv`](../../../../tools/ck_image_normalizer/reports/runs/pilote_20260520/lot_x_arbitrage_moa.csv) | Lot X arbitré MOA — exclusion temporaire |
| [`lot_x_demande_fournisseur.csv`](../../../../tools/ck_image_normalizer/reports/runs/pilote_20260520/lot_x_demande_fournisseur.csv) | Lot X (7) — demande fournisseur |
