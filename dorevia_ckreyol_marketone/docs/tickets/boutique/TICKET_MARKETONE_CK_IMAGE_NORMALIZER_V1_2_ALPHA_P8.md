# TICKET — CK Image Normalizer — V1.2-alpha hybride packshot (P8)

| Champ | Valeur |
|-------|--------|
| **ID** | `TICKET_MARKETONE_CK_IMAGE_NORMALIZER_V1_2_ALPHA_P8` |
| **Univers** | **Boutique** — tuiles commerce `/shop` |
| **Type** | **Évolution CLI ciblée** — alpha contrôlé sur vrais packshots |
| **Statut** | **Clôturé MOA — STOP v1.2-alpha** (2026-05-20) · piste alpha retirée du flux actif · doctrine **image pleine v1.1** |
| **Ticket amont POC** | [`RAPPORT_POC_V1_2_ALPHA_3_PACKSHOTS`](../../recette/boutique/RAPPORT_POC_V1_2_ALPHA_3_PACKSHOTS.md) |
| **Ticket amont P7** | [`TICKET_MARKETONE_CK_IMAGE_NORMALIZER_V1_5_IMPLEMENTATION`](./TICKET_MARKETONE_CK_IMAGE_NORMALIZER_V1_5_IMPLEMENTATION.md) |
| **Note doctrinale** | [`NOTE_CK_IMAGE_NORMALIZER_V1_2_TRANSPARENT_PROPOSAL`](../../cadrage/NOTE_CK_IMAGE_NORMALIZER_V1_2_TRANSPARENT_PROPOSAL.md) |
| **Recette candidate** | `tools/ck_image_normalizer/recipes/ck_shop_tile_v1.2-alpha.yaml` |
| **Module** | `dorevia_ckreyol_marketone` (aucun changement modèle attendu) |
| **Effort indicatif** | **4–5 j/h Dev** + **1–2 j/h MOA** audit |

---

## Doctrine MOA retenue (P8) — **historique, retirée 2026-05-20**

> **STOP MOA** : la voie alpha est abandonnée. Recette active : **`ck_shop_tile_v1.1` uniquement** (image pleine, sans transparence). Voir [`RAPPORT_RETRAIT_V12_ALPHA_EXECUTION.md`](../../recette/boutique/RAPPORT_RETRAIT_V12_ALPHA_EXECUTION.md).

```text
Packshot fond uni propre   → alpha possible (v1.2-alpha)   [RETIRÉ]
Lifestyle                  → image pleine v1.1
Pseudo-packshot douteux    → revue humaine · v1.1 par défaut · reprise source à terme
Fond conteneur tuile       → proche du blanc (#FDFCFA)
```

**Règle absolue** : l'alpha ne s'applique **jamais automatiquement** à toutes les images. Chaque packshot doit être audité.

---

## Objectif P8

Hybridation contrôlée :

- **conserver V1.5 Odoo lite** (champ `image_shop_tile`, flag, fallback)
- **conserver `ck_shop_tile_v1.1`** pour lifestyle
- **introduire `ck_shop_tile_v1.2-alpha`** pour vrais packshots fond uni
- **auditer** la classification packshot/lifestyle/douteux sur les 43 images pilote
- **re-exporter** uniquement les packshots audités éligibles
- **valider** le rendu hybride `/shop` en MOA

Pas de traitement massif. Pas de cron. Pas d'IA.

---

## Phases P8

| Phase | Action | Responsable | Statut |
|-------|--------|-------------|--------|
| **P8-1** | Pré-audit Dev des 43 sources → CSV proposition | Dev | ✅ 6 packshot_alpha · 3 needs_review · 34 lifestyle |
| **P8-1b** | **Validation MOA** du CSV d'audit | MOA | ✅ 9 packshots alpha validés (6 + 3) |
| **P8-2** | Intégrer `v1.2-alpha` dans CLI (`processor.py` + recipe) | Dev | ✅ |
| **P8-3** | Re-export packshots audités éligibles → `output/png/` | Dev | ✅ 9/9 |
| **P8-4** | Import comparatif `/shop` hybride v1.1 + v1.2-alpha | Dev | ✅ 9 alpha + 34 v1.1 |
| **P8-5** | Revue MOA finale | MOA | ✅ GO avec réserves gouvernées — hybride validé, Lot B sous gouvernance source |

---

## Critères de pré-audit (P8-1)

Indicateurs Dev calculés automatiquement par image :

| Indicateur | Méthode | Seuil indicatif |
|------------|---------|-----------------|
| **Uniformité du fond** | Distance couleur entre les 4 coins | ≤ 25 (uniforme) / > 25 (non uniforme) |
| **Clarté du fond** | Luminance moyenne des coins | ≥ 220 (clair) / < 220 (sombre/complexe) |
| **Entropie périphérique** | Variance des patchs périphériques | ≤ 0.18 (uniforme) / > 0.30 (lifestyle) |
| **Contraste produit / fond** | Bbox produit vs fond détecté | ≥ 60 (net) |

Classification auto initiale :

| Cas | Indicateurs | Classe proposée |
|-----|-------------|----------------|
| Fond uniforme clair, contraste net | uniformité ≤ 25 · clarté ≥ 220 · entropie ≤ 0.18 | **packshot_alpha** (candidat v1.2-alpha) |
| Fond non uniforme ou sombre | uniformité > 30 ou entropie > 0.30 | **lifestyle** (reste v1.1) |
| Cas intermédiaires | autres | **NEEDS_REVIEW** (reste v1.1 par défaut, validation MOA requise) |

**La proposition Dev n'est jamais auto-appliquée.** Tout passage en `packshot_alpha` doit être confirmé MOA.

---

## Critères d'acceptation P8

| Critère | Seuil |
|---------|-------|
| `image_1920` master | **Jamais modifié** |
| Audit classification 43/43 | ✅ couvert |
| Packshots alpha re-exportés | uniquement liste validée MOA |
| Lifestyle | inchangés (v1.1 conservé) |
| Pas d'alpha sur lifestyle | ✅ contrôle |
| Pas d'alpha sur NEEDS_REVIEW | ✅ contrôle |
| Effet « image dans l'image » sur packshots audités | **éliminé** |
| Halos packshots éligibles | **aucun** (sinon retour NEEDS_REVIEW) |
| Tests T1–T7 | verts |
| Rollback flag opérationnel | ✅ inchangé |

---

## Hors périmètre P8 (interdit)

- Aucune modification `image_1920`
- Aucune modification du modèle Odoo (champs existants suffisent)
- Aucune modification fiche produit, hero, culture, éditorial, sidebar
- Aucun traitement automatique global / cron
- Aucun détourage IA (rembg, BiRefNet, etc.)
- Aucune extension hors lot pilote 43
- Aucun export alpha sur lifestyle ou NEEDS_REVIEW
- Aucun re-shoot studio (relève de la MOA amont, hors Dev)

---

## Garde-fous opérationnels

```text
Flag marketone.shop_tile_enabled : conservé
Rollback R0 : marketone.shop_tile_enabled = False
Recette v1.1 : conservée pour lifestyle
Recette v1.2-alpha : packshots audités uniquement
shop_tile_recipe_version : conservé · trace par enregistrement
Manifest CSV : ligne par produit avec recipe_version explicite
Lot X : toujours exclu
```

---

## Fichiers attendus (indicatif Dev)

| Fichier | Action |
|---------|--------|
| `docs/recette/boutique/AUDIT_CLASSIFICATION_PILOTE_43_V1_2_ALPHA.csv` | **Créer** (P8-1) — proposition Dev |
| `docs/recette/boutique/AUDIT_CLASSIFICATION_PILOTE_43_V1_2_ALPHA.md` | **Créer** (P8-1) — rapport méthodo + résumé |
| `tools/ck_image_normalizer/ck_image_normalizer/processor.py` | **Modifier** (P8-2) — branche output_format PNG + background_alpha |
| `tools/ck_image_normalizer/ck_image_normalizer/recipe.py` | **Modifier** (P8-2) — champs alpha |
| `tools/ck_image_normalizer/recipes/ck_shop_tile_v1.2-alpha.yaml` | **Existant** (POC) — finaliser |
| `docs/recette/boutique/import_pilote_v1_2_alpha_packshots.csv` | **Créer** (P8-3) — manifest packshots alpha audités MOA |
| `docs/recette/boutique/RAPPORT_P8_RENDU_HYBRIDE.md` | **Créer** (P8-4) — capture + métriques |
| `docs/recette/boutique/capture_p8_*.png` | **Créer** (P8-4) — captures comparatives |
| `docs/recette/boutique/RAPPORT_P8_5_RESERVES_ACTIONS_CIBLEES.md` | **Créer** (P8-5) — plan d'ajustements ciblés |
| `docs/recette/boutique/RAPPORT_P8_5_LOTA_LOTB_EXECUTION.md` | **Créer** (P8-5) — exécution Lot A + Lot B |

---

## Plan tickets aval (post-P8)

| Si... | Action |
|-------|--------|
| Catalogue packshot alpha couvre > 70 % | Industrialiser P9 — extension hors pilote |
| Couverture < 50 % | Discuter avec MOA d'un mini-brief photo studio reprise |
| Halos persistants | Repli intégral v1.1 + cadrage explicite limite Odoo-side |

---

## Décision finale

```text
P8-5 clôturé MOA — GO avec réserves gouvernées.
Modèle hybride v1.1 + v1.2-alpha validé (9 alpha + 34 v1.1).
Lot B maintenu en NEEDS_REVIEW_SOURCE sous gouvernance source.
Aucun nouveau traitement technique demandé à ce stade.
```

**Signal Dev** :

```text
Verdict MOA final consigné :
GO avec réserves gouvernées — modèle hybride validé.
Suivi restant limité à la gouvernance source des 5 cas NEEDS_REVIEW_SOURCE.
```

---

## Historique

| Date | Auteur | Action |
|------|--------|--------|
| 2026-05-20 | MOA | **GO P8** — option A — audit + alpha hybride |
| 2026-05-20 | Dev | **P8 ticket ouvert** — pré-audit en cours |
| 2026-05-20 | Dev | **P8-1 livré** — 43/43 sources analysées · CSV + rapport · proposition 6+3 alpha |
| 2026-05-20 | MOA | **P8-1b validé** — 3 NEEDS_REVIEW basculés packshot_alpha (9 au total) |
| 2026-05-20 | Dev | **P8-2 livré** — CLI v1.2-alpha intégré (recipe + processor) |
| 2026-05-20 | Dev | **P8-3 livré** — re-export officiel 9 PNG alpha |
| 2026-05-20 | Dev | **P8-4 livré** — import hybride 9 alpha + 34 v1.1 · captures + rapport |
| 2026-05-20 | MOA | **P8-5 GO avec réserves** — doctrine validée, ajustements ciblés demandés |
| 2026-05-20 | Dev | **P8-5 analyse ciblée livrée** — audit occupation + plan correctif limité |
| 2026-05-20 | MOA | **GO Lot A + Lot B** — ajustements ciblés sans refonte |
| 2026-05-20 | Dev | **Lot A exécuté** — 3 packshots alpha retraités (fill 0.84) |
| 2026-05-20 | Dev | **Lot B exécuté** — 5 lifestyle v1.1 marqués NEEDS_REVIEW_SOURCE |
| 2026-05-20 | Dev | **Rapport exécution livré** — captures comparatives Lot A + liste explicite Lot B |
| 2026-05-20 | MOA | **Verdict final P8-5** — GO avec réserves gouvernées · hybride validé · Lot B maintenu en NEEDS_REVIEW_SOURCE |
| 2026-05-20 | MOA | **STOP v1.2-alpha** — GO retrait R1→R5 · doctrine image pleine sans transparence |
| 2026-05-20 | Dev | **Retrait alpha exécuté** — 9 produits rebasculés v1.1 · import PNG bloqué · [`RAPPORT_RETRAIT_V12_ALPHA_EXECUTION.md`](../../recette/boutique/RAPPORT_RETRAIT_V12_ALPHA_EXECUTION.md) |
