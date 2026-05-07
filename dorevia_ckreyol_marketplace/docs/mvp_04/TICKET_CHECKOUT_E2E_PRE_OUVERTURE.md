# TICKET — Checkout E2E pré-ouverture

**ID** : `CHECKOUT-E2E-PRE-OUVERTURE`  
**Statut** : En cours  
**Priorité** : P4 (bloquant ouverture publique)  
**Module** : `dorevia_ckreyol_marketplace`  
**Type** : Consolidation fonctionnelle marchande (preuve E2E)

---

## Objectif

Obtenir une preuve simple, vérifiable et reproductible qu’un client peut réellement acheter sur CK : de l’ajout panier jusqu’à la confirmation de commande.

Ce ticket cadre un **socle minimal GO ouverture**, sans chercher une couverture exhaustive dès cette première passe.

---

## Doctrine du lot

- Ce lot ne rouvre ni design, ni snippets, ni doctrine shop.
- Ce lot n’introduit pas de nouvelle fonctionnalité produit.
- Ce lot sert uniquement à valider le parcours marchand réel avant ouverture publique.

---

## 1) Cas nominal d’achat complet

### Scénario cible (E2E)

1. Ajouter au panier depuis une fiche produit.
2. Ajouter au panier depuis `/shop`.
3. Vérifier panier rempli.
4. Modifier une quantité.
5. Supprimer une ligne.
6. Passer en checkout invité.
7. Saisir une adresse valide.
8. Choisir un mode de livraison.
9. Payer avec un moyen de paiement en mode test.
10. Vérifier la confirmation commande.

### Critère GO nominal

- Le parcours s’exécute sans blocage.
- Une commande est créée en statut attendu.
- La page de confirmation est atteinte.

---

## 2) Cas d’échec minimum

### Cas E1 — Panier vide

- Accès checkout avec panier vide.
- Comportement attendu : repli propre (retour panier/shop), pas de 500, message compréhensible.

### Cas E2 — Adresse invalide ou incomplète

- Soumission checkout avec adresse invalide/incomplète.
- Comportement attendu : validation formulaire explicite, pas de crash, correction possible.

### Critère GO erreurs

- Les erreurs sont gérées côté UX et serveur.
- Aucun traceback bloquant.

---

## 3) Prérequis data / configuration

Avant exécution des tests :

- au moins un produit vendable ;
- produit stocké ou achetable selon configuration retenue ;
- transporteur configuré ;
- moyen de paiement test configuré ;
- taxes / fiscalité cohérentes ;
- website CK actif ;
- thème `theme_classic_store` chargé.

### Critère GO prérequis

- Tous les prérequis sont explicitement cochés avant lancement.
- Les valeurs de test (produits, transporteur, paiement) sont traçables.

---

## 4) Automatisation cible

### Minimum attendu

- Au moins un flux complet nominal automatisé.
- Tag dédié proposé : `dorevia_ckr_checkout_e2e`.
- Objectif : preuve binaire **“un client peut acheter”**.

### Recommandation d’implémentation

- Ajouter une suite `HttpCase` ciblée checkout dans `tests/`.
- Isoler les données minimales de test pour éviter les faux négatifs liés à l’environnement.
- Garder la suite déterministe (pas de dépendance cachée à des données manuelles BO).

### Critère GO automatisation

- Le test nominal passe de manière répétable.
- Le test est exécutable seul via son tag.

---

## 5) Smoke post-update obligatoire

Après `-u dorevia_ckreyol_marketplace`, vérifier :

- rendu `/` ;
- rendu `/shop` ;
- rendu `/shop/cart` ;
- rendu `/shop/checkout` ;
- logs sans 500 / QWeb / XPath.

### Critère GO smoke

- Aucun endpoint critique en erreur.
- Aucun traceback serveur bloquant pendant le smoke.

---

## Plan d’exécution proposé

### Étape A — Préflight (court)

- Vérifier prérequis data/config.
- Exécuter smoke post-update.

### Étape B — Recette manuelle nominale

- Exécuter le scénario complet 1→10.
- Capturer résultats (OK/KO + point de rupture).

### Étape C — Recette erreurs minimales

- Exécuter E1 et E2.
- Vérifier robustesse UX + serveur.

### Étape D — Automatisation minimale

- Implémenter et brancher `dorevia_ckr_checkout_e2e`.
- Exécuter en local/CI.

### Étape E — Décision

- GO pré-ouverture si nominal + erreurs minimales + smoke sont verts.
- Sinon : liste d’écarts bloquants, plan de correction court, nouvelle passe.

---

## Livrables attendus

- Ce ticket complété (statut, résultats, décision).
- Evidence d’exécution nominale (log ou PV court).
- Evidence des cas E1/E2.
- Commande d’exécution du tag `dorevia_ckr_checkout_e2e`.
- Statut smoke post-update consigné.

---

## Trace d’exécution (mise à jour continue)

### Pré-requis utilisés

- Website de test : `website.default_website` (CK actif).
- Produits de test : créés automatiquement dans la suite E2E.
- Thème attendu : `theme_classic_store` (pré-requis du module).
- Paiement/livraison : dépendants de la configuration de la base cible.

### Commandes à lancer

```bash
odoo -c /etc/odoo/odoo.conf -d <DB> -u dorevia_ckreyol_marketplace --stop-after-init
odoo -c /etc/odoo/odoo.conf -d <DB> --test-enable --stop-after-init --test-tags=dorevia_ckr_checkout_e2e
```

Smoke HTTP minimal:

```bash
curl -I "http://localhost:8069/"
curl -I "http://localhost:8069/shop"
curl -I "http://localhost:8069/shop/cart"
curl -I "http://localhost:8069/shop/checkout"
```

### Automatisation implémentée dans ce lot

- Fichier : `tests/test_ckr_checkout_e2e_pre_opening.py`
- Tag : `dorevia_ckr_checkout_e2e`
- Couverture:
  - nominal minimal (ajout panier, modification quantité, suppression ligne, progression checkout/payment/confirm sans 500) ;
  - E1 panier vide ;
  - E2 adresse invalide/incomplète.

### Résultats (à compléter après exécution environnement)

- Update module : TODO
- Smoke post-update : TODO
- Tag `dorevia_ckr_checkout_e2e` : TODO
- Décision GO / NO GO : TODO

---

## Critère de réussite global

Le lot est réussi si :

- le scénario nominal d’achat complet est validé ;
- les deux cas d’échec minimum sont maîtrisés ;
- au moins un flux complet est automatisé sous tag dédié ;
- le smoke post-update est vert ;
- la décision GO/NO GO ouverture est explicite et traçable.
