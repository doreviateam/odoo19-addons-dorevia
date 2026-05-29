# Mémo raffinement — qualité comptable et analytique

## 1. Intention

Ce mémo conserve une piste de raffinement à traiter après les paliers cockpit déjà engagés.

L'objectif est de transformer certains contrôles ponctuels en indicateurs permanents de qualité des données, afin de sécuriser la lecture du cockpit GLC et les travaux de contrôle de gestion.

Deux KPI sont particulièrement pertinents :

- le taux de couverture analytique ;
- le taux de lettrage.

Un troisième besoin est à instruire avec le développeur :

- la lecture du statut de paiement des factures dans le cockpit.

Ces indicateurs ne remplacent pas les KPI d'exploitation. Ils servent à mesurer si les données comptables sont suffisamment propres pour que les KPI d'exploitation soient fiables.

## 2. KPI 1 — taux de couverture analytique

### 2.1 Question métier

Est-ce que les factures, avoirs et lignes comptables d'exploitation sont correctement rattachés à un axe analytique exploitable ?

### 2.2 Définition proposée

```text
Taux de couverture analytique =
Nombre de pièces comptables couvertes analytiquement
/
Nombre total de pièces comptables devant être couvertes analytiquement
```

Une pièce est considérée comme couverte si toutes ses lignes métier pertinentes disposent d'une distribution analytique ou d'une écriture analytique exploitable.

### 2.3 Périmètre recommandé

Inclure :

- factures clients ;
- factures fournisseurs ;
- avoirs clients ;
- avoirs fournisseurs ;
- lignes de produits et de charges.

Exclure :

- lignes de tiers ;
- lignes de banque ;
- lignes de TVA ;
- écritures purement bilan ;
- écritures de trésorerie sans portée analytique ;
- lignes techniques Odoo non exploitables par le cockpit.

### 2.4 Restitution attendue

Le module pourrait afficher :

- nombre de pièces contrôlées ;
- nombre de pièces couvertes ;
- taux de couverture ;
- nombre de pièces en anomalie ;
- liste actionnable des pièces à corriger ;
- détail des lignes sans analytique.

### 2.5 Seuils proposés

```text
Vert   : 100 %
Orange : 95 % à 99,99 %
Rouge  : < 95 % ou anomalie bloquante sur une période de clôture
```

Pour une période de clôture mensuelle, l'objectif cible doit rester 100 %.

### 2.6 Critères d'acceptation

- Le contrôle distingue les lignes métier des lignes techniques.
- Les comptes de bilan, banque, TVA et tiers ne polluent pas le taux.
- La liste des anomalies permet d'ouvrir rapidement la pièce concernée.
- Le contrôle peut être filtré par société, période, type de pièce et journal.
- Le KPI est lisible sans ambiguïté pour la MOA.

## 3. KPI 2 — taux de lettrage

### 3.1 Question métier

Est-ce que les comptes clients et fournisseurs sont correctement rapprochés avec leurs règlements ?

### 3.2 Définition proposée

```text
Taux de lettrage =
Montant des lignes tiers lettrées
/
Montant total des lignes tiers lettrables
```

Le taux peut aussi être décliné en nombre de lignes ou nombre de pièces, mais le montant est l'indicateur le plus utile pour le pilotage.

### 3.3 Périmètre recommandé

Inclure :

- comptes clients 411 ;
- comptes fournisseurs 401 ;
- autres comptes tiers si utilisés dans le suivi opérationnel.

Exclure :

- comptes de produits ;
- comptes de charges ;
- comptes de TVA ;
- comptes bancaires ;
- comptes analytiques ;
- écritures non postées.

### 3.4 Restitution attendue

Le module pourrait afficher :

- taux de lettrage clients ;
- taux de lettrage fournisseurs ;
- montant client non lettré ;
- montant fournisseur non lettré ;
- nombre de pièces non lettrées ;
- ancienneté des montants non lettrés ;
- liste actionnable des écritures ou pièces à traiter.

### 3.5 Seuils proposés

```text
Vert   : taux élevé et absence de reliquats anciens significatifs
Orange : taux incomplet ou reliquats récents à suivre
Rouge  : montants anciens non lettrés ou écart significatif
```

Les seuils exacts devront être arbitrés avec la MOA selon le rythme de saisie, de paiement et de rapprochement bancaire.

### 3.6 Critères d'acceptation

- Le contrôle sépare clairement clients et fournisseurs.
- Le calcul repose sur les lignes tiers lettrables, pas sur les lignes de charge ou de produit.
- Les montants non lettrés sont actionnables.
- L'ancienneté est visible pour prioriser les corrections.
- Le KPI ne modifie aucune écriture comptable.

## 4. Positionnement dans le module

Ces indicateurs peuvent être regroupés dans un futur espace :

```text
Pilotage GLC → Qualité des données
```

ou dans un onglet dédié du cockpit :

```text
Contrôles qualité
```

La préférence métier est de ne pas mélanger ces KPI avec les KPI d'exploitation principaux. Ils doivent être visibles comme des contrôles de fiabilité.

## 5. Besoin complémentaire — suivi paiement des factures

### 5.1 Problème constaté

Le cockpit affiche aujourd'hui des chiffres bruts d'exploitation et de trésorerie, mais il ne permet pas encore de distinguer clairement :

- ce qui est facturé mais non payé ;
- ce qui est partiellement payé ;
- ce qui est en cours de traitement de paiement ;
- ce qui est payé et réconcilié ;
- ce qui reste à encaisser côté clients ;
- ce qui reste à décaisser côté fournisseurs.

Cette information est plus opérationnelle que le seul taux de lettrage. Elle doit être spécifiée au développeur comme un besoin cockpit à part entière.

### 5.2 Question métier

Parmi les montants comptabilisés, quelle part est réellement payée, encore ouverte, partiellement réglée ou en cours de traitement ?

### 5.3 Objectif fonctionnel

Ajouter une lecture du cycle de paiement des factures pour éviter de confondre :

- résultat analytique ;
- trésorerie constatée ;
- reste à encaisser ;
- reste à payer ;
- factures en attente de traitement.

### 5.4 Restitution attendue

Un futur onglet cockpit pourrait être dédié au suivi des paiements :

```text
Tiers & paiements
```

ou :

```text
Suivi paiement
```

Il devrait afficher au minimum :

- factures clients émises ;
- factures clients payées ;
- factures clients partiellement payées ;
- factures clients ouvertes ;
- reste à encaisser ;
- factures fournisseurs reçues ;
- factures fournisseurs payées ;
- factures fournisseurs partiellement payées ;
- factures fournisseurs ouvertes ;
- reste à payer ;
- taux de lettrage clients ;
- taux de lettrage fournisseurs.

### 5.5 Statuts à distinguer

Le développeur devra vérifier les champs Odoo 19 disponibles, notamment :

- statut de paiement de la facture ;
- montant résiduel ;
- réconciliation complète ou partielle ;
- lignes tiers lettrées ;
- éventuel état de paiement en cours.

Statuts métier attendus :

```text
Payé
Partiellement payé
Non payé
En cours de paiement
Réconcilié
Non réconcilié
```

Les libellés exacts devront être alignés avec Odoo pour éviter une divergence entre statut fonctionnel et statut technique.

### 5.6 Règles de calcul à préciser

Pour les clients :

```text
Facturé client = total factures clients postées
Déjà encaissé = montant rapproché ou payé
Reste à encaisser = montant résiduel client
```

Pour les fournisseurs :

```text
Facturé fournisseur = total factures fournisseurs postées
Déjà payé = montant rapproché ou payé
Reste à payer = montant résiduel fournisseur
```

Le calcul doit être compatible avec :

- paiement partiel ;
- avoir ;
- facture non payée ;
- facture totalement payée ;
- réconciliation partielle ;
- multi-société ;
- filtre période.

### 5.7 Critères d'acceptation

- Le cockpit distingue exploitation, trésorerie et reste à payer / encaisser.
- Une facture comptabilisée mais non payée apparaît dans les montants ouverts.
- Une facture partiellement payée apparaît avec son reste dû.
- Une facture totalement réglée ne pollue plus les montants ouverts.
- Les avoirs sont correctement pris en compte.
- Le taux de lettrage reste un KPI de qualité, distinct du montant ouvert.
- Les montants sont filtrables par société, période et type de tiers.
- Aucun calcul ne modifie les écritures comptables.

### 5.8 Vigilance

Ce besoin ne doit pas être mélangé avec le calcul du réalisé analytique.

Une recette comptabilisée peut ne pas être encaissée. Une dépense comptabilisée peut ne pas être payée. Le cockpit doit donc afficher ces informations comme une couche de lecture complémentaire, pas comme une correction des KPI d'exploitation.

## 6. Valeur métier

Le taux de couverture analytique garantit que le cockpit peut ventiler correctement le réalisé par activité.

Le taux de lettrage garantit que les comptes tiers sont propres et que les factures sont correctement rapprochées avec les règlements.

Le suivi paiement permet de comprendre ce qui reste réellement à encaisser ou à payer, au-delà du résultat analytique comptabilisé.

Ensemble, ces indicateurs répondent à une même logique :

```text
Avant de piloter, vérifier que les données de pilotage sont fiables.
```

## 7. Points de vigilance

- Ne pas bloquer trop tôt les utilisateurs si le processus de saisie n'est pas stabilisé.
- Préférer d'abord une alerte et une liste d'anomalies actionnable.
- Ne pas confondre anomalie analytique et anomalie de lettrage.
- Ne pas inclure les flux bilan ou trésorerie dans la couverture analytique.
- Documenter clairement les exclusions pour éviter les incompréhensions MOA.
- Ne pas assimiler montant comptabilisé et montant payé.
- Ne pas confondre paiement, lettrage et réconciliation bancaire.

## 8. Proposition de lot futur

**Ticket de cadrage :** [TICKET_COCKPIT_QUALITE_COMPTABLE_ANALYTIQUE_SUIVI_PAIEMENT.md](./TICKET_COCKPIT_QUALITE_COMPTABLE_ANALYTIQUE_SUIVI_PAIEMENT.md) · **Recette :** [RECETTE_MANUELLE_COCKPIT_QUALITE_PAIEMENT.md](./recette/RECETTE_MANUELLE_COCKPIT_QUALITE_PAIEMENT.md)

Nom possible :

```text
Lot Qualité comptable, analytique et suivi paiement
```

Contenu minimal :

- KPI de couverture analytique ;
- liste des pièces sans analytique ;
- KPI de lettrage clients ;
- KPI de lettrage fournisseurs ;
- liste des montants non lettrés ;
- suivi des factures clients ouvertes ;
- suivi des factures fournisseurs ouvertes ;
- reste à encaisser ;
- reste à payer ;
- filtres période / société / type de pièce ;
- documentation MOA des règles de calcul.

## 9. Décision à reprendre plus tard

À arbitrer lors du raffinement :

- simple indicateur ou contrôle bloquant ;
- périmètre exact des pièces concernées ;
- seuils couleur ;
- emplacement UI ;
- niveau de détail attendu ;
- lien éventuel avec une procédure de clôture mensuelle.
- niveau de détail du suivi paiement ;
- traitement des paiements partiels et avoirs ;
- distinction entre statut Odoo de paiement et lettrage comptable.
