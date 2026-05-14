# SPEC_TECHNIQUE — `dorevia_cash_guard` (V0.1)

Spécification technique d’implémentation du module Odoo 19 CE **Sécurité Trésorerie**.

Ce document traduit le cadrage fonctionnel du `README.md` en éléments techniques exécutables, sans entrer dans le détail ligne à ligne du code Python/XML.

---

## 1. Portée et objectifs techniques

### 1.1 Objectif de la V1

Fournir un module Odoo permettant de :

- projeter une trésorerie bancaire sur une période donnée ;
- calculer automatiquement le solde initial, le solde final et le solde minimum ;
- classifier le niveau de risque (`safe`, `warning`, `risk`) selon un seuil ;
- suivre des flux complémentaires (manuel / simulation) ;
- préparer une comparaison simple prévu / réalisé.

### 1.2 Hors périmètre V1

- dépendance MIS Builder / `mis_builder_cash_flow` ;
- scénarios multi-hypothèses avancés ;
- moteur d’alertes email ;
- matching intelligent automatique ;
- intégrations externes (LYNKR, Vault).

---

## 2. Architecture module Odoo

### 2.1 Nom technique

- Module : `dorevia_cash_guard`
- Dépendances minimales : `account`, `base_account_budget`, `base_accounting_kit`, `dorevia_budget_post_unique_accounts`, `mail`

### 2.1 bis Environnement de recette (référence sandbox)

Pour les tests manuels et la mise à jour module sur la stack Docker Dorevia : URL `http://localhost:18079`, base PostgreSQL **`tenant_o8`** (lettre **o**, pas `tenant_08`), commandes détaillées dans `docs/SCENARIO_MANUEL_V1_1_HEBDO.md`.

### 2.2 Arborescence cible

```text
dorevia_cash_guard/
├── README.md
├── __init__.py
├── __manifest__.py
├── security/
│   ├── ir.model.access.csv
│   └── dorevia_cash_guard_security.xml
├── data/
│   ├── sequence.xml
│   ├── cash_guard_cron.xml
│   └── budget_post_seed.xml          # optionnel, nomenclature 20 postes
├── models/
│   ├── __init__.py
│   ├── cash_guard.py
│   ├── cash_guard_line.py
│   └── budget_post.py                # extension légère si nécessaire
├── views/
│   ├── cash_guard_views.xml
│   ├── cash_guard_line_views.xml
│   ├── budget_post_views.xml         # optionnel
│   └── menus.xml
└── docs/
    └── SPEC_TECHNIQUE.md
```

---

## 3. Modèle de données

### 3.1 Objet principal — `dorevia.cash.guard`

Rôle : représenter un **document de projection** sur une période.

**Création par défaut (sans dates saisies)** : `situation_date` = date du jour ; `date_from` = `situation_date` ; `date_to` = `date_from` + 90 jours (projection opérationnelle).

### Champs fonctionnels

| Champ | Type | Requis | Index | Notes |
| --- | --- | --- | --- | --- |
| `name` | Char | Oui | Oui | Identifiant lisible du point |
| `date_from` | Date | Oui | Oui | Début période |
| `date_to` | Date | Oui | Oui | Fin période |
| `bank_journal_id` | Many2one `account.journal` | Oui | Oui | Journal de type banque |
| `company_id` | Many2one `res.company` | Oui | Oui | Multi-société |
| `currency_id` | Many2one `res.currency` | Oui | Non | Devise société/journal |
| `alert_threshold` | Monetary | Oui | Non | Seuil de vigilance |
| `initial_balance` | Monetary | Oui | Non | Calculé |
| `forecast_final_balance` | Monetary | Oui | Non | Calculé — projection fin de période (suivi) |
| `forecast_min_balance` | Monetary | Oui | Non | Calculé — min des projections Situation + projection engagée |
| `min_balance_date` | Date | Non | Non | Calculé — fin de maille du minimum projeté |
| `risk_status` | Selection | Oui | Oui | `safe` / `warning` / `risk` |
| `state` | Selection | Oui | Oui | `draft` / `validated` / `closed` |
| `responsible_id` | Many2one `res.users` | Non | Oui | Responsable métier |
| `line_ids` | One2many `dorevia.cash.guard.line` | Non | Non | Lignes de flux |
| `note` | Text | Non | Non | Notes |

### Contraintes

- `date_from <= date_to`
- `alert_threshold >= 0`
- `bank_journal_id.type in ('bank', 'cash')`
- cohérence société : `bank_journal_id.company_id == company_id`

### SQL constraints pressenties

- unicité recommandée : `(company_id, name)` (à confirmer métier)
- check seuil non négatif

---

### 3.2 Objet ligne — `dorevia.cash.guard.line`

Rôle : représenter un flux de trésorerie daté (prévu ou simulé) et son avancement de réalisation.

### Champs fonctionnels

| Champ | Type | Requis | Index | Notes |
| --- | --- | --- | --- | --- |
| `guard_id` | Many2one `dorevia.cash.guard` | Oui | Oui | Parent |
| `projection_date` | Date | Oui | Oui | Date de projection |
| `budget_post_id` | Many2one `account.budget.post` | Oui | Oui | Poste budgétaire obligatoire |
| `budget_line_id` | Many2one `budget.lines` | Non | Oui | Optionnel |
| `analytic_account_id` | Many2one `account.analytic.account` | Non | Oui | Optionnel |
| `direction` | Selection | Oui | Oui | `inflow` / `outflow` |
| `line_type` | Selection | Oui | Oui | `planned` / `simulated` |
| `label` | Char | Oui | Non | Libellé métier |
| `projected_amount` | Monetary | Oui | Non | Montant absolu (>= 0) |
| `realized_amount` | Monetary | Non | Non | Montant absolu réalisé (>= 0) |
| `signed_projected_amount` | Monetary | Oui | Non | Calculé, `+` entrée / `-` sortie |
| `signed_realized_amount` | Monetary | Non | Non | Calculé, `+` entrée / `-` sortie |
| `variance_amount` | Monetary | Non | Non | Calculé |
| `balance_after_line` | Monetary | Non | Non | Calculé séquentiellement |
| `partner_id` | Many2one `res.partner` | Non | Oui | Tiers |
| `source_move_id` | Many2one `account.move` | Non | Oui | Source comptable |
| `source_move_line_id` | Many2one `account.move.line` | Non | Oui | Source ligne |
| `bank_move_line_id` | Many2one `account.move.line` | Non | Oui | Ligne rapprochée |
| `certainty` | Selection | Non | Oui | `certain` / `confirmed` / `uncertain` |
| `priority` | Selection | Non | Oui | `mandatory` / `deferrable` |
| `cash_state` | Selection | Oui | Oui | `planned` / `booked` / `payment_entered` / `reconciled` / `variance` / `cancelled` |
| `sequence` | Integer | Oui | Oui | Tri secondaire |
| `company_id` | Many2one `res.company` | Oui | Oui | Related/store |
| `currency_id` | Many2one `res.currency` | Oui | Non | Related/store |
| `note` | Text | Non | Non | Commentaire |

### Contraintes

- `projected_amount >= 0`
- `realized_amount >= 0` (si renseigné)
- `sequence >= 0`
- cohérence société entre ligne et parent.

---

### 3.3 Référentiel — `account.budget.post`

Le module **`dorevia_budget_post_unique_accounts`** (dépendance de Cash Guard) étend les postes budgétaires :

- champ **`active`** (par défaut actif) pour distinguer postes courants et postes archivés ;
- contrainte métier : **un même compte comptable ne peut être lié qu’à un seul poste actif par société** ; les postes archivés (`active=False`) ne participent pas à la contrainte, ce qui permet de réaffecter les comptes vers un nouveau poste actif.

Extensions futures possibles (hors périmètre actuel) : `cash_direction_default`, `cash_sequence`, etc.

Suppression interdite pour postes utilisés ; archivage recommandé.

---

## 4. Règles de calcul

### 4.1 Solde initial

Source : journal bancaire sélectionné, à `date_from`.

Principe :

```text
initial_balance = solde comptable du journal bancaire à date_from
```

Le calcul doit être centralisé dans une méthode dédiée (ex : service métier ou méthode modèle) pour garantir la cohérence entre affichage, recalcul manuel et cron.

### 4.2 Ordonnancement des flux

Tri strict :

```text
projection_date ASC
sequence ASC
id ASC
```

Objectif : rendre le calcul déterministe.

### 4.3 Synthèse « projection » (alignée sur le suivi)

Les champs **Projection en fin de période**, **Projection minimum** et **Date du point bas projeté** sont alignés sur la colonne **Projection** du suivi : après chaque recalcul, ils sont dérivés des `projected_balance` stockés sur les mailles **Situation** et **Projection engagée** (même source que la grille).

### 4.4 Solde après ligne (flux)

Algorithme pour `balance_after_line` sur les lignes de flux :

1. `running_balance = initial_balance` (logique des lignes éditables)
2. Pour chaque ligne triée :
   - appliquer le flux (`+` entrée, `-` sortie)
   - stocker `balance_after_line`
   - mettre à jour le minimum observé sur la trajectoire ligne à ligne

### 4.5 Statut de risque

À partir de `forecast_min_balance` (projection minimum) et `alert_threshold` :

- `risk` si `< 0`
- `warning` si `>= 0` et `< alert_threshold`
- `safe` si `>= alert_threshold`

### 4.6 Variance prévu / réalisé

```text
variance_amount = signed_realized_amount - signed_projected_amount
```

Convention figée V0.1 : montants absolus + `direction`, avec champs signés calculés.

---

## 5. Gestion des états

### 5.1 États du document de projection (`state`)

- `draft` : modifiable
- `validated` : projection figée fonctionnellement (édition limitée selon droits)
- `closed` : période clôturée, saisie bloquée

### 5.2 Transitions

- `draft -> validated` : action utilisateur autorisé
- `validated -> draft` : autorisée seulement pour profils manager
- `validated -> closed` : action de clôture
- `closed -> draft/validated` : interdit (ou réservé admin selon stratégie)

---

## 6. UX Odoo (vues et navigation)

### 6.1 Menus

```text
Comptabilité / Trésorerie / Projection de trésorerie
```

Sous-menus :

- Documents de projection
- Postes budgétaires (raccourci)
- Reporting (V1.1)

### 6.2 Vue liste `dorevia.cash.guard`

Colonnes minimales :

- nom, période, journal bancaire, seuil, solde initial, solde final, solde minimum, statut, état.

### 6.3 Vue formulaire `dorevia.cash.guard`

Blocs :

- En-tête : identité + période + journal
- Indicateurs : seuil, soldes, statut
- Onglet suivi : trajectoire de trésorerie calculée
- Onglet notes : commentaires internes
- Boutons : actualiser (recalcul), valider, clôturer
- **Actualiser (V1.2)** : outre le recalcul, réaligne par défaut la période sur la situation à date + **90 jours** (`date_from` = `situation_date`, `date_to` = `date_from` + 90 jours). Les autres déclencheurs de recalcul ne modifient pas les dates.

### 6.4 Vue lignes

Affichage orienté pilotage :

- date, poste budgétaire, libellé, type ligne, état cash, montant projeté, réalisé, écart, solde après ligne.

Filtres clés :

- par type (`planned` / `simulated`)
- par état cash
- par poste budgétaire
- par période

---

## 7. Sécurité et droits

### 7.1 Groupes

- `cash_guard_user` : consultation + édition en brouillon
- `cash_guard_manager` : validation/clôture + réouverture autorisée

### 7.2 ACL

- `dorevia.cash.guard`
  - user : read/write/create
  - manager : read/write/create/unlink (option à arbitrer)
- `dorevia.cash.guard.line`
  - user : read/write/create
  - manager : read/write/create/unlink

### 7.3 Record rules

- restriction par `company_id` (multi-société standard Odoo)

---

## 8. Données d’initialisation

### 8.1 Nomenclature 20 postes budgétaires

Mode d’initialisation :

- optionnel à l’installation (data XML)
- idempotent (ne pas dupliquer)
- non destructif (ne pas écraser personnalisations existantes)

Note V0.1 :

- la V1 fournit une nomenclature documentaire complète des 20 postes standards avec :
  - nom ;
  - sens cash par défaut ;
  - famille entrée/sortie ;
  - ordre d'affichage ;
  - description métier ;
  - comptes comptables suggérés ;
- le seed XML automatique reste optionnel, car il nécessite un mapping fiable avec le plan comptable de l’instance (comptes associés aux postes) ;
- aucun chargement automatique des postes sans validation manuelle préalable du mapping comptes dans l'instance.

### 8.2 Séquences

Séquence recommandée pour les points :

```text
CG/%(year)s/%(seq)s
```

---

## 9. Jobs techniques (option V1)

Cron quotidien possible :

- recalcul des points en `draft` et `validated` non clôturés
- mise à jour du `risk_status`

Le cron doit être désactivable par configuration.

---

## 10. API interne et services

Méthodes métier attendues :

- `action_compute_initial_balance()`
- `action_recompute_projection()`
- `action_validate()`
- `action_close()`
- `action_reopen()` (manager)

Méthodes utilitaires :

- `_compute_running_balances()`
- `_compute_risk_status()`
- `_compute_variances()`
- `_check_business_constraints()`

Principe : un seul point d’entrée de recalcul pour éviter les divergences.

---

## 11. Performance et volumétrie

Hypothèses V1 :

- 100 à 5 000 lignes par document de projection.

Mesures :

- index sur `(guard_id, projection_date, sequence, id)`
- lectures groupées (éviter N+1)
- recalcul ciblé à la modification de lignes impactantes.

---

## 12. Journalisation et audit

Attendus minimaux :

- chatter activé sur `dorevia.cash.guard` (`mail.thread`) ;
- journal des changements d’état (`draft`, `validated`, `closed`) ;
- traçabilité des modifications de seuil et de période.

---

## 13. Tests d’acceptation techniques (V1)

Jeux de tests prioritaires :

1. Calcul solde initial depuis journal bancaire.
2. Projection triée avec séquence stable.
3. Détection correcte du solde minimum (pas seulement solde final).
4. Statut `risk` / `warning` / `safe` sur cas limites.
5. Lignes simulées incluses/exclues de la projection.
6. Comparaison simple prévu / réalisé et variance.
7. Respect des droits utilisateur vs manager.
8. Multi-société : isolation des données.

---

## 14. Points d’arbitrage avant implémentation

Décisions à figer avant démarrage code :

1. **Convention de signe** : montants absolus + direction (figé V0.1).
2. **Édition après validation** : totalement bloquée ou partiellement autorisée.
3. **Réouverture d’un point clôturé** : jamais ou admin only.
4. **Création automatique d’une ligne “solde initial”** : non en V1 (solde porté par le point).
5. **Graphique V1** : report possible en V1.1 si la vue graph standard n’est pas suffisante.

### 14.1 Arbitrages retenus pour V0.1

| Sujet | Décision V0.1 |
| --- | --- |
| Convention de signe | montants absolus + champ `direction` |
| Montants signés | champs calculés `signed_projected_amount` et `signed_realized_amount` |
| Journal suivi | journaux de type `bank` ou `cash` |
| Solde initial | calculé sur le point, pas créé comme ligne |
| Poste budgétaire | obligatoire sur toutes les lignes de flux |
| Graphique | report possible en V1.1 si la vue graph standard ne suffit pas |
| Réalisé bancaire | saisie/semi-manuel en V1, rapprochement assisté en V1.1/V2 |
| Seed 20 postes | optionnel, dépend du mapping comptable disponible |

---

## 15. Plan d’exécution recommandé

Ordre d’implémentation :

1. Modèles + contraintes + sécurité.
2. Moteur de calcul (initial/final/min/statut).
3. Vues CRUD opérationnelles.
4. Workflows d’état.
5. Variance prévu/réalisé simple.
6. Seed de postes budgétaires.
7. Cron et optimisations.
8. Graphique (selon décision V1/V1.1).

---

## 16. Statut du document

- Version : `SPEC_TECHNIQUE v0.1`
- Source de vérité fonctionnelle : `README.md`
- Niveau : prêt pour découpage en tickets dev exécutable
