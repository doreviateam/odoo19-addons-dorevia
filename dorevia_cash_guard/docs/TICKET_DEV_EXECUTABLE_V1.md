# TICKET_DEV_EXECUTABLE_V1 — `dorevia_cash_guard`

**Date d'ouverture** : 2026-05  
**Version de référence** : `README.md v0.1` + `SPEC_TECHNIQUE v0.1`  
**Statut** : **Prêt à exécuter**

---

## 1. Objectif

Découper la V1 en tickets exécutable dans un ordre de livraison sûr, avec dépendances explicites et critères d’acceptation vérifiables.

La logique produit visée :

- projection de trésorerie sur période ;
- calcul du solde initial/final/minimum ;
- statut `safe` / `warning` / `risk` ;
- flux `planned` / `simulated` ;
- comparaison simple prévu / réalisé.

---

## 2. Règles transverses (à respecter sur tous les tickets)

- pas de dépendance à MIS Builder ;
- montants stockés en absolu + `direction` ;
- journal suivi de type `bank` ou `cash` ;
- solde initial porté par le point (pas de ligne technique) ;
- `budget_post_id` obligatoire sur chaque flux ;
- seed des 20 postes budgétaires optionnel ;
- multi-société respectée via `company_id`.

---

## 3. Backlog V1 (ordre exécutable)

Ordre de réalisation retenu :

1. `CG-V1-01-SCAFFOLD`
2. `CG-V1-02-MODELS`
3. `CG-V1-03-CONSTRAINTS`
4. `CG-V1-04-CALC-ENGINE`
5. `CG-V1-04B-AUTOTESTS-CALC`
6. `CG-V1-05-SECURITY`
7. `CG-V1-06-WORKFLOW`
8. `CG-V1-07-UI`
9. `CG-V1-08-VARIANCE-TESTS`
10. `CG-V1-09-SEED-OPTIONAL`
11. `CG-V1-10-CRON-OPTIONAL`

## Ticket 01 — Scaffold module et manifest

**ID** : `CG-V1-01-SCAFFOLD`  
**Priorité** : P0  
**Dépend de** : aucun

### Portée

- créer le squelette module `dorevia_cash_guard` ;
- déclarer `depends` : `account`, `base_account_budget`, `mail` ;
- enregistrer fichiers `models`, `views`, `security`, `data` (même si partiels).

### Livrables

- `__manifest__.py`
- `__init__.py`
- structure dossiers conforme à la spec.

### Critères d’acceptation

- module installable sans crash ;
- dépendances résolues ;
- module visible dans Apps (mode dev).

---

## Ticket 02 — Modèles et champs métier

**ID** : `CG-V1-02-MODELS`  
**Priorité** : P0  
**Dépend de** : `CG-V1-01-SCAFFOLD`

### Portée

- créer `dorevia.cash.guard` ;
- créer `dorevia.cash.guard.line` ;
- faire hériter `dorevia.cash.guard` de `mail.thread` ;
- ajouter `mail.activity.mixin` sur `dorevia.cash.guard` (préparation des actions/relances futures) ;
- déclarer sélections :
  - `risk_status`: `safe` / `warning` / `risk`
  - `state`: `draft` / `validated` / `closed`
  - `line_type`: `planned` / `simulated`
  - `direction`: `inflow` / `outflow`
  - `cash_state`: `planned` / `booked` / `payment_entered` / `reconciled` / `variance` / `cancelled`
- ajouter champs signés calculés :
  - `signed_projected_amount`
  - `signed_realized_amount`.

### Livrables

- `models/cash_guard.py`
- `models/cash_guard_line.py`
- mise à jour `models/__init__.py`.

### Critères d’acceptation

- modèles créés en base ;
- champs visibles via technique Odoo ;
- pas d’ambiguïté de convention de signe.

---

## Ticket 03 — Contraintes métier et cohérence données

**ID** : `CG-V1-03-CONSTRAINTS`  
**Priorité** : P0  
**Dépend de** : `CG-V1-02-MODELS`

### Portée

- contraintes Python/SQL :
  - `date_from <= date_to`
  - `alert_threshold >= 0`
  - `projected_amount >= 0`
  - `realized_amount >= 0` si renseigné
  - `sequence >= 0`
  - `bank_journal_id.type in ('bank', 'cash')`
  - cohérence `company_id` parent/ligne/journal ;
- imposer `budget_post_id` requis sur les lignes.

### Livrables

- contraintes dans `cash_guard.py` et `cash_guard_line.py`.

### Critères d’acceptation

- création invalide bloquée avec message explicite ;
- création valide acceptée ;
- comportement stable multi-société.

---

## Ticket 04 — Moteur de calcul trésorerie

**ID** : `CG-V1-04-CALC-ENGINE`  
**Priorité** : P0  
**Dépend de** : `CG-V1-03-CONSTRAINTS`

### Portée

- implémenter calcul `initial_balance` depuis les écritures postées du journal bancaire/caisse sélectionné, à `date_from` ;
- trier les flux par `projection_date`, `sequence`, `id` ;
- calculer pour chaque ligne :
  - `signed_projected_amount`
  - `signed_realized_amount`
  - `balance_after_line`
  - `variance_amount`
- calculer sur le point :
  - `forecast_final_balance`
  - `forecast_min_balance`
  - `min_balance_date`
  - `risk_status`.
- point de vigilance d’implémentation :
  - selon le comportement Odoo 19, confirmer sur instance réelle si le calcul se fait par journal de liquidité ou par comptes de liquidité rattachés au journal ; le choix final doit être testé et documenté.

### Livrables

- méthodes de recalcul dans les modèles ;
- bouton/action “Recalculer”.

### Critères d’acceptation

- le point bas est correct même si le solde final est positif ;
- statut `safe` / `warning` / `risk` correct sur cas limites ;
- recalcul déterministe (ordre stable).

---

## Ticket 04B — Autotests calcul et contraintes

**ID** : `CG-V1-04B-AUTOTESTS-CALC`  
**Priorité** : P0  
**Dépend de** : `CG-V1-04-CALC-ENGINE`

### Portée

- ajouter tests automatiques du moteur Lot A ;
- couvrir :
  - solde initial seul ;
  - projection simple entree/sortie ;
  - tri deterministe `projection_date`, `sequence`, `id` ;
  - statuts `safe`, `warning`, `risk` ;
  - cas critique : solde final positif mais minimum negatif => `risk` ;
  - ligne `simulated` prise en compte (pas d'option d'exclusion en V1) ;
  - variance simple prevu/realise ;
  - contraintes cles (dates, montants, journal, poste budget obligatoire, coherence societe).

### Livrables

- `tests/__init__.py`
- `tests/test_cash_guard_calc.py`
- `tests/test_cash_guard_constraints.py`

### Critères d’acceptation

- les tests passent en environnement Odoo de test ;
- les regressions moteur Lot A sont detectees automatiquement ;
- aucun demarrage Lot B sans validation de cette suite.

---

## Ticket 05 — Sécurité ACL + règles multi-société

**ID** : `CG-V1-05-SECURITY`  
**Priorité** : P1  
**Dépend de** : `CG-V1-04B-AUTOTESTS-CALC`

### Portée

- groupes :
  - `cash_guard_user`
  - `cash_guard_manager`
- ACL sur point et lignes ;
- record rules par `company_id`.

### Livrables

- `security/dorevia_cash_guard_security.xml`
- `security/ir.model.access.csv`.

### Critères d’acceptation

- un user standard ne dépasse pas ses droits ;
- un manager dispose des droits attendus ;
- isolation multi-société confirmée.

---

## Ticket 06 — Workflow d’états et journalisation

**ID** : `CG-V1-06-WORKFLOW`  
**Priorité** : P1  
**Dépend de** : `CG-V1-05-SECURITY`

### Portée

- actions :
  - `action_validate`
  - `action_close`
  - `action_reopen` (manager) ;
- règles d’édition selon `state` ;
- après validation, les champs structurants (période, journal, seuil, lignes) ne sont modifiables que par un manager ou après retour en brouillon ;
- tracer changements sensibles (état, seuil, période).

### Livrables

- logique d’état dans `cash_guard.py`.

### Critères d’acceptation

- transitions interdites correctement bloquées ;
- transitions autorisées opérationnelles ;
- historique visible dans le chatter.

---

## Ticket 07 — Vues, menus et UX de base

**ID** : `CG-V1-07-UI`  
**Priorité** : P1  
**Dépend de** : `CG-V1-06-WORKFLOW`

### Portée

- menu `Comptabilité / Trésorerie / Sécurité Trésorerie` ;
- vues liste/form du point ;
- one2many lignes dans le formulaire ;
- vue liste lignes avec filtres clés ;
- affichage des indicateurs principaux en formulaire.

### Livrables

- `views/menus.xml`
- `views/cash_guard_views.xml`
- `views/cash_guard_line_views.xml`.

### Critères d’acceptation

- parcours CRUD complet possible sans mode technique ;
- filtres principaux utilisables ;
- lisibilité correcte des soldes/statuts.

---

## Ticket 08 — Prévu / réalisé simple + tests V1

**ID** : `CG-V1-08-VARIANCE-TESTS`  
**Priorité** : P1  
**Dépend de** : `CG-V1-07-UI`

### Portée

- finaliser le flux simple prévu/réalisé (`cash_state`, montants réalisés, écart) ;
- préciser explicitement que le rapprochement bancaire assisté/intelligent reste hors V1 ;
- couvrir tests d’acceptation techniques prioritaires ;
- stabiliser données de démonstration minimales.

### Livrables

- tests (unitaires et/ou transactionnels Odoo) ;
- scénarios de recette documentés.

### Critères d’acceptation

- cas nominal de comparaison prévu/réalisé validé ;
- non-régression sur moteur de calcul ;
- tests exécutables en CI locale.

---

## Ticket 09 — Seed optionnel des 20 postes budgétaires

**ID** : `CG-V1-09-SEED-OPTIONAL`  
**Priorité** : P2  
**Dépend de** : `CG-V1-08-VARIANCE-TESTS`

### Portée

- fournir nomenclature documentaire des 20 postes ;
- optionnel : seed XML idempotent si mapping comptable fiable disponible ;
- ne pas charger `budget_post_seed.xml` par défaut si les comptes comptables cibles ne sont pas garantis ;
- ne pas casser une instance sans mapping.

### Livrables

- `data/budget_post_seed.xml` (optionnel activable) ;
- note d’exploitation sur prérequis mapping comptes.

### Critères d’acceptation

- aucun doublon à réinstallation/mise à jour ;
- aucune création invalide de poste sans comptes requis ;
- activation/désactivation du seed maîtrisée.

---

## Ticket 10 — Cron de recalcul (option V1)

**ID** : `CG-V1-10-CRON-OPTIONAL`  
**Priorité** : P2  
**Dépend de** : `CG-V1-08-VARIANCE-TESTS`

### Portée

- cron quotidien de recalcul points non clôturés ;
- désactivation possible par configuration ;
- logs minimum en cas d’erreur.

### Livrables

- `data/cash_guard_cron.xml` ;
- méthode batch de recalcul sécurisée.

### Critères d’acceptation

- cron fonctionne sans bloquer les opérations usuelles ;
- erreurs traçables ;
- désactivation effective.

---

## 4. Définition of Done V1

La V1 est considérée livrable si :

- tickets P0 et P1 sont validés ;
- règles transverses respectées ;
- calcul du risque fiable sur jeux de tests ;
- sécurité opérationnelle (ACL + multi-société) ;
- documentation mise à jour (`README.md`, `SPEC_TECHNIQUE.md`, ce fichier) ;
- mise à jour explicite du `README.md` en cas d’écart d’implémentation ;
- mise à jour explicite de `SPEC_TECHNIQUE.md` en cas d’arbitrage technique différent ;
- mini-recette utilisateur validée : créer un point, ajouter des flux, recalculer, lire le statut.

---

## 5. Découpage de livraison recommandé

- **Lot A (fondation)** : tickets 01 a 04 + 04B
- **Lot B (operationnel)** : tickets 05 a 08
- **Lot C (optionnels)** : tickets 09 a 10

---

## 6. Statut document

- Fichier : `docs/TICKET_DEV_EXECUTABLE_V1.md`
- Version : `v0.1`
- Statut : **prêt pour lancement dev**
