# Ticket — Compte bancaire de référence du cockpit GLC

**Module :** `dorevia_glc_analytics` (+ croisement `dorevia_cash_guard` en lecture seule)  
**Version installée (réf.) :** `19.0.4.9.0` *(Palier 4 — exploitation)*  
**Statut :** **Décision MOA figée** — **non implémenté** (Palier 5 / extension trésorerie)  
**Date :** 2026-05-28

**Références :** [CADRAGE_BUDGET_COCKPIT.md](./CADRAGE_BUDGET_COCKPIT.md) · [CADRAGE_FINAL_PALIER_4.md](./CADRAGE_FINAL_PALIER_4.md) § I5 · [PALIERS.md](./PALIERS.md) § Palier 5 · [TICKET_COCKPIT_SOURCE_REALISE.md](./TICKET_COCKPIT_SOURCE_REALISE.md)

---

## 1. Décision MOA

Le cockpit GLC doit être rattaché à un **compte bancaire de référence**, sélectionnable parmi les comptes / journaux bancaires de l’association.

| Paramètre | Valeur GLC |
|---|---|
| Compte par défaut | **Compte courant** |
| Sélection | Parmi les journaux / comptes bancaires de la société |
| Portée | Point de vue de **lecture trésorerie** du cockpit |

Cette décision **ne remplace pas** la doctrine Palier 4 sur le réalisé d’exploitation (classes 6/7, analytique). Elle **ajoute** une couche de lecture trésorerie distincte.

---

## 2. Triple lecture — doctrine figée

| Couche | Rôle | Exemple |
|---|---|---|
| **Compte bancaire de référence** | Point de vue de **lecture trésorerie** | Entrée / sortie sur le compte courant observé |
| **Compte comptable** (`general_account_id`) | **Nature comptable** | 706 recette · 641 salaire · 512 banque · 580 virement interne |
| **Compte analytique** | **Qualification métier GLC** | BAR · SUBVENTIONS · STRUCTURE · RH / Personnel |

Règle d’or :

> Le compte bancaire de référence donne le **point de vue** ; le compte comptable donne la **nature** ; le compte analytique donne la **qualification métier**.

---

## 3. Lecture trésorerie depuis le compte de référence

Depuis le point de vue du compte bancaire de référence sélectionné :

| Mouvement | Lecture cockpit trésorerie |
|---|---|
| **Entrée** sur le compte de référence | Entrée de trésorerie |
| **Sortie** du compte de référence | Sortie de trésorerie |
| **Virement interne** impliquant ce compte | **Visible** comme mouvement de trésorerie du compte observé |

### Exclusion des KPI d’exploitation

Un **virement interne** (ex. compte courant → livret, ou compte courant → compte de transfert) :

- **doit** apparaître dans la lecture trésorerie du compte observé ;
- **ne doit pas** être compté comme :
  - recette ;
  - charge / dépense ;
  - marge d’activité (solde d’exploitation) ;
  - financement économique.

Même règle pour les autres flux **I5** déjà exclus de l’exploitation (emprunt `164`, reprise de solde, etc.) : visibles en trésorerie si impactent le compte de référence, **jamais** dans Recette · Cumul RH · Dépense · Solde.

---

## 4. Cohérence avec Palier 4 (état actuel `19.0.4.9.0`)

| Sujet | Palier 4 actuel | Après implémentation ticket |
|---|---|---|
| KPI Recette · Cumul RH · Dépense · Solde | Source : `account.analytic.line` classes **6/7** | **Inchangé** |
| Exclusion 512/53/411/401/164 | Domaines analytiques | **Inchangé** pour l’exploitation |
| Champ compte bancaire sur cockpit | **Absent** | À ajouter (`journal_id` ou compte 512 de référence) |
| Bloc trésorerie / soldes | **Hors scope** Palier 4 | Nouveau bloc Palier 5 |
| Virements internes | Exclus par nature comptable (hors 6/7) | **Détection explicite** + affichage trésorerie séparé |

**Conséquence :** les **88 post-tests** Palier 4 restent valides ; l’implémentation ajoute un **bloc ou onglet trésorerie** sans modifier `_sum_revenue_realized`, `_sum_expense_realized`, etc.

---

## 5. Périmètre technique envisagé

### 5.1 Modèle cockpit

Champ proposé sur `glc.coverage.cockpit` :

| Champ | Type | Rôle |
|---|---|---|
| `reference_bank_journal_id` | `Many2one` → `account.journal` (type `bank`) | Journal bancaire de référence |
| *(dérivé)* `reference_bank_account_id` | `Many2one` → `account.account` | Compte 512 lié au journal (related ou compute) |

Valeur par défaut société GLC : journal du **compte courant** (paramètre société ou `ir.config_parameter`).

### 5.2 Source données trésorerie

| Option | Source | Remarque |
|---|---|---|
| **A** | Lignes d’écriture sur le compte 512 du journal de référence | Aligné point de vue compte observé |
| **B** | `account.bank.statement.line` filtré par journal | Rapprochement bancaire |
| **C** | Lecture seule `dorevia_cash_guard` | Croisement V2 — pas de doublon métier |

Recommandation cadrage : **A ou B** pour le cockpit ; **C** en tableau de bord transversal (cf. [README.md](./README.md) § intégration trésorerie).

### 5.3 Classification virement interne

Critères candidats (à trancher en implémentation) :

- paire de comptes trésorerie **512 ↔ 512** (ou 512 ↔ 53) sans ligne analytique activité/financement ;
- journal dédié « virement interne » ;
- compte comptable **580** (virements internes) ;
- libellé / type d’écriture métier GLC.

Règle métier figée MOA : **quelle que soit la détection technique**, le mouvement reste **hors** recette / charge / marge / financement.

### 5.4 UI

- Filtre cockpit : **Compte bancaire de référence** (liste journaux `bank` de la société).
- Bloc ou onglet **Trésorerie** (Palier 5) : entrées / sorties / virements internes / solde période — **séparé** de Synthèse et Détail exploitation.

---

## 6. Scénarios de recette (à décliner)

| ID | Scénario | Attendu exploitation | Attendu trésorerie |
|---|---|---|---|
| TREF-01 | Paiement client → crédit compte courant + analytique BAR | Recette BAR | Entrée trésorerie compte courant |
| TREF-02 | Paiement fournisseur → débit compte courant + analytique 626 | Dépense | Sortie trésorerie |
| TREF-03 | Virement compte courant → livret (580 ou 512↔512) | **Aucun** impact Recette / Dépense / Solde | Entrée **ou** sortie selon compte observé ; visible des **deux** côtés si on change le compte de référence |
| TREF-04 | Paie 645 rapprochée banque | Cumul RH (645) | Sortie trésorerie |
| TREF-05 | Changement compte de référence (courant → livret) | KPI exploitation **identiques** | Flux trésorerie **inversés / filtrés** selon nouveau POV |

---

## 7. Critères d’acceptation (implémentation future)

- [ ] CA-TREF-FIELD — Champ compte bancaire de référence sur cockpit, défaut compte courant GLC
- [ ] CA-TREF-POV — Entrée/sortie lues depuis le POV du compte sélectionné
- [ ] CA-TREF-VIR — Virement interne visible en trésorerie, exclu de Recette · Cumul RH · Dépense · Solde · financements
- [ ] CA-TREF-ISO — KPI exploitation Palier 4 **inchangés** quand le compte de référence change
- [ ] CA-TREF-DOC — Cadrage + recette mis à jour
- [ ] CA-TREF-TEST — Tests auto scénarios TREF-01 à TREF-05

---

## 8. Priorité et séquence

| P | Action | Lot |
|---|---|---|
| **0** | Figement doctrine (ce ticket + cadrage) | **Fait** 2026-05-28 |
| **1** | Paramètre société « journal bancaire par défaut » | Palier 5 amorce |
| **2** | Champ filtre cockpit + persistance refresh | Palier 5 |
| **3** | Agrégation flux trésorerie + exclusion virements internes KPI exploitation | Palier 5 |
| **4** | Recette TREF + non-régression 88 tests Palier 4 | Palier 5 |

**Hors scope immédiat :** modification des agrégats exploitation `19.0.4.9.0` ; budget multi-axes ; onglet Données exclues (ticket réalignement §3.5).

---

## 9. Verdict MOA

**Doctrine acceptée** — le cockpit GLC dispose désormais d’une **triple lecture** explicite :

1. **Trésorerie** — compte bancaire de référence (compte courant par défaut) ;
2. **Exploitation** — compte comptable classes 6/7 ;
3. **Pilotage métier** — axe analytique GLC.

L’implémentation technique est **reportée Palier 5** ; le Palier 4 reste **GO technique** sans régression.

---

*Ticket ouvert post-GO R17 (`19.0.4.9.0`). Ne pas mélanger avec les correctifs exploitation Palier 4 sans mise à jour explicite de ce ticket.*
