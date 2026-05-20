# Réponse MOA — réintégration des 5 images lot M corrigé

| Champ | Valeur |
|-------|--------|
| **Date** | 2026-05-20 |
| **Run initial** | `tools/ck_image_normalizer/reports/runs/pilote_20260520/` |
| **Mini-batch** | `tools/ck_image_normalizer/reports/runs/pilote_20260520_lot_m_corrige/` |
| **Recette** | `ck_shop_tile_v1.1` |
| **Périmètre** | Qualité source catalogue — tuiles `/shop` |

---

## 1. Validation visuelle des 5 images récupérées

Previews consultées :

```text
tools/ck_image_normalizer/reports/runs/pilote_20260520_lot_m_corrige/reports/previews/
```

Planche de contrôle :

```text
tools/ck_image_normalizer/reports/runs/pilote_20260520_lot_m_corrige/reports/contact_sheet_5_ok_visuel.jpg
```

| Produit | Statut mini-batch | Décision MOA | Note |
|---------|-------------------|--------------|------|
| Biscuits coco vanille | `OK` | OK avec réserve | Produit lisible, visuel exploitable ; réserve sur cadrage horizontal et proximité avec le visuel coffret. |
| Rougail épices Réunion | `OK` | OK visuel | Composition lisible, poids visuel correct, rendu commerce acceptable. |
| Chutney mangue verte | `OK` | OK avec réserve | Ensemble de pots lisible ; réserve sur identification exacte du SKU en mobile. |
| Tartinade coco citron vert | `OK` | OK avec réserve | Visuel chaleureux et exploitable ; réserve sur scène lifestyle dense. |
| Coffret biscuits et douceurs | `OK` | OK avec réserve | Exploitable en tuile ; réserve sur proximité visuelle avec Biscuits coco vanille. |

Décision :

```text
5 / 5 images récupérées acceptées visuellement.
```

Ces images sont comptabilisables comme exploitables ou exploitables avec réserve.

---

## 2. Bilan exploitable mis à jour

Avant mini-batch :

```text
36 / 50 images exploitables ou exploitables avec réserve
```

Après validation des 5 images récupérées :

```text
41 / 50 images exploitables ou exploitables avec réserve
Taux exploitable : 82 %
```

---

## 3. Deux cas manioc rejetés

Produits concernés :

| Produit | Statut | Décision |
|---------|--------|----------|
| Pâtes de manioc Mayotte | `REJECTED` mini-batch | En attente source distincte |
| Semoule manioc fine Mayotte | `REJECTED` mini-batch | En attente source distincte |

Constat :

- les sources disponibles sont visuellement identiques ;
- le mini-batch rejette les deux cas avec `produit petit dans la source` ;
- utiliser la même image pour deux SKU distincts n’est pas acceptable catalogue ;
- aucune relance ne doit être faite tant que deux sources distinctes ne sont pas disponibles.

Fichier de suivi :

```text
tools/ck_image_normalizer/reports/runs/pilote_20260520/lot_manioc_redemande_source.csv
```

Décision :

```text
2 SKU manioc restent en attente de sources distinctes.
```

---

## 4. Lot X

Fichier ouvert et arbitré :

```text
tools/ck_image_normalizer/reports/runs/pilote_20260520/lot_x_demande_fournisseur.csv
tools/ck_image_normalizer/reports/runs/pilote_20260520/lot_x_arbitrage_moa.csv
```

Décision :

```text
Lot X maintenu en demande fournisseur / exclusion temporaire du flux image.
```

Raison :

- sources non adaptées ;
- visuels génériques ;
- incohérences SKU/image ;
- produit non identifiable en tuile commerce.

---

## 5. Signal Dev

```text
GO réintégration pilote — 5 images lot M corrigé validées visuellement — bilan exploitable porté à 41 / 50.
```

Réserve à joindre :

```text
2 SKU manioc restent en attente de sources distinctes ; lot X maintenu en demande fournisseur / exclusion.
```

---

## 6. Règle catalogue retenue

```text
Un produit publié doit avoir une image source exploitable, distincte et identifiable.
Pas de même visuel pour deux SKU différents, sauf pack assumé ou collection.
```

Cette règle vise à éviter que le moteur d’image compense des erreurs de catalogue.

---

## 7. Garde-fous confirmés

- Pas de champ `image_shop_tile`.
- Pas de QWeb.
- Pas d’intégration Odoo.
- Pas de remplacement `image_1920`.
- Pas de traitement massif.

La suite reste concentrée sur la qualité source.
