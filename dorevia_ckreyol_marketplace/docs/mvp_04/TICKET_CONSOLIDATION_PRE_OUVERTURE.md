# TICKET — Consolidation pré-ouverture

## Objectif

Sécuriser le socle existant avant ouverture publique: corriger les ambiguïtés techniques/fonctionnelles, aligner la documentation et cadrer les preuves de parcours d'achat réel.

## Périmètre

- Données (unicité slugs).
- ACL / exposition publique.
- Canon URL documentaire.
- Tunnel marchand réel (panier -> checkout -> paiement).
- Robustesse installation/update/rendu sur thème.

## Priorités

### P1 — Contraintes de slugs collections / origines

Constat: `unique(website_id, slug)` ne protège pas les lignes `website_id IS NULL` en PostgreSQL.

À traiter pour:
- `ckr.shop.collection`
- `ckr.shop.origin`

Actions attendues:
- proposer correction par contrainte Python ou index unique partiel ;
- ajouter test associé ;
- éviter deux slugs globaux identiques.

Référence de décision: `docs/mvp_04/DECISION_SLUGS_COLLECTIONS_ORIGINES.md`.

### P2 — ACL / exposition publique des collections

Constat: intention documentaire de non-exposition publique ambiguë vis-à-vis de la lecture publique actuelle.

Actions attendues:
- clarifier si la lecture publique est voulue pour le rendu QWeb ;
- si oui, documenter explicitement le choix ;
- si non, ajouter record rules ou mécanisme limitant aux collections visibles/publiées.

Référence de décision: `docs/mvp_04/DECISION_ACL_COLLECTIONS.md`.

### P3 — Canon documentaire URL

Constat: contradictions entre documents et comportement réel.

Points à clarifier:
- `/collections/<slug>` vs redirection `/shop?ckr_collection=...` ;
- porte Catégories: `/shop/category/...` vs `ckr_category` ;
- statut des anciennes URLs marketing ;
- statut canonique réel de `/shop`.

Actions attendues:
- produire/mettre à jour un document canonique unique ;
- corriger les docs contradictoires pour éviter des développements basés sur une doctrine obsolète.

Référence canonique: `docs/mvp_04/CANON_URL_BOUTIQUE.md`.

### P4 — Tests tunnel marchand réel

Constat: couverture actuelle solide sur invariants front, insuffisante pour prouver l'achat réel.

Ajouter/cadrer les tests:
- ajout panier depuis fiche produit ;
- ajout panier depuis shop ;
- panier rempli ;
- modification quantité ;
- suppression ligne ;
- panier vide ;
- checkout invité ;
- checkout connecté ;
- adresse ;
- livraison ;
- paiement ;
- confirmation commande ;
- email commande ;
- mobile.

Objectif: prouver qu'un client peut effectivement acheter.

### P5 — Installation / update / rendu `/shop`

Contexte: dépendance forte au DOM `theme_classic_store`.

Ajouter une vérification systématique:
- installation ;
- mise à jour `-u` ;
- rendu `/shop` ;
- rendu home ;
- rendu panier ;
- absence d'erreur serveur.

Objectif: limiter les casses XPath/thème lors des évolutions.

## Doctrine de cette passe

À éviter:
- nouvelle refonte home ;
- nouvelle refonte shop ;
- nouvelle doctrine images ;
- nouvelle fonctionnalité communautaire ;
- extension B2B complète ;
- marketplace producteurs ;
- recettes communautaires ;
- nouveaux écrans non nécessaires.

À faire:
- consolider ;
- documenter ;
- corriger les ambiguïtés ;
- sécuriser le tunnel marchand ;
- préparer l'ouverture publique de manière réaliste.

## Critère de réussite

La passe est réussie si:
- l'état pré-ouverture est documenté ;
- les snippets mûrs sont créés ;
- ce ticket consolidation existe et est suivi ;
- les risques slugs / ACL / canon URL sont clarifiés ;
- le périmètre tests panier / checkout est cadré ;
- aucune nouvelle divergence documentaire n'est introduite.
