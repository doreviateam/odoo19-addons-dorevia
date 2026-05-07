# CK — Décision ACL collections (pré-ouverture)

## Contexte

Une ambiguïté existe entre l'intention documentaire ("pas d'exposition publique large") et l'ACL actuelle qui permet une lecture publique de `ckr.shop.collection`.

## Décision de consolidation

Maintenir la lecture publique de `ckr.shop.collection` **strictement utilitaire front** (rendu QWeb/website_sale), avec filtrage systématique côté contrôleurs/services sur les collections visibles.

## Règles cibles

- Lecture publique autorisée seulement pour:
  - collections publiées ;
  - collections visibles sur le site courant.
- Aucune donnée métier sensible ne doit être exposée au public.
- Les usages back-office complets restent réservés aux groupes internes.

## Application dans cette passe

1. ACL publique conservée pour éviter toute régression front immédiate.
2. Décision explicitée : le rendu public passe par des domaines de visibilité (`active`, fenêtre de dates, site).
3. Le ticket de consolidation trace un audit complémentaire record rules + endpoints JSON/RPC.

## Arbitrages restants

- Faut-il ajouter une record rule publique stricte dès maintenant, ou après audit des chemins BO/front qui lisent `ckr.shop.collection` ?
- Faut-il distinguer davantage les usages `portal` et `public` (domaines différents) ?

## Critère de validation

- Un visiteur public ne lit que les collections destinées à l'affichage boutique.
- Aucun effet de bord sur le rendu homepage/shop.
- La décision est traçable et cohérente entre code, ACL et documentation.
