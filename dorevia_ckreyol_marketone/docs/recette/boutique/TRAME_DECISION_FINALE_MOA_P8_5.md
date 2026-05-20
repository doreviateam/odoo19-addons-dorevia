# Trame de décision finale MOA — P8-5 — Rendu hybride `v1.1 + v1.2-alpha`

| Champ | Valeur |
|-------|--------|
| **Périmètre** | Tuiles `/shop` uniquement |
| **Base** | `ckr-marketone-01` |
| **Flag** | `marketone.shop_tile_enabled = True` |
| **État final recettes** | `v1.2-alpha`: **9** · `v1.1`: **34** · total `image_shop_tile`: **43** |
| **Master** | `image_1920` inchangé |
| **Statut phase** | P8-5 — revue visuelle finale MOA |

---

## 1) Captures clés (8)

### A. Lot A — comparatifs avant / après (3)

1. `capture_p8_lotA_compare_01_product-7_maniocookies-sales-la-platine.png`
2. `capture_p8_lotA_compare_14_product-163_mix-beignets-manioc.png`
3. `capture_p8_lotA_compare_33_ck-mo-033_palettes-coco-vanille.png`

### B. Lot A — rendu `/shop` après ajustement (3)

4. `capture_p8_lotA_after_maniocookies.png`
5. `capture_p8_lotA_after_mix_beignets.png`
6. `capture_p8_lotA_after_palettes_coco.png`

### C. Lot B — cas lifestyle maintenus v1.1 (2)

7. `capture_p8_lotB_v11_biscuits_coco.png`
8. `capture_p8_lotB_v11_pates_manioc.png`

> Référence complémentaire (hors 8 captures clés) :
> `capture_p8_hybride_shop_global.png`.

---

## 2) Liste des produits concernés

### Lot A — packshots alpha retraités (`content_fill_ratio = 0.84`)

- `Maniocookies salés La Platine` (`product_id=7`)
- `Mix beignets manioc` (`product_id=163`)
- `Palettes coco vanille` (`default_code=CK-MO-033`)

### Lot B — lifestyle maintenus `v1.1` + `pending_review` (`NEEDS_REVIEW_SOURCE`)

- `Biscuits banane confiture` (`product_id=471`)
- `Biscuits coco vanille` (`product_id=156`)
- `Pâtes de manioc Mayotte` (`product_id=9`)
- `Coffret biscuits et douceurs` (`product_id=188`)
- `Semoule manioc fine Mayotte` (`product_id=184`)

---

## 3) État final des recettes (pré-rempli)

### Répartition globale

| Recette | Volume |
|--------|--------|
| `ck_shop_tile_v1.2-alpha` | **9** |
| `ck_shop_tile_v1.1` | **34** |
| Total `image_shop_tile` | **43** |

### Détail produit par produit

- Voir CSV audit/état :
  - `AUDIT_P8_5_VISUAL_OCCUPANCY.csv`
  - `AUDIT_CLASSIFICATION_PILOTE_43_V1_2_ALPHA.csv`

---

## 4) Rappel des garde-fous (à maintenir)

- `image_1920` jamais modifié
- pas d’alpha sur lifestyle
- pas d’IA / rembg
- pas de cron
- pas de traitement massif automatique
- pas de modification fiche produit
- lot X inchangé
- rollback via flag (`marketone.shop_tile_enabled`) maintenu

---

## 5) Proposition de verdict Dev (pré-remplie)

**Proposition Dev** : **GO avec réserves gouvernées**

Motif :

- Doctrine hybride validée et techniquement stable (`9 alpha / 34 v1.1`).
- Lot A améliore la présence commerciale des packshots ciblés.
- Lot B identifie proprement les limites de qualité source sans forcer d’alpha.
- Aucune régression structurelle et garde-fous respectés.

Réserve gouvernée : maintenir `pending_review / NEEDS_REVIEW_SOURCE` sur les 5 lifestyle Lot B jusqu’à recadrage/reprise source.

---

## 6) Zone de décision MOA (à compléter)

### Décision finale MOA P8-5

- [ ] **GO final hybride**
- [ ] **GO avec réserves**
- [ ] **Fallback partiel**
- [ ] **Ajustement ciblé complémentaire**

### Si GO avec réserves / fallback / ajustement : produits concernés

```text
(compléter ici)
```

### Actions MOA demandées au Dev

```text
(compléter ici)
```

### Date + validation MOA

```text
Date :
Nom / rôle :
Décision signée :
```

---

## 7) Références

- `RAPPORT_P8_RENDU_HYBRIDE.md`
- `RAPPORT_P8_5_RESERVES_ACTIONS_CIBLEES.md`
- `RAPPORT_P8_5_LOTA_LOTB_EXECUTION.md`
- `TICKET_MARKETONE_CK_IMAGE_NORMALIZER_V1_2_ALPHA_P8.md`
