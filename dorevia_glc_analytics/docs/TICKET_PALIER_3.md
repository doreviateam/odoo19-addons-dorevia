# Ticket Palier 3 — Budget prévisionnel GLC (`dorevia_glc_budget`)


> **Document historique** — ne décrit plus le produit installé depuis **`19.0.13.0.0`** / **`19.0.14.0.0`**. État actuel : [ETAT_MODULE_ACTUEL.md](./ETAT_MODULE_ACTUEL.md).

---

**Module :** `dorevia_glc_budget` *(nouveau module — séparé de `dorevia_glc_analytics`)*  
**Branche cible :** `feat/glc-budget-palier-3`  
**Version cible :** `19.0.1.0.0`  
**Statut :** **Validé MOA** — ticket ouvert, développement après merge renommage  
**Prérequis :**
- Palier 0 gelé : socle analytique (`dorevia_glc_analytics`)
- Palier 1 gelé : anomalies analytiques
- Palier 2 gelé : ventilation salariale (PR #26)
- Plans `GLC - Activités` et `GLC - Financements` opérationnels

**Références :** [CADRAGE_BUDGET_COCKPIT.md](./CADRAGE_BUDGET_COCKPIT.md) · [PALIERS.md](./PALIERS.md) · [spec V1.1](./README.md)

---

## 1. Contexte

Le Palier 2 fournit le **réalisé salarial ventilé** (overlay de gestion).

Le besoin MOA suivant est un **cockpit de soutenabilité économique** (Palier 4), croisant :

```text
réalisé analytique  vs  budget prévisionnel  vs  alertes de couverture
```

Le Palier 3 prépare cette couche en créant un **module budget léger**, centré GLC, **sans** reprendre un moteur budgétaire générique (pas de démarrage OCA Budget).

Objectif Palier 3 : permettre de saisir une **trajectoire prévisionnelle simple**, mois par mois, par axe analytique GLC.

---

## 2. Objectif Palier 3

Créer le module **`dorevia_glc_budget`** pour :

- structurer un budget annuel par société ;
- gérer un scénario (`initial`, `revised`, `landing`) ;
- saisir des lignes mensuelles par compte analytique ;
- typer chaque ligne : recette / charge / financement ;
- conserver un montant prévu et un commentaire optionnel.

Le budget sert **uniquement** de référence prévisionnelle pour le futur cockpit (Palier 4).

---

## 3. Doctrine d’architecture

### 3.1 Pas d’écriture comptable

Le Palier 3 ne génère **aucune** écriture comptable (`account.move`).

### 3.2 Pas d’écriture analytique

Le Palier 3 ne crée **pas** d’`account.analytic.line`.

### 3.3 Référentiel analytique GLC

Les lignes budgétaires sont rattachées aux comptes du plan **`GLC - Activités`** et, si besoin MOA, aux comptes du plan **`GLC - Financements`** pour les lignes de type `funding`.

### 3.4 Module autonome et léger

- **Nouveau module** `dorevia_glc_budget` — ne pas alourdir `dorevia_glc_analytics`.
- **Pas** de dépendance OCA Budget.
- Dépendance minimale : `dorevia_glc_analytics` (plans, comptes, sécurité GLC).

### 3.5 Applicabilités analytiques

**Inchangées** — le Palier 3 n’introduit aucun durcissement des applicabilités Odoo.

---

## 4. Modèles attendus

### 4.1 `glc.budget`

En-tête de budget prévisionnel.

| Champ | Type / valeurs | Description |
|---|---|---|
| `name` | Char | Libellé (ex. « Budget 2026 — initial ») |
| `year` | Integer | Année budgétaire |
| `company_id` | Many2one `res.company` | Société |
| `scenario` | Selection | `initial` · `revised` · `landing` |
| `state` | Selection | `draft` · `validated` · `archived` |
| `line_ids` | One2many → `glc.budget.line` | Lignes mensuelles |
| `note` | Text | Commentaire global |
| `validated_by` | Many2one `res.users` | Validateur |
| `validated_date` | Datetime | Date validation |

**Contrainte d’unicité proposée :** `(company_id, year, scenario)` — un scénario par année et société.

### 4.2 `glc.budget.line`

Ligne budgétaire mensuelle.

| Champ | Type / valeurs | Description |
|---|---|---|
| `budget_id` | Many2one `glc.budget` | Budget parent |
| `period_date` | Date | Premier jour du mois concerné |
| `analytic_account_id` | Many2one `account.analytic.account` | Axe analytique GLC |
| `line_type` | Selection | `revenue` · `expense` · `funding` |
| `amount` | Monetary | Montant prévu |
| `currency_id` | Related | Devise société |
| `note` | Char / Text | Commentaire ligne |

**Contraintes métier :**

| Règle | Détail |
|---|---|
| Axe analytique | Doit appartenir au plan `GLC - Activités` **ou** `GLC - Financements` selon `line_type` |
| Type `revenue` / `expense` | Compte du plan **Activités GLC** uniquement |
| Type `funding` | Compte du plan **Financements GLC** (ex. `SUBVENTIONS`, adhésions) |
| Unicité | Pas de doublon `(budget_id, period_date, analytic_account_id, line_type)` |
| Montant | `amount` ≥ 0 en V1 (signe porté par `line_type`) |

### 4.3 Exemple de saisie

| Mois | Axe analytique | Type | Montant prévu |
|---|---|---|---|
| Avril | RH / Personnel (`STRUCTURE` ou compte RH dédié) | `expense` | 8 500 € |
| Avril | Frais généraux | `expense` | 1 200 € |
| Avril | Prestation & Animation | `revenue` | 3 000 € |
| Avril | Subvention d’exploitation | `funding` | 5 000 € |

> Les codes analytiques exacts suivent la nomenclature Palier 0 (cf. spec §4.2–4.3).

---

## 5. Workflow et statuts

| État | Description | Actions |
|---|---|---|
| `draft` | Saisie en cours | CRUD lignes libre |
| `validated` | Budget validé MOA / gestionnaire | Lignes en lecture seule sauf déverrouillage contrôlé |
| `archived` | Exercice ou scénario clos | Lecture seule |

**Règles V1 :**

- validation **non bloquante** pour la comptabilité ;
- pas de contrôle automatique « total budget = total comptable » en Palier 3 ;
- déverrouillage réservé **Gestionnaire GLC** (à confirmer MOA en recette).

---

## 6. Interface attendue (minimal Palier 3)

| Écran | Description |
|---|---|
| **Budgets GLC** | Liste / formulaire `glc.budget` |
| ***(retiré — lignes budget)*** | Onglet inline ou vue liste filtrée par budget |
| **Filtres** | Année · scénario · société · mois · type · axe analytique |

**Menus proposés** (sous `Facturation → Pilotage GLC` ou racine dédiée « Budget GLC ») :

- `*(retiré — budgets)*`

**Groupe :** Gestionnaire GLC (CRUD) · Utilisateur GLC (lecture seule, option MOA).

---

## 7. Lien Palier 4 (cockpit — hors implémentation Palier 3)

Le Palier 4 consommera :

```text
Prévisionnel : glc.budget.line (Palier 3)
Réalisé      : account.analytic.line (Palier 0 + discipline de saisie)
```

Agrégations attendues côté cockpit :

- mois × compte analytique × type (`revenue` / `expense` / `funding`) ;
- indicateurs couverture salaires et frais généraux ;
- écart budget / réalisé ;
- alertes rouge / orange / vert.

Le Palier 3 **prépare les données** ; il n’implémente **pas** le cockpit.

---

## 8. Dépendances techniques

| Dépendance | Motif |
|---|---|
| `account` | Monnaie, société |
| `analytic` | Comptes analytiques GLC |
| **`dorevia_glc_analytics`** | Plans Activités / Financements, groupes sécurité, menus racine |

**Exclus explicitement :**

- modules OCA Budget ;
- `hr` / `hr_payroll` ;
- génération d’écritures.

---

## 9. Sécurité

- `ir.model.access.csv` : droits sur `glc.budget`, `glc.budget.line`
- Réutiliser les groupes `Utilisateur GLC` / `Gestionnaire GLC` (extension ou dépendance manifest)
- Données prévisionnelles : accès lecture large possible ; édition **Gestionnaire GLC** minimum

---

## 10. Hors périmètre Palier 3

- Contrôle de gestion (Palier 4)
- Croisement réalisé / budget / alertes
- Graphiques avancés, export Excel / PDF
- Comparaison scénarios multiples côte à côte
- Projections fin d’année, atterrissage automatique
- Bloc trésorerie / mouvements financiers
- Intégration OCA Budget
- Écritures comptables ou analytiques automatiques
- Registre bénévole
- Clôture analytique mensuelle
- Ventilation salariale (Palier 2 — gelé, consommé en lecture seule par Palier 4)

---

## 11. Critères d’acceptation

| ID | Critère |
|---|---|
| CA1 | Module `dorevia_glc_budget` installable sans OCA Budget |
| CA2 | Création budget annuel avec scénario `initial` / `revised` / `landing` |
| CA3 | Saisie lignes mensuelles par axe analytique GLC |
| CA4 | Types `revenue`, `expense`, `funding` avec domaines analytiques cohérents |
| CA5 | Refus d’un compte Financements sur ligne `revenue` ou `expense` |
| CA6 | Refus d’un compte Activités sur ligne `funding` (si règle MOA retenue) |
| CA7 | Workflow brouillon → validé → archivé |
| CA8 | Aucune écriture comptable ni analytique générée |
| CA9 | Non-régression `dorevia_glc_analytics` (25 tests existants verts) |
| CA10 | Tests automatisés Palier 3 (budget + lignes + contraintes) |

---

## 12. Documentation attendue

- [ ] [PALIERS.md](./PALIERS.md) — statut Palier 3
- [ ] [CADRAGE_BUDGET_COCKPIT.md](./CADRAGE_BUDGET_COCKPIT.md) — lien croisé
- [x] `RECETTE_MANUELLE_PALIER_3.md` — recette MOA (2026-05-27 · `glc-rgl-test-import`)
- [x] README module `dorevia_glc_budget`

---

## 13. Règle de livraison

```text
Branche : feat/glc-budget-palier-3
Base    : main (post merge PR #26 + renommage dorevia_glc_analytics)

Ne pas mélanger avec :
- Palier 2 (gelé)
- Palier 4 cockpit (ticket séparé)
- Renommage module analytics (branche refactor/rename-dorevia-glc-analytics)
```

**Séquence :**

1. Validation MOA du présent ticket
2. Création squelette module `dorevia_glc_budget`
3. Développement Palier 3 sur branche dédiée
4. Recette MOA sur `glc-rgl-test-import`
5. Merge PR Palier 3
6. Gel Palier 3 → ouverture Palier 4

---

## 14. Décisions MOA validées (2026-05-27)

| # | Décision |
|---|---|
| D1 | Module séparé `dorevia_glc_budget` — pas d’extension monolithique analytics |
| D2 | Pas d’OCA Budget en V1 |
| D3 | Aucune écriture comptable ni analytique |
| D4 | Lignes mensuelles × axe analytique × type recette/charge/financement |
| D5 | Scénarios `initial` / `revised` / `landing` |
| D6 | Un scénario actif par `(société, année, scénario)` |
| D7 | Montants prévus ≥ 0 — sens porté par `line_type` |
| D8 | Cockpit et alertes = Palier 4 |

### Points ouverts (non bloquants Palier 3)

- Menu sous `Pilotage GLC` vs entrée racine « Budget GLC ».
- Déverrouillage budget validé : workflow simple vs chatter.
- Import CSV des lignes budgétaires (V2 ?).
- Mapping exact codes analytiques ↔ libellés MOA (Bar & Restau = `BAR`, etc.).

---

## Annexe — mapping axes MOA ↔ codes Palier 0

| Libellé MOA cockpit | Code analytique (Palier 0) |
|---|---|
| Bar & Restau | `BAR` |
| Prestation & Animation | `PRESTATIONS` |
| Privatisation Espace | `PRIVATISATIONS` |
| RH / Personnel | Ventilation Palier 2 — comptes activités cibles (pas `RH_PERSONNEL` historique) |
| Frais généraux | `STRUCTURE` (ou compte dédié si créé MOA) |
| Résidence artiste | `RESIDENCES` |
| Déplacement & Mission | `MISSIONS` |
| Subvention d’exploitation | Plan Financements — `SUBVENTIONS` |
