# Réponse MOA — réintégration des 2 SKU manioc avec sources distinctes

| Champ | Valeur |
|-------|--------|
| **Date** | 2026-05-20 |
| **Run** | `tools/ck_image_normalizer/reports/runs/pilote_20260520_lot_manioc_sources/` |
| **Recette** | `ck_shop_tile_v1.1` |
| **Périmètre** | Mini-batch ciblé sur 2 SKU manioc |
| **Garde-fous** | Aucun code Odoo · aucun remplacement `image_1920` · aucune industrialisation |

---

## 1. Sources fournies

Deux sources distinctes ont été fournies pour lever la réserve catalogue :

| Produit | Source |
|---------|--------|
| Pâtes de manioc Mayotte | `manio_pate.png` |
| Semoule manioc fine Mayotte | `manio_fin.png` |

Les deux images sont distinctes, lisibles, et alignées avec les SKU concernés.

Manifest utilisé :

```text
tools/ck_image_normalizer/manifest.pilote_lot_manioc_sources.csv
```

---

## 2. Résultat mini-batch

Rapport :

```text
tools/ck_image_normalizer/reports/runs/pilote_20260520_lot_manioc_sources/reports/batch_20260520T131653Z.csv
```

| Produit | Statut moteur | Décision MOA |
|---------|---------------|--------------|
| Pâtes de manioc Mayotte | `OK` | OK visuel — retenir |
| Semoule manioc fine Mayotte | `NEEDS_REVIEW` | OK avec réserve — retenir |

Lecture MOA :

- le produit Pâtes est lisible, distinct et propre ;
- la Semoule est passée en `NEEDS_REVIEW` car plein cadre, mais la preview est nette et exploitable ;
- les deux sources corrigent le problème initial de duplication visuelle.

Décision :

```text
2 / 2 SKU manioc réintégrés dans le flux exploitable.
```

---

## 3. Bilan pilote consolidé

Après réintégration des 5 images lot M corrigé :

```text
41 / 50 exploitables ou exploitables avec réserve
```

Après réintégration des 2 SKU manioc :

```text
43 / 50 exploitables ou exploitables avec réserve
Taux exploitable : 86 %
```

Reste hors flux :

```text
7 / 50 = 14 %
```

Ces 7 images correspondent au lot X, maintenu en demande fournisseur / exclusion temporaire.

---

## 4. Fichiers de suivi

Décision MOA mini-batch :

```text
tools/ck_image_normalizer/reports/runs/pilote_20260520_lot_manioc_sources/decision_moa_manioc_sources.csv
```

Lot X :

```text
tools/ck_image_normalizer/reports/runs/pilote_20260520/lot_x_arbitrage_moa.csv
```

---

## 5. Signal MOA

```text
GO réintégration pilote — 2 SKU manioc validés sur sources distinctes — bilan exploitable porté à 43 / 50.
```

Réserve maintenue :

```text
Lot X maintenu en demande fournisseur / exclusion temporaire.
```

---

## 6. Règle catalogue confirmée

```text
Un produit publié doit avoir une image source exploitable, distincte et identifiable.
Pas de même visuel pour deux SKU différents, sauf pack assumé ou collection.
```

Le mini-batch manioc confirme que la correction des sources améliore directement le taux exploitable.
