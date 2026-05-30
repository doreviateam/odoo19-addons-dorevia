# Ticket de cadrage — Source de vérité du réalisé cockpit GLC

> **Addendum `19.0.14.1.0` (2026-05-30)** — Ce ticket documente le cadrage et la livraison **`19.0.4.7.0`**. Depuis la simplification MOA :
> - **source unique** du réalisé : `account.analytic.line` (classes 6/7 + financements) ;
> - **Cumul RH** = comptes paie 631/633/641/645 via analytique — **plus** de `glc.salary.allocation` ;
> - budget et ventilations Palier 2 **retirés** (`19.0.13` / `19.0.14`).
> État actuel : [ETAT_MODULE_ACTUEL.md](./ETAT_MODULE_ACTUEL.md). Les sections 2–12 ci-dessous conservent la **trace historique** du cadrage.

**Module :** `dorevia_glc_analytics`  
**Branche :** `feat/glc-cockpit-source-realise-19.0.4.7.0`  
**Version cible :** `19.0.4.7.0`  
**Statut :** **Validé MOA · implémenté** (2026-05-28)  
**Prérequis :** cockpit GLC livré et validé UX (`19.0.4.6.1`, PR #36) · cadrage Palier 4 I1–I7 ([CADRAGE_FINAL_PALIER_4.md](./CADRAGE_FINAL_PALIER_4.md))

**Références :** [CADRAGE_FINAL_PALIER_4.md](./CADRAGE_FINAL_PALIER_4.md) · [recette période libre](./recette/RECETTE_MANUELLE_COCKPIT_GLC_PERIODE_LIBRE.md) · [TICKET_PALIER_2.md](./TICKET_PALIER_2.md) · [TICKET_PALIER_4.md](./TICKET_PALIER_4.md)

> **Note de lecture :** ce ticket ouvre un **cadrage fonctionnel plus large** que le seul cas 645200. Le correctif ne doit **pas** être limité aux salaires. Aucun code avant validation MOA des sections 4 (doctrine cible), 6 (arbitrages) et 8 (recette).

---

## 1. Contexte MOA

Le cockpit GLC (Synthèse graphique + Détail par activité) est **validé UX** sur `19.0.4.6.1`.

Un **écart fonctionnel** a été identifié lors de la vérification d'alimentation du réalisé :

- cas révélateur : écriture **645200 Cotisations mutuelles** + analytique **[STRUCTURE]** issue d'un **rapprochement bancaire sans facture** (1,54 €) ;
- attendu MOA : alimentation **SALAIRES** sur l'activité [STRUCTURE] Structure & Administration, mois mai 2026 ;
- constat code : **non couvert** aujourd'hui.

**Élargissement MOA :** le sujet n'est pas limité aux salaires. Il s'agit de définir la **source de vérité unique** du **réalisé cockpit** pour toutes les familles métier.

---

## 2. Problème identifié

### 2.1. Doctrine MOA cible (à cadrer)

Le cockpit GLC doit agréger les **lignes comptables réelles de produit ou de charge** portant une **distribution analytique exploitable**, **quelle que soit l'origine** :

| Origine | Exemple |
|---|---|
| Facture client / fournisseur | Facture BAR avec analytique |
| Écriture comptable directe | OD charge/produit + analytique |
| Rapprochement bancaire sans facture | 645200 + [STRUCTURE] depuis relevé |
| Opération de caisse | Écriture caisse 6xxx/7xxx + analytique |

La **famille cockpit** est déterminée par le **compte comptable** (`general_account_id`), pas par le journal ni par la présence d'une facture.

### 2.2. Cadrage actuel Palier 4 (I2 / I3) — implémentation `glc_coverage_cockpit.py`

| Famille cockpit | Source actuelle code | Filtre notable |
|---|---|---|
| **RECETTES** | `account.analytic.line` via `_sum_analytic_realized` | `account_type` ∈ revenus ; axes BAR / PRESTATIONS / PRIVATISATIONS |
| **DÉPENSES** | `account.analytic.line` via `_sum_analytic_realized` | axe STRUCTURE ; **exclusion préfixes 631/633/641/645** |
| **SALAIRES** | `glc.salary.allocation.line` via `_sum_payroll_realized` | ventilations Palier 2 **validated/locked uniquement** |
| **FINANCEMENTS / Ressources** | `account.analytic.line` | axes SUBVENTIONS / ADHESIONS |

**Exclusions code actuelles (cohérentes avec doctrine tiers/trésorerie) :**

- `general_account_id.account_type` limité aux types **revenus / charges** → exclut **512 / 53** (trésorerie) et **411 / 401** (tiers) ;
- préfixe **164** exclu (`GLC_EXCLUDED_GL_ACCOUNT_PREFIXES`).

**Écart principal :**

```text
Cadrage I2/I3 (Palier 4)     :  réalisé exploitation = analytic.line HORS 631/633/641/645
                               +  masse salariale = ventilations Palier 2 UNIQUEMENT

Doctrine MOA cible (2026-05) :  réalisé = toute écriture charge/produit + analytique
                               +  famille déterminée par compte GL (y compris 645…)
```

→ Certaines **écritures réelles analytiques** (rapprochement, caisse, OD) **ne remontent pas** dans le cockpit, alors qu'elles portent une nature économique et une distribution analytique valides.

---

## 3. Doctrine MOA cible — cartographie comptable → familles cockpit

### 3.1. Inclusion

| Compte comptable (nature) | Préfixes / types indicatifs | Famille cockpit | Axe analytique |
|---|---|---|---|
| **Produits** | 7xxx · `account_type` revenus | **RECETTES** | Activités GLC (BAR, PRESTATIONS, PRIVATISATIONS) |
| **Charges salariales / sociales** | 631, 633, 641, 645 · `account_type` charges | **SALAIRES** | Activités GLC (ventilation par axe) |
| **Charges hors salaires** | 6xxx hors 631/633/641/645 | **DÉPENSES** | STRUCTURE (et autres axes si doctrine étendue) |
| **Financements** | Selon plan Financements GLC | **RESSOURCES / FINANCEMENTS** | SUBVENTIONS, ADHESIONS, … |

**Règle transversale :** la présence d'une **`account.analytic.line`** (ou équivalent Odoo 19 : distribution analytique sur `account.move.line` générant la ligne analytique) est le **signal d'inclusion**, indépendamment de l'origine documentaire.

### 3.2. Exclusion explicite

| Compte / nature | Motif MOA |
|---|---|
| **411 / 401** | Comptes de **tiers** — suivi client/fournisseur, pas nature économique |
| **512 / 53** | **Trésorerie / caisse** — trace du flux de paiement |
| Lignes de **lettrage / paiement seul** | Preuve du flux, pas charge/produit d'activité |
| Écritures **sans distribution analytique** | Non pilotables par activité — hors cockpit détail |

### 3.3. Cas révélateur 645200

| Élément | Attendu MOA |
|---|---|
| Écriture | 645200 Cotisations mutuelles · 1,54 € · mai 2026 |
| Analytique | [STRUCTURE] Structure & Administration |
| Famille | **SALAIRES** |
| Ligne 512100 banque | **Exclue** (trésorerie) |

---

## 4. Points à arbitrer MOA

| # | Question | Options | Recommandation technique *(à valider MOA)* |
|---|---|---|---|
| **A1** | Source unique du réalisé ? | (1) `account.analytic.line` pour tout · (2) mixte I2/I3 conservé · (3) hybrid avec complément | **(1) ou (3)** — alignement doctrine MOA |
| **A2** | Place des comptes 631/633/641/645 ? | Inclus dans SALAIRES via analytic.line · exclus · mixte | **Inclus** dans SALAIRES si analytique activité présente |
| **A3** | Rôle ventilations Palier 2 ? | Source exclusive · contrôle / écart · complément si non ventilé · abandon | **Contrôle + complément anti-trou** *(à trancher)* |
| **A4** | Anti-double comptage RH ? | Exclure RH_PERSONNEL · exclure si déjà ventilé · règle temporelle mois/activité | Règle explicite **sans double comptage** mois × activité × société |
| **A5** | Écritures sans facture ? | Inclus si analytic.line · exclus | **Inclus** — origine neutre |
| **A6** | Exclusions 411/401/512/53 | Par `account_type` · par préfixe code · les deux | **Les deux** (défense en profondeur) |
| **A7** | Impact cadrage I2/I3 Palier 4 ? | Révision I2/I3 · addendum Palier 4bis · nouveau palier 4ter | **Addendum** + mise à jour recette R14 |

---

## 5. État des lieux code (audit 2026-05-28)

### 5.1. Méthodes clés

| Méthode | Fichier | Rôle |
|---|---|---|
| `_analytic_line_domain` | `models/glc_coverage_cockpit.py` | Filtre `account.analytic.line` — **exclut 631/633/641/645** |
| `_sum_analytic_realized` | idem | Agrège recettes / dépenses / financements depuis analytic.line |
| `_sum_payroll_realized` | idem | Agrège **SALAIRES** depuis `glc.salary.allocation.line` uniquement |

### 5.2. Tests existants pertinents

| Test | Couverture |
|---|---|
| `test_payroll_from_validated_allocation_only` | SALAIRES = ventilations validées **uniquement** |
| `_create_revenue_on_account` / `_create_expense_on_account` | Factures avec analytique → recettes / dépenses |
| *(absent)* | Rapprochement bancaire sans facture |
| *(absent)* | 645xxx + analytique → SALAIRES |
| *(absent)* | Exclusion 512 / 411 |
| *(absent)* | Anti-doublon ventilations vs compta |

### 5.3. Verdict audit

| Cas | Couvert aujourd'hui ? |
|---|---|
| Facture client 7xxx + analytique → RECETTES | **Oui** (via analytic.line) |
| Facture fournisseur 6xxx hors payroll + STRUCTURE → DÉPENSES | **Oui** |
| Financement + analytique → Ressources | **Oui** |
| Rapprochement 6xxx hors payroll + analytique → DÉPENSES | **Probablement oui** *(si analytic.line générée)* |
| Rapprochement **645xxx** + analytique → SALAIRES | **Non** |
| Caisse / OD sans facture (charge/produit + analytique) | **Partiel** — même logique que ci-dessus |
| Ligne 512 / 411 | **Exclu** ✓ |
| Ventilation Palier 2 seule (sans écriture) | **Oui** pour SALAIRES |

---

## 6. Cible fonctionnelle proposée (post-arbitrage MOA)

### 6.1. Principe

```text
Réalisé cockpit (toutes familles) =
    Σ account.analytic.line
    où general_account_id = nature économique (7xxx / 6xxx payroll / 6xxx autre / financement)
    ET distribution analytique sur axe GLC exploitable
    ET exclusions tiers / trésorerie / lettrage
    ± règle anti-double comptage ventilations Palier 2 (A3/A4)
```

### 6.2. Mapping implémentation indicatif

| Famille | Domaine analytic.line (indicatif) |
|---|---|
| RECETTES | `account_type` ∈ revenus · axe ∈ {BAR, PRESTATIONS, PRIVATISATIONS} |
| SALAIRES | `account_type` ∈ charges · code GL ∈ {631*, 633*, 641*, 645*} · axe activité |
| DÉPENSES | `account_type` ∈ charges · code GL **hors** payroll · axe STRUCTURE (…) |
| FINANCEMENTS | axes plan Financements |

### 6.3. Ventilations Palier 2 — rôles possibles

| Rôle | Description |
|---|---|
| **R1 — Source exclusive** *(statut actuel)* | SALAIRES = ventilations uniquement |
| **R2 — Contrôle** | Bandeau écart compta 645… vs ventilé — informatif |
| **R3 — Complément** | SALAIRES = ventilations + écritures 645… non couvertes par ventilation |
| **R4 — Source compta** | SALAIRES = analytic.line payroll ; ventilations = outil de pilotage RH |

→ **Décision MOA requise** avant implémentation.

---

## 7. Recette cible — section R14 (à ajouter post-correctif)

| Réf | Cas de non-régression | Famille attendue | OK |
|---|---|---|:---:|
| R14-FAC-CLI | Facture client 7xxx + analytique [BAR] | RECETTES | [ ] |
| R14-FAC-FOU | Facture fournisseur 6xxx hors payroll + [STRUCTURE] | DÉPENSES | [ ] |
| R14-BNK-6XX | Rapprochement sans facture · 6xxx hors payroll + analytique | DÉPENSES | [ ] |
| R14-BNK-645 | Rapprochement sans facture · **645200** + [STRUCTURE] | **SALAIRES** | [ ] |
| R14-CAISSE | Opération caisse · charge/produit + analytique | RECETTES / DÉPENSES / SALAIRES selon GL | [ ] |
| R14-EXCL-512 | Ligne 512100 banque seule | **Exclue** | [ ] |
| R14-EXCL-411 | Ligne 411 client / 401 fournisseur | **Exclue** | [ ] |
| R14-NODOUBLON | Écriture 645 + ventilation Palier 2 même mois/activité | **Pas de double comptage** | [ ] |
| R14-OD | Écriture comptable directe (OD) + analytique | Selon compte GL | [ ] |

**Pré-requis recette :** upgrade version post-correctif + jeu de données `glc-rgl-test-import` ou script de charge dédié.

---

## 8. Tests automatisés cibles (post-correctif)

| Test Python (indicatif) | Comportement asserté |
|---|---|
| `test_realized_revenue_from_invoice_analytic` | 7xxx + BAR → RECETTES *(existant partiel)* |
| `test_realized_expense_from_invoice_analytic` | 6xxx + STRUCTURE → DÉPENSES *(existant partiel)* |
| `test_realized_payroll_from_bank_recon_645_analytic` | 645 + STRUCTURE sans facture → SALAIRES |
| `test_realized_expense_from_bank_recon_6xx_analytic` | 6xx hors payroll sans facture → DÉPENSES |
| `test_excluded_treasury_512_not_in_cockpit` | 512 exclu |
| `test_excluded_partner_411_401_not_in_cockpit` | 411/401 exclus |
| `test_no_double_count_payroll_allocation_and_analytic` | Anti-doublon Palier 2 |

**Non-régression :** conserver **67 post-tests** verts + nouveaux tests R14.

---

## 9. Hors périmètre (ce ticket)

- Modification du **prévisionnel** (`glc.budget.line`) — inchangé ;
- Refonte UX cockpit (Synthèse / Détail) — inchangée ;
- Responsive mobile complet — réserve documentée ;
- Trésorerie prévisionnelle / OCA Budget ;
- Réécriture du module ventilations Palier 2 — seulement clarification de son **rôle** vis-à-vis du réalisé cockpit.

---

## 10. Décisions MOA attendues

| Point | Décision MOA |
|---|---|
| Doctrine : réalisé = écritures charge/produit + analytique, **avec ou sans facture** | ✅ GO |
| Comptes 631/633/641/645 → **SALAIRES** via compta analytique | ✅ GO |
| Rôle ventilations Palier 2 | ✅ **R2 — Contrôle** (pas source primaire concurrente) |
| Règle anti-double comptage | ✅ GO |
| Exclusions 411/401/512/53 confirmées | ✅ GO |
| Révision cadrage I2/I3 ([CADRAGE_FINAL_PALIER_4.md](./CADRAGE_FINAL_PALIER_4.md)) | ✅ GO |
| GO implémentation post-cadrage (`19.0.4.7.0`) | ✅ GO |

---

## 11. Trajectoire proposée (post-validation MOA)

1. **Validation MOA** de ce ticket (section 10) — arbitrage A1–A7 ;
2. **Mise à jour** [CADRAGE_FINAL_PALIER_4.md](./CADRAGE_FINAL_PALIER_4.md) § I2/I3 ou addendum Palier 4ter ;
3. **Implémentation** `_sum_analytic_realized` / `_sum_payroll_realized` — refonte mapping familles ;
4. **Tests** R14 automatisés + section recette [RECETTE_MANUELLE_COCKPIT_GLC_PERIODE_LIBRE.md](./recette/RECETTE_MANUELLE_COCKPIT_GLC_PERIODE_LIBRE.md) ;
5. **Recette MOA** sur `glc-rgl-test-import` — cas facture, rapprochement, caisse, exclusions ;
6. Bump **`19.0.4.7.0`** · commit · PR → `main`.

---

## 12. Verdict MOA (2026-05-28)

| Élément | Verdict |
|---|---|
| Écart fonctionnel identifié | **Oui** — source de vérité réalisé incohérente avec doctrine MOA cible |
| Limité aux salaires | **Non** — ticket élargi à l'alimentation générale du réalisé |
| Cadrage MOA section 10 | **GO** — R2 retenu pour Palier 2 |
| Implémentation `19.0.4.7.0` | **Livré** — `_sum_payroll_realized` basculé sur `account.analytic.line` |
| Tests automatisés R14 | **7 nouveaux tests** · **74 post-tests verts** (70 analytics + 14 budget) |
| Recette MOA `19.0.4.7.0` (2026-05-28) | **GO technique** — upgrade + restart + rejeu complet sur `glc-rgl-test-import` |
| Compléments manuels R14 | **En attente** — R14-CAISSE · R14-OD · R14-645-REEL |

### Implémentation (2026-05-28)

| Changement | Fichier |
|---|---|
| `_payroll_analytic_line_domain` + refonte `_sum_payroll_realized` | `models/glc_coverage_cockpit.py` |
| Exclusion payroll maintenue sur `_analytic_line_domain` (DÉPENSES hors 631/633/641/645) | idem |
| Tests R14 + non-régression alertes | `tests/test_coverage_cockpit.py` |
| Révision invariants I2/I3/I4 | `docs/CADRAGE_FINAL_PALIER_4.md` |

---

---

## 13. État actuel `19.0.14.1.0`

| Famille UI | Source code actuelle |
|---|---|
| **Ressources** | `account.analytic.line` — revenus + axes financements |
| **Cumul RH** | `account.analytic.line` — charges paie 631/633/641/645 |
| **Dépenses** | `account.analytic.line` — charges hors paie |
| **Solde** | `Ressources − Cumul RH − Dépenses` |

- Méthode `_sum_payroll_realized` : agrège depuis **analytique paie**, pas depuis ventilations.
- Palier 2 (`glc.salary.allocation`) et module budget : **supprimés** — sections A3, 6.3 et R14-NODOUBLON ci-dessus sont **historiques**.
- Menu recette : **Facturation → Pilotage GLC → Contrôle de gestion**.

---

*Ticket de cadrage rédigé MOA — 2026-05-28.  
Révélateur : cas 645200 + [STRUCTURE] rapprochement bancaire sans facture.  
Suite : simplification pilotage `19.0.14` — [RELEASE_NOTE_19.0.14_SIMPLIFICATION_PILOTAGE.md](./RELEASE_NOTE_19.0.14_SIMPLIFICATION_PILOTAGE.md).*
