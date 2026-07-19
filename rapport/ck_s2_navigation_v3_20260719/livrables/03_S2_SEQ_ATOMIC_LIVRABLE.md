# S2 — Assignation atomique des séquences racines (après NO GO Garant `6afb44d`)

**SHA parent :** `6afb44d36c6aab4ae905c6fcfcebca502b9bcfa9`  
**Version :** `dorevia_ck_marketone_content` **19.0.1.98.0**

## Priorité explicite (arbitrage Dev)

1. **Créneaux réservés** `{10, 60, 70}` → Boutique / Producteurs / Professionnels, **toujours** imposés.
2. **Personnalisation BO catégorie** préservée **seulement si** elle reste unique dans le plan final **et** hors créneaux réservés.
3. Un rayon BO à `60` n’est donc **pas** une personnalisation protégeable : ce créneau appartient à Producteurs. Il est réassigné au prochain créneau libre (`20, 30, …`) **dans le même sync**.

Cette règle tranche la contradiction signalée par le Garant : on ne peut pas garantir à la fois `Producteurs≡60` et la conservation d’une catégorie BO sur `60`.

## Cause du NO GO

`_repair_managed_root_sequence_collisions` ne réparait que les séquences *déjà* en collision. Déplacer `Producteurs 20→60` créait une **nouvelle** collision avec un rayon BO=60, résolue seulement au 2ᵉ sync — en écrasant la BO.

## Correctif

`_assign_managed_root_sequences_atomic` calcule le plan complet (fixes + catégories) puis écrit en **un passage**.

## Tests

- `test_s2_cascade_collision_resolved_in_one_pass` (scénario Garant)
- BO catégorie hors réservés préservée ; fixes toujours 60/70
- Suite nav complète : **0 failed / 73 tests**
