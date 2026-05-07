# CK — Décision unicité slugs collections/origines

## Contexte

Les contraintes SQL `unique(website_id, slug)` ne couvrent pas correctement les cas où `website_id` vaut `NULL` (comportement PostgreSQL sur les `NULL`).

## Décision de consolidation

Garantir l'unicité des slugs sur deux niveaux:

1. Unicité par site quand `website_id` est défini.
2. Unicité globale quand `website_id` est `NULL`.

## Option technique privilégiée

- Conserver la contrainte métier existante.
- Ajouter une validation Python explicite (`@api.constrains`) sur `slug` + `website_id` pour bloquer les doublons globaux (`website_id = False`) et les doublons par site.
- En complément possible: index SQL partiels pour robustesse base.

## Modèles concernés

- `ckr.shop.collection`
- `ckr.shop.origin`

## Plan de tests attendu

- Création de deux slugs globaux identiques -> refus attendu.
- Création de deux slugs identiques sur même site -> refus attendu.
- Création de deux slugs identiques sur deux sites différents -> autorisé si doctrine multi-site le permet.
- Mise à jour d'un slug existant vers un doublon -> refus attendu.

## Critère de validation

- Impossible d'obtenir deux slugs globaux identiques.
- Comportement stable et prévisible en import/migration.
- Message d'erreur explicite côté back-office.
