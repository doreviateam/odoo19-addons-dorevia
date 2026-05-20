# Réponse MOA — CK Image Normalizer — v1.1 calibrage accepté · P3 ciblé

| Champ | Valeur |
|-------|--------|
| **Statut** | **Décision MOA officielle** |
| **Date** | 2026-05-20 |
| **Recette candidate** | `ck_shop_tile_v1.1` — **acceptée comme base de revue** |
| **Kit revue P3** | [`RECETTE_P3_CIBLE_7_NEEDS_REVIEW.md`](./RECETTE_P3_CIBLE_7_NEEDS_REVIEW.md) |

---

Bonjour Dev,

Merci pour l'implémentation de `ck_shop_tile_v1.1` et la relance ciblée sur les 7 fichiers.

Le résultat correspond bien à l'arbitrage MOA attendu :

- les cas plein cadre ne sont plus considérés comme des échecs techniques ;
- ils passent désormais en `NEEDS_REVIEW` ;
- le taux `REJECTED` tombe à 0 % sur ce lot ciblé ;
- aucun changement Odoo ;
- recette, fond `#F8EEDB`, exports WebP/JPEG, previews et rapports conservés.

---

## Décision MOA

**Calibrage v1.1 accepté comme base de revue.**

Pas encore de GO POC final.

Nous passons maintenant en **P3 ciblé — revue visuelle des 7 fichiers `NEEDS_REVIEW`**.

---

## Objectif P3 ciblé

Pour chaque fichier, déterminer si le statut `NEEDS_REVIEW` est pertinent :

- image exploitable telle quelle ;
- image acceptable avec réserve ;
- image nécessitant reprise manuelle ;
- image à exclure du process catalogue.

---

## Points de recette (G1–G6)

| Critère | Objet |
|---------|--------|
| **G1** | Lisibilité en taille tuile |
| **G2** | Chaleur / premium CK |
| **G3** | Cohérence avec les autres tuiles |
| **G4** | Absence d'effet artificiel |
| **G5** | Préservation texture / étiquette |
| **G6** | Couture image / carte — fond `#F8EEDB` baked-in |

---

## Décision après revue des 7

1. Adopter `ck_shop_tile_v1.1` comme recette candidate ;
2. Relancer le batch complet des 21 images en `v1.1` ;
3. Ajuster encore la règle plein cadre si les 7 previews ne sont pas satisfaisantes.

---

## Rappel

- Pas de code Odoo
- Pas de GO POC final à ce stade
- **Prochaine action MOA** : revue visuelle des 7 previews

---

**Validé par** : MOA · **Date** : 2026-05-20
