# P8-5 — GO avec réserves — Propositions d'ajustements ciblés
| Champ | Valeur |
|-------|--------|
| **Statut MOA** | GO avec réserves (P8-5) |
| **Objectif** | Corriger les cas résiduels qui cassent l'homogénéité, sans refonte |
| **Méthode** | Audit quantifié sur les 43 tuiles actives (`AUDIT_P8_5_VISUAL_OCCUPANCY.csv`) |

---

## 1) Résultats de l'audit ciblé

- Tuiles analysées : **43**
- Cas alpha à faible présence (R1) : **3**
- Cas lifestyle effet rectangle (R2) : **5**

### R1 — Packshots alpha avec présence commerciale faible

| Produit | ID | bbox_area_ratio | Action proposée |
|---|---:|---:|---|
| Maniocookies salés La Platine | 7 | 0.321 | `v1.2-alpha` ciblé : augmenter `content_fill_ratio` (0.78 → 0.84) et re-export unitaire |
| Mix beignets manioc | 163 | 0.321 | `v1.2-alpha` ciblé : augmenter `content_fill_ratio` (0.78 → 0.84) et re-export unitaire |
| Palettes coco vanille | 472 | 0.321 | `v1.2-alpha` ciblé : augmenter `content_fill_ratio` (0.78 → 0.84) et re-export unitaire |

### R2 — Lifestyle v1.1 avec effet rectangle interne

| Produit | ID | bbox_area_ratio | Action proposée |
|---|---:|---:|---|
| Biscuits banane confiture | 471 | 0.292 | priorité haute : `NEEDS_REVIEW_SOURCE` (recadrage source) ; option fallback temporaire à étudier |
| Biscuits coco vanille | 156 | 0.333 | priorité haute : `NEEDS_REVIEW_SOURCE` (recadrage source) ; option fallback temporaire à étudier |
| Pâtes de manioc Mayotte | 9 | 0.337 | maintenir `v1.1` + marquer `NEEDS_REVIEW_SOURCE` (recadrage source) |
| Coffret biscuits et douceurs | 188 | 0.350 | maintenir `v1.1` + marquer `NEEDS_REVIEW_SOURCE` (recadrage source) |
| Semoule manioc fine Mayotte | 184 | 0.419 | maintenir `v1.1` + marquer `NEEDS_REVIEW_SOURCE` (recadrage source) |

---

## 2) Proposition Dev (sans changer la doctrine)

1. **Lot A — micro-ajustement alpha**
   - Scope: 3 packshots alpha listés R1 uniquement.
   - Action: recette `ck_shop_tile_v1.2-alpha` avec `content_fill_ratio=0.84` **sur run ciblé** (pas global).
   - Attendu: produit plus présent en tuile, sans toucher lifestyle.

2. **Lot B — lifestyle rectangle**
   - Scope: 5 produits R2.
   - Action: conserver `v1.1`, statut `NEEDS_REVIEW_SOURCE` (recadrage / reprise source).
   - Option temporaire (si MOA le souhaite): fallback Odoo standard pour 1–2 cas les plus gênants.

3. **Aucun changement doctrine**
   - packshots éligibles -> `v1.2-alpha`
   - lifestyle -> `v1.1`
   - cas douteux -> revue humaine

---

## 3) Garde-fous maintenus

- `image_1920` inchangé
- pas d'alpha sur lifestyle
- pas de détourage IA / rembg
- pas de cron / pas de traitement massif
- pas de changement fiche produit
- rollback flag inchangé

---

## 4) Décision attendue MOA

- **Option 1**: GO Lot A + Lot B (recommandation Dev)
- **Option 2**: GO Lot A seul
- **Option 3**: statu quo + revue source uniquement
