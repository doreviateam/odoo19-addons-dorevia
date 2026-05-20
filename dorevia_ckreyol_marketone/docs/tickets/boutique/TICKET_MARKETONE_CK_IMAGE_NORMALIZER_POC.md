# TICKET — CK Image Normalizer V1 — POC CLI externe (tuiles commerce `/shop`)

| Champ | Valeur |
|-------|--------|
| **ID** | `TICKET_MARKETONE_CK_IMAGE_NORMALIZER_POC` |
| **Univers** | **Boutique** — qualité catalogue `/shop` |
| **Type** | **POC externe** — CLI batch, hors module Odoo |
| **Statut** | **Clôturé — GO POC avec réserves MOA** (2026-05-20) |
| **Emplacement POC** | `tools/ck_image_normalizer/` (hors module Odoo) |
| **Module Odoo** | **Aucun changement** dans `dorevia_ckreyol_marketone` |
| **Cadrage** | [`NOTE_CK_IMAGE_NORMALIZER_SHOP_V1.md`](../../cadrage/NOTE_CK_IMAGE_NORMALIZER_SHOP_V1.md) |
| **ADR** | **ADR-033** |
| **Effort indicatif** | **3–5 j/h dev** (phase A) + **2–4 j/h** calibrage MOA |

---

## Objectif

Prouver, sur un **échantillon réel de 21 références produit**, qu’un moteur de normalisation **déterministe** (sans IA) peut produire des tuiles commerce homogènes pour la grille `/shop` :

- carré **1024 × 1024 px** ;
- fond **`#F8EEDB` baked-in** (à valider visuellement MOA) ;
- produit centré, poids visuel homogène ;
- export **WebP** + **JPEG** fallback ;
- **original conservé** ;
- **rapport de traitement** par image.

Ce ticket **n’intègre pas Odoo**. L’intégration lite (V1.5) est un ticket ultérieur, conditionné au GO recette MOA.

---

## Décisions MOA figées (2026-05-20)

| # | Décision |
|---|----------|
| **D1** | **GO POC** — pas d’implémentation Odoo en V1 |
| **D2** | Périmètre strict : **tuiles commerce `/shop` uniquement** |
| **D3** | Séquence : POC CLI → recette MOA → pilote catalogue → V1.5 Odoo lite **seulement après validation recette** |
| **D4** | Fond **`#F8EEDB` baked-in** — **validé MOA** (revue grille 2026-05-20) |
| **D5** | **Ne jamais remplacer `image_1920`** — originaux conservés ; V1 = fichiers dérivés + rapport |
| **D6** | Échantillon **21 références** — lot officiel **validé MOA** (2026-05-20) |
| **D7** | Recette candidate **`ck_shop_tile_v1.1`** (dérivée de `ck_shop_tile_v1`) |
| **D8** | Pas de détourage complexe, pas d’IA générative, pas de BO Odoo |
| **D9** | **GO POC avec réserves** — pas d’intégration Odoo immédiate · reprises manuelles sur cas signalés |

---

## Hors périmètre (interdit)

| Élément | Statut |
|---------|--------|
| Module Odoo / champ `image_shop_tile` | ❌ Ticket ultérieur V1.5 |
| Remplacement `product.template.image_1920` | ❌ Interdit |
| Hero, fiche produit, culture, recettes, blog | ❌ Hors V1 |
| `rembg` / segmentation / IA | ❌ Interdit |
| BO preview / cron massif Odoo | ❌ Interdit |

---

## Recette V1 retenue — `ck_shop_tile_v1`

Fichier normatif à versionner dans le dépôt POC :

```yaml
recipe_id: ck_shop_tile_v1
canvas_size: 1024
ratio: "1:1"
width: 1024
height: 1024
background: "#F8EEDB"
color_space: "sRGB"

content_fill_ratio: 0.78
min_padding_px: 64
max_padding_px: 128

trim_uniform_border: true
white_background_replace: true      # profil packshot uniquement
white_threshold: 245

profiles:
  packshot:
    white_background_replace: true
    content_fill_ratio: 0.78
  lifestyle:
    white_background_replace: false
    content_fill_ratio: 0.72

output:
  webp: { quality: 85 }
  jpeg: { quality: 90 }

reject_if:
  - content_area_ratio < 0.15
  - content_area_ratio > 0.95
  - background_entropy > 0.42

statuses:
  - OK
  - OK_WITH_WARNINGS
  - NEEDS_REVIEW
  - REJECTED
```

---

## Échantillon MOA — 21 références

L’échantillon = **21 images catalogue disponibles** (banque `marketplace/docs/assets`). Pas d’extension à 30 refs MOA.

| # | Type source | Quantité cible | Objectif test |
|---|-------------|----------------|---------------|
| E1 | Packshots fond clair | 4 | ROI principal |
| E2 | Packshots mal cadrés | 2 | Trim + centrage |
| E4–E7 | Sachets, bocaux, bouteilles, coffrets | 5 | Formes variées |
| E8 | Lifestyle simples | 4 | Profil lifestyle conservateur |
| E9 | Cas difficiles / hero | 6 | `NEEDS_REVIEW` attendus |

**Livrable MOA** : **21 fichiers** + `manifest.csv` — voir `manifest.moa.template.csv`.

---

## Livrables Dev

| # | Livrable | Critère d’acceptation |
|---|----------|----------------------|
| L1 | **CLI batch** Python 3 + Pillow | Traite un dossier `input/` → `output/webp/`, `output/jpeg/`, `archive/orig/`, `reports/` |
| L2 | **Recette `ck_shop_tile_v1.yaml`** | Paramètres conformes § Recette ; versionnée dans le repo POC |
| L3 | **Profils `packshot` / `lifestyle`** | Sélection manuelle par fichier (CSV manifest) ou heuristique documentée |
| L4 | **Rapport JSON + CSV** | Par image : statut, métriques (`content_area_ratio`, `background_entropy`, padding, profil), warnings |
| L5 | **Vignettes comparatif** | Avant / après par image (HTML ou dossier `reports/previews/`) |
| L6 | **Grille MOA** | **21 tuiles** en mock HTML grille 4 colonnes sur fond UX-3 B1 |
| L7 | **Doc opérateur** | README : installation, commande, lecture rapport, cas `NEEDS_REVIEW` |
| L8 | **Recette manuelle MOA** | `docs/recette/boutique/RECETTE_MANUELLE_CK_IMAGE_NORMALIZER_POC.md` — créée au GO technique |

### Structure de sortie attendue

```text
ck_image_normalizer_poc/
├── recipes/ck_shop_tile_v1.yaml
├── input/                    # originaux MOA (non versionnés si lourds)
├── output/webp/
├── output/jpeg/
├── archive/orig/             # copie horodatée
├── reports/
│   ├── batch_YYYYMMDD.json
│   ├── batch_YYYYMMDD.csv
│   └── previews/             # comparatifs avant/après
└── README.md
```

**Emplacement repo** : à arbitrer Dev — hors `dorevia_ckreyol_marketone` (outil externe) ou sous `tools/ck_image_normalizer/` à la racine monorepo. **Pas de dépendance Odoo.**

---

## Grille de notation MOA (recette visuelle)

Pour chaque tuile normalisée, noter **1–5** :

| Critère | Question |
|---------|----------|
| **G1 — Lisibilité** | Produit identifiable en ~320 px (taille tuile mobile) ? |
| **G2 — Chaleur / premium CK** | Cohérent avec ligne UX-3 B1 (`#F8EEDB`, sobre, chaleureux) ? |
| **G3 — Cohérence grille** | Poids visuel comparable aux autres tuiles du batch ? |
| **G4 — Absence effet IA** | Pas de halo agressif, pas de détourage visible, pas de « sale » ? |
| **G5 — Texture produit** | Épices, étiquettes, matière préservées ? |
| **G6 — Couture image/carte** | Fond baked-in améliore-t-il la transition vers `#FDF9F0` ? |

---

## Critères GO / NO-GO POC

### GO recette MOA si

| Critère | Seuil |
|---------|-------|
| Statut `OK` sans retouche | **≥ 60 %** du batch (≥ **13 / 21**) |
| Statut `REJECTED` | **≤ 10 %** (≤ **2 / 21**) |
| Gain visuel grille | MOA valide net sur desktop 4 col. **et** mobile 2 col. |
| Fond baked-in `#F8EEDB` | MOA valide ou tranche variante (ex. fill ratio ± 0.04) |
| Recette stable | Rejeu identique sur 5 images témoin |

### NO-GO / itération si

- `OK` < 50 % sans plan de reprise photo fournisseurs ;
- ≥ 30 % `REJECTED` sur packshots fond blanc (échec algo, pas sources) ;
- Dégradation texture systématique (épices, sachets) ;
- Fond baked-in rejeté MOA **et** aucune variante acceptable en 2 itérations.

### Sortie POC

| Résultat | Suite |
|----------|-------|
| **GO MOA recette** | Ticket pilote 50–100 SKU + ticket V1.5 Odoo lite (cadrage) |
| **GO avec réserves** | **Retenu MOA 2026-05-20** — recette `ck_shop_tile_v1.1` candidate · reprises manuelles `NEEDS_REVIEW` · ticket pilote média limité · **pas de code Odoo immédiat** |
| **NO GO** | Clôture ou pivot (ex. budget reprise photo, pas moteur auto) |

---

## Plan d’exécution

| Phase | Action | Responsable |
|-------|--------|-------------|
| **P0** | MOA fournit liste 21 références + fichiers source | MOA |
| **P1** | Scaffold CLI + recette YAML + traitement 5 images témoin | Dev |
| **P2** | Revue Dev intermédiaire (métriques + 5 previews) | Dev |
| **P2** | Batch **21 refs** MOA en `v1.1` + rapport | Dev |
| **P4** | Injection manuelle tuiles en BO recette **ou** mock grille HTML | Dev + MOA |
| **P5** | Session recette MOA (grille G1–G6) | MOA |
| **P6** | Rédaction `RECETTE_MANUELLE_CK_IMAGE_NORMALIZER_POC.md` + clôture | Dev |

**Estimation** : P1–P3 ≈ **3–5 j/h dev** · P4–P6 ≈ **2–4 j/h** (dont MOA).

---

## Risques POC

| Risque | Mitigation |
|--------|------------|
| Échantillon trop « facile » | Respecter matrice § Échantillon |
| Fond baked-in rejeté MOA | Tester aussi variante CSS-only en parallèle (rapport comparatif) |
| Cas lifestyle sur-promis | Profil lifestyle conservateur ; `NEEDS_REVIEW` explicite |
| Tentation scope creep Odoo | Ce ticket = **0 ligne** dans `dorevia_ckreyol_marketone` |

---

## Décision de sortie (MOA)

```text
[x] GO POC — ouvrir exécution CLI externe
[x] GO POC avec réserves
[ ] NO GO
```

**Date** : 2026-05-20 · **Validé par** : MOA

**Signal MOA acté** :

```text
GO POC avec réserves — lot officiel 21 refs validé — recette candidate ck_shop_tile_v1.1
```

→ [`REPONSE_MOA_GO_POC_IMAGE_NORMALIZER_V1_1.md`](../../recette/boutique/REPONSE_MOA_GO_POC_IMAGE_NORMALIZER_V1_1.md) · [`RAPPORT_V1_1_BATCH_21_PROXY.md`](../../recette/boutique/RAPPORT_V1_1_BATCH_21_PROXY.md)

**Réserves MOA** : reprise manuelle `homepage_manioc_pates_mayotte_la_platine`, `stitch_guava_jam_jar` · lifestyle moins homogènes que packshots · `NEEDS_REVIEW` = sas opérateur.

**Confirmation explicite (2026-05-20)** : GO POC CLI externe · **21 refs MOA validées** · recette candidate **`ck_shop_tile_v1.1`** · **aucun code Odoo** avant ticket d’intégration dédié.

**P1 validé MOA (2026-05-20)** : scaffold CLI accepté comme base de travail · validation fixtures cohérente (cas simples OK, cas difficile rejeté) · passage **P0** constitution échantillon réel.

**Passage P0 confirmé MOA (2026-05-20)** :

- scaffold CLI opérationnel ;
- recette `ck_shop_tile_v1` en place ;
- fixtures Dev validées ;
- sorties WebP/JPEG, archive, rapports et previews disponibles ;
- aucun code Odoo ;
- `dorevia_ckreyol_marketone` inchangé.

**P2-proxy legacy — prise d’acte MOA (2026-05-20)** :

```text
Total        : 21 images (banque marketplace/docs/assets)
OK           : 13
OK_WARNINGS  : 1
REJECTED     : 7
OK rate      : 67 %   (seuil ≥ 60 % ✅)
Rejected rate: 33 %   (seuil ≤ 10 % ❌)
GO candidate : non
```

**Décision MOA P2-proxy** : **GO technique partiel — calibrage recette requis** · pas de GO POC final sur ce batch · batch d’apprentissage.

**Calibrage v1.1 accepté MOA (2026-05-20)** · **P3 ciblé clôturé** — décision 2 · **batch 21 v1.1 livré** · **revue grille MOA** → **GO POC avec réserves**.

→ [`RECETTE_P3_CIBLE_7_NEEDS_REVIEW.md`](../../recette/boutique/RECETTE_P3_CIBLE_7_NEEDS_REVIEW.md) · [`RAPPORT_V1_1_BATCH_21_PROXY.md`](../../recette/boutique/RAPPORT_V1_1_BATCH_21_PROXY.md) · [`REPONSE_MOA_GO_POC_IMAGE_NORMALIZER_V1_1.md`](../../recette/boutique/REPONSE_MOA_GO_POC_IMAGE_NORMALIZER_V1_1.md)

**Livrable P0 MOA** : lot **21 refs validé** (banque assets) — signal acté via GO POC avec réserves.

---

## Journal d'exécution

| Phase | Statut | Date | Notes |
|-------|--------|------|-------|
| **P0** — Validation **21 refs** MOA | ✅ **Validé MOA** | 2026-05-20 | Lot officiel acté · banque assets |
| **P1** — Scaffold CLI + 5 témoins Dev | ✅ **Validé MOA** | 2026-05-20 | Fixtures Dev : **4/5 OK**, 1 REJECTED (attendu) |
| **P2-proxy** — Batch legacy marketplace (21 PNG) | ✅ Livré · **GO technique partiel MOA** | 2026-05-20 | 67 % OK · 33 % REJECTED · calibrage recette requis |
| **P2-proxy-analyse** — 7 REJECTED | ✅ Livré Dev | 2026-05-20 | [`ANALYSE_REJETS_P2_PROXY_CK_IMAGE_NORMALIZER.md`](../../recette/boutique/ANALYSE_REJETS_P2_PROXY_CK_IMAGE_NORMALIZER.md) |
| **P2-v1.1** — Calibrage + batch ciblé 7 | ✅ **Accepté MOA** | 2026-05-20 | Base revue v1.1 · [`RAPPORT_V1_1_RECALIBRATION_7FICHIERS.md`](../../recette/boutique/RAPPORT_V1_1_RECALIBRATION_7FICHIERS.md) |
| **P2** — Batch **21 refs** MOA (`v1.1`) | ✅ **Validé MOA** | 2026-05-20 | 14/21 OK+WARN · 0 REJECTED · [`RAPPORT_V1_1_BATCH_21_PROXY.md`](../../recette/boutique/RAPPORT_V1_1_BATCH_21_PROXY.md) |
| **P3-ciblé** — Revue 7 `NEEDS_REVIEW` | ✅ **Clôturé MOA** | 2026-05-20 | E:1 · R:4 · M:2 · X:0 · décision **2** |
| **P2-proxy-v1.1** — Batch 21 images | ✅ **Livré** | 2026-05-20 | 67 % OK · 0 % REJECTED · GO candidate auto **oui** · [`RAPPORT_V1_1_BATCH_21_PROXY.md`](../../recette/boutique/RAPPORT_V1_1_BATCH_21_PROXY.md) |
| **P3** — Revue grille 21 v1.1 complète | ✅ **GO POC avec réserves MOA** | 2026-05-20 | [`REPONSE_MOA_GO_POC_IMAGE_NORMALIZER_V1_1.md`](../../recette/boutique/REPONSE_MOA_GO_POC_IMAGE_NORMALIZER_V1_1.md) |
| **P4** — Clôture POC | ✅ **Livré Dev** | 2026-05-20 | [`RECETTE_MANUELLE_CK_IMAGE_NORMALIZER_POC.md`](../../recette/boutique/RECETTE_MANUELLE_CK_IMAGE_NORMALIZER_POC.md) |

### Livrables P1 (Dev)

| # | Livrable | Statut |
|---|----------|--------|
| L1 | CLI batch Python | ✅ `python -m ck_image_normalizer run` |
| L2 | Recette `recipes/ck_shop_tile_v1.yaml` | ✅ |
| L3 | Profils packshot / lifestyle + manifest CSV | ✅ |
| L4 | Rapport JSON + CSV | ✅ |
| L5 | Previews avant / après | ✅ `reports/previews/` |
| L6 | Fixtures Dev (5 témoins) | ✅ `python -m ck_image_normalizer fixtures` |
| L7 | README opérateur | ✅ `tools/ck_image_normalizer/README.md` |
| L8 | Recette manuelle MOA | ✅ [`RECETTE_MANUELLE_CK_IMAGE_NORMALIZER_POC.md`](../../recette/boutique/RECETTE_MANUELLE_CK_IMAGE_NORMALIZER_POC.md) |

**Emplacement POC** : [`tools/ck_image_normalizer/`](../../../../tools/ck_image_normalizer/) (racine monorepo, hors module Odoo).

---

## Prochaines étapes

| Qui | Action | Phase |
|-----|--------|-------|
| **MOA** | Valider cadrage pilote · sélection SKU | [`TICKET_MARKETONE_CK_IMAGE_NORMALIZER_PILOTE_MEDIA.md`](./TICKET_MARKETONE_CK_IMAGE_NORMALIZER_PILOTE_MEDIA.md) |
| **MOA / Dev** | V1.5 Odoo lite — **après pilote** · cadrage séparé | Post-pilote |

**POC clôturé** — voir [`RECETTE_MANUELLE_CK_IMAGE_NORMALIZER_POC.md`](../../recette/boutique/RECETTE_MANUELLE_CK_IMAGE_NORMALIZER_POC.md).

**Pas de code Odoo** — garde-fou maintenu post-GO POC avec réserves.

---

## Références

| Document | Rôle |
|----------|------|
| [`NOTE_CK_IMAGE_NORMALIZER_SHOP_V1.md`](../../cadrage/NOTE_CK_IMAGE_NORMALIZER_SHOP_V1.md) | Avis technique Dev |
| [`cadrage/DECISIONS.md`](../../cadrage/DECISIONS.md) — ADR-033 | Arbitrages MOA |
| [`RECETTE_MANUELLE_SHOP_UX3_B1_CREOLE_BACKGROUNDS.md`](../../recette/ux/RECETTE_MANUELLE_SHOP_UX3_B1_CREOLE_BACKGROUNDS.md) | Contexte visuel `/shop` |
| [`REPONSE_MOA_P2_PROXY_LEGACY_CK_IMAGE_NORMALIZER.md`](../../recette/boutique/REPONSE_MOA_P2_PROXY_LEGACY_CK_IMAGE_NORMALIZER.md) | Décision MOA — GO technique partiel |
| [`REPONSE_MOA_P3_CIBLE_7FICHIERS.md`](../../recette/boutique/REPONSE_MOA_P3_CIBLE_7FICHIERS.md) | v1.1 accepté · P3 ciblé |
| [`REPONSE_MOA_GO_POC_IMAGE_NORMALIZER_V1_1.md`](../../recette/boutique/REPONSE_MOA_GO_POC_IMAGE_NORMALIZER_V1_1.md) | **GO POC avec réserves** — décision finale MOA |
| [`RECETTE_MANUELLE_CK_IMAGE_NORMALIZER_POC.md`](../../recette/boutique/RECETTE_MANUELLE_CK_IMAGE_NORMALIZER_POC.md) | **Clôture POC** — flux opérateur |
| [`RAPPORT_V1_1_BATCH_21_PROXY.md`](../../recette/boutique/RAPPORT_V1_1_BATCH_21_PROXY.md) | Batch 21 v1.1 — synthèse + revue grille |
| [`RECETTE_P3_CIBLE_7_NEEDS_REVIEW.md`](../../recette/boutique/RECETTE_P3_CIBLE_7_NEEDS_REVIEW.md) | P3 ciblé — clôturé MOA |
| [`RAPPORT_P2_PROXY_LEGACY_CK_IMAGE_NORMALIZER.md`](../../recette/boutique/RAPPORT_P2_PROXY_LEGACY_CK_IMAGE_NORMALIZER.md) | Batch proxy 21 PNG — synthèse |
| [`TICKET_MARKETONE_CK_IMAGE_NORMALIZER_PILOTE_MEDIA.md`](./TICKET_MARKETONE_CK_IMAGE_NORMALIZER_PILOTE_MEDIA.md) | **Suite post-POC** — pilote média catalogue |
