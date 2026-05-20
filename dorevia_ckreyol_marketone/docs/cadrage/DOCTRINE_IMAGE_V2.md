# Doctrine image v2 — CK Image Normalizer / Marketone

| Champ | Valeur |
|-------|--------|
| **Statut** | **Validé MOA en pratique** (2026-05-20) · GO visuel `/shop` post-promotion · 19 `validated_grid` actifs |
| **Signal MOA** | GO doctrine image v2 — deux images, trois décisions · GO visuel grille post-promotion |
| **ADR** | [ADR-033](./DECISIONS.md#adr-033--ck-image-normalizer-v1--poc-tuiles-commerce-shop) |
| **Plan alignement** | [`PLAN_ALIGNEMENT_DOCTRINE_IMAGE_V2.md`](../recette/boutique/PLAN_ALIGNEMENT_DOCTRINE_IMAGE_V2.md) |

---

## Formulation MOA

> Le moteur image est un **sas qualité média** entre la photo vendeur et la tuile boutique.  
> Il produit un **dérivé contrôlé** sans toucher au master.  
> Seules les tuiles visuellement conformes entrent en grille ; les autres restent en gouvernance source.

---

## Principe — Deux images, trois décisions

### Deux images — rôles fixes (invariants)

| Champ | Rôle |
|-------|------|
| **`image_1920`** | Master produit · vérité BO / fiche / référence · **jamais écrasé** par le moteur sans décision MOA explicite |
| **`image_shop_tile`** | Dérivé commerce `/shop` · produit par normalisation ou reprise source · **seul champ modifiable** par le flux image |

### Trois décisions distinctes

| Décision | Question | Décideur |
|----------|----------|----------|
| **A — Source** | La photo fournie est-elle acceptable ? | MOA / gouvernance fournisseur |
| **B — Traitement** | Le moteur produit-il un dérivé exploitable ? | Moteur + opérateur |
| **C — Affichage grille** | Ce dérivé (ou le master) peut-il aller en `/shop` ? | MOA visuel |

> Un dérivé stocké dans `image_shop_tile` **n'est pas** automatiquement affichable en grille.

---

## Règle visuelle grille

> Image pleine, bord à bord, sans transparence, sans carré interne, sans produit flottant.

Référence comportementale : photo pleine type **Colombo** (lifestyle maîtrisé), pas un produit détouré flottant.

---

## Règle d'affichage grille `/shop`

```text
SI image_shop_tile.shop_tile_status = validated_grid
   ET flag marketone.shop_tile_enabled actif
   → afficher image_shop_tile

SINON
   → afficher image_1920 (fallback master Odoo standard)

SI ni dérivé conforme ni master exploitable visuellement
   → gouvernance source / redemande fournisseur
```

Le pilote v1.1 peut avoir **importé** N dérivés sans que N soient **affichables**.

---

## Statuts `shop_tile_status`

| Statut | Signification | Affichage `/shop` |
|--------|---------------|-------------------|
| `validated_grid` | OK MOA pour grille via `image_shop_tile` | **Oui** |
| `validated_storage` | Dérivé stocké, pipeline OK, non affiché | Non (fallback master) |
| `validated_reserve` | Exploitable avec réserve · revue MOA | Non |
| `pending_review` | En attente | Non |
| `needs_review_source` | Source à redemander / recadrer | Non |
| `rejected` | Non exploitable | Non |
| `none` | Aucune tuile | Non |
| `validated` *(legacy)* | Pilote · équivalent **`validated_storage`** | Non |

---

## Reprise source

| Règle | Détail |
|-------|--------|
| Entrée | Source originale · archive pilote · dépôt vendeur |
| Sortie | `image_shop_tile` + métadonnées tuile |
| Interdit | Modifier `image_1920` |
| Run | `shop_tile_source_run = reprocess_<id>_<date>` |
| Grille | Uniquement si MOA passe en `validated_grid` |

---

## Rôle du moteur — fait / ne fait pas

| Fait | Ne fait pas |
|------|-------------|
| Normaliser | Remplacer le master |
| Qualifier | Corriger une mauvaise source par magie |
| Alerter | Alpha / détourage / rembg |
| Préparer flux vendeur futur | Compensation CSS excessive |
| Produire dérivé contrôlé | Traitement massif automatique sans revue |

---

## Garde-fous confirmés MOA

- pas de retour alpha
- pas de détourage / rembg
- pas de compensation CSS excessive
- pas de traitement massif automatique
- pas de remplacement de `image_1920`
- revue MOA visuelle **prime** sur métriques auto
- rollback via `marketone.shop_tile_enabled`

---

## Références

| Document | Rôle |
|----------|------|
| [`NOTE_CK_IMAGE_NORMALIZER_VISION_MOA.md`](./NOTE_CK_IMAGE_NORMALIZER_VISION_MOA.md) | Enjeu produit |
| [`RECETTE_MANUELLE_CK_IMAGE_NORMALIZER_V1_5_SHOP_TILE.md`](../recette/boutique/RECETTE_MANUELLE_CK_IMAGE_NORMALIZER_V1_5_SHOP_TILE.md) | Opérateur import |
| [`RAPPORT_RETRAIT_V12_ALPHA_EXECUTION.md`](../recette/boutique/RAPPORT_RETRAIT_V12_ALPHA_EXECUTION.md) | Clôture alpha |
| [`RAPPORT_REVUE_VISUELLE_MOA_EXECUTION.md`](../recette/boutique/RAPPORT_REVUE_VISUELLE_MOA_EXECUTION.md) | GO visuel post-promotion |
