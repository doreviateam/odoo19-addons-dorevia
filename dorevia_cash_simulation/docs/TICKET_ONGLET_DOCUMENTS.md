# Ticket — Évolution UX Cash Guard : onglet `Documents` et intégration des simulations

**Modules concernés** :

* `dorevia_cash_guard`
* `dorevia_cash_simulation`
* `dorevia_cash_simulation_purchase`

**Type** : évolution UX / process
**Priorité** : P1
**Statut** : à implémenter
**Contexte** : suite refactoring V1.0.1 / V1.1 — scénario porté par Cash Guard

---

## 1. Contexte

Après le refactoring de `dorevia_cash_simulation`, la simulation est désormais portée par la projection Cash Guard, et non plus par les objets `sale.order` ou `purchase.order`.

La projection Cash Guard peut donc contenir un scénario de simulation composé de :

* devis clients sélectionnés explicitement ;
* commandes achat sélectionnées explicitement ;
* documents encore soumis aux règles d'éligibilité.

Aujourd'hui, l'onglet `Facturation` affiche les factures réelles / quasi réelles qui expliquent la projection.

Mais en mode simulation, les devis clients simulés et les commandes achat simulées participent également à la lecture de la projection affichée.

Il faut donc faire évoluer l'onglet pour qu'il devienne une liste unique des documents qui expliquent la projection courante.

---

## 2. Décision produit

Renommer l'onglet :

```text
Facturation → Documents
```

Doctrine cible :

```text
Projection = trajectoire de trésorerie par période
Documents = documents qui expliquent la projection affichée
Notes = contexte libre
```

---

## 3. Comportement attendu

### 3.1 Mode simulation OFF

Lorsque `Mode simulation = False` :

```text
Documents = factures réelles / quasi réelles uniquement
```

L'onglet `Documents` affiche les documents actuellement affichés dans l'onglet `Facturation`, sans intégrer de devis ni de commandes achat simulées.

Les smart buttons simulation sont masqués ou à 0 selon le comportement existant.

---

### 3.2 Mode simulation ON

Lorsque `Mode simulation = True` :

```text
Documents = factures réelles + documents simulés retenus
```

L'onglet `Documents` doit afficher :

* les factures clients réelles / quasi réelles ;
* les factures fournisseurs réelles / quasi réelles ;
* les devis clients simulés retenus ;
* les commandes achat simulées retenues.

Important : seuls les documents simulés effectivement retenus dans le calcul doivent apparaître.

Un devis ou une commande achat sélectionné dans le M2M mais devenu non éligible ne doit pas impacter la projection. À arbitrer côté dev : il peut soit ne pas apparaître dans `Documents`, soit apparaître avec un statut d'exclusion si cela existe déjà. Pour cette évolution, la priorité est d'afficher les documents retenus dans la projection.

---

## 4. Types affichés

La distinction réel / simulation doit passer par la colonne existante `Type`.

Types attendus :

```text
Facture client
Facture fournisseur
Devis client simulé
Commande achat simulée
```

On n'ajoute pas de colonne `Nature` en V1.

La colonne `Type` suffit à distinguer clairement les documents.

---

## 5. Couleur / style

Les factures réelles conservent la couleur liée à leur statut ou niveau de risque :

```text
Risque
Tension
Confort
```

Les documents simulés doivent utiliser une couleur neutre :

```text
anthracite / noir
```

Objectif :

* ne pas colorer les hypothèses comme des flux réels ;
* éviter qu'un devis simulé apparaisse comme une facture en risque ;
* rendre les simulations visibles sans dramatiser leur statut.

Les documents simulés ne doivent donc pas être colorés en rouge/orange/vert selon les statuts `Risque`, `Tension`, `Confort`.

---

## 6. Données attendues pour les documents simulés

### 6.1 Devis client simulé

Pour un `sale.order` retenu dans la simulation :

| Champ liste | Valeur attendue |
| ----------- | --------------- |
| Statut | libellé neutre, par exemple `Simulation` |
| Période | période Cash Guard correspondant à `validity_date` |
| Document | numéro du devis |
| Partenaire | client |
| Type | `Devis client simulé` |
| Échéance | `sale.order.validity_date` |
| Retard | vide ou non applicable |
| Impact | `+ amount_total` |
| Échue | non applicable ou `Non` |
| Lien | ouverture du devis |

---

### 6.2 Commande achat simulée

Pour un `purchase.order` retenu dans la simulation :

| Champ liste | Valeur attendue |
| ----------- | --------------- |
| Statut | libellé neutre, par exemple `Simulation` |
| Période | période Cash Guard correspondant à `date_planned` |
| Document | numéro de la commande achat |
| Partenaire | fournisseur |
| Type | `Commande achat simulée` |
| Échéance | `purchase.order.date_planned` convertie en date |
| Retard | vide ou non applicable |
| Impact | `- amount_total` |
| Échue | non applicable ou `Non` |
| Lien | ouverture de la commande achat |

---

## 7. Règles d'éligibilité rappelées

### 7.1 Devis client simulé

Un devis client sélectionné est retenu si :

```text
state in ('draft', 'sent')
invoice_ids = False
company_id = cash_guard.company_id
currency_id = cash_guard.currency_id
validity_date renseignée
validity_date dans la période Cash Guard
```

### 7.2 Commande achat simulée

Une commande achat sélectionnée est retenue si :

```text
state in ('draft', 'sent')
invoice_ids = False
company_id = cash_guard.company_id
currency_id = cash_guard.currency_id
date_planned renseignée
date_planned dans la période Cash Guard
```

---

## 8. Onglets Cash Guard

Structure cible :

```text
Projection
Documents
Notes
```

L'ancien onglet `Facturation` devient `Documents`.

Pas d'onglet `Simulation` dédié pour le moment.

Raison : les documents simulés concernent directement la lecture de la projection courante. Ils doivent donc apparaître dans la même liste explicative que les factures réelles, mais avec un type et une couleur clairement distincts.

---

## 9. Règle sur `Réinitialiser`

Confirmer le comportement du bouton `Réinitialiser`.

Doctrine :

```text
Actualiser = recalculer la projection actuelle
Réinitialiser = repartir d'aujourd'hui en projection prudente
```

Comportement attendu de `Réinitialiser` :

```text
date_from / date début = date du jour
Mode simulation = False
Devis simulés vidés
Commandes achat simulées vidées
projection recalculée sans hypothèses
```

Ce comportement est cohérent avec la doctrine :

```text
Mode simulation OFF = scénario vidé = projection prudente
```

---

## 10. Critères de recette

Le ticket est considéré conforme si :

* l'onglet `Facturation` est renommé `Documents` ;
* en mode simulation OFF, l'onglet `Documents` affiche uniquement les factures réelles / quasi réelles ;
* en mode simulation ON, l'onglet `Documents` affiche les factures réelles + les devis clients simulés retenus + les commandes achat simulées retenues ;
* les devis clients simulés ont le type `Devis client simulé` ;
* les commandes achat simulées ont le type `Commande achat simulée` ;
* les documents simulés utilisent une couleur neutre anthracite / noir ;
* les documents simulés ne sont pas colorés comme `Risque`, `Tension` ou `Confort` ;
* les impacts sont correctement signés :
  * devis client simulé = positif ;
  * commande achat simulée = négatif ;
* les échéances utilisées sont correctes :
  * devis client = `validity_date` ;
  * achat = `date_planned` ;
* les liens d'ouverture vers les documents fonctionnent ;
* `Réinitialiser` remet la projection à aujourd'hui, désactive le mode simulation et vide les documents sélectionnés ;
* aucun document simulé ne crée de facture, écriture comptable, paiement ou mouvement bancaire.

---

## 11. Limites maintenues

Cette évolution ne change pas les limites actuelles :

```text
Les simulations impactent projected_balance et risk_status,
pas encore inflow_amount / outflow_amount.
```

Pas de conversion multi-devise.

Pas d'éclatement selon conditions de paiement.

Pas de nouvel onglet `Simulation` pour le moment.

---

## 12. Objectif produit

L'objectif est d'obtenir une lecture claire et unifiée :

```text
Je regarde la projection.
Je vais dans Documents.
Je vois tous les documents qui expliquent cette projection.
Si le mode simulation est OFF, je vois seulement le réel.
Si le mode simulation est ON, je vois le réel + les hypothèses retenues.
```

La simulation reste donc lisible, maîtrisée, et clairement distinguée des flux réels.
