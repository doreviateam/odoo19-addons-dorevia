# CK — Décision ACL collections (pré-ouverture)

## Contexte

Une ambiguïté existe entre l'intention documentaire ("pas d'exposition publique large") et l'ACL actuelle qui permet une lecture publique de `ckr.shop.collection`.

## Décision de consolidation

Maintenir une lecture publique **strictement utilitaire front** pour le rendu QWeb, mais limiter l'exposition aux enregistrements publiables/visibles boutique.

## Règles cibles

- Lecture publique autorisée seulement pour:
  - collections publiées ;
  - collections visibles sur le site courant.
- Aucune donnée métier sensible ne doit être exposée au public.
- Les usages back-office complets restent réservés aux groupes internes.

## Actions à exécuter

1. Auditer ACL + record rules de `ckr.shop.collection`.
2. Si nécessaire, ajouter une record rule publique filtrée (publie/site courant).
3. Documenter explicitement la raison de la lecture publique résiduelle (rendu boutique/QWeb).
4. Ajouter tests de non-régression sécurité (public vs utilisateur interne).

## Critère de validation

- Un visiteur public ne lit que les collections destinées à l'affichage boutique.
- Aucun effet de bord sur le rendu homepage/shop.
- La décision est traçable et cohérente entre code, ACL et documentation.
