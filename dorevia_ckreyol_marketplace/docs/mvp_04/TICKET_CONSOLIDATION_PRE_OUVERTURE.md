# TICKET — Consolidation pré-ouverture

**ID** : `CONSOLIDATION-PRE-OUVERTURE`  
**Statut** : À lancer  
**Priorité** : P0 / P1  
**Module** : `dorevia_ckreyol_marketplace`  
**Périmètre** : C-Kreyol — socle e-commerce Odoo 19 CE  
**Type** : Consolidation technique, documentaire et fonctionnelle

---

## Objectif

Sécuriser le socle existant avant ouverture publique : corriger les ambiguïtés techniques/fonctionnelles, aligner la documentation et cadrer les preuves de parcours d'achat réel.

Le module CK dispose désormais d’un socle front/catalogue avancé. Cette passe vise à consolider ce niveau de maturité avant d’ouvrir une nouvelle phase projet.

---

## Périmètre

Inclus :

- Données : unicité des slugs.
- ACL / exposition publique.
- Canon URL documentaire.
- Tunnel marchand réel : panier → checkout → paiement.
- Robustesse installation / update / rendu sur thème.
- Documentation de décision associée.

Hors périmètre :

- refonte home ;
- refonte shop ;
- nouvelle doctrine images ;
- fonctionnalité communautaire ;
- extension B2B complète ;
- marketplace producteurs ;
- recettes communautaires ;
- nouveaux écrans non nécessaires.

---

## Priorités

### P1 — Contraintes de slugs collections / origines

Constat : `unique(website_id, slug)` ne protège pas les lignes `website_id IS NULL` en PostgreSQL.

À traiter pour :

- `ckr.shop.collection`
- `ckr.shop.origin`

Actions attendues :

- proposer correction par contrainte Python ou index unique partiel ;
- ajouter test associé ;
- éviter deux slugs globaux identiques.

Référence de décision :

- `docs/mvp_04/DECISION_SLUGS_COLLECTIONS_ORIGINES.md`

Critère GO :

- deux collections ou origines globales ne peuvent pas partager le même slug ;
- le comportement multi-site est explicitement documenté ;
- un test couvre le cas `website_id IS NULL`.

---

### P2 — ACL / exposition publique des collections

Constat : intention documentaire de non-exposition publique ambiguë vis-à-vis de la lecture publique actuelle.

Actions attendues :

- clarifier si la lecture publique est voulue pour le rendu QWeb ;
- si oui, documenter explicitement le choix ;
- si non, ajouter record rules ou mécanisme limitant aux collections visibles/publiées.

Référence de décision :

- `docs/mvp_04/DECISION_ACL_COLLECTIONS.md`

Critère GO :

- la lecture publique de `ckr.shop.collection` est soit assumée et documentée, soit restreinte ;
- il n’y a plus de contradiction entre code, ACL et documentation ;
- le rendu public de la boutique reste fonctionnel.

---

### P3 — Canon documentaire URL

Constat : contradictions entre documents et comportement réel.

Points à clarifier :

- `/collections/<slug>` vs redirection `/shop?ckr_collection=...` ;
- porte Catégories : `/shop/category/...` vs `ckr_category` ;
- statut des anciennes URLs marketing ;
- statut canonique réel de `/shop`.

Actions attendues :

- produire / mettre à jour un document canonique unique ;
- corriger les docs contradictoires ;
- éviter des développements basés sur une doctrine obsolète.

Référence canonique :

- `docs/mvp_04/CANON_URL_BOUTIQUE.md`

Critère GO :

- un seul document fait autorité sur les URLs boutique ;
- les anciennes doctrines contradictoires sont corrigées ou explicitement marquées comme obsolètes ;
- les routes, redirections et liens front sont alignés.

---

### P4 — Tests tunnel marchand réel

Constat : couverture actuelle solide sur invariants front, insuffisante pour prouver l'achat réel.

Tests à ajouter ou cadrer :

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

Objectif : prouver qu'un client peut effectivement acheter.

Critère GO :

- le périmètre de tests panier / checkout est formalisé ;
- au minimum, un scénario d’achat complet est décrit ;
- si l’automatisation complète n’est pas encore possible, les limites sont documentées ;
- les points bloquants avant ouverture publique sont identifiés.

---

### P5 — Installation / update / rendu `/shop`

Contexte : dépendance forte au DOM `theme_classic_store`.

Ajouter une vérification systématique :

- installation ;
- mise à jour `-u` ;
- rendu `/shop` ;
- rendu home ;
- rendu panier ;
- absence d'erreur serveur.

Objectif : limiter les casses XPath / thème lors des évolutions.

Critère GO :

- une commande ou procédure de vérification est documentée ;
- le rendu home / shop / panier est contrôlé après update ;
- les erreurs XPath / QWeb / assets sont détectables rapidement.
- référence d'exécution : `docs/mvp_04/PROCEDURE_SMOKE_INSTALL_UPDATE.md`.

---

## Livrables attendus

Créer ou mettre à jour :

- `docs/mvp_04/ETAT_PRE_OUVERTURE_COMMERCIALE.md`
- `docs/mvp_04/TICKET_CONSOLIDATION_PRE_OUVERTURE.md`
- `docs/mvp_04/DECISION_SLUGS_COLLECTIONS_ORIGINES.md`
- `docs/mvp_04/DECISION_ACL_COLLECTIONS.md`
- `docs/mvp_04/CANON_URL_BOUTIQUE.md`
- `docs/mvp_04/PROCEDURE_SMOKE_INSTALL_UPDATE.md`

Capitalisation design system/snippets : reportée en lot suivant (hors priorité de sécurisation du socle).

---

## Doctrine de cette passe

À éviter :

- nouvelle refonte home ;
- nouvelle refonte shop ;
- nouvelle doctrine images ;
- nouvelle fonctionnalité communautaire ;
- extension B2B complète ;
- marketplace producteurs ;
- recettes communautaires ;
- nouveaux écrans non nécessaires.

À faire :

- consolider ;
- documenter ;
- corriger les ambiguïtés ;
- sécuriser le tunnel marchand ;
- préparer l'ouverture publique de manière réaliste.

---

## Critère de réussite

La passe est réussie si :

- l'état pré-ouverture est documenté ;
- ce ticket consolidation existe et est suivi ;
- les risques slugs / ACL / canon URL sont clarifiés ;
- le périmètre tests panier / checkout est cadré ;
- aucune nouvelle divergence documentaire n'est introduite.

---

## Décision

Avant d’ouvrir une nouvelle phase fonctionnelle ou éditoriale, CK entre dans une passe de consolidation pré-ouverture.

Le projet ne cherche pas à étendre le périmètre à ce stade, mais à stabiliser le socle existant : données, sécurité d’exposition, canon URL, patterns UX mûrs, robustesse d’installation et preuve de parcours d’achat réel.
