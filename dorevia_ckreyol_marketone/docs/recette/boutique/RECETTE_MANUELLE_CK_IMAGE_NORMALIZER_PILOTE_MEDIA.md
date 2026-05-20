# Recette manuelle — CK Image Normalizer — Clôture pilote média P5 (CLI externe)

| Champ | Valeur |
|-------|--------|
| **Ticket** | [`TICKET_MARKETONE_CK_IMAGE_NORMALIZER_PILOTE_MEDIA`](../../tickets/boutique/TICKET_MARKETONE_CK_IMAGE_NORMALIZER_PILOTE_MEDIA.md) |
| **Ticket amont** | [`TICKET_MARKETONE_CK_IMAGE_NORMALIZER_POC`](../../tickets/boutique/TICKET_MARKETONE_CK_IMAGE_NORMALIZER_POC.md) — **clôturé GO avec réserves** |
| **ADR** | [ADR-033](../../cadrage/DECISIONS.md#adr-033--ck-image-normalizer-v1--poc-tuiles-commerce-shop) |
| **Outil** | `tools/ck_image_normalizer/` (hors module Odoo) |
| **Recette candidate** | `ck_shop_tile_v1.1` |
| **Lot pilote** | **50 SKU** — run `pilote_20260520` |
| **Run de référence** | `tools/ck_image_normalizer/reports/runs/pilote_20260520/` |
| **Statut pilote** | **Clôturé MOA** (2026-05-20) · **GO avec réserves confirmé** · **43/50 (86 %)** |

---

## Verdict MOA

```text
GO pilote avec réserves — recette ck_shop_tile_v1.1 utile — sas NEEDS_REVIEW indispensable — pas de GO exploitation automatique.
```

| Date | Verdict | Commentaire |
|------|---------|-------------|
| 2026-05-20 | **GO pilote avec réserves** | Moteur et flux CLI validés sous contrôle opérateur · **43/50 exploitables (86 %)** après revue + mini-batches · lot X hors flux · **pas de code Odoo** · **pas d’exploitation automatique** |

Décisions amont :

- [`REPONSE_MOA_GO_PILOTE_MEDIA.md`](./REPONSE_MOA_GO_PILOTE_MEDIA.md)
- [`REPONSE_MOA_GO_EXECUTION_PILOTE_MEDIA.md`](./REPONSE_MOA_GO_EXECUTION_PILOTE_MEDIA.md)
- [`RAPPORT_PILOTE_MEDIA_50SKU_20260520.md`](./RAPPORT_PILOTE_MEDIA_50SKU_20260520.md) — batch automatique
- [`RAPPORT_P4_PILOTE_MEDIA_50SKU_20260520.md`](./RAPPORT_P4_PILOTE_MEDIA_50SKU_20260520.md) — revue opérateur

---

## 1. Résultat consolidé du pilote

### 1.1 Résultat moteur seul (batch automatique)

| Statut moteur | Nombre | Taux |
|---------------|-------:|-----:|
| `OK` | 18 | 36 % |
| `OK_WITH_WARNINGS` | 3 | 6 % |
| `NEEDS_REVIEW` | 29 | 58 % |
| `REJECTED` | 0 | 0 % |

Synthèse automatique :

```text
OK + OK_WITH_WARNINGS : 21 / 50 = 42 %
REJECTED              : 0 / 50 = 0 %
NEEDS_REVIEW          : 29 / 50 = 58 %
```

Lecture : le moteur **ne rejette aucune image** ; le taux `NEEDS_REVIEW` est **élevé** et impose un sas opérateur systématique sur ce lot.

### 1.2 Résultat après revue opérateur (P4)

Revue des **29** lignes `NEEDS_REVIEW` dans `pilote_operateur.csv` :

| Décision MOA | Sens | Nombre |
|--------------|------|-------:|
| `E` | Exploitable tel quel | 3 |
| `R` | Exploitable avec réserve | 12 |
| `M` | Reprise manuelle nécessaire | 7 |
| `X` | Source à redemander / exclure | 7 |

Temps opérateur mesuré :

```text
NEEDS_REVIEW revus     : 29 / 29
Temps moyen de revue   : ~0,88 min / image
Temps total de revue   : ~26 min (25,6 min mesurés)
```

### 1.3 Bilan cumulé exploitable — final

| Catégorie | Nombre | Décision MOA |
|-----------|-------:|:---:|
| `OK` moteur | 18 | ✅ |
| `OK_WITH_WARNINGS` moteur | 3 | ✅ |
| `NEEDS_REVIEW` validés `E` (P4) | 3 | ✅ |
| `NEEDS_REVIEW` validés `R` (P4) | 12 | ✅ |
| Lot M mini-batch validés MOA (5 OK) | 5 | ✅ |
| Manioc — Pâtes de manioc Mayotte (`OK` visuel) | 1 | ✅ |
| Manioc — Semoule manioc fine (`NEEDS_REVIEW` → R) | 1 | ✅ |
| **Total exploitable / avec réserve** | **43 / 50** | |
| Lot X — demande fournisseur / exclusion temporaire | 7 | ⏳ |
| **Total hors flux** | **7 / 50** | |

Taux consolidés (bilan définitif pilote) :

```text
Exploitable après revue + mini-batches : 43 / 50 = 86 %
Hors flux (lot X)                      : 7 / 50 = 14 %
REJECTED définitif                     : 0 / 50 = 0 %
```

Signaux MOA reçus :

- [`REPONSE_MOA_REINTEGRATION_5_LOT_M_CORRIGE.md`](./REPONSE_MOA_REINTEGRATION_5_LOT_M_CORRIGE.md) — 41/50
- [`REPONSE_MOA_REINTEGRATION_2_MANIOC_SOURCES_DISTINCTES.md`](./REPONSE_MOA_REINTEGRATION_2_MANIOC_SOURCES_DISTINCTES.md) — **43/50 définitif**

### 1.4 Lecture par type de source

| Profil | OK + WARN auto | NEEDS_REVIEW |
|--------|---------------:|-------------:|
| `packshot` | 9 / 38 (24 %) | 29 / 38 |
| `lifestyle` | 12 / 12 (100 %) | 0 / 12 |

| Origine lot | OK + WARN auto | NEEDS_REVIEW |
|-------------|---------------:|-------------:|
| Noyau historique 27 | 6 / 27 | 21 / 27 |
| Extension catalogue 23 | 15 / 23 | 8 / 23 |

Lecture MOA validée :

- le moteur `ck_shop_tile_v1.1` est **utile** ;
- le sas `NEEDS_REVIEW` est **indispensable** ;
- le flux opérateur est **viable à l’échelle pilote** ;
- le blocage principal vient surtout des **sources images hétérogènes ou incohérentes** ;
- la charge de revue se concentre sur les **packshots plein cadre** et les **visuels BO hétérogènes** du noyau historique ;
- la **reprise source ciblée** (lot M + mini-batch manioc) permet de récupérer **7 images supplémentaires**, portant le bilan définitif à **86 %** ;
- la règle catalogue **un SKU = une source distincte** est actée : [`REGLE_CATALOGUE_IMAGES_SOURCE.md`](../../cadrage/REGLE_CATALOGUE_IMAGES_SOURCE.md).

---

## 2. Verdict MOA — GO avec réserves

```text
GO avec réserves.
```

Ce GO **valide** :

- l’**intérêt du moteur** `ck_shop_tile_v1.1` pour homogénéiser les tuiles commerce `/shop` ;
- la **viabilité du flux CLI externe** sous contrôle opérateur ;
- la **conservation de la recette** comme candidate de référence ;
- l’**exploitation manuelle contrôlée** des tuiles validées (E/R + OK/WARN contrôlés).

Ce GO **ne valide pas** :

- une **exploitation automatique** sans revue des `NEEDS_REVIEW` ;
- une **intégration Odoo** (V1.5 ou autre) ;
- un **traitement massif catalogue** ;
- une **modification de recette** tant que les problèmes source ne sont pas séparés des limites moteur.

---

## 3. Réserves principales

| # | Réserve | Détail |
|---|---------|--------|
| **R1** | Taux `NEEDS_REVIEW` élevé | **29 / 50 (58 %)** — flux non automatisable tel quel |
| **R2** | Reprises manuelles | **7 images `M`** — recadrage source ou reprise visuelle avant mini-batch |
| **R3** | Sources à remplacer | **7 images `X`** — incohérence SKU/visuel ou visuel générique non publiable |
| **R4** | Charge packshot | Problème concentré sur packshots plein cadre et visuels BO hétérogènes |
| **R5** | Charte source fournisseur | Nécessaire en amont pour réduire les cas `X` et stabiliser le taux auto |
| **R6** | Source vs moteur | Distinguer explicitement les échecs liés aux **sources** des limites du **moteur** avant toute évolution recette |

Conséquence opérationnelle :

```text
La recette ck_shop_tile_v1.1 ne doit pas être déployée en publication automatique.
Le sas NEEDS_REVIEW reste obligatoire sur tout lot comparable.
```

---

## 4. Lots opérationnels MOA

Deux lots de suite sont formalisés à partir de `pilote_operateur.csv`.

Fichiers opérationnels :

| Lot | Fichier | Action attendue |
|-----|---------|-----------------|
| **Lot M** | [`lot_m_reprise_manuelle.csv`](../../../../tools/ck_image_normalizer/reports/runs/pilote_20260520/lot_m_reprise_manuelle.csv) | Reprise manuelle / recadrage source → mini-batch ciblé post-correction |
| **Lot X** | [`lot_x_demande_fournisseur.csv`](../../../../tools/ck_image_normalizer/reports/runs/pilote_20260520/lot_x_demande_fournisseur.csv) | Redemande fournisseur ou exclusion du flux |

### 4.1 Lot M — reprise manuelle (7 images)

| Fichier | Référence | Motif MOA |
|---------|-----------|-----------|
| `03_product-9_pates-de-manioc-mayotte.png` | Pâtes de manioc Mayotte | Détourage / zone vide visible sur sachet plein cadre |
| `07_product-156_biscuits-coco-vanille.jpg` | Biscuits coco vanille | Produit trop cadré sur un bord · poids visuel déséquilibré |
| `10_product-159_rougail-epices-reunion.jpg` | Rougail épices Réunion | Visuel ingrédient/recette · SKU peu identifiable |
| `11_product-160_chutney-mangue-verte.jpg` | Chutney mangue verte | Groupe de pots sans identification nette du SKU |
| `19_product-180_tartinade-coco-citron-vert.png` | Tartinade coco citron vert | Scène éditoriale · SKU insuffisamment identifiable |
| `23_product-184_semoule-manioc-fine-mayotte.png` | Semoule manioc fine Mayotte | Détourage / zone vide visible (même défaut que pâtes manioc) |
| `27_product-188_coffret-biscuits-et-douceurs.jpg` | Coffret biscuits et douceurs | Produit trop latéralisé / coupé |

**Procédure Lot M** :

1. MOA reprend manuellement la source (recadrage, détourage propre, packshot dédié si possible).
2. Déposer la source corrigée dans `input/pilote/` (nouveau nom ou remplacement tracé).
3. Demander à Dev un **mini-batch ciblé** sur les 7 fichiers corrigés uniquement.
4. Repasser la revue E/R/M/X sur les sorties `NEEDS_REVIEW` éventuelles.

### 4.2 Lot X — demande fournisseur / exclusion (7 images)

| Fichier | Référence | Motif MOA |
|---------|-----------|-----------|
| `08_product-157_sirop-de-canne-vanille.jpg` | Sirop de canne vanille | Rayon de bouteilles générique · SKU non identifiable |
| `12_product-161_cafe-arabica-antilles.png` | Café arabica Antilles | Étagère générique · aucun produit principal identifiable |
| `13_product-162_infusion-vetiver-citronnelle.jpg` | Infusion vétiver citronnelle | Portrait / lifestyle non produit |
| `21_product-182_confiture-ananas-vanille.png` | Confiture ananas vanille | Visuel plage / bouteilles générique |
| `45_ck-mo-045_sirop-banane-flambee.jpg` | Sirop banane flambée | Visuel miel incohérent avec le SKU sirop |
| `48_ck-mo-048_farine-banane-plantain.png` | Farine banane plantain | Image pâtes/sachet manioc incohérente |
| `49_ck-mo-049_flocons-manioc-instantanes.png` | Flocons manioc instantanés | Image pâtes/sachet manioc incohérente |

**Procédure Lot X** :

1. **Exclure** ces visuels du flux tuile `/shop` tant qu’aucune source conforme n’est disponible.
2. **Redemander** au fournisseur un packshot ou lifestyle **SKU-identifiable** par référence.
3. Alimenter une **charte source fournisseur** (voir § 6) avant réintégration.
4. Ne **pas** tenter de corriger ces cas par évolution de recette seule.

---

## 5. Garde-fous — interdictions maintenues

Les garde-fous du POC et du pilote restent **fermement actifs** après clôture P5 :

| Règle | Statut |
|-------|--------|
| **Pas de code Odoo** | ❌ Aucune modification `dorevia_ckreyol_marketone` |
| **Pas de champ `image_shop_tile`** | ❌ Cadrage futur uniquement |
| **Pas d’héritage QWeb** | ❌ Pas de branchement tuile normalisée en production |
| **Pas de remplacement `image_1920`** | ❌ Originaux produit intacts |
| **Pas de cron** | ❌ Aucune tâche planifiée |
| **Pas de traitement massif automatique** | ❌ Sans nouveau GO MOA explicite |
| **Pas de BO complet** | ❌ Pas d’écran Odoo dédié normalizer |
| **Pas d’exploitation sans revue `NEEDS_REVIEW`** | ❌ Sas opérateur obligatoire |

Périmètre image inchangé :

```text
Tuiles commerce /shop uniquement — pas hero, fiche, culture, blog.
```

Recette :

```text
Utiliser ck_shop_tile_v1.1 — toute évolution = nouvelle version YAML + arbitrage MOA.
Ne pas modifier la recette tant que source vs moteur n’est pas clarifié.
```

---

## 6. V1.5 Odoo lite — cadrage futur uniquement

La **V1.5 Odoo lite** peut être **évoquée** comme suite possible, **via ticket séparé**, **après** cette clôture P5.

Elle **n’est pas lancée** dans le cadre de ce document.

Le futur ticket V1.5 devra d’abord clarifier :

| Sujet | Question à trancher |
|-------|---------------------|
| Séparation source vs dérivé | Où stocker l’original · où stocker la tuile normalisée |
| Champ dédié | Éventuel `image_shop_tile` vs autre mécanisme |
| Fallback | Comportement si tuile absente · retour `image` standard |
| Périmètre usage | Limitation stricte aux tuiles `/shop` |
| Import | Conditions d’import des images validées (E/R + OK/WARN contrôlés) |
| Gouvernance | Règles de traitement et traçabilité des `NEEDS_REVIEW` |

**Phase ticket** : **P6 — cadrage V1.5** (MOA) — **sans code immédiat**.

---

## 7. Flux opérateur validé (rappel)

### Commande batch pilote

```bash
cd tools/ck_image_normalizer
python -m ck_image_normalizer run \
  --input input/pilote \
  --manifest manifest.pilote.csv \
  --recipe recipes/ck_shop_tile_v1.1.yaml \
  --output-dir reports/runs/pilote_YYYYMMDD
```

### Lecture des statuts

| Statut | Action opérateur |
|--------|------------------|
| `OK` | Exploitable après contrôle visuel |
| `OK_WITH_WARNINGS` | Exploitable avec réserve documentée |
| `NEEDS_REVIEW` | Revue obligatoire · décision E/R/M/X |
| `REJECTED` | Non utilisable sans reprise source |

Voir aussi : [`RECETTE_MANUELLE_CK_IMAGE_NORMALIZER_POC.md`](./RECETTE_MANUELLE_CK_IMAGE_NORMALIZER_POC.md) — grille G1–G6 et codes E/R/M/X.

---

## 8. Clôture pilote — phases P0 à P5

| Phase | Action | Statut |
|-------|--------|--------|
| **P0** | Validation cadrage pilote | ✅ Validé MOA (2026-05-20) |
| **P0-dev** | Préparation structure pilote | ✅ Livré (2026-05-20) |
| **P1** | Sélection 50 SKU + export images | ✅ Livré (2026-05-20) |
| **P2** | `manifest.pilote.csv` + `input/pilote/` | ✅ Livré — 50/50 |
| **P3** | Exécution batch v1.1 — run `pilote_20260520` | ✅ Livré (2026-05-20) |
| **P4** | Revue 29 `NEEDS_REVIEW` — E/R/M/X | ✅ Clôturé MOA (2026-05-20) |
| **P5** | Document de clôture + verdict officiel | ✅ **Ce document** |
| **P6** | Cadrage V1.5 Odoo lite | ✅ **Validé MOA** · [`TICKET_V1_5_CADRAGE`](../../tickets/boutique/TICKET_MARKETONE_CK_IMAGE_NORMALIZER_V1_5_CADRAGE.md) |
| **P7** | Implémentation V1.5 lite | 🔄 **Ouvert** · [`TICKET_V1_5_IMPLEMENTATION`](../../tickets/boutique/TICKET_MARKETONE_CK_IMAGE_NORMALIZER_V1_5_IMPLEMENTATION.md) |

---

## Décision finale

```text
Pilote média CK Image Normalizer clôturé
GO avec réserves confirmé
43 / 50 exploitables (86 %)
Recette candidate : ck_shop_tile_v1.1
Lot X maintenu en demande fournisseur / exclusion (7 / 50)
P6 V1.5 Odoo lite en attente décision MOA
```

Décision MOA consignée : [`REPONSE_MOA_CLOTURE_PILOTE_MEDIA_CATALOGUE.md`](./REPONSE_MOA_CLOTURE_PILOTE_MEDIA_CATALOGUE.md)

**Signal Dev** :

```text
Pilote média clôturé — GO avec réserves confirmé — 43/50 exploitables — aucune suite Dev sans signal MOA explicite.
```

---

## Références

| Document | Rôle |
|----------|------|
| [`TICKET_MARKETONE_CK_IMAGE_NORMALIZER_PILOTE_MEDIA.md`](../../tickets/boutique/TICKET_MARKETONE_CK_IMAGE_NORMALIZER_PILOTE_MEDIA.md) | Ticket pilote |
| [`TICKET_MARKETONE_CK_IMAGE_NORMALIZER_V1_5_CADRAGE.md`](../../tickets/boutique/TICKET_MARKETONE_CK_IMAGE_NORMALIZER_V1_5_CADRAGE.md) | P6 cadrage — validé MOA |
| [`TICKET_MARKETONE_CK_IMAGE_NORMALIZER_V1_5_IMPLEMENTATION.md`](../../tickets/boutique/TICKET_MARKETONE_CK_IMAGE_NORMALIZER_V1_5_IMPLEMENTATION.md) | **P7 implémentation** — ouvert |
| [`RECETTE_MANUELLE_CK_IMAGE_NORMALIZER_POC.md`](./RECETTE_MANUELLE_CK_IMAGE_NORMALIZER_POC.md) | Clôture POC · flux opérateur |
| [`RAPPORT_PILOTE_MEDIA_50SKU_20260520.md`](./RAPPORT_PILOTE_MEDIA_50SKU_20260520.md) | Batch automatique 50 SKU |
| [`RAPPORT_P4_PILOTE_MEDIA_50SKU_20260520.md`](./RAPPORT_P4_PILOTE_MEDIA_50SKU_20260520.md) | Revue opérateur P4 |
| [`RAPPORT_P4_LOTS_M_X_QUALITE_SOURCE.md`](./RAPPORT_P4_LOTS_M_X_QUALITE_SOURCE.md) | Lots M/X qualité source |
| [`RAPPORT_MINI_BATCH_LOT_M_CORRIGE_20260520.md`](./RAPPORT_MINI_BATCH_LOT_M_CORRIGE_20260520.md) | Mini-batch lot M · **bilan final 41/50** |
| [`REPONSE_MOA_REINTEGRATION_5_LOT_M_CORRIGE.md`](./REPONSE_MOA_REINTEGRATION_5_LOT_M_CORRIGE.md) | Validation visuelle MOA · 5 lot M → 41/50 |
| [`REPONSE_MOA_CLOTURE_PILOTE_MEDIA_CATALOGUE.md`](./REPONSE_MOA_CLOTURE_PILOTE_MEDIA_CATALOGUE.md) | **Clôture définitive MOA** — GO confirmé · 43/50 |
| [`REGLE_CATALOGUE_IMAGES_SOURCE.md`](../../cadrage/REGLE_CATALOGUE_IMAGES_SOURCE.md) | Règle catalogue source — actée MOA |
| [`NOTE_CK_IMAGE_NORMALIZER_SHOP_V1.md`](../../cadrage/NOTE_CK_IMAGE_NORMALIZER_SHOP_V1.md) | Cadrage technique initial |
| [`tools/ck_image_normalizer/README.md`](../../../../tools/ck_image_normalizer/README.md) | README CLI opérateur |
| `tools/ck_image_normalizer/reports/runs/pilote_20260520/pilote_operateur.csv` | Suivi opérateur complet |
| `tools/ck_image_normalizer/reports/runs/pilote_20260520/lot_m_reprise_manuelle.csv` | Lot M — 7 reprises |
| `tools/ck_image_normalizer/reports/runs/pilote_20260520/lot_manioc_redemande_source.csv` | 2 manioc — redemande source distincte |
| `tools/ck_image_normalizer/reports/runs/pilote_20260520/lot_x_arbitrage_moa.csv` | Lot X arbitré — exclusion temporaire |
| `tools/ck_image_normalizer/reports/runs/pilote_20260520/lot_x_demande_fournisseur.csv` | Lot X — 7 demandes fournisseur |
