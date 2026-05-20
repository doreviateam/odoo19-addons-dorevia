# Réponse MOA — CK Image Normalizer — GO calibrage `ck_shop_tile_v1.1`

| Champ | Valeur |
|-------|--------|
| **Statut** | **Décision MOA officielle** |
| **Date** | 2026-05-20 |
| **Livrable Dev** | [`RAPPORT_V1_1_RECALIBRATION_7FICHIERS.md`](./RAPPORT_V1_1_RECALIBRATION_7FICHIERS.md) |

---

Bonjour Dev,

Merci pour l'analyse des 7 rejets.

Nous validons la lecture : les 7 `REJECTED` du batch proxy legacy ne correspondent pas à des échecs techniques du moteur, mais à une règle de rejet trop binaire sur les cas plein cadre.

Le point clé est bien identifié :

> `content_area_ratio > 0.95` rejette automatiquement des images qui devraient plutôt passer en revue MOA.

Le cas `stitch_jerk_marinade_bottle`, classé `OK_WITH_WARNINGS` avec un ratio `0.929`, confirme que le seuil actuel crée une frontière trop dure entre warning et rejet.

---

## Décision MOA

**GO pour implémenter `ck_shop_tile_v1.1` et relancer un batch ciblé sur les 7 fichiers concernés.**

Il ne s'agit pas encore d'un GO POC final.

Il s'agit d'un **calibrage de recette CLI/YAML**, sans code Odoo.

---

## Arbitrage retenu

Pour les profils `packshot` :

| Ratio packshot | Statut attendu |
|----------------|----------------|
| `< 0.15` | `REJECTED` |
| `0.15 – 0.95` | `OK` / `OK_WITH_WARNINGS` |
| `0.95 – 1.0` | `NEEDS_REVIEW` au lieu de `REJECTED` |

---

## Rappel — inchangé

- Périmètre POC · 1024×1024 · `#F8EEDB` baked-in · WebP/JPEG · archive · rapports · previews
- **Aucun code Odoo** · **pas de remplacement `image_1920`**

---

## Suite après batch ciblé (MOA)

1. Relancer batch **21 images** complet en v1.1 ;
2. Valider les **21 refs** comme lot officiel POC (révision MOA 2026-05-20) ;
3. Conserver v1.1 comme recette candidate POC.

**Revue visuelle requise** sur les 7 previews `NEEDS_REVIEW`.

---

**Validé par** : MOA · **Date** : 2026-05-20

**Exécution Dev** : [`RAPPORT_V1_1_RECALIBRATION_7FICHIERS.md`](./RAPPORT_V1_1_RECALIBRATION_7FICHIERS.md)
