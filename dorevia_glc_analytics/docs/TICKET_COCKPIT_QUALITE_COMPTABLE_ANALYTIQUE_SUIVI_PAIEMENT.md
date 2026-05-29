# Ticket — Cockpit · Qualité comptable, analytique & suivi paiement

**Module :** `dorevia_glc_analytics` *(extension cockpit)*  
**Version installée (réf.) :** **`19.0.5.0.1`** · lot trésorerie Palier 5 **GO complet MOA**  
**Statut :** **GO cadrage MOA confirmé** (2026-05-29) — recette validée · Option A · V1 Q1+Q2+Q3 · **GQ-6 en attente — pas de GO code**  
**Date ouverture :** 2026-05-29

**Références :** [MEMO_RAFFINEMENT_QUALITE_COMPTABLE_ANALYTIQUE.md](./MEMO_RAFFINEMENT_QUALITE_COMPTABLE_ANALYTIQUE.md) · [Recette qualité & paiement](./recette/RECETTE_MANUELLE_COCKPIT_QUALITE_PAIEMENT.md) · [PALIERS.md](./PALIERS.md) · [TICKET_PALIER_5_TRESORERIE_COMPTE_BANCAIRE_REFERENCE.md](./TICKET_PALIER_5_TRESORERIE_COMPTE_BANCAIRE_REFERENCE.md) · [TICKET_COCKPIT_COMPTE_BANCAIRE_REFERENCE.md](./TICKET_COCKPIT_COMPTE_BANCAIRE_REFERENCE.md) · [TICKET_PALIER_1.md](./TICKET_PALIER_1.md) · [Recette période libre](./recette/RECETTE_MANUELLE_COCKPIT_GLC_PERIODE_LIBRE.md)

---

## 1. Contexte MOA

Le cockpit GLC affiche aujourd’hui des **KPI d’exploitation bruts** utiles au pilotage :

- **Recette** · **Cumul RH** · **Dépense** · **Solde**

Ces chiffres proviennent du **réalisé analytique comptabilisé** (classes 6/7 · `account.analytic.line`) et restent **gelés** depuis le Palier 4 réaligné `19.0.4.9.0`.

Le Palier 5 a ajouté une **lecture trésorerie séparée** (compte bancaire de référence · flux 512) sans modifier l’exploitation.

**Constat MOA :** les KPI exploitation ne répondent pas encore aux questions opérationnelles suivantes :

| Question MOA | Couche attendue |
|---|---|
| Quelle part est facturée mais non payée ? | Suivi paiement |
| Quelle part est partiellement payée / en cours ? | Suivi paiement |
| Quel reste à encaisser / à payer ? | Suivi paiement |
| Les pièces sont-elles correctement ventilées analytiquement ? | Qualité analytique |
| Les comptes tiers sont-ils lettrés ? | Qualité comptable |

**Décision MOA :** ouvrir un **lot de raffinement cockpit** — qualité comptable, analytique et suivi paiement — par **cadrage avant code**, sur le modèle Palier 5 trésorerie.

---

## 2. Doctrine — quadruple lecture cockpit

> **Règle non négociable :** ce lot **n’altère aucun agrégat exploitation** existant. Il ajoute des **lectures complémentaires** de fiabilité et de cycle de paiement.

| Couche | Source | Rôle | Impact changement compte bancaire |
|---|---|---|---|
| **Exploitation** | `account.analytic.line` classes 6/7 | Recette · Cumul RH · Dépense · Solde | **Aucun** *(gelé Palier 4)* |
| **Trésorerie** | `account.move.line` compte 512 de référence | Entrées · sorties · virements · solde période | **Filtré** par journal bancaire |
| **Suivi paiement** | `account.move` / lignes tiers 401·411 | Facturé · payé · partiel · ouvert · reste dû | **Indépendant** du compte bancaire cockpit |
| **Qualité comptable** | `account.move` / `account.move.line` | Couverture analytique · lettrage tiers | **Indépendant** du compte bancaire cockpit |

### Distinctions MOA à préserver

```text
Comptabilisé  ≠  Payé        ≠  Encaissé en banque
Lettrage tiers ≠  Rapprochement bancaire
Anomalie A1–A6 (Palier 1)    ≠  KPI couverture cockpit (agrégat période)
```

---

## 3. Objectif du lot

Transformer des **contrôles ponctuels** (assistant anomalies Palier 1, contrôles manuels MOA) en **indicateurs permanents** dans le cockpit, pour répondre à :

```text
Avant de piloter, vérifier que les données de pilotage sont fiables.
```

---

## 4. Proposition périmètre V1

### 4.1 Inclus V1 *(MVP MOA)*

| Bloc | Contenu V1 |
|---|---|
| **Q1 — Couverture analytique** | KPI période · compteur pièces · liste actionnable des pièces/lignes non couvertes |
| **Q2 — Lettrage tiers** | Taux clients / fournisseurs · montants non lettrés · ancienneté *(bucket 0–30 / 31–60 / 61–90 / 90+ j)* |
| **Q3 — Suivi paiement** | Synthèse clients + fournisseurs · statuts Odoo · reste à encaisser / payer |
| **Transversal** | Filtres **société** · **période cockpit** · pièces **postées** uniquement |
| **UI** | **2 onglets cockpit séparés** *(recommandation §8)* |
| **Tests** | Non-régression **invariant exploitation** · tests auto par bloc |
| **Docs** | Recette manuelle dédiée |

### 4.2 Exclus V1 *(report V2)*

| Sujet | Report |
|---|---|
| Contrôle **bloquant** à la validation de pièce | V2 — alerte seule en V1 |
| Rapprochement **bancaire** (`account.bank.statement`) | V2 / `dorevia_cash_guard` |
| Prévisionnel encaissement / échéancier trésorerie | V2 |
| Export Excel / PDF des listes | Palier 5 élargi |
| Seuils couleur **configurables** par société | V2 — seuils fixes documentés en V1 |
| Drill-down OWL avancé multi-niveaux | V1 = listes Odoo actionnables |
| Recalcul des KPI exploitation « net de non payé » | **Hors scope — interdit** |

---

## 5. Bloc Q1 — Taux de couverture analytique

### 5.1 Question métier

Les pièces d’exploitation de la période sont-elles **correctement rattachées** à un axe analytique GLC exploitable ?

### 5.2 Définition V1

```text
Taux couverture analytique =
  Pièces postées « pertinentes » entièrement couvertes
  /
  Pièces postées « pertinentes » contrôlées
```

**Pièce couverte :** toutes les lignes **métier pertinentes** portent une `analytic_distribution` non vide **ou** génèrent des `account.analytic.line` exploitables cockpit.

### 5.3 Périmètre pièces V1

| Inclus | Exclus |
|---|---|
| `out_invoice` · `out_refund` | Écritures banque 512/53 |
| `in_invoice` · `in_refund` | Lignes TVA · lignes tiers 401/411 seules |
| Lignes produit / charge (`display_type = product`) | Écritures purement bilan |
| État **`posted`** | Brouillons · annulés |
| Date pièce ∈ `[date_from, date_to]` cockpit | Hors période |

**Alignement Palier 1 :** réutiliser la logique de distinction lignes métier / techniques du wizard `glc.analytic.anomaly.wizard` (contrôles A1–A6) — **sans dupliquer** les règles métier contradictoires.

### 5.4 Restitution V1

| Indicateur | Type |
|---|---|
| `quality_analytic_moves_checked` | Entier |
| `quality_analytic_moves_covered` | Entier |
| `quality_analytic_coverage_rate` | % |
| `quality_analytic_moves_uncovered` | Entier |
| Liste pièces non couvertes | Action `account.move` filtrée |
| Détail lignes sans analytique | Sous-liste `account.move.line` |

### 5.5 Seuils MOA proposés *(mémo)*

| Couleur | Seuil |
|---|---|
| Vert | **100 %** |
| Orange | **95 % – 99,99 %** |
| Rouge | **< 95 %** |

---

## 6. Bloc Q2 — Taux de lettrage

### 6.1 Question métier

Les comptes **clients** et **fournisseurs** sont-ils correctement rapprochés de leurs règlements ?

### 6.2 Définition V1 *(montant)*

```text
Taux lettrage clients =
  Σ |balance| lignes 411 lettrées (reconciled)
  /
  Σ |balance| lignes 411 lettrables postées

Taux lettrage fournisseurs =
  idem sur comptes 401 (liability_payable)
```

**Lettrable :** ligne tiers postée sur compte `asset_receivable` / `liability_payable`, hors section technique, **à la date de clôture du filtre période** *(solde ouvert cumulé — voir risque §9)*.

### 6.3 Restitution V1

| Indicateur | Clients | Fournisseurs |
|---|---|---|
| Taux lettrage | `quality_reconcile_rate_customer` | `quality_reconcile_rate_supplier` |
| Montant non lettré | `quality_unreconciled_amount_customer` | `quality_unreconciled_amount_supplier` |
| Nb lignes / pièces ouvertes | compteur | compteur |
| Ancienneté | buckets jours sur `date_maturity` ou `date` | idem |
| Liste actionnable | `account.move.line` domaine 411 non lettrées | domaine 401 |

### 6.4 Distinction lettrage vs suivi paiement

| KPI | Objet | Granularité |
|---|---|---|
| **Lettrage** | Qualité rapprochement comptable tiers | Lignes 401/411 |
| **Suivi paiement** | Cycle facture → règlement | Pièces `account.move` |

Les deux coexistent ; le lettrage **ne remplace pas** le statut `payment_state`.

---

## 7. Bloc Q3 — Suivi paiement des factures

### 7.1 Question métier

Parmi le **facturé posté** de la période, quelle part est payée, partielle, ouverte ou en cours de traitement ?

### 7.2 Périmètre V1

| Type | `move_type` |
|---|---|
| Clients | `out_invoice` · `out_refund` |
| Fournisseurs | `in_invoice` · `in_refund` |
| État | `posted` |
| Période | `invoice_date` *(ou `date` si vide)* ∈ fenêtre cockpit |

### 7.3 Restitution V1 — clients

| Indicateur | Calcul V1 proposé |
|---|---|
| Factures clients émises | `count` + `Σ amount_total_signed` pièces `out_invoice` |
| Factures clients payées | `payment_state = paid` |
| Partiellement payées | `payment_state = partial` |
| En cours de paiement | `payment_state = in_payment` |
| Non payées | `payment_state = not_paid` |
| Avoirs clients | `out_refund` — montants **signés** |
| Reste à encaisser | `Σ amount_residual_signed` sur `out_invoice` ouverts |

### 7.4 Restitution V1 — fournisseurs

| Indicateur | Calcul V1 proposé |
|---|---|
| Factures fournisseurs reçues | `in_invoice` postées |
| Payées / partielles / en cours / ouvertes | idem via `payment_state` |
| Avoirs fournisseurs | `in_refund` |
| Reste à payer | `Σ amount_residual_signed` sur `in_invoice` ouverts |

### 7.5 Règles métier V1

```text
Déjà encaissé (client)  = amount_total_signed - amount_residual_signed  (facture)
Reste à encaisser       = amount_residual_signed                        (facture ouverte)
```

- **Paiement partiel :** `payment_state = partial` · `amount_residual > 0`
- **Avoir :** intégré via `move_type` refund · réduit le reste à encaisser / payer via signe et rapprochement natif Odoo
- **Multi-société :** `company_id = cockpit.company_id`
- **Aucune écriture modifiée** par le cockpit

---

## 8. Emplacement UI — proposition

### Options arbitrées

| Option | Emplacement | Avantages | Inconvénients |
|---|---|---|---|
| **A — 2 onglets cockpit** *(recommandé V1)* | `Contrôles qualité` + `Tiers & paiements` | Cohérent Palier 5 · séparation fiabilité / cycle paiement · même filtres période | Cockpit passe à 6 onglets |
| **B — 1 onglet fusionné** | `Qualité & paiements` | Compact | Mélange KPI qualité et opérationnel |
| **C — Menu dédié** | `Pilotage GLC → Qualité des données` | Allège le cockpit | Fragmentation UX · filtres période à dupliquer |

### Recommandation MOA V1 — **validée GO cadrage 2026-05-29**

**Option A — deux onglets cockpit**, en reprenant la grammaire Palier 5 :

```text
Synthèse · Détail · Trésorerie · Contrôles qualité · Tiers & paiements · Infos
```

| Onglet | Contenu |
|---|---|
| **Contrôles qualité** | Couverture analytique + lettrage clients/fournisseurs + liens listes |
| **Tiers & paiements** | Synthèse factures clients/fournisseurs · statuts · reste à encaisser/payer |

Texte d’aide obligatoire *(comme onglet Trésorerie)* :

> *« Ces indicateurs mesurent la fiabilité des données et le cycle de paiement. Ils ne modifient pas Recette · Cumul RH · Dépense · Solde. »*

**Option C en fallback** si MOA juge le cockpit trop dense : menu dédié avec **même transient** `glc.coverage.cockpit` et mêmes filtres.

---

## 9. Points techniques Odoo 19 — champs retenus V1

### 9.1 `account.move` *(suivi paiement)*

| Champ Odoo 19 | Usage lot |
|---|---|
| `state` | Filtrer `posted` |
| `move_type` | Client / fournisseur / avoir |
| `payment_state` | `not_paid` · `in_payment` · `partial` · `paid` · `reversed` |
| `amount_total` / `amount_total_signed` | Facturé |
| `amount_residual` / `amount_residual_signed` | Reste dû |
| `amount_untaxed_signed` | Optionnel — détail HT |
| `invoice_date` | Filtre période primaire |
| `date` | Fallback date comptable |
| `company_id` | Multi-société |
| `line_ids` | Drill-down |

### 9.2 `account.move.line` *(lettrage + couverture)*

| Champ Odoo 19 | Usage lot |
|---|---|
| `reconciled` | Ligne tiers lettrée ou non |
| `amount_residual` | Solde ouvert ligne |
| `matched_debit_ids` / `matched_credit_ids` | Détail rapprochement |
| `full_reconcile_id` | Lettrage complet |
| `account_id.account_type` | `asset_receivable` · `liability_payable` |
| `account_id.code` | Filtre 411 / 401 |
| `analytic_distribution` | Couverture analytique ligne |
| `display_type` | Exclure sections techniques |
| `date_maturity` | Ancienneté créances / dettes |
| `parent_state` | Cohérence pièce postée |

### 9.3 `account.analytic.line` *(référence exploitation — lecture seule)*

| Usage | Règle |
|---|---|
| Non utilisé pour **modifier** l’exploitation | Invariant |
| Peut servir de **contrôle croisé** couverture *(ligne analytique générée)* | Option V1 |

### 9.4 Champs cockpit *(extension `glc.coverage.cockpit`)*

Nouveaux champs **stored computed** ou agrégation `_aggregate_quality()` / `_aggregate_payment()` — **séparés** de `_aggregate_period()` exploitation.

Persistance refresh : étendre `_current_refresh_key` avec identifiant stable *(pas de nouveau filtre utilisateur en V1)*.

---

## 10. Architecture technique proposée

```text
glc.coverage.cockpit
├── _aggregate_period()           # INCHANGÉ — exploitation Palier 4
├── _aggregate_treasury()         # INCHANGÉ — trésorerie Palier 5
├── _aggregate_quality_analytic() # NOUVEAU — Q1
├── _aggregate_quality_reconcile()# NOUVEAU — Q2
└── _aggregate_payment_tracking() # NOUVEAU — Q3

Invariant test obligatoire :
  changement onglet qualité / paiement  → KPI exploitation IDENTIQUES
  changement compte bancaire référence    → KPI exploitation IDENTIQUES
  changement période                    → qualité + paiement recalculés
                                        → exploitation recalculée (normal)
```

**Réutilisation Palier 1 :** factoriser helpers `_is_business_line()` · `_has_analytic_coverage()` depuis `glc.analytic.anomaly.wizard` vers un mixin partagé *(éviter triple logique)*.

---

## 11. Risques techniques

| # | Risque | Mitigation V1 |
|---|---|---|
| R1 | **Confusion comptabilisé / payé / encaissé** | Textes d’aide · onglets séparés · doc recette |
| R2 | **Lettrage cumulé vs période** | Documenter : lettrage = **stock** tiers à date fin période ; paiement = **flux** factures date pièce |
| R3 | **`payment_state` vs lettrage réel** | Afficher libellés Odoo natifs · ne pas recalculer un pseudo-statut |
| R4 | **Avoirs / partial / in_payment** | Jeux de test dédiés · cas MOA documentés |
| R5 | **Performance** | Agrégats SQL · pas de boucle Python sur toutes les lignes sans domaine |
| R6 | **Régression exploitation** | Test invariant `test_quality_blocks_do_not_change_exploitation_kpis` |
| R7 | **Multi-société** | Tous domaines `company_id` · tests sur `My Company` |
| R8 | **Doublon assistant anomalies** | Couverture cockpit = **KPI période** ; wizard Palier 1 = **audit ponctuel** |
| R9 | **Odoo 19 `payment_state` legacy** | Traiter `invoicing_legacy` explicitement · exclure ou mapper |

---

## 12. Critères d’acceptation MOA

### 12.1 Invariant global

- [ ] **CA-INV-01** — Recette · Cumul RH · Dépense · Solde **strictement identiques** avant/après livraison lot qualité
- [ ] **CA-INV-02** — Onglet Trésorerie Palier 5 **non régressé**
- [ ] **CA-INV-03** — Aucun domaine `_revenue_analytic_line_domain` / `_expense_*` / `_payroll_*` modifié

### 12.2 Couverture analytique

- [ ] **CA-Q1-01** — Taux affiché = pièces couvertes / pièces contrôlées
- [ ] **CA-Q1-02** — Lignes TVA · banque · tiers exclues du contrôle
- [ ] **CA-Q1-03** — Liste pièces non couvertes **actionnable**
- [ ] **CA-Q1-04** — Filtre période cockpit appliqué

### 12.3 Lettrage

- [ ] **CA-Q2-01** — Taux clients et fournisseurs **séparés**
- [ ] **CA-Q2-02** — Montants non lettrés clients / fournisseurs visibles
- [ ] **CA-Q2-03** — Ancienneté visible *(au moins 4 buckets)*
- [ ] **CA-Q2-04** — Aucune écriture modifiée

### 12.4 Suivi paiement

- [ ] **CA-Q3-01** — Distinction `not_paid` · `partial` · `in_payment` · `paid`
- [ ] **CA-Q3-02** — Reste à encaisser / payer = `amount_residual_signed`
- [ ] **CA-Q3-03** — Avoir client / fournisseur pris en compte
- [ ] **CA-Q3-04** — Facture payée **absente** des montants ouverts
- [ ] **CA-Q3-05** — Libellés alignés Odoo 19

### 12.5 Non-régression

- [ ] **CA-TEST** — Post-install **≥ 95 tests** · **0 failed** · bloc qualité **≥ 8 tests** dédiés
- [ ] **CA-DOC** — Recette manuelle MOA validée

---

## 13. Recette manuelle

**Fichier :** [RECETTE_MANUELLE_COCKPIT_QUALITE_PAIEMENT.md](./recette/RECETTE_MANUELLE_COCKPIT_QUALITE_PAIEMENT.md)

Scénarios **QP-*** · critères GO / NO GO · cas paiement partiel / impayé / payé / avoir · preuve non-régression exploitation et trésorerie.

---

## 14. Gate MOA — conditions avant code

| # | Condition | Statut |
|---|---|---|
| GQ-1 | Palier 5 trésorerie **GO complet MOA** | **OK** — `19.0.5.0.1` |
| GQ-2 | Mémo qualité **validé** | **OK** — [MEMO](./MEMO_RAFFINEMENT_QUALITE_COMPTABLE_ANALYTIQUE.md) |
| GQ-3 | Ce ticket **revu MOA** | **OK** — 2026-05-29 |
| GQ-4 | Emplacement UI arbitré *(§8)* | **OK** — **Option A** · 2 onglets |
| GQ-5 | Périmètre V1 vs V2 accepté | **OK** — Q1 + Q2 + Q3 |
| GQ-6 | GO MOA explicite « démarrage code » | **En attente** — GO cadrage confirmé · **pas de GO code** |

---

## 15. Plan de livraison suggéré

| Phase | Contenu | Version cible |
|---|---|---|
| **1** | Cadrage MOA *(ce ticket)* | — |
| **2** | Q1 couverture analytique + tests | `19.0.6.x.0` |
| **3** | Q2 lettrage + Q3 suivi paiement + UI | `19.0.6.x.0` ou `19.0.7.0.0` |
| **4** | Recette MOA + non-régression 95+ | GO lot |

**Règle commit :** un commit / PR **ne mélange jamais** modification agrégats exploitation et code qualité/paiement sans revue explicite.

---

## 16. Verdict MOA attendu

| Verdict | Signification |
|---|---|
| **GO cadrage** | Arbitrages §4 · §8 · §9 validés · recette rédigée · code autorisé après **GQ-6** |
| **GO avec réserves** | MVP réduit *(ex. paiement seul, sans lettrage)* |
| **NO GO** | Repositionner dans menu hors cockpit |

**Statut actuel :** **GO cadrage MOA confirmé** (2026-05-29) — recette validée · Option A · V1 Q1+Q2+Q3 · **GQ-6 en attente — aucun code autorisé**

---

## 17. Liens

| Document | Rôle |
|---|---|
| [MEMO_RAFFINEMENT_QUALITE_COMPTABLE_ANALYTIQUE.md](./MEMO_RAFFINEMENT_QUALITE_COMPTABLE_ANALYTIQUE.md) | Source MOA |
| [TICKET_PALIER_5_TRESORERIE_COMPTE_BANCAIRE_REFERENCE.md](./TICKET_PALIER_5_TRESORERIE_COMPTE_BANCAIRE_REFERENCE.md) | Précédent lot cockpit · invariant |
| [TICKET_PALIER_1.md](./TICKET_PALIER_1.md) | Assistant anomalies A1–A6 |
| [PALIERS.md](./PALIERS.md) | Roadmap |

---

*Ticket ouvert post-GO Palier 5 trésorerie. Lot qualité / paiement = **lecture complémentaire** — exploitation Palier 4 **gelée**.*
