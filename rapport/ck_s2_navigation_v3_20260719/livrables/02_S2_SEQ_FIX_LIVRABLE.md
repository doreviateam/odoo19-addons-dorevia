# S2 — Correctif séquences racines (après NO GO QA)

**Branche :** `refactor/s2-canonical-navigation-v3`  
**Commit parent refusé QA :** `c39ce6329f06625efb218198c7aba01046bea010`  
**Module :** `dorevia_ck_marketone_content` **19.0.1.97.0**

## Cause

1. Les catégories racine reçoivent le créneau `20` (+10) avec `preserve_existing_sequence=True`.
2. `Producteurs` était upserté avec le **compteur post-catégories** (souvent 30) **et** `preserve_existing_sequence=True`.
3. Sur les bases héritées, `Producteurs` était déjà à **20** (dette V1 : `NAV_V1_PRODUCTEURS_SEQUENCE = 20`).
4. La préservation BO gardait donc `Épicerie=20` et `Producteurs=20` → collision → ordre `sequence, id` non déterministe.

## Règle retenue

| Situation | Comportement |
|---|---|
| Création / défaut | Boutique=10, catégories=20… (skip 60/70), Producteurs=**60**, Professionnels=**70** |
| Personnalisation BO **sans collision** (séquences distinctes entre racines gérées) | **Préservée** |
| **Collision** entre ≥2 racines gérées (même `sequence`) | Réparation vers les valeurs **canoniques** (jamais départage par id ORM) |

Implémentation : `_repair_managed_root_sequence_collisions` après les upserts.

## Tests

- Nouveau : `tests/test_ck_nav_s2_root_sequences.py` (frais, collision 20/20, BO distincte, Pro absent/réapparu, ordre ≠ id).
- Import manquant corrigé : `test_ck_nav_s2_canonical_v3` + `test_ck_nav_s2_root_sequences` dans `tests/__init__.py`.

## Résultats

```text
0 failed, 0 error(s) of 72 tests
tags: dorevia_ck_nav_s2,dorevia_ck_nav_catalogue,dorevia_ck_nav_v1,
      dorevia_ck_nav_communaute,dorevia_ck_nav_axe_b,dorevia_ck_marketone_nav_sync
db jetable détruite après coup
```

## Hors périmètre (inchangé)

Réserves Garant R1/R5 ; pas de refonte générale `nav_sync.py` ; pas de push/PR/deploy.
