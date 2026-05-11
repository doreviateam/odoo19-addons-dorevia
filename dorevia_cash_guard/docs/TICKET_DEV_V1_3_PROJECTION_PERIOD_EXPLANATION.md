# TICKET_DEV — `dorevia_cash_guard` V1.3

## Détail explicatif de la projection par période

**ID** : `CG-V1.3-01-PROJECTION-PERIOD-EXPLANATION`  
**Module** : `dorevia_cash_guard`  
**Priorité** : P0  
**Statut** : À implémenter  
**Dépend de** : V1.2 validée — projection de trésorerie depuis factures ouvertes  
**Périmètre explicite** : expliquer la projection affichée, sans ouvrir budget, simulations, relances, IA ou matching intelligent.

---

## 1. Contexte

La V1.2 permet d’afficher une trajectoire de trésorerie par période :

```text
Trésorerie constatée
+/- factures postées ouvertes
= Projection
```

L’écran **Suivi de trésorerie** permet déjà de voir, semaine par semaine :

```text
Période | Début | Fin | État | Projection | Couverture | Statut
```

Dans l’UI actuelle, **Projection** correspond au solde projeté cumulé de la période, et **Couverture** correspond à l’écart entre cette projection et le seuil d’alerte.

Le moteur est cohérent et permet d’identifier les périodes :

- sécurisées ;
- en vigilance ;
- en risque.

Mais il reste un angle mort important : l’écran indique qu’une période est en **Risque**, sans expliquer immédiatement **quelles factures provoquent ce risque**.

Exemple :

```text
S30 -> Risque
Projection : -1 330 EUR
Couverture : -3 980 EUR
```

L’utilisateur doit pouvoir comprendre :

```text
Pourquoi S30 passe en risque ?
Quelles factures client / fournisseur expliquent cette baisse ?
Quel est l’impact net de la période ?
```

---

## 2. Objectif

Ajouter une lecture explicative de la projection par période.

Objectif produit :

> Cash Guard ne doit pas seulement signaler un risque ; il doit montrer les pièces qui provoquent ce risque.

La V1.3 doit permettre à Esther / Véréna de consulter une période et de comprendre :

- les factures client intégrées à cette période ;
- les factures fournisseur intégrées à cette période ;
- les avoirs éventuels ;
- l’impact net de la période ;
- le lien entre ces pièces et la **Projection** affichée.

---

## 3. Doctrine V1.3

La V1.3 ne modifie pas le moteur de projection principal.

Elle rend visible le raisonnement déjà calculé.

Doctrine :

```text
V1.2 = voir la trajectoire
V1.3 = expliquer la trajectoire
```

Formule métier inchangée :

```text
Projection période N
= projection cumulée calculée par le moteur V1.2 après intégration
  de l’impact des factures ouvertes rattachées à la période N
```

Le détail V1.3 ne recalcule pas une trajectoire autonome. Il liste les apports de la maille (factures / avoirs ouverts rattachés à la période) qui expliquent la **Projection** affichée, tandis que le cumul reste celui du moteur existant.

---

## 4. Périmètre fonctionnel

### Inclus

Inclure dans le détail explicatif :

- factures client postées ouvertes ;
- factures fournisseur postées ouvertes ;
- avoirs client / fournisseur ouverts ;
- montant résiduel utilisé ;
- date projetée utilisée ;
- période de rattachement ;
- impact signé ;
- total entrées ;
- total sorties ;
- impact net factures de la période.

### Exclus

Hors périmètre V1.3 :

- budget management ;
- postes budgétaires ;
- simulations / flux hypothétiques ;
- relances automatiques ;
- arbitrage de paiement ;
- matching bancaire intelligent ;
- recommandations IA ;
- intégration LYNKR / Vault ;
- génération automatique de lignes de flux.

Les flux complémentaires techniques ou historiques éventuellement présents en base restent hors périmètre du détail V1.3. Le détail explique la composante **factures ouvertes** de la projection, pas une projection parallèle complète.

---

## 5. Source des données

Les données explicatives doivent provenir de la même source que la projection V1.2 :

```text
account.move
```

Critères principaux :

```text
move_type in ('out_invoice', 'in_invoice', 'out_refund', 'in_refund')
state = 'posted'
amount_residual != 0
company_id = guard.company_id
```

Date projetée :

```text
reference_due = invoice_date_due or invoice_date or situation_date
projected_date = max(reference_due, situation_date)
```

La facture est rattachée à la période contenant `projected_date`.

Si `projected_date` est hors de la période suivie par le document, aucune ligne explicative n’est créée pour cette pièce dans le document courant.

---

## 6. Signes attendus

| Type de pièce               | Sens dans la projection |
| --------------------------- | ----------------------: |
| Facture client ouverte      |                 positif |
| Facture fournisseur ouverte |                 négatif |
| Avoir client ouvert         |                 négatif |
| Avoir fournisseur ouvert    |                 positif |

Montant utilisé :

```text
amount_residual
```

ou champ Odoo 19 équivalent fiable pour le reste dû.

Le calcul du signe doit réutiliser la même doctrine que la V1.2, afin d’éviter tout écart entre la **Projection** affichée et son détail explicatif.

Devise d’affichage attendue : devise société du document Cash Guard, comme le reste de la projection. Si une pièce est en devise étrangère, utiliser la même valeur résiduelle convertie / normalisée que le moteur V1.2 afin que le détail et les totaux restent cohérents.

---

## 7. Modèle de données proposé

### 7.1 Option recommandée : modèle explicatif non source de vérité

Créer un modèle de détail explicatif, régénéré à chaque recalcul du point.

Nom technique proposé :

```text
dorevia.cash.guard.period.move
```

Libellé métier :

```text
Pièce de projection
```

Objet :

> Représenter les pièces `account.move` qui expliquent l’impact de projection d’une période.

### 7.2 Champs proposés

| Champ              | Type                               | Description                                             |
| ------------------ | ---------------------------------- | ------------------------------------------------------- |
| `guard_id`         | Many2one `dorevia.cash.guard`      | Document de projection parent                           |
| `week_id`          | Many2one `dorevia.cash.guard.week` | Période de rattachement                                 |
| `move_id`          | Many2one `account.move`            | Facture / avoir source                                  |
| `partner_id`       | Many2one `res.partner`             | Client ou fournisseur                                   |
| `move_type`        | Selection / related                | Type de pièce                                           |
| `name`             | Char / related                     | Numéro de facture                                       |
| `invoice_date`     | Date                               | Date de facture                                         |
| `invoice_date_due` | Date                               | Date d’échéance d’origine                               |
| `projected_date`   | Date                               | Date utilisée pour la projection                        |
| `amount_residual`  | Monetary                           | Montant résiduel source                                 |
| `signed_amount`    | Monetary                           | Impact signé sur la projection                          |
| `currency_id`      | Many2one `res.currency`            | Devise                                                  |
| `company_id`       | Many2one `res.company`             | Société                                                 |
| `explanation_type` | Selection                          | `inflow` / `outflow`                                    |
| `is_overdue`       | Boolean                            | Échéance de référence antérieure à la date de situation |
| `sequence`         | Integer                            | Tri d’affichage                                         |

### 7.3 Règle importante

Ces lignes explicatives ne doivent pas devenir une source de vérité autonome.

Elles sont dérivées de `account.move`.

Elles peuvent être supprimées / régénérées à chaque recalcul.

---

## 8. Lien avec `dorevia.cash.guard.week`

Ajouter sur `dorevia.cash.guard.week` :

```python
projection_move_ids = fields.One2many(
    "dorevia.cash.guard.period.move",
    "week_id",
    string="Pièces de projection",
)
```

Réutiliser les champs existants si disponibles :

| Champ                    | Type     | Description                              |
| ------------------------ | -------- | ---------------------------------------- |
| `invoice_inflow_amount`  | Monetary | Total des entrées factures de la période |
| `invoice_outflow_amount` | Monetary | Total des sorties factures de la période |

Ajouter si utile :

| Champ                | Type     | Description                            |
| -------------------- | -------- | -------------------------------------- |
| `invoice_net_amount` | Monetary | Impact net factures de la période      |
| `invoice_move_count` | Integer  | Nombre de pièces expliquant la période |

Ces champs d’agrégat portent uniquement sur les pièces `account.move` ouvertes. Ils ne doivent pas inclure les flux complémentaires techniques ou historiques.

---

## 9. Calcul attendu

Lors du recalcul de projection :

1. recalculer les périodes ;
2. calculer la trajectoire projetée ;
3. rattacher les factures ouvertes à leur période via `projected_date` ;
4. créer / régénérer les lignes explicatives ;
5. calculer les totaux par période :
   - entrées ;
   - sorties ;
   - net ;
   - nombre de pièces.

Pseudo-logique :

```text
Pour chaque facture ouverte :
    reference_due = invoice_date_due or invoice_date or situation_date
    projected_date = max(reference_due, situation_date)
    period = période contenant projected_date
    signed_amount = signe(move_type) * amount_residual
    créer ligne explicative sur period
```

Tri technique recommandé :

```text
week_index asc
projected_date asc
signed_amount asc
move_id asc
```

`signed_amount asc` permet de faire ressortir les sorties en premier lorsqu’elles existent sur une même période.

---

## 10. UX attendue

### 10.1 Onglet existant : Suivi de trésorerie

Conserver la vue principale :

```text
Période | Début | Fin | État | Projection | Couverture | Statut
```

Ne pas renommer ces colonnes dans ce ticket, sauf décision produit explicite. Le ticket V1.3 porte sur l’explication de la projection, pas sur un changement global de vocabulaire UI.

### 10.2 Ajouter une capacité de détail

Sur chaque période, l’utilisateur doit pouvoir accéder aux pièces qui expliquent la projection.

Options acceptables :

- Option A — Sous-liste / smart button par période ;
- Option B — Onglet complémentaire ;
- Option C — One2many repliable sous la période si techniquement simple.

Recommandation UX V1.3 :

> Commencer par un onglet **Détail projection**, plus simple et lisible.

---

## 11. Onglet `Détail projection`

Ajouter un onglet au document de projection :

```text
Détail projection
```

Colonnes recommandées :

| Colonne       | Description                                             |
| ------------- | ------------------------------------------------------- |
| Période       | ex. `S30`                                               |
| Date projetée | Date retenue pour la projection                         |
| Pièce         | Numéro facture / avoir                                  |
| Partenaire    | Client / fournisseur                                    |
| Type          | Client / Fournisseur / Avoir client / Avoir fournisseur |
| Échéance      | Date d’échéance d’origine                               |
| Impact        | Montant signé                                           |
| Retard        | Oui/non si échéance initiale < date de situation        |

Tri recommandé :

```text
Période asc
Date projetée asc
Impact asc
Pièce asc
```

Vue en lecture seule dans l’UI standard.

---

## 12. Lecture d’une période critique

Exemple attendu pour une période en risque :

```text
S30 — Risque

Projection : -1 330 EUR
Couverture : -3 980 EUR

Pièces de projection :
- FACTU/2026/06/0001 — Fournisseur X — -4 000 EUR — échéance 31/07
- FAC/2026/00008 — Client Y — +300 EUR — échéance 29/07

Impact net période : -3 700 EUR
```

Objectif :

> L’utilisateur doit comprendre immédiatement quelle pièce provoque ou aggrave le risque.

---

## 13. Synthèse / indicateurs optionnels

En V1.3, on peut ajouter sans obligation dans `dorevia.cash.guard.week` :

- total entrées factures période ;
- total sorties factures période ;
- impact net période ;
- nombre de pièces.

Ces données peuvent préparer un futur affichage :

```text
Entrées attendues
Sorties attendues
Impact net
```

Mais l’objectif minimal est l’onglet de détail.

---

## 14. Sécurité / droits

Les utilisateurs Cash Guard ne doivent pas obtenir plus de droits comptables que nécessaire.

Règles :

- afficher uniquement les informations utiles à l’explication ;
- ne pas donner d’accès large aux écritures comptables ;
- les liens vers `account.move` doivent respecter les droits existants ;
- si l’utilisateur ne peut pas ouvrir la facture source, afficher au moins le numéro, partenaire, échéance et impact dans la ligne explicative.

Les lignes explicatives peuvent être créées en `sudo()` contrôlé si nécessaire, mais elles ne doivent contenir que des données métier utiles à l’explication.

Accès recommandé :

- lecture pour les utilisateurs Cash Guard ;
- création / modification / suppression réservées au moteur de recalcul ;
- pas d’édition manuelle depuis l’UI.

---

## 15. Tests attendus

Créer une suite :

```text
tests/test_cash_guard_projection_explanation.py
```

### Cas 1 — Facture client future

Données :

- facture client ouverte `+300 EUR` ;
- échéance en S21.

Attendu :

- une ligne explicative créée sur S21 ;
- impact signé `+300`.

### Cas 2 — Facture fournisseur future

Données :

- facture fournisseur ouverte `-500 EUR` ;
- échéance en S22.

Attendu :

- ligne explicative sur S22 ;
- impact signé `-500`.

### Cas 3 — Facture échue ouverte

Données :

- facture client ouverte, échéance avant `situation_date`.

Attendu :

- `projected_date = situation_date` ;
- ligne rattachée à la période Situation ;
- `is_overdue = True`.

### Cas 4 — Facture payée

Données :

- facture soldée, `amount_residual = 0`.

Attendu :

- aucune ligne explicative.

### Cas 5 — Facture brouillon

Données :

- `state = draft`.

Attendu :

- aucune ligne explicative.

### Cas 6 — Avoir client

Attendu :

- impact négatif.

### Cas 7 — Avoir fournisseur

Attendu :

- impact positif.

### Cas 8 — Cohérence de la composante factures

Créer plusieurs factures sur une même période.

Attendu :

```text
invoice_net_amount période
= somme signed_amount des lignes explicatives de la période

invoice_inflow_amount période
= somme des signed_amount positifs

invoice_outflow_amount période
= valeur absolue de la somme des signed_amount négatifs
```

Si aucune autre composante de projection n’existe sur la période, alors la variation de `projected_balance` entre deux périodes doit être cohérente avec cette somme. Si des flux complémentaires techniques ou historiques existent encore en base, l’égalité stricte avec `projected_balance` ne doit pas être exigée : le détail V1.3 explique uniquement les factures ouvertes.

### Cas 9 — Régénération sans doublons

Après deux recalculs successifs.

Attendu :

- pas de doublons dans les lignes explicatives ;
- les anciennes lignes sont remplacées ou mises à jour proprement.

### Cas 10 — Pièce hors période suivie

Données :

- facture ouverte avec `projected_date` postérieure à `guard.date_to`.

Attendu :

- aucune ligne explicative créée sur le document courant ;
- pas d’impact sur les périodes affichées.

### Cas 11 — Flux complémentaires hors détail

Données :

- une ligne technique `dorevia.cash.guard.line` existe sur une période ;
- une facture ouverte existe sur la même période.

Attendu :

- seule la facture ouverte génère une ligne `dorevia.cash.guard.period.move` ;
- les agrégats `invoice_*` ne tiennent compte que de la facture ;
- le test ne compare pas strictement la somme des pièces explicatives au delta complet de `projected_balance` si le flux complémentaire modifie aussi la projection.

---

## 16. Scénario manuel de recette

Créer :

```text
docs/SCENARIO_MANUEL_V1_3_DETAIL_PROJECTION.md
```

Scénario :

1. ouvrir un document de projection existant ;
2. vérifier la trajectoire dans **Suivi de trésorerie** ;
3. créer une facture client ouverte avec échéance future ;
4. créer une facture fournisseur ouverte avec échéance future ;
5. rouvrir le document ou recalculer ;
6. vérifier que la trajectoire change ;
7. ouvrir **Détail projection** ;
8. vérifier que les factures apparaissent sur les bonnes périodes ;
9. vérifier les signes ;
10. vérifier une période en risque et identifier la pièce qui l’explique ;
11. payer une facture ;
12. vérifier qu’elle disparaît du détail après recalcul.

---

## 17. Garde-fous

- Ne pas créer de simulation.
- Ne pas intégrer le budget.
- Ne pas modifier la logique de projection validée V1.2.
- Ne pas créer de lignes de flux complémentaires à partir des factures.
- Ne pas élargir aux devis.
- Ne pas ajouter de recommandations automatiques.
- Ne pas transformer le détail en source de vérité.
- Ne pas exposer de complexité comptable inutile à l’utilisateur.

---

## 18. Critères d’acceptation

Le ticket est validé si :

- un utilisateur peut voir les pièces qui expliquent la projection par période ;
- les factures client ouvertes apparaissent avec un impact positif ;
- les factures fournisseur ouvertes apparaissent avec un impact négatif ;
- les avoirs sont correctement signés ;
- les factures payées / brouillon sont exclues ;
- les factures échues sont rattachées à la période Situation ;
- les montants et agrégats sont cohérents avec la devise société utilisée par Cash Guard ;
- les colonnes principales conservent le wording UI actuel **Projection** / **Couverture** ;
- les flux complémentaires éventuels ne sont pas présentés comme des pièces de projection V1.3 ;
- les lignes explicatives sont régénérables sans doublons ;
- une période en risque peut être expliquée par ses pièces ;
- les tests automatisés passent ;
- le scénario manuel V1.3 est documenté.

---

## 19. Résumé produit

La V1.2 permet de voir la trajectoire.

La V1.3 doit permettre de comprendre cette trajectoire.

Formule :

```text
Solde constaté
+/- factures ouvertes
= Projection
```

Explication attendue :

```text
Période critique
-> pièces qui entrent / sortent
-> impact net
-> raison du statut
```

Phrase produit :

> Cash Guard ne se contente pas d’indiquer qu’une période est en risque : il montre les factures qui expliquent ce risque.
