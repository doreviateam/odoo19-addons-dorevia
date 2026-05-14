# TICKET_DEV — `dorevia_cash_guard` V1.1

## Suivi hebdomadaire de trésorerie sur exercice comptable

**ID** : `CG-V1.1-01-WEEKLY-FISCAL-CASH-FOLLOWUP`  
**Module** : `dorevia_cash_guard`  
**Priorité** : P0  
**Statut** : À implémenter  
**Dépend de** : V1 validée — Lots A/B/C GO  

**Contexte fonctionnel** : amélioration du modèle de calcul et de lecture métier après test utilisateur « nouveau venu » sur base vierge.

---

## 1. Constat V1

La V1 fonctionne techniquement, mais son modèle de lecture est trop centré sur :

```text
date_from
→ solde initial à cette date
→ flux complémentaires
```

Ce comportement est correct pour une projection simple, mais il n’est pas assez naturel pour un suivi réel de trésorerie.

Lors du test utilisateur, le cas suivant a posé problème :

```text
Exercice : 2026
Point créé du 01/01/2026 au 31/12/2026
Encaissement bancaire réalisé en 2026 : 2 400 €
Solde initial affiché au 01/01/2026 : 0 €
```

Techniquement, c’est logique : le solde au 01/01 ne contient pas un encaissement réalisé plus tard.

Mais fonctionnellement, l’utilisateur attend plutôt :

> « Je suis mon exercice 2026. À la date de situation, combien ai-je en banque, et que prévoient les semaines restantes ? »

---

## 2. Nouvelle doctrine V1.1

La V1.1 doit faire évoluer le modèle mental de Cash Guard.

Doctrine retenue :

```text
Horizon par défaut = exercice comptable courant
Découpage de lecture = semaines de l’exercice
Point de départ projeté = dernier solde bancaire à date
Capacité historique = rejouer la trésorerie à une date antérieure, par semaine, jusqu’à la date de début de l’exercice par défaut
```

Formulation métier :

> Cash Guard suit l’exercice comptable courant, semaine par semaine.  
> Les semaines passées sont recalculées depuis les écritures comptables datées.  
> La date de situation fournit le solde bancaire constaté à date.  
> Les semaines futures sont projetées depuis ce solde, avec les flux complémentaires et simulés.

Phrase courte :

> **L’exercice est l’horizon. La semaine est la maille. Le solde bancaire à date est le point de départ. Le passé se rejoue depuis les écritures comptables.**

---

## 3. Objectif du ticket

Implémenter une lecture hebdomadaire par exercice comptable dans `dorevia_cash_guard`.

Le module doit permettre de calculer et d’afficher :

1. l’exercice comptable suivi ;
2. la date de situation ;
3. le solde bancaire calculé à la date de situation ;
4. l’historique hebdomadaire depuis le début de l’exercice jusqu’à la date de situation ;
5. la projection hebdomadaire depuis la date de situation jusqu’à la fin de l’exercice ;
6. le statut `safe` / `warning` / `risk` sur la trajectoire future.

---

## 4. Comportement cible

Exemple cible :

```text
Exercice : 2026
Début exercice : 01/01/2026
Fin exercice : 31/12/2026
Date de situation : 09/05/2026
Solde bancaire à date : 2 400 €

Lecture historique :
S01 → S18 : soldes hebdomadaires recalculés depuis les écritures comptables

Lecture projetée :
S19 → S52 : projection depuis le solde bancaire à date
```

### 4.1 Historique

Pour les semaines passées :

```text
S01 → semaine précédant ou contenant la date de situation
```

Le module calcule le solde bancaire à la fin de chaque semaine à partir des écritures bancaires postées.

Formule :

```text
Solde fin semaine N =
somme des écritures bancaires postées
jusqu’à la date de fin de semaine N
```

### 4.2 Date de situation

La date de situation est la date à laquelle on fait le point.

Exemple :

```text
situation_date = 09/05/2026
```

Le module calcule :

```text
observed_balance =
solde bancaire calculé à situation_date
```

Ce solde devient le point de départ opérationnel de la projection future.

### 4.3 Projection future

Pour les semaines futures :

```text
solde courant = observed_balance

Pour chaque semaine future :
    solde courant
    + entrées prévues de la semaine
    - sorties prévues de la semaine
    = solde fin de semaine projeté
```

Les flux utilisés sont les flux dont :

```text
projection_date > situation_date
```

Les lignes `simulated` sont prises en compte en V1.1 comme en V1, sauf si une option d’exclusion est ajoutée explicitement dans un ticket séparé.

---

## 5. Modèle de données à faire évoluer

### 5.1 Modèle `dorevia.cash.guard`

Ajouter les champs suivants :

| Champ                   | Type                               | Requis | Description                                   |
| ----------------------- | ---------------------------------- | -----: | --------------------------------------------- |
| `fiscal_date_from`      | Date                               |    Oui | Début de l’exercice suivi                     |
| `fiscal_date_to`        | Date                               |    Oui | Fin de l’exercice suivi                       |
| `situation_date`        | Date                               |    Oui | Date de situation / date de calcul            |
| `observed_balance`      | Monetary                           |    Non | Solde bancaire calculé à la date de situation |
| `observed_balance_date` | Date                               |    Non | Date effective du calcul du solde observé     |
| `weekly_line_ids`       | One2many `dorevia.cash.guard.week` |    Non | Lignes hebdomadaires calculées                |

Question d’implémentation :

- soit remplacer progressivement `date_from` / `date_to` par `fiscal_date_from` / `fiscal_date_to` ;
- soit conserver `date_from` / `date_to` en V1.1 et les interpréter comme début/fin d’exercice.

**Recommandation** :

> Pour limiter la migration, conserver `date_from` et `date_to`, mais renommer leur libellé UI en « Début exercice » et « Fin exercice ». Ajouter seulement `situation_date` et `observed_balance`.

Donc mapping V1.1 recommandé :

| Champ existant           | Nouveau sens métier                                  |
| ------------------------ | ---------------------------------------------------- |
| `date_from`              | Début exercice                                       |
| `date_to`                | Fin exercice                                         |
| `initial_balance`        | Solde début exercice, conservé pour information      |
| `observed_balance`       | Solde bancaire à date de situation                   |
| `forecast_min_balance`   | Solde minimum futur à partir de la date de situation |
| `forecast_final_balance` | Solde projeté à fin d’exercice                       |

### 5.2 Nouveau modèle `dorevia.cash.guard.week`

Créer un modèle de lecture hebdomadaire.

Nom technique :

```text
dorevia.cash.guard.week
```

Objet métier :

```text
Solde de trésorerie
```

#### Champs proposés

| Champ             | Type                          | Requis | Description                           |
| ----------------- | ----------------------------- | -----: | ------------------------------------- |
| `guard_id`        | Many2one `dorevia.cash.guard` |    Oui | Document de projection parent          |
| `week_index`      | Integer                       |    Oui | Numéro de semaine dans l’exercice     |
| `week_label`      | Char                          |    Oui | Libellé, ex. `S19`                    |
| `date_from`       | Date                          |    Oui | Début de semaine                      |
| `date_to`         | Date                          |    Oui | Fin de semaine                        |
| `period_type`     | Selection                     |    Oui | `historical` / `current` / `forecast` |
| `opening_balance` | Monetary                      |    Non | Solde début semaine                   |
| `inflow_amount`   | Monetary                      |    Non | Entrées de la semaine                 |
| `outflow_amount`  | Monetary                      |    Non | Sorties de la semaine                 |
| `closing_balance` | Monetary                      |    Non | Solde fin semaine                     |
| `min_balance`     | Monetary                      |    Non | Point bas de la semaine si calculable |
| `risk_status`     | Selection                     |    Non | `safe` / `warning` / `risk`           |
| `currency_id`     | Related                       |    Oui | Devise                                |
| `company_id`      | Related                       |    Oui | Société                               |

#### Sélection `period_type`

```python
period_type = [
    ("historical", "Historique"),
    ("current", "Semaine de situation"),
    ("forecast", "Projeté"),
]
```

---

## 6. Règles de calcul V1.1

### 6.1 Calcul du solde bancaire à date

Créer ou adapter une méthode dédiée :

```python
_compute_bank_balance_at_date(target_date)
```

Règles :

- lecture comptable contrôlée ;
- `sudo()` contrôlé autorisé comme en correctif V1 ;
- domaine strict :
  - `company_id = guard.company_id`
  - `journal_id = guard.bank_journal_id`
  - `parent_state = posted`
  - `date <= target_date`
  - comptes de liquidité si disponibles.

Le résultat est un agrégat uniquement.

Ne pas donner d’accès direct aux écritures comptables aux utilisateurs Cash Guard.

### 6.2 Calcul du solde début exercice

Le champ existant `initial_balance` reste calculé au début de l’exercice :

```text
initial_balance =
solde bancaire calculé à date_from
```

Mais il ne doit plus être le point de départ opérationnel du projeté si une `situation_date` existe.

### 6.3 Calcul du solde à date de situation

```text
observed_balance =
solde bancaire calculé à situation_date
```

Ce solde devient le point de départ du projeté futur.

### 6.4 Génération des semaines de l’exercice

À partir de :

```text
date_from = début exercice
date_to = fin exercice
```

Générer des semaines consécutives couvrant tout l’exercice.

Chaque semaine contient :

```text
week_index
date_from
date_to
week_label
period_type
```

La dernière semaine peut être partielle si l’exercice ne se termine pas un dimanche.

Ne pas supposer strictement 52 semaines : selon les dates, il peut y avoir 52 ou 53 semaines calendaires.

Mais côté UX, on peut parler de « semaines de l’exercice ».

### 6.5 Classification historique / courant / projeté

Pour chaque semaine :

- si `week.date_to < situation_date` :
  - `period_type = historical`
- si `week.date_from <= situation_date <= week.date_to` :
  - `period_type = current`
- si `week.date_from > situation_date` :
  - `period_type = forecast`

### 6.6 Calcul des semaines historiques

Pour chaque semaine historique :

```text
closing_balance =
solde bancaire calculé à week.date_to
```

`opening_balance` peut être :

- soit le `closing_balance` de la semaine précédente ;
- soit le solde bancaire calculé à `week.date_from - 1`.

**Recommandation** :

```text
opening_balance = closing_balance précédent
closing_balance = solde bancaire à week.date_to
```

Les entrées/sorties historiques détaillées peuvent être calculées en V1.1 si simple, sinon reportées.

**Minimum requis V1.1** :

- `opening_balance`
- `closing_balance`
- `risk_status`

### 6.7 Calcul de la semaine courante

Pour la semaine contenant la date de situation :

```text
closing_balance = observed_balance
period_type = current
```

Cette semaine marque le passage entre historique et projeté.

Nuance possible :

- les jours <= `situation_date` sont constatés ;
- les jours > `situation_date` sont projetés.

Pour V1.1, ne pas complexifier : la semaine courante peut simplement afficher le solde à date comme point d’ancrage.

### 6.8 Calcul des semaines futures

Point de départ :

```text
running_balance = observed_balance
```

Pour chaque semaine future :

```text
inflow_amount =
somme signed_projected_amount > 0
pour les flux dont projection_date est dans la semaine

outflow_amount =
somme abs(signed_projected_amount < 0)
pour les flux dont projection_date est dans la semaine

closing_balance =
running_balance + inflow_amount - outflow_amount

risk_status =
safe / warning / risk selon closing_balance ou min_balance

running_balance = closing_balance
```

Pour la V1.1, le statut hebdomadaire peut être basé sur `closing_balance`.

Si on veut être plus précis, on peut calculer le point bas intra-semaine à partir des lignes datées dans la semaine, triées par date.

**Recommandation** :

> Utiliser le point bas intra-semaine si les lignes de flux sont disponibles, sinon `closing_balance`.

### 6.9 Calcul du risque global

Le risque global du point doit désormais s’appuyer sur la trajectoire future à partir de `situation_date`.

```text
forecast_min_balance =
minimum des soldes futurs calculés après situation_date
```

Puis :

```text
risk si forecast_min_balance < 0
warning si forecast_min_balance >= 0 et < alert_threshold
safe si forecast_min_balance >= alert_threshold
```

Si aucun flux futur :

```text
forecast_min_balance = observed_balance
forecast_final_balance = observed_balance
```

---

## 7. UX attendue

### 7.1 Formulaire Document de projection

Renommer visuellement les champs :

| Champ technique          | Libellé UI V1.1                   |
| ------------------------ | --------------------------------- |
| `date_from`              | Début exercice                    |
| `date_to`                | Fin exercice                      |
| `situation_date`         | Date de situation                 |
| `initial_balance`        | Solde début exercice              |
| `observed_balance`       | Solde bancaire à date             |
| `forecast_min_balance`   | Projection minimum                |
| `forecast_final_balance` | Projection en fin de période      |

### 7.2 Bloc synthèse cible

Afficher en haut :

```text
Exercice : 01/01/2026 → 31/12/2026
Date de situation : 09/05/2026
Solde bancaire à date : 2 400 €
Seuil d’alerte : 3 000 €
Projection minimum : ...
Statut : safe / warning / risk
```

### 7.3 Onglets

Ajouter ou réorganiser les onglets :

```text
Flux complémentaires
Soldes de trésorerie
Notes
```

L’onglet **Soldes de trésorerie** affiche les lignes `dorevia.cash.guard.week`.

Colonnes recommandées :

- Semaine ;
- Période ;
- Type : Historique / Situation / Projeté ;
- Solde début ;
- Entrées ;
- Sorties ;
- Solde fin ;
- Statut.

---

## 8. Menu et libellés UX

Libellés actés (alignement doctrine projection) :

```text
Projection de trésorerie
```

Sous-menus :

```text
Projection de trésorerie
- Documents de projection
- Flux complémentaires
```

---

## 9. Tests attendus

Ajouter une suite de tests V1.1.

Fichier suggéré :

```text
tests/test_cash_guard_weekly.py
```

### 9.1 Tests principaux

#### Cas 1 — Solde à date

Données :

- écriture bancaire +2 400 € datée avant ou égale à `situation_date`
- point exercice 2026
- `situation_date = 09/05/2026`

Attendu :

```text
observed_balance = 2 400 €
```

#### Cas 2 — Historique hebdomadaire

Données :

- écritures bancaires sur plusieurs semaines passées.

Attendu :

- les semaines passées sont générées ;
- les soldes de fin de semaine sont recalculés ;
- les semaines avant `situation_date` sont `historical`.

#### Cas 3 — Semaine courante

Attendu :

- la semaine contenant `situation_date` est `current`.

#### Cas 4 — Projection future

Données :

- solde à date : 2 400 €
- flux futur +5 000 €
- flux futur -2 000 €
- flux futur -4 500 €

Attendu :

- projection hebdomadaire correcte ;
- `forecast_final_balance` correct ;
- `forecast_min_balance` correct.

#### Cas 5 — Risque futur

Créer une séquence où le solde futur passe sous zéro.

Attendu :

```text
risk_status = risk
```

#### Cas 6 — Vigilance future

Créer une séquence où le solde futur reste positif mais sous seuil.

Attendu :

```text
risk_status = warning
```

#### Cas 7 — Exclusion des points clôturés du recalcul cron

Le cron ne doit pas écraser les semaines ou soldes d’un point `closed`.

---

## 10. Scénario manuel de recette V1.1

### Contexte de recette et commandes (Docker)

```text
URL : http://localhost:18079
Base : tenant_o8
Module : dorevia_cash_guard
```

Nom de base : **`tenant_o8`** avec la lettre **o**, pas **`tenant_08`** avec un zéro.

Exécuter les commandes depuis le répertoire qui contient **`docker-compose.yml`** (stack Odoo locale ; exemple typique : dossier **`sandbox-odoo19`**). Sinon Docker répond *« no configuration file provided »*.

```bash
cd ~/sandbox-odoo19
docker compose exec odoo odoo -d tenant_o8 -u dorevia_cash_guard --stop-after-init
docker compose restart odoo
```

Tests :

```bash
cd ~/sandbox-odoo19
docker compose exec odoo odoo -d tenant_o8 -u dorevia_cash_guard --test-enable --stop-after-init --http-port=8071
```

Document détaillé :

```text
docs/SCENARIO_MANUEL_V1_1_HEBDO.md
```

### Contenu attendu du scénario

Créer / maintenir :

```text
docs/SCENARIO_MANUEL_V1_1_HEBDO.md
```

Scénario attendu :

1. créer ou utiliser une base avec un journal banque ;
2. enregistrer un encaissement bancaire en 2026 ;
3. créer un point :
   - exercice : 01/01/2026 → 31/12/2026 ;
   - date de situation : après l’encaissement ;
   - seuil : 3 000 € ;
4. cliquer **Actualiser** ;
5. vérifier :
   - `observed_balance = solde bancaire à date` ;
   - semaines historiques générées ;
   - semaine courante identifiée ;
6. ajouter des flux futurs ;
7. vérifier la projection hebdomadaire ;
8. vérifier les statuts `safe`, `warning`, `risk`.

---

## 11. Contraintes et garde-fous

- Ne pas supprimer le comportement V1 sans migration.
- Ne pas exposer les écritures comptables aux utilisateurs Cash Guard.
- Ne pas donner `account.group_account_readonly` automatiquement au groupe Cash Guard User.
- Le calcul bancaire à date doit rester agrégé.
- Les points `closed` ne doivent pas être modifiés automatiquement par le cron.
- Les semaines calculées doivent être régénérables sans doublons.

---

## 12. Migration / compatibilité V1

Pour les points existants V1 :

- initialiser `situation_date` à `date_from` ou à la date du jour ?
- **recommandation** : pour ne pas modifier le sens historique, initialiser `situation_date = date_from` sur les anciens points.

Mais pour les nouveaux points :

```text
situation_date = date du jour par défaut
date_from/date_to = exercice courant si détectable
```

---

## 13. Critères d’acceptation

Le ticket est validé si :

- un document de projection peut être rattaché à un exercice ;
- une date de situation est disponible ;
- le solde bancaire à date est calculé correctement ;
- les semaines de l’exercice sont générées ;
- les semaines passées sont marquées `historical` ;
- la semaine de situation est marquée `current` ;
- les semaines futures sont marquées `forecast` ;
- la projection future démarre depuis `observed_balance` ;
- le risque global est calculé sur la trajectoire future ;
- l’interface affiche clairement :
  - exercice ;
  - date de situation ;
  - solde bancaire à date ;
  - projection minimum ;
  - statut ;
- les tests automatisés passent ;
- un scénario manuel V1.1 est documenté et exécuté.

---

## 14. Hors périmètre de ce ticket

- matching bancaire intelligent ;
- génération automatique des flux futurs depuis factures ouvertes ;
- intégration LYNKR ;
- intégration Vault ;
- scellement de snapshots ;
- option d’exclusion des simulations ;
- dashboard graphique avancé ;
- recommandations IA.

---

## 15. Résumé produit

Ce ticket transforme Cash Guard d’une projection simple en outil de suivi de trésorerie à date.

**Avant** :

```text
solde au début de période
+ flux saisis
= projection
```

**Après** :

```text
exercice comptable courant
+ lecture hebdomadaire
+ solde bancaire calculé à date
+ projection future
= suivi opérationnel de trésorerie
```

**Formule finale** :

> **L’exercice est l’horizon.**  
> **La semaine est la maille.**  
> **Le solde bancaire à date est le point de départ.**  
> **Le passé se rejoue depuis les écritures comptables.**

---

*Ce document est le ticket exécutable V1.1 ; il peut être découpé en sous-tickets techniques au moment du sprint.*
