# Réponse MOA — revue visuelle `validated_grid`

| Champ | Valeur |
|-------|--------|
| **Date revue** | 2026-05-20 |
| **Revue par** | MOA |
| **Périmètre** | Trames revue visuelle produit par produit |
| **Base** | `ckr-marketone-01` |
| **Action technique base** | Aucune |

---

## CSV complétés

Les trois CSV de revue ont été renseignés :

```text
docs/recette/boutique/TRAME_REVUE_VISUELLE_MOA_VALIDATED_STORAGE.csv
docs/recette/boutique/TRAME_REVUE_VISUELLE_MOA_ANNEXE.csv
docs/recette/boutique/TRAME_REVUE_VISUELLE_MOA_PRODUIT_PAR_PRODUIT.csv
```

Colonnes MOA complétées :

```text
decision_moa
motif_principal
commentaire_moa
date_revue_moa
revue_par
```

---

## Synthèse des décisions

### Périmètre principal — 20 `validated_storage`

| Décision | Nombre |
|----------|-------:|
| `validated_grid` | 7 |
| `validated_storage` | 2 |
| `needs_review_source` | 11 |

### Annexe — 23 lignes

| Décision | Nombre |
|----------|-------:|
| `validated_grid` | 12 |
| `validated_storage` | 2 |
| `needs_review_source` | 6 |
| `fallback_master` | 3 |

### Vue consolidée — 43 lignes

| Décision | Nombre |
|----------|-------:|
| `validated_grid` | 19 |
| `validated_storage` | 4 |
| `needs_review_source` | 17 |
| `fallback_master` | 3 |

---

## Lecture MOA

La promotion en `validated_grid` est volontairement ciblée :

- uniquement les visuels lisibles, cohérents et défendables en grille ;
- pas de promotion automatique des cas Crackers, fallback, sources faibles ou visuels génériques ;
- les sources non alignées avec le SKU restent en `needs_review_source` ;
- les trois cas fallback P1/P2 restent en `fallback_master`.

Cas Crackers product `8` :

```text
validated_storage maintenu — revue capture grille dédiée obligatoire avant promotion.
```

---

## Signal Dev

```text
CSV MOA complétés — 19 promotions validated_grid autorisées — 4 validated_storage maintenus — 17 needs_review_source — 3 fallback_master — aucune promotion hors CSV.
```

Garde-fous maintenus :

- pas de modification `image_1920` ;
- pas de retraitement moteur ;
- pas de promotion automatique ;
- import ciblé uniquement sur les lignes `decision_moa=validated_grid`.
