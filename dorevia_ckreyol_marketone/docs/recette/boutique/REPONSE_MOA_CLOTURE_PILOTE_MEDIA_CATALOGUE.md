# Réponse MOA — clôture définitive pilote média catalogue 50 SKU

| Champ | Valeur |
|-------|--------|
| **Date** | 2026-05-20 |
| **Ticket** | [`TICKET_MARKETONE_CK_IMAGE_NORMALIZER_PILOTE_MEDIA`](../../tickets/boutique/TICKET_MARKETONE_CK_IMAGE_NORMALIZER_PILOTE_MEDIA.md) |
| **Ticket amont** | [`TICKET_MARKETONE_CK_IMAGE_NORMALIZER_POC`](../../tickets/boutique/TICKET_MARKETONE_CK_IMAGE_NORMALIZER_POC.md) — clôturé GO avec réserves |
| **Recette candidate** | `ck_shop_tile_v1.1` |
| **Run principal** | `tools/ck_image_normalizer/reports/runs/pilote_20260520/` |
| **Volume** | 50 SKU |
| **Décision** | **GO pilote avec réserves — pilote clôturé** |

---

## Verdict final MOA

```text
GO pilote avec réserves confirmé
Recette candidate : ck_shop_tile_v1.1
Taux exploitable final : 43 / 50 = 86 %
Lot X restant : 7 / 50 = 14 %
REJECTED définitif : 0
```

---

## Lecture MOA

Le pilote démontre que la combinaison suivante est **viable** :

```text
moteur ck_shop_tile_v1.1 + revue opérateur + correction source ciblée
```

Progression mesurée :

| Étape | Résultat | Taux |
|-------|----------|-----:|
| Batch seul | 21 / 50 | 42 % |
| Après revue P4 | 36 / 50 | 72 % |
| Après lot M corrigé | 41 / 50 | 82 % |
| Après sources manioc | **43 / 50** | **86 %** |

Le moteur prouve sa valeur, mais le pilote confirme aussi que la **qualité source reste déterminante**.

Les échecs résiduels (lot X) viennent de sources incohérentes, génériques ou non identifiables — pas d’un rejet massif du moteur.

---

## Décisions actées

| # | Décision |
|---|----------|
| 1 | **`ck_shop_tile_v1.1`** conservée comme recette candidate |
| 2 | Fond **`#F8EEDB` baked-in** validé |
| 3 | **`NEEDS_REVIEW`** = sas opérateur obligatoire |
| 4 | **Séparation stricte** source / dérivé — pas de remplacement `image_1920` |
| 5 | **Règle catalogue** — un SKU = une source distincte, exploitable et identifiable · [`REGLE_CATALOGUE_IMAGES_SOURCE.md`](../../cadrage/REGLE_CATALOGUE_IMAGES_SOURCE.md) |
| 6 | **Lot X (7)** maintenu en demande fournisseur / exclusion temporaire |

Réponses amont consolidées :

- [`REPONSE_MOA_REINTEGRATION_5_LOT_M_CORRIGE.md`](./REPONSE_MOA_REINTEGRATION_5_LOT_M_CORRIGE.md)
- [`REPONSE_MOA_REINTEGRATION_2_MANIOC_SOURCES_DISTINCTES.md`](./REPONSE_MOA_REINTEGRATION_2_MANIOC_SOURCES_DISTINCTES.md)
- [`RECETTE_MANUELLE_CK_IMAGE_NORMALIZER_PILOTE_MEDIA.md`](./RECETTE_MANUELLE_CK_IMAGE_NORMALIZER_PILOTE_MEDIA.md)

---

## Garde-fous maintenus

Ce bilan **ne vaut pas GO exploitation automatique**.

Sans ticket séparé, restent **interdits** :

| Élément | Statut |
|---------|--------|
| Code Odoo | ❌ |
| Champ `image_shop_tile` | ❌ |
| Héritage QWeb | ❌ |
| Remplacement `image_1920` | ❌ |
| Cron | ❌ |
| Traitement massif automatique | ❌ |
| BO complet | ❌ |

---

## Suite

```text
Pilote média clôturé.
Prochaine action Dev : uniquement sur signal MOA explicite.
```

Sujet technique futur identifié :

```text
P6 — cadrage V1.5 Odoo lite → validé MOA
P7 — implémentation V1.5 lite → ouvert — voir TICKET_MARKETONE_CK_IMAGE_NORMALIZER_V1_5_IMPLEMENTATION.md
```

Le futur ticket P6 devra clarifier :

- séparation source vs dérivé ;
- champ dédié éventuel `image_shop_tile` ;
- fallback image standard ;
- usage limité aux tuiles `/shop` ;
- conditions d’import des images validées ;
- règles de gouvernance des `NEEDS_REVIEW`.

---

## Décision finale

```text
Pilote média CK Image Normalizer clôturé
GO avec réserves confirmé
43 / 50 exploitables
Recette candidate : ck_shop_tile_v1.1
Lot X maintenu en demande fournisseur / exclusion
P6 V1.5 Odoo lite en attente décision MOA
```

**Signal MOA** :

```text
Pilote média clôturé — GO avec réserves confirmé — 43/50 exploitables — aucune suite Dev sans signal MOA explicite.
```
