# Recette manuelle — CK Image Normalizer V1 — Clôture POC (CLI externe)

| Champ | Valeur |
|-------|--------|
| **Ticket** | [`TICKET_MARKETONE_CK_IMAGE_NORMALIZER_POC`](../../tickets/boutique/TICKET_MARKETONE_CK_IMAGE_NORMALIZER_POC.md) |
| **ADR** | [ADR-033](../../cadrage/DECISIONS.md#adr-033--ck-image-normalizer-v1--poc-tuiles-commerce-shop) |
| **Outil** | `tools/ck_image_normalizer/` (hors module Odoo) |
| **Recette candidate** | `ck_shop_tile_v1.1` |
| **Lot officiel POC** | **21 références** — banque `dorevia_ckreyol_marketplace/docs/assets` |
| **Run de référence** | `tools/ck_image_normalizer/reports/runs/v1_1_proxy_21/` |
| **Statut recette** | **GO POC avec réserves MOA** (2026-05-20) |

---

## Verdict MOA

```text
GO POC avec réserves — lot officiel 21 refs validé — recette candidate ck_shop_tile_v1.1
```

Décision consignée : [`REPONSE_MOA_GO_POC_IMAGE_NORMALIZER_V1_1.md`](./REPONSE_MOA_GO_POC_IMAGE_NORMALIZER_V1_1.md)

| Date | Verdict | Commentaire |
|------|---------|-------------|
| 2026-05-20 | **GO POC avec réserves** | Grille plus homogène et plus chaude · fond `#F8EEDB` accepté · 14/21 OK+WARN · 0 REJECTED · **pas de code Odoo** |

---

## Périmètre validé

| Élément | Statut |
|---------|--------|
| Tuiles commerce `/shop` uniquement | ✅ |
| Carré **1024×1024** · fond **`#F8EEDB` baked-in** | ✅ validé MOA |
| Export **WebP** + **JPEG** · original conservé | ✅ |
| Rapport batch JSON/CSV + previews | ✅ |
| Profils **`packshot`** / **`lifestyle`** | ✅ |
| Intégration Odoo / remplacement `image_1920` | ❌ interdit post-POC |

---

## Prérequis opérateur

| Élément | Détail |
|---------|--------|
| Python | **3.10+** |
| Dépendances | Pillow, PyYAML — voir `tools/ck_image_normalizer/requirements.txt` |
| Environnement | venv local dans `tools/ck_image_normalizer/.venv` |
| Manifest | `manifest.csv` — template [`manifest.moa.template.csv`](../../../../tools/ck_image_normalizer/manifest.moa.template.csv) |
| Recette | **`recipes/ck_shop_tile_v1.1.yaml`** (obligatoire — ne pas utiliser v1 seule) |

```bash
cd tools/ck_image_normalizer
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

---

## Procédure batch (opérateur)

### 1. Préparer le lot

1. Copier les originaux dans `input/` (noms sans espace).
2. Copier et compléter le manifest :

```bash
cp manifest.moa.template.csv manifest.csv
```

3. Vérifier **21 lignes** + colonnes `filename`, `profile` (`packshot` | `lifestyle`), `reference`.

Voir [`input/README.md`](../../../../tools/ck_image_normalizer/input/README.md).

### 2. Lancer le batch

```bash
python -m ck_image_normalizer run \
  --input input \
  --manifest manifest.csv \
  --recipe recipes/ck_shop_tile_v1.1.yaml
```

### 3. Contrôler les sorties

| Dossier / fichier | Contenu |
|-------------------|---------|
| `output/webp/` | Tuiles WebP 1024×1024 |
| `output/jpeg/` | Tuiles JPEG fallback |
| `archive/orig/` | Copies horodatées des originaux |
| `reports/batch_*.json` | Rapport détaillé + indicateur `go_candidate` |
| `reports/batch_*.csv` | Synthèse tabulaire |
| `reports/previews/` | Comparatifs avant / après |

### 4. Seuils GO batch (lot 21 refs)

| Critère | Seuil | Résultat POC |
|---------|-------|--------------|
| `OK` + `OK_WITH_WARNINGS` | ≥ **60 %** (≥ **13/21**) | **14/21** ✅ |
| `REJECTED` | ≤ **10 %** (≤ **2/21**) | **0/21** ✅ |

Les seuils automatiques ne remplacent **pas** la revue visuelle MOA sur les `NEEDS_REVIEW`.

---

## Lecture des statuts

| Statut | Signification | Action opérateur |
|--------|---------------|------------------|
| **OK** | Tuile exploitable sans retouche | Peut être retenue pour publication manuelle |
| **OK_WITH_WARNINGS** | Exploitable avec réserve documentée | Vérifier preview · noter la réserve |
| **NEEDS_REVIEW** | Sas humain obligatoire | Revue G1–G6 · décision E/R/M/X (voir § ci-dessous) |
| **REJECTED** | Source ou algo inadapté | Reprise source ou exclusion · ne pas publier tel quel |

### Règle packshot v1.1 (plein cadre)

| `content_area_ratio` | Statut attendu |
|----------------------|----------------|
| &lt; 0.15 | `REJECTED` |
| 0.15 – 0.95 | `OK` / `OK_WITH_WARNINGS` |
| ≥ 0.95 | **`NEEDS_REVIEW`** (plus de rejet auto) |

---

## Flux opérateur — `NEEDS_REVIEW`

Pour chaque ligne `NEEDS_REVIEW` du CSV :

1. Ouvrir la **preview** dans `reports/previews/`.
2. Noter **G1–G6** (1–5) — grille MOA :

| Critère | Question |
|---------|----------|
| **G1** | Produit identifiable en ~320 px ? |
| **G2** | Chaleur / premium CK cohérent UX-3 B1 ? |
| **G3** | Poids visuel comparable aux autres tuiles ? |
| **G4** | Pas de halo agressif / détourage visible ? |
| **G5** | Texture / étiquette préservées ? |
| **G6** | Couture `#F8EEDB` / carte `#FDF9F0` acceptable ? |

3. Trancher :

| Code | Décision | Suite |
|------|----------|-------|
| **E** | Exploitable | Retenir la tuile normalisée |
| **R** | Acceptable avec réserve | Retenir sous contrôle · documenter la réserve |
| **M** | Reprise manuelle | Retoucher la source ou la tuile · relancer le batch sur le fichier |
| **X** | Exclure | Ne pas utiliser pour `/shop` · prévoir nouvelle source |

**Ne jamais** passer un `NEEDS_REVIEW` en production sans décision explicite.

---

## Réserves MOA (lot POC 21 refs)

### Reprise manuelle obligatoire ou recommandée

| Fichier | Statut batch | Décision P3 | Motif MOA |
|---------|--------------|-------------|-----------|
| `homepage_manioc_pates_mayotte_la_platine.png` | NEEDS_REVIEW | **M** | Artefacts de fond visibles (droite / bas) |
| `stitch_guava_jam_jar.png` | NEEDS_REVIEW | **M** | Artefacts bas / table trop visibles |

### Acceptables sous réserve (NEEDS_REVIEW → flux contrôlé)

| Fichier | Décision P3 | Notes |
|---------|-------------|-------|
| `exemple_produit_manioc_crackers_la_platine.png` | R | Ligne noire bas · cadrage plein cadre |
| `stitch_curry_powder_pouch.png` | R | Artefacts de fond autour de la scène |
| `stitch_scotch_bonnet_sauce.png` | R | Réserve découpe / couture fond-carte |

### Exploitable malgré NEEDS_REVIEW

| Fichier | Décision P3 |
|---------|-------------|
| `mvp02_reference_coffret_gourmand_bois.png` | **E** |

### Lifestyle — réserve générale

Les visuels **lifestyle** passent souvent en `OK` auto mais restent **moins homogènes** que les packshots. Le profil `lifestyle` est **conservateur** (pas de replace bg agressif) — comportement attendu.

---

## Grilles de référence (revue MOA POC)

| Livrable | Chemin |
|----------|--------|
| Grille normalisée desktop / mobile | `reports/runs/v1_1_proxy_21/reports/mock_grid_v1_1_normalized_desktop_mobile.html` |
| Comparatif source / normalisée | `reports/runs/v1_1_proxy_21/reports/mock_grid_v1_1_compare_desktop_mobile.html` |
| Rapport CSV batch | `reports/runs/v1_1_proxy_21/reports/batch_20260520T111233Z.csv` |
| Scoring P3 ciblé (7 fichiers) | `reports/runs/v1_1_recal_7/reports/moa_scoring_p3_cible_7.csv` |

Contexte visuel `/shop` : [`RECETTE_MANUELLE_SHOP_UX3_B1_CREOLE_BACKGROUNDS.md`](../ux/RECETTE_MANUELLE_SHOP_UX3_B1_CREOLE_BACKGROUNDS.md)

---

## Garde-fous post-POC

| Règle | Détail |
|-------|--------|
| **Pas de code Odoo** | Aucune modification `dorevia_ckreyol_marketone` sans ticket dédié |
| **Pas de remplacement `image_1920`** | Originaux produit intacts · tuiles = fichiers dérivés |
| **`NEEDS_REVIEW` visible** | Toujours présents dans le rapport · pas de masquage auto |
| **Recette figée** | Utiliser `ck_shop_tile_v1.1` · toute évolution = nouvelle version YAML + arbitrage MOA |
| **Qualité source amont** | Le moteur n’impose pas une charte fournisseur — prévoir règles photo en amont |

---

## Suite post-POC

| Sujet | Statut | Ticket |
|-------|--------|--------|
| Pilote média catalogue (50 SKU) | **Clôturé MOA — GO avec réserves** | [`RECETTE_MANUELLE_CK_IMAGE_NORMALIZER_PILOTE_MEDIA.md`](./RECETTE_MANUELLE_CK_IMAGE_NORMALIZER_PILOTE_MEDIA.md) |
| V1.5 Odoo lite | Cadrage P6 · ticket séparé | — |

---

## Synthèse batch POC (référence)

| Statut | Nombre |
|--------|-------:|
| `OK` | 13 |
| `OK_WITH_WARNINGS` | 1 |
| `NEEDS_REVIEW` | 7 |
| `REJECTED` | 0 |

Rapport complet : [`RAPPORT_V1_1_BATCH_21_PROXY.md`](./RAPPORT_V1_1_BATCH_21_PROXY.md)

---

## Clôture POC

| Phase | Statut |
|-------|--------|
| P0 — Lot 21 refs | ✅ Validé MOA |
| P1 — Scaffold CLI | ✅ Validé MOA |
| P2 — Batch v1.1 | ✅ Validé MOA |
| P3 — Revue grille | ✅ GO POC avec réserves |
| **P4 — Document de clôture** | ✅ **Ce document** |

**Signal de clôture Dev** :

```text
POC CK Image Normalizer clôturé — recette candidate ck_shop_tile_v1.1 — GO avec réserves MOA
```

---

## Références

| Document | Rôle |
|----------|------|
| [`NOTE_CK_IMAGE_NORMALIZER_SHOP_V1.md`](../../cadrage/NOTE_CK_IMAGE_NORMALIZER_SHOP_V1.md) | Cadrage technique |
| [`REPONSE_MOA_GO_POC_IMAGE_NORMALIZER_V1_1.md`](./REPONSE_MOA_GO_POC_IMAGE_NORMALIZER_V1_1.md) | Décision MOA finale |
| [`RAPPORT_V1_1_BATCH_21_PROXY.md`](./RAPPORT_V1_1_BATCH_21_PROXY.md) | Synthèse batch 21 |
| [`RECETTE_P3_CIBLE_7_NEEDS_REVIEW.md`](./RECETTE_P3_CIBLE_7_NEEDS_REVIEW.md) | Revue ciblée 7 fichiers |
| [`tools/ck_image_normalizer/README.md`](../../../../tools/ck_image_normalizer/README.md) | README opérateur CLI |
