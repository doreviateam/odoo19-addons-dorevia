# TICKET_DEV — `dorevia_cash_guard` V1.2

## Solde projeté depuis factures ouvertes

*Interface utilisateur : colonne **Projection** (`projected_balance`), colonne **État** (Constaté / Situation / Prévisionnel).*

**ID** : `CG-V1.2-01-PROJECTED-BALANCE-FROM-OPEN-INVOICES`  
**Module** : `dorevia_cash_guard`  
**Priorité** : P0  
**Statut** : À implémenter  
**Date de rédaction** : 2026-05-10  
**Dépend de** : V1.1 validée — solde de trésorerie constaté, périodicité, suivi de trésorerie

**Périmètre explicite** : pas d’ouverture ni d’intégration du budget, des devis, ni des simulations avancées dans ce ticket.

**Référence temporelle** : tout le raisonnement Cash Guard V1.2 s’appuie sur la **date de situation** du point (`situation_date`), pas sur la seule date du jour serveur. Les soldes constatés, les dates projetées et les statuts doivent être cohérents avec cette date de lecture.

---

## 1. Contexte

La V1.1 permet de calculer un **solde de trésorerie constaté** à une date de situation, à partir des journaux de trésorerie sélectionnés :

```text
Trésorerie constatée = banques + caisse / espèces
```

Le suivi de trésorerie affiche aujourd’hui une trajectoire simple par période :

```text
Période | Début | Fin | État | Solde | Statut
```

Cette lecture donne le solde constaté / rejoué / projeté selon la période, mais elle ne tient pas encore compte automatiquement des factures ouvertes.

Or les factures validées non payées constituent le premier niveau fiable du prévisionnel :

> **Prévisionnel engagé = factures ouvertes validées dans Odoo.**

---

## 2. Objectif

Ajouter une colonne **Projection** dans le suivi de trésorerie, calculée à partir du solde constaté et des factures ouvertes validées.

Doctrine V1.2 :

```text
Solde = trésorerie constatée à date de situation
Projection = solde + impact des factures validées ouvertes à leur date d’échéance (projetée)
```

« À date » signifie **à la date de situation** du point, alignée sur le calcul V1.1 du solde constaté — pas une lecture implicite sur la date serveur seule.

Le but est de fournir une première projection automatique, objective et non probabiliste.

---

## 3. Périmètre fonctionnel

### Inclus

Inclure dans le solde projeté :

- factures client validées non payées ;
- factures fournisseur validées non payées ;
- factures partiellement payées, pour leur montant résiduel uniquement ;
- avoirs validés ouverts, avec le bon sens de trésorerie ;
- factures échues non payées, traitées comme exigibles immédiatement à la date de situation.

### Exclus

Exclure du solde projeté V1.2 :

- devis ;
- commandes non facturées ;
- factures brouillon / à valider échues ;
- budget management ;
- flux attendus issus du budget ;
- simulations avancées ;
- matching intelligent ;
- recommandations IA.

---

## 4. Règles métier

### 4.1 Factures validées ouvertes

Une facture validée ouverte devient un flux prévisionnel engagé.

**Facture client**

```text
Facture client validée non payée
→ encaissement attendu
→ impact positif sur le solde projeté
```

**Facture fournisseur**

```text
Facture fournisseur validée non payée
→ décaissement attendu
→ impact négatif sur le solde projeté
```

**Montant**

Utiliser le montant résiduel :

```text
amount_residual
```

ou le champ Odoo 19 équivalent fiable pour le reste dû.

Ne jamais utiliser le montant total si la facture est partiellement payée.

---

### 4.2 Date d’intégration

Le solde projeté s’appuie sur une **date de référence échéance** pour chaque facture, puis la borne à la date de situation.

**Fallbacks si les dates Odoo sont vides** (ne pas perdre une facture ouverte pour autant) :

- si `invoice_date_due` est vide → utiliser `invoice_date` ;
- si `invoice_date_due` et `invoice_date` sont vides → utiliser `situation_date` comme ancrage minimal.

Formule unique V1.2 :

```text
reference_due = invoice_date_due or invoice_date or situation_date
projected_date = max(reference_due, situation_date)
```

Conséquences :

- une facture échue avant la date de situation est traitée comme **exigible à la date de situation** (`projected_date = situation_date`) ;
- une facture validée échue non payée ne disparaît pas du projeté.

---

### 4.3 Factures à valider

Les factures à valider ne font pas partie du prévisionnel engagé.

Règles V1.2 :

| Cas                                    | Traitement                     |
| -------------------------------------- | ------------------------------ |
| Facture à valider avec échéance passée | ignorée                        |
| Facture à valider avec échéance future | exclue du solde projeté engagé |
| Facture à valider sans échéance        | ignorée                        |

Une lecture « à confirmer » pourra être ajoutée plus tard, mais elle est hors périmètre de ce ticket.

---

### 4.4 Factures payées

Les factures payées ne doivent pas alimenter le solde projeté.

Raison :

> elles sont déjà intégrées dans le solde de trésorerie constaté via les journaux de trésorerie.

Règle :

```text
Facture payée = exclue du projeté
```

---

### 4.5 Factures rapprochées

Une facture payée et rapprochée est considérée comme constatée.

Règle :

```text
Facture rapprochée = déjà constatée = exclue du projeté
```

---

### 4.6 Avoirs

Les avoirs doivent être traités avec le bon sens de trésorerie.

| Type                       | Sens cash                           |
| -------------------------- | ----------------------------------- |
| Avoir client ouvert        | sortie / diminution d’encaissement  |
| Avoir fournisseur ouvert   | entrée / diminution de décaissement |

Le traitement peut être minimal en V1.2, mais ne doit pas inverser les signes.

---

## 5. Modèle de données

### 5.1 Modèle de suivi de période

Le modèle de ligne de suivi, actuellement utilisé pour l’onglet **Suivi de trésorerie**, doit recevoir un champ supplémentaire.

Champ à ajouter :

| Champ               | Type     | Description                                                            |
| ------------------- | -------- | ---------------------------------------------------------------------- |
| `projected_balance` | Monetary | Projection à fin de période après intégration des factures ouvertes |

Libellé UI :

```text
Projection
```

Colonnes cible :

```text
Période | Début | Fin | État | Solde | Projection | Statut
```

### 5.2 Optionnel : agrégats factures

Si utile pour debug ou future UX, ajouter des champs techniques non affichés ou affichés plus tard :

| Champ                    | Type     | Description                                                    |
| ------------------------ | -------- | -------------------------------------------------------------- |
| `invoice_inflow_amount`  | Monetary | Encaissements projetés issus des factures client ouvertes       |
| `invoice_outflow_amount` | Monetary | Décaissements projetés issus des factures fournisseur ouvertes |

Non obligatoire en UI V1.2.

---

## 6. Source Odoo

Les factures sont à lire depuis `account.move`.

**Critère principal d’« ouvert »** (évite les écarts selon les variantes de `payment_state` entre versions ou modules) :

```text
state = 'posted'
amount_residual != 0
```

Une facture **postée** avec un **résiduel non nul** est ouverte au sens projection ; le résiduel est la donnée métier de projection.

Le champ `payment_state` peut servir de **contrôle** ou de filtre secondaire (ex. exclure explicitement `reversed` si pertinent), mais **ne doit pas remplacer** le couple `posted` + `amount_residual`.

Filtres attendus sur le périmètre document :

```text
move_type in ('out_invoice', 'in_invoice', 'out_refund', 'in_refund')
state = 'posted'
amount_residual != 0
company_id = guard.company_id
```

Les dates d’échéance / facture sont gérées selon §4.2 (fallbacks + `projected_date`).

Les factures brouillon doivent être exclues :

```text
state != 'posted'
→ exclu
```

---

## 7. Calcul du solde projeté

### 7.1 Point de départ

Le calcul démarre du solde de trésorerie **constaté à la date de situation** :

```text
running_projected_balance = observed_balance
```

### 7.2 Factures à intégrer

Pour chaque facture ouverte (cf. §6), avec les fallback §4.2 :

```text
reference_due = invoice_date_due or invoice_date or situation_date
projected_date = max(reference_due, situation_date)
```

La facture est rattachée à la période de suivi contenant `projected_date`.

Selon le type :

```text
Facture client → +amount_residual
Facture fournisseur → -amount_residual
Avoir client → -amount_residual
Avoir fournisseur → +amount_residual
```

### 7.3 Propagation du solde projeté

Le solde projeté est cumulatif.

Exemple :

```text
Période 1 :
Projection = observed_balance + factures de période 1

Période 2 :
Projection = projection période 1 + factures de période 2

Période N :
Projection = projection période N-1 + factures de période N
```

### 7.4 Règles complémentaires V1.2

- Cash Guard raisonne toujours à partir de **`situation_date`**, jamais à partir de la date serveur seule (le solde constaté et les projections doivent être alignés sur cette date de lecture).
- Si `invoice_date_due` est vide → utiliser `invoice_date`.
- Si `invoice_date_due` et `invoice_date` sont vides → utiliser `situation_date` comme date de référence avant application du `max(..., situation_date)`.
- Une facture ouverte est identifiée **principalement** par `state = 'posted'` et `amount_residual != 0` (cf. §6).
- Le **statut de chaque ligne de période** est calculé sur son **`projected_balance`** (cf. §8).
- Le **statut global du point** : cf. §8.2 (minimum des `projected_balance` **forward**, hors historique pur avant la date de situation).

---

## 8. Statut de risque

### 8.1 Ligne de période

Sur chaque ligne du suivi de trésorerie, le statut se base sur le **solde projeté** de cette ligne :

```text
risk si projected_balance < 0
warning si projected_balance >= 0 et < alert_threshold
safe si projected_balance >= alert_threshold
```

### 8.2 Document de projection (statut global)

Le statut affiché sur le **document de projection** (`dorevia.cash.guard`) doit refléter le **minimum des `projected_balance`** sur les périodes **à partir de la date de situation** : inclure la ligne « Situation » (courante) et les lignes « Prévisionnel » ; **exclure** les lignes « Constaté » dont la période est entièrement **avant** la date de situation (historique pur). Appliquer les **mêmes seuils** que §8.1 à ce minimum.

Le dev doit mettre à jour **à la fois** les statuts de ligne **et** le champ `risk_status` du point selon cette règle — pas uniquement l’un des deux, ni un minimum indifférencié sur tout l’exercice si cela masque un risque sur la trajectoire future.

Objectif :

> Cash Guard sert à anticiper. Le statut doit refléter la trajectoire projetée, pas seulement le solde constaté.

Point à vérifier :

- si aucune facture ouverte n’existe, les `projected_balance` alignés sur le solde de colonne « Solde » donnent un comportement équivalent à V1.1 pour le risque.

---

## 9. UX attendue

### 9.1 Onglet Suivi de trésorerie

Colonnes cible :

```text
Période
Début
Fin
État
Solde
Projection
Statut
```

Sens :

| Colonne       | Signification                                         |
| ------------- | ----------------------------------------------------- |
| Solde         | solde de trésorerie constaté / rejoué sur la période |
| Projection   | solde après prise en compte des factures ouvertes à leur date d’échéance |
| Statut        | statut calculé sur la projection de la ligne (cf. §8) |

### 9.2 Vocabulaire

Valeurs de la colonne **État** :

```text
Constaté
Situation
Prévisionnel
```

### 9.3 Aucune lecture devis

Ne pas afficher de devis, ni de prévision commerciale probable.

---

## 10. Exemple attendu

Contexte :

```text
Date de situation : 09/05/2026
Solde de trésorerie constaté : 2 520 €
Seuil d’alerte : 3 000 €
```

Facture client validée non payée :

```text
Montant résiduel : 300 €
Date d’échéance : 20/05/2026
```

Résultat attendu :

| Période               | État         |   Solde | Projection | Statut  |
| --------------------- | ------------ | ------: | ---------: | ------- |
| Semaine 09/05 → 15/05 | Situation    | 2 520 € |    2 520 € | Warning |
| Semaine 16/05 → 22/05 | Prévisionnel | 2 520 € |    2 820 € | Warning |

Si seuil = 2 000 € :

| Période       | Projection | Statut |
| ------------- | ---------: | ------ |
| 16/05 → 22/05 |    2 820 € | Safe   |

---

## 11. Tests attendus

Créer ou compléter une suite de tests :

```text
tests/test_cash_guard_projected_invoices.py
```

### Cas 1 — Facture client ouverte future

Données :

- `observed_balance` = 2 520 €
- facture client posted non payée
- `amount_residual` = 300 €
- `due_date` future

Attendu :

```text
projected_balance augmente de 300 € à la période d’échéance
```

### Cas 2 — Facture fournisseur ouverte future

Données :

- facture fournisseur posted non payée
- `amount_residual` = 500 €
- `due_date` future

Attendu :

```text
projected_balance diminue de 500 € à la période d’échéance
```

### Cas 3 — Facture partiellement payée

Données :

- facture client total 1 000 €
- déjà payé 600 €
- résidu 400 €

Attendu :

```text
seuls 400 € alimentent le solde projeté
```

### Cas 4 — Facture échue non payée

Données :

- `due_date` < `situation_date`
- facture validée ouverte

Attendu :

```text
facture intégrée à la date de situation
```

### Cas 5 — Facture payée

Données :

- facture postée soldée (`amount_residual` = 0), ou équivalent métier « payée »

Attendu :

```text
aucun impact sur projected_balance
```

### Cas 6 — Facture brouillon / à valider

Données :

- facture state draft
- `due_date` passée ou future

Attendu :

```text
aucun impact sur projected_balance
```

### Cas 7 — Avoir client

Données :

- avoir client ouvert

Attendu :

```text
impact négatif sur projected_balance
```

### Cas 8 — Avoir fournisseur

Données :

- avoir fournisseur ouvert

Attendu :

```text
impact positif sur projected_balance
```

### Cas 9 — Statut basé sur solde projeté

Créer un cas où :

```text
Solde constaté safe
mais solde projeté passe sous seuil ou sous zéro
```

Attendu :

```text
le statut du point et des lignes reflète le solde projeté (cf. §8 : ligne vs minimum forward)
```

---

## 12. Scénario manuel de recette

Créer :

```text
docs/SCENARIO_MANUEL_V1_2_FACTURES_OUVERTES.md
```

Scénario minimal :

1. Créer ou utiliser un document de projection avec date de situation, journaux Banque + Caisse, solde constaté connu, périodicité semaine.
2. Créer une facture client validée non payée avec échéance future.
3. Actualiser le point.
4. Vérifier que la **Projection** augmente à la période d’échéance.
5. Créer une facture fournisseur validée non payée.
6. Vérifier que la **Projection** diminue à la période d’échéance.
7. Payer une facture.
8. Vérifier qu’elle disparaît du projeté après actualisation.
9. Créer une facture brouillon / à valider.
10. Vérifier qu’elle n’impacte pas le solde projeté.

---

## 13. Garde-fous

- Ne pas substituer la date serveur à la **date de situation** pour les règles V1.2 (cohérence avec le solde constaté).
- Ne pas intégrer les devis.
- Ne pas intégrer les factures brouillon.
- Ne pas intégrer le budget.
- Ne pas intégrer les simulations dans ce ticket.
- Ne pas créer automatiquement de lignes `dorevia.cash.guard.line` pour les factures si ce n’est pas nécessaire.
- Préférer un calcul agrégé du solde projeté depuis `account.move`.
- Éviter les doublons.
- Ne pas reprojeter une facture payée (résiduel nul).
- Ne pas exposer de complexité de rapprochement bancaire dans l’UX V1.2.

---

## 14. Question technique ouverte

Décider si les factures ouvertes alimentent :

1. directement les lignes de suivi période (`projected_balance`) par calcul agrégé ;
2. ou des lignes de flux Cash Guard matérialisées.

**Recommandation V1.2** :

> Calcul agrégé direct depuis `account.move`, sans créer de lignes de flux automatiques.

Raison :

- éviter les doublons ;
- éviter une synchronisation complexe ;
- garder la source de vérité dans `account.move`.

Les lignes de flux manuelles restent réservées aux prévisions attendues et simulations.

---

## 15. Critères d’acceptation

Le ticket est validé si :

- une colonne **Projection** est visible dans le suivi de trésorerie ;
- les factures client validées ouvertes augmentent le solde projeté ;
- les factures fournisseur validées ouvertes diminuent le solde projeté ;
- les montants résiduels sont utilisés ;
- les factures payées sont exclues ;
- les factures brouillon / à valider sont exclues ;
- les factures échues ouvertes sont traitées comme exigibles à la date de situation ;
- le statut de risque de **chaque ligne** se base sur son **solde projeté** ; le statut global du **point** sur le **minimum des soldes projetés à partir de la date de situation** (cf. §8) ;
- les tests automatiques passent ;
- un scénario manuel V1.2 est documenté.

---

## 16. Résumé produit

Ce ticket ajoute le premier niveau automatique de prévisionnel :

```text
Prévisionnel engagé = factures ouvertes
```

Il permet de lire :

```text
Solde de trésorerie constaté
+/- factures ouvertes à leur date d’échéance
= Projection
```

Formule courte :

> **Facture validée ouverte = prévisionnel engagé.  
> Facture payée = constaté.  
> Facture brouillon = ignorée.**
