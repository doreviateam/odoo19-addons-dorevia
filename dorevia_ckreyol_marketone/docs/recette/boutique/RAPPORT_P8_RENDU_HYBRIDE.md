# Rapport P8 — Rendu hybride v1.1 + v1.2-alpha

| Champ | Valeur |
|-------|--------|
| **Phase** | P8-2 + P8-3 + P8-4 |
| **Date** | 2026-05-20 |
| **Base recette** | `ckr-marketone-01` |
| **URL** | http://localhost:18079/shop |
| **Flag** | `marketone.shop_tile_enabled = True` |

---

## Résumé exécution

| Étape | Résultat |
|------|----------|
| P8-2 intégration CLI `v1.2-alpha` | ✅ (`recipe.py` + `processor.py`) |
| P8-3 re-export 9 packshots | ✅ 9/9 PNG alpha |
| P8-4 import comparatif Odoo | ✅ 9 alpha + 34 v1.1 |
| Vérification garde-fou `image_1920` | ✅ inchangé |

### Statuts pipeline alpha (9)

- `OK`: 6
- `OK_WITH_WARNINGS`: 3
- `NEEDS_REVIEW`: 0
- `REJECTED`: 0

---

## Répartition recette en base

| Recette `image_shop_tile` | Volume |
|--------------------------|--------|
| `ck_shop_tile_v1.2-alpha` | 9 |
| `ck_shop_tile_v1.1` | 34 |
| Total `image_shop_tile` | 43 |

Liste alpha active (9):

- Maniocookies salés La Platine (`7`) · opaque=0.2461
- Crackers manioc Sainte-Anne (`8`) · opaque=0.6088
- Shrub agrumes créole (`155`) · opaque=0.323
- Mix beignets manioc (`163`) · opaque=0.2461
- Chips banane plantain salées (`183`) · opaque=0.6088
- Marinade jerk authentique (`187`) · opaque=0.323
- Marinade jerk citron vert (`CK-MO-031`) · opaque=0.323
- Palettes coco vanille (`CK-MO-033`) · opaque=0.2461
- Chips patate douce créole (`CK-MO-034`) · opaque=0.6088

---

## Contrôles visuels

### Packshots alpha (v1.2-alpha)

- `capture_p8_hybride_packshot_maniocookies.png`
- `capture_p8_hybride_packshot_crackers.png`
- `capture_p8_hybride_packshot_chips.png`

Constat: effet "image dans l'image" fortement réduit sur packshots validés MOA.

### Lifestyle conservés (v1.1)

- `capture_p8_hybride_lifestyle_confiture.png`
- `capture_p8_hybride_lifestyle_colombo.png`
- `capture_p8_hybride_lifestyle_pates.png`

Constat: rendu lifestyle inchangé, aucune application alpha hors périmètre.

### Vue globale

- `capture_p8_hybride_shop_global.png`

---

## Garde-fous confirmés

- Aucun remplacement de `image_1920`
- Aucun alpha hors liste MOA 9 packshots
- Lifestyle maintenus en `v1.1`
- Pas d'IA, pas de `rembg`
- Pas de cron / pas de traitement massif automatique
- Fallback et flag inchangés

---

## Livrables techniques P8

| Fichier | Rôle |
|---------|------|
| `tools/ck_image_normalizer/recipes/ck_shop_tile_v1.2-alpha.yaml` | Recette alpha exploitable |
| `tools/ck_image_normalizer/ck_image_normalizer/recipe.py` | Support `output_format=PNG` + `background_alpha` |
| `tools/ck_image_normalizer/ck_image_normalizer/processor.py` | Pipeline alpha + sortie PNG |
| `tools/ck_image_normalizer/run_p8_packshot_alpha.py` | Run officiel P8-3 (9 packshots) |
| `docs/recette/boutique/import_p8_packshots_alpha_9.csv` | Manifest import 9 alpha |

---

## Signal Dev

```text
P8-2, P8-3 et P8-4 réalisés.
Rendu hybride v1.1 + v1.2-alpha prêt pour revue MOA finale (P8-5).
```
