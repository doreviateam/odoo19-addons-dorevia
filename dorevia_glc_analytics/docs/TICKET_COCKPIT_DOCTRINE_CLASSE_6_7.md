# Ticket — Doctrine cockpit GLC : classe 6/7 + analytique exploitable

**Module :** `dorevia_glc_analytics`
**Branche :** `feat/glc-cockpit-doctrine-classe-6-7-19.0.4.8.0`
**Version cible :** `19.0.4.8.1`
**Statut :** **Validé MOA — implémenté** (2026-05-28)
**Référence amont :** [TICKET_COCKPIT_SOURCE_REALISE.md](./TICKET_COCKPIT_SOURCE_REALISE.md) (`19.0.4.7.0`, PR #40) · [CADRAGE_FINAL_PALIER_4.md](./CADRAGE_FINAL_PALIER_4.md)

---

## 1. Contexte MOA

Le cockpit GLC livré en `19.0.4.7.0` corrige la **source du réalisé SALAIRES** (compta analytique 631/633/641/645) mais conserve une limite héritée de la V1 Palier 4 :

| Famille cockpit | Périmètre activités `19.0.4.7.0` |
|---|---|
| Recettes activité | **BAR**, **PRESTATIONS**, **PRIVATISATIONS** uniquement |
| Dépenses hors salaires | **STRUCTURE** uniquement |
| Salaires | toute activité (via 631/633/641/645 + analytique) |
| Financements | **SUBVENTIONS**, **ADHESIONS** uniquement |

Conséquence : une charge **625100 + [MISSIONS]** (ex. : 1 552 € sur `glc-rgl-test-import` 2026) **n'apparaît nulle part** dans le cockpit, alors qu'elle réunit toutes les conditions d'une dépense réelle exploitable.

---

## 2. Doctrine MOA validée

> Une ligne remonte dans le cockpit si elle réunit les 4 conditions suivantes :
>
> 1. elle porte une **date** dans la période analysée ;
> 2. elle porte un **montant non nul** ;
> 3. elle est rattachée à un **compte comptable de classe 6 ou 7** ;
> 4. elle porte une **distribution analytique exploitable**.

**Règle de lecture :**

| Classe GL | Signification | Famille cockpit |
|---|---|---|
| **6xxx** + analytique | argent qui **sort** pour l'activité | **soustraction** — DÉPENSES (hors payroll) ou SALAIRES (631/633/641/645) |
| **7xxx** + analytique | argent qui **entre** pour l'activité | **addition** — RECETTES ou RESSOURCES selon plan analytique |

**Cartographie par plan analytique :**

| Compte analytique | Plan | Réception classe 7 | Réception classe 6 |
|---|---|---|---|
| `BAR`, `PRESTATIONS`, `PRIVATISATIONS`, `RESIDENCES`, `MISSIONS`, `LOCATION_RADIO`, `STRUCTURE` | **Activités GLC** | **RECETTES** | **DÉPENSES** (hors payroll) ou **SALAIRES** |
| `SUBVENTIONS`, `ADHESIONS`, `DONS`, `RESSOURCES_PROPRES` | **Financements GLC** | **FINANCEMENTS / RESSOURCES** | n/a *(financements ne portent pas de charge en pratique)* |

**Clarification MOA complémentaire (2026-05-28) — périmètre analytique :**

> Par défaut, le cockpit traite **tous les comptes analytiques, quel que soit leur plan**, dès lors qu'ils sont associés à une ligne comptable réelle de classe 6 ou 7.

| Règle | Valeur |
|---|---|
| Périmètre analytique par défaut | **Tous les plans** (Activités GLC, Financements GLC, et tout autre plan) |
| Filtre par plan analytique | **Option UX ultérieure** — ne doit pas limiter le calcul par défaut |
| Exclusions analytiques | codes legacy (`BAR_RESTAU`, …) · `RH_PERSONNEL` |
| Filtre `glc_report_active` | **Hors périmètre calcul réalisé** — réservé à un futur filtre d'affichage |

**Exemples financements (classe 7) :**

| Écriture | Résultat cockpit |
|---|---|
| 741xxx + [SUBVENTIONS] | ressource SUBVENTIONS (onglet Ressources + détail) |
| 756xxx + [ADHESIONS] | ressource ADHESIONS |
| 758xxx + [RESSOURCES_PROPRES] | ressource propre |

---

## 3. Exclusions confirmées

Les classes hors 6/7 ne remontent pas dans le cockpit, même si la ligne porte une analytique :

| Classe / Compte | Motif d'exclusion |
|---|---|
| **5xx** (512 banque, 53 caisse) | trésorerie — preuve du flux, pas nature économique |
| **4xx** (401 fournisseurs, 411 clients, 467 attente/passage) | tiers — pas charge ni produit |
| **1xx** (164 emprunts) | financement bilan — hors exploitation |
| Lignes de **lettrage / paiement seul** | flux comptable sans nature d'activité |
| Écritures **sans distribution analytique exploitable** | non pilotables — hors cockpit détail |

**Défense en profondeur (cumul) :**

1. `account_type` ∈ income / income_other / expense / expense_direct_cost / expense_depreciation
2. **GL code commence par `6` ou `7`** *(nouveau garde-fou explicite)*
3. exclusion préfixes legacy (164) et codes analytiques legacy (`RH_PERSONNEL`, `BAR_RESTAU`, etc.)
4. exclusion préfixes payroll des DÉPENSES (déjà actif)

---

## 4. Conséquences fonctionnelles

| Cas | Comportement attendu | Avant `19.0.4.8.0` | Après `19.0.4.8.0` |
|---|---|---|---|
| 625100 + `[MISSIONS]` | DÉPENSES MISSIONS | **manquant** | ✅ remonte |
| 606xxx + `[BAR]` | DÉPENSES BAR | **manquant** *(STRUCTURE only)* | ✅ remonte |
| 707xxx + `[BAR]` | RECETTES BAR | ✅ | ✅ |
| 706xxx + `[PRESTATIONS]` | RECETTES PRESTATIONS | ✅ | ✅ |
| 741xxx + `[SUBVENTIONS]` | FINANCEMENTS | ✅ | ✅ |
| 645200 + `[STRUCTURE]` | SALAIRES STRUCTURE | ✅ *(depuis `19.0.4.7.0`)* | ✅ |
| 615xxx + `[RESIDENCES]` | DÉPENSES RESIDENCES | **manquant** | ✅ remonte |
| 512100 + `[BAR]` | exclu | ✅ exclu | ✅ exclu *(explicite classe 6/7)* |
| 467000 + `[STRUCTURE]` | exclu | ✅ exclu *(par account_type)* | ✅ exclu *(double garde-fou)* |

---

## 5. Implémentation

### 5.1. Comptabilité analytique — domaines

| Méthode | Comportement `19.0.4.8.1` |
|---|---|
| `_cockpit_analytic_accounts` *(nouveau)* | **tous** les comptes analytiques société, **tous plans**, hors codes legacy / `RH_PERSONNEL` |
| `_funding_analytic_accounts` | sous-ensemble financement (plan Financements GLC ou `glc_activity_type = financement`) |
| `_activity_revenue_analytic_accounts` | cockpit accounts − funding accounts |
| `_revenue_analytic_line_domain` | classe **7** + analytique exploitable |
| `_expense_analytic_line_domain` | classe **6** hors payroll + analytique exploitable |
| `_payroll_analytic_line_domain` | classe **6** payroll (631/633/641/645) + analytique exploitable |

### 5.2. Agrégation `_aggregate_period`

| Indicateur | Périmètre analytique | Périmètre GL |
|---|---|---|
| `activity_revenue_realized` | comptes **hors financement** (tous plans) | classe 7 |
| `funding_realized` | comptes **financement** (plan Financements GLC) | classe 7 |
| `general_expenses_realized` | **tous** comptes analytiques exploitables | classe 6 hors payroll |
| `payroll_realized` | **tous** comptes analytiques exploitables | classe 6 payroll |

### 5.3. Détail par activité

Pour **chaque** compte analytique exploitable (tous plans) × mois :

- `revenue_realized` = classe 7 + cet axe
- `expense_realized` = classe 6 hors payroll + cet axe
- `payroll_realized` = classe 6 payroll + cet axe
- comptes financement : budget lu via `line_type = funding`

→ **SUBVENTIONS**, **ADHESIONS**, **RESSOURCES_PROPRES** apparaissent dans le détail dès qu'ils portent du réel classe 7.

### 5.4. Budget — hors scope `19.0.4.8.0`

Le mapping budget (`glc.budget.line` Palier 3) reste **inchangé** :

- recettes : codes `BAR` / `PRESTATIONS` / `PRIVATISATIONS`
- frais généraux : code `STRUCTURE`
- masse salariale : codes `GLC_COCKPIT_PAYROLL_BUDGET_CODES`

Réserve documentée (déjà tracée) : **mapping budget vs lecture réalisé** — à réaligner dans un ticket Palier 5 si MOA le souhaite.

---

## 6. Tests cibles `19.0.4.8.0`

| Réf | Cas | Famille attendue | Type |
|---|---|---|---|
| R15-DEP-MISSIONS | 625xxx + `[MISSIONS]` | DÉPENSES MISSIONS | auto |
| R15-DEP-RESIDENCES | 615xxx + `[RESIDENCES]` | DÉPENSES RESIDENCES | auto |
| R15-DEP-BAR | 606xxx + `[BAR]` | DÉPENSES BAR | auto |
| R15-REV-PRESTATIONS | 706xxx + `[PRESTATIONS]` | RECETTES PRESTATIONS | auto |
| R15-EXCL-467 | 467xxx + `[STRUCTURE]` | **exclu** *(classe 4)* | auto |
| R15-EXCL-512-PAR-CLASS | 512xxx + analytique | **exclu** *(classe 5)* | auto |
| R15-FUND-SUB | 741xxx + [SUBVENTIONS] | FINANCEMENTS + détail | auto |
| R15-FUND-ADH | 756xxx + [ADHESIONS] | FINANCEMENTS + détail | auto |
| R15-FUND-RP | 758xxx + [RESSOURCES_PROPRES] | FINANCEMENTS + détail | auto |
| R15-FUND-TOTAL | Recettes BAR + financements multi-plans | `resources_realized` cohérent | auto |

**Non-régression :** 74 post-tests `19.0.4.7.0` conservés.

---

## 7. Recette MOA manuelle (post-livraison)

1. Recharger `-u dorevia_glc_analytics` + restart Odoo + hard refresh navigateur.
2. Ouvrir le cockpit, période **2026-01-01 → 2026-12-31**, scénario `Initial`.
3. **Onglet Détail par activité** :
   - Vérifier la présence d'une ligne **MISSIONS** sur les mois portant des frais 625xxx.
   - Vérifier la présence d'une ligne **RESIDENCES** si des charges 6xxx + `[RESIDENCES]` existent.
   - Vérifier le maintien des lignes **BAR / PRESTATIONS / PRIVATISATIONS / STRUCTURE**.
4. **Onglet Charges de structure** :
   - `general_expenses_realized` doit refléter **toutes** les charges hors payroll, pas seulement STRUCTURE.
5. **Onglet Synthèse graphique** :
   - Graphe Structure mensuelle : les barres Dépenses incluent désormais MISSIONS, RESIDENCES, etc.
   - Graphe Marge par activité : toutes activités productrices d'écart visibles.
6. **Exclusions à vérifier** :
   - lignes 401 / 411 / 467 / 512 / 53 → **absentes**, même si elles portent une analytique.

---

## 8. Décisions MOA (2026-05-28)

| Point | Décision |
|---|---|
| Date + montant + classe 6/7 + analytique = règle unique de remontée | ✅ GO |
| Étendre DÉPENSES à toutes les activités (pas seulement STRUCTURE) | ✅ GO |
| Étendre RECETTES à toutes les activités (pas seulement BAR/PRESTATIONS/PRIVATISATIONS) | ✅ GO |
| Périmètre analytique = **tous les plans** par défaut (pas seulement Activités GLC) | ✅ GO |
| Financements (SUBVENTIONS, ADHESIONS, RESSOURCES_PROPRES) visibles dans le détail | ✅ GO |
| Filtre par plan analytique = option UX ultérieure, pas limite de calcul | ✅ GO |
| Garde-fou explicite classe 6/7 sur le code GL | ✅ GO |
| Exclusions 4xx / 5xx (411/401/467/512/53) confirmées | ✅ GO |
| Mapping budget Palier 3 inchangé dans `19.0.4.8.0` | ✅ GO *(réserve documentée)* |
| Bump version `19.0.4.8.0` | ✅ GO |

---

## 9. Verdict cible

> Le cockpit GLC doit refléter **toute** activité réelle portée par des écritures classe 6/7 + analytique exploitable. Aucune activité du plan **Activités GLC** ne doit être invisible dès lors qu'elle porte un mouvement réel.

---

*Ticket rédigé MOA — 2026-05-28 — alignement cockpit sur doctrine source réalisé (suite `19.0.4.7.0`).*
