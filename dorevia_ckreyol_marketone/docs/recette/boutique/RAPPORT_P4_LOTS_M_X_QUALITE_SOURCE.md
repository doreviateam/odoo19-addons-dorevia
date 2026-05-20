# Rapport P4 — lots M et X — qualité source

| Champ | Valeur |
|-------|--------|
| **Date** | 2026-05-20 |
| **Run initial** | `tools/ck_image_normalizer/reports/runs/pilote_20260520/` |
| **Recette** | `ck_shop_tile_v1.1` |
| **Périmètre** | Qualité source post-P4 |
| **Garde-fous** | Aucun code Odoo · aucun remplacement `image_1920` · aucune industrialisation |

---

## 1. Lots produits

Deux fichiers de travail ont été produits dans le dossier du run :

```text
tools/ck_image_normalizer/reports/runs/pilote_20260520/lot_m_reprise_manuelle.csv
tools/ck_image_normalizer/reports/runs/pilote_20260520/lot_x_demande_fournisseur.csv
```

| Lot | Nombre | Décision |
|-----|-------:|----------|
| `M` | 7 | Reprise manuelle / recadrage local |
| `X` | 7 | Demande fournisseur ou exclusion |

---

## 2. Lot M — reprise manuelle

Les 7 images du lot M ont été copiées et préparées dans un dossier séparé :

```text
tools/ck_image_normalizer/input/pilote_lot_m_corrige/
```

Manifest dédié :

```text
tools/ck_image_normalizer/manifest.pilote_lot_m_corrige.csv
```

Planche de contrôle :

```text
tools/ck_image_normalizer/reports/runs/pilote_20260520/lot_m_corrige_contact_sheet.jpg
```

Les sources originales du pilote ne sont pas écrasées.

---

## 3. Lot X — demande fournisseur

Les 7 images du lot X ne sont pas traitées en reprise locale.

Raison :

- visuel générique sans produit principal identifiable ;
- image non alignée avec le SKU ;
- produit attendu absent ou ambigu ;
- source trop éloignée d’une tuile commerce.

Décision :

```text
Demande fournisseur ou exclusion du pilote.
```

---

## 4. Signal pour mini-batch ciblé

Signal transmis :

```text
GO mini-batch ciblé lot M corrigé
```

Commande exécutée (2026-05-20) :

```bash
cd tools/ck_image_normalizer
.venv/bin/python -m ck_image_normalizer run \
  --input input/pilote_lot_m_corrige \
  --manifest manifest.pilote_lot_m_corrige.csv \
  --recipe recipes/ck_shop_tile_v1.1.yaml \
  --output-dir reports/runs/pilote_20260520_lot_m_corrige
```

→ Rapport Dev : [`RAPPORT_MINI_BATCH_LOT_M_CORRIGE_20260520.md`](./RAPPORT_MINI_BATCH_LOT_M_CORRIGE_20260520.md)

---

## 5. Résultat mini-batch lot M

| Statut | Nombre |
|--------|-------:|
| `OK` | 5 |
| `REJECTED` | 2 |
| `NEEDS_REVIEW` | 0 |

Les **2 REJECTED** (pâtes + semoule manioc) partagent la **même source** — `content_area_ratio` 0,1013 · produit trop petit dans la frame. Reprise : **2 packshots dédiés** recadrés plus serrés.

Bilan pilote après validation des 5 OK :

```text
41 / 50 exploitable (82 %) · 9 / 50 hors flux (2 manioc + 7 lot X)
```

Addendum consolidé : les 2 SKU manioc ont ensuite reçu des sources distinctes et ont été réintégrés.

```text
43 / 50 exploitables (86 %) · 7 / 50 hors flux (lot X)
```

→ [`REPONSE_MOA_REINTEGRATION_2_MANIOC_SOURCES_DISTINCTES.md`](./REPONSE_MOA_REINTEGRATION_2_MANIOC_SOURCES_DISTINCTES.md)

---

## 6. Signal actuel

```text
Lot M clôturé — 5 OK réintégrés · 2 manioc réintégrés après sources distinctes — lot X inchangé (demande fournisseur/exclusion temporaire).
```
