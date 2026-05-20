# Rapport exécution — revue visuelle MOA — promotion `validated_grid`

| Champ | Valeur |
|-------|--------|
| **Signal MOA** | CSV MOA complétés — 19 promotions `validated_grid` autorisées |
| **Date exécution Dev** | 2026-05-20 |
| **Date validation MOA** | 2026-05-20 |
| **Statut phase** | **Clôturée — GO visuel MOA post-promotion** |
| **Base** | `ckr-marketone-01` |
| **Flag** | `marketone.shop_tile_enabled = True` |
| **Script** | `scripts/apply_moa_revue_visuelle.py` |
| **Manifest** | `docs/recette/boutique/TRAME_REVUE_VISUELLE_MOA_PRODUIT_PAR_PRODUIT.csv` |

---

## 1) Actions exécutées

Import **statuts uniquement** — 43 lignes CSV MOA appliquées :

| Décision MOA | Statut Odoo | Nombre |
|--------------|-------------|-------:|
| `validated_grid` | `validated_grid` | **19** |
| `validated_storage` | `validated_storage` | **4** |
| `needs_review_source` | `needs_review_source` | **17** |
| `fallback_master` | `pending_review` + tuile vidée si présente | **3** |

> Aucune modification `image_1920`. Aucun retraitement moteur. Aucune promotion hors CSV.

---

## 2) État final base

| Indicateur | Avant | Après |
|-----------|------:|------:|
| `validated_grid` | 0 | **19** |
| `marketone_use_shop_tile_on_grid() = True` | 0 | **19** |
| `validated_storage` | 20 | **4** |
| `needs_review_source` | 0 | **17** |
| `image_shop_tile` actives | 40 | **40** |
| Fallback master sans tuile (154, 156, 471) | 3 | **3** |

---

## 3) Produits promus `validated_grid` (19)

| ID | Produit |
|----|---------|
| 9 | Pâtes de manioc Mayotte |
| 153 | Confiture banane flambée |
| 155 | Shrub agrumes créole |
| 158 | Sauce piment cadji |
| 159 | Rougail épices Réunion |
| 160 | Chutney mangue verte |
| 164 | Miel créole baie rose |
| 177 | Coffret gourmand îles créoles |
| 178 | Palets manioc croustillants La Platine |
| 181 | Assortiment apéritif créole |
| 184 | Semoule manioc fine Mayotte |
| 186 | Trio sirops des Antilles |
| 187 | Marinade jerk authentique |
| 467 | Sauce scotch bonnet créole (CK-MO-028) |
| 469 | Pochette curry des Antilles (CK-MO-030) |
| 470 | Marinade jerk citron vert (CK-MO-031) |
| 477 | Confiture christophine gingembre (CK-MO-038) |
| 479 | Quatre épices créoles (CK-MO-040) |
| 489 | Miel polyfloral créole (CK-MO-050) |

---

## 4) Maintiens `validated_storage` (4)

| ID | Produit | Motif MOA |
|----|---------|-----------|
| 8 | Crackers manioc Sainte-Anne | Revue capture grille dédiée obligatoire |
| 7 | Maniocookies salés La Platine | Produit flottant — présence commerciale faible |
| 474 | Crackers sarrasin Réunion | Intitulé/source à sécuriser |
| 188 | Coffret biscuits et douceurs | Rectangle interne — ne pas promouvoir |

---

## 5) `needs_review_source` (17)

183, 473, 475, 476, 478, 480, 481, 482, 483, 485, 486, 163, 179, 180, 185, 468, 472

---

## 6) Fallback master confirmé (3)

| ID | Produit | Affichage grille |
|----|---------|------------------|
| 154 | Colombo des Antilles (épices) | `image_1920` master |
| 156 | Biscuits coco vanille | `image_1920` master |
| 471 | Biscuits banane confiture | `image_1920` master |

---

## 7) Garde-fous confirmés

- `image_1920` **inchangé** sur les 43 produits
- Pas de retraitement moteur
- Pas de promotion automatique hors CSV
- Notes MOA mises à jour (`shop_tile_moa_note` préfixe `MOA_REVUE_20260520`)
- Rollback flag maintenu

---

## 8) Contrôle visuel MOA — `/shop` post-promotion

**Environnement** : sandbox `http://localhost:18079/shop`  
**Date revue** : 2026-05-20

Revue visuelle effectuée par MOA après exécution des 19 promotions `validated_grid`.

### Verdict MOA

**GO visuel.**

Le rendu est conforme à l'intention MOA :

- grille plus propre, homogène, marchande et premium ;
- pas d'effet massif « image dans l'image » sur les tuiles visibles ;
- cohérent avec la doctrine image v2.

### Points validés MOA

| Point | Validation |
|-------|------------|
| `validated_grid` seul statut affichable en grille | Validé |
| Fallback master sur produits non validés | Validé |
| Séparation dérivé stocké / dérivé affiché | Validé |
| Protection `image_1920` | Validé |
| Rendu visuel global boutique | Validé |
| Logique « revue MOA avant affichage » | Validé |

### Lecture MOA

> La doctrine v2 fonctionne : un dérivé peut être stocké sans être affiché ; seule la revue visuelle MOA permet l'entrée en grille. Le résultat visuel confirme que cette approche est la bonne.

---

## 9) Décision MOA — clôture phase

| Décision | Détail |
|----------|--------|
| **GO visuel `/shop` post-promotion** | Validé |
| **19 `validated_grid` actifs** | Confirmé |
| **Fallback master** | Maintenu pour les autres produits |
| **Doctrine image v2** | Validée en pratique |

### Garde-fous maintenus (MOA)

- pas de promotion automatique ;
- pas de traitement massif ;
- pas de modification `image_1920` ;
- pas d'alpha ;
- pas de détourage ;
- **revue MOA obligatoire** pour toute future promotion `validated_grid`.

---

## Signal Dev

```text
GO visuel MOA post-promotion — 19 validated_grid actifs — fallback master maintenu — doctrine image v2 validée en pratique — garde-fous maintenus — phase revue visuelle clôturée.
```
