# Ticket Palier 5 — Trésorerie & compte bancaire de référence

**Module :** `dorevia_glc_analytics` *(extension cockpit)* · croisement lecture seule `dorevia_cash_guard` *(V2)*  
**Palier 4 de référence :** **`19.0.4.9.0`** — **gelé** · GO livraison MOA (2026-05-28)  
**Statut :** **GO complet MOA** (2026-05-29) · lot trésorerie **`19.0.5.0.1`** validé · Option C + S1 livrées  
**Date ouverture :** 2026-05-28

**Références :** [PALIERS.md](./PALIERS.md) · [TICKET_COCKPIT_COMPTE_BANCAIRE_REFERENCE.md](./TICKET_COCKPIT_COMPTE_BANCAIRE_REFERENCE.md) *(doctrine MOA)* · [CADRAGE_BUDGET_COCKPIT.md](./CADRAGE_BUDGET_COCKPIT.md) · [CADRAGE_FINAL_PALIER_4.md](./CADRAGE_FINAL_PALIER_4.md) § I5 · [TICKET_COCKPIT_REALIGNEMENT_CONTROLE_GESTION.md](./TICKET_COCKPIT_REALIGNEMENT_CONTROLE_GESTION.md) · [Recette période libre](./recette/RECETTE_MANUELLE_COCKPIT_GLC_PERIODE_LIBRE.md) · [Recette Palier 5 trésorerie](./recette/RECETTE_MANUELLE_PALIER_5_TRESORERIE_COMPTE_BANCAIRE_REFERENCE.md)

---

## 1. Contexte MOA

Le Palier 4 réaligné est **livré et gelé** en `19.0.4.9.0` :

- grammaire **Recette · Cumul RH · Dépense · Solde** ;
- réalisé d’exploitation = `account.analytic.line` classes **6/7** ;
- **88 post-tests** verts ;
- doctrine « compte bancaire de référence » **documentée** ([TICKET_COCKPIT_COMPTE_BANCAIRE_REFERENCE.md](./TICKET_COCKPIT_COMPTE_BANCAIRE_REFERENCE.md)) — **sans impact code**.

**Décision MOA :** ouvrir le **Palier 5** par un **cadrage propre** avant toute implémentation. Pause de verrouillage Palier 4 — pas d’enchaînement code immédiat.

---

## 2. Invariant central *(cœur du ticket)*

> **Un cockpit = période + compte bancaire de référence + lecture trésorerie séparée.**  
> **Les KPI d’exploitation ne changent jamais quand on change de compte bancaire.**

| Dimension cockpit | Rôle | Impact changement compte bancaire |
|---|---|---|
| **Période** (`date_from` / `date_to`) | Fenêtre temporelle commune | — |
| **Compte bancaire de référence** | Point de vue **trésorerie** | Modifie **uniquement** la lecture trésorerie |
| **Lecture exploitation** | Recette · Cumul RH · Dépense · Solde | **Inchangée** |
| **Lecture trésorerie** | Entrées · sorties · virements internes · solde période | **Filtrée** selon le compte observé |

### Triple lecture (rappel doctrine)

| Couche | Rôle |
|---|---|
| Compte bancaire de référence | POV trésorerie (défaut GLC : **compte courant**) |
| Compte comptable | Nature comptable |
| Compte analytique | Qualification métier GLC |

---

## 3. Objectif Palier 5 (lot trésorerie)

Ajouter au cockpit GLC une **lecture trésorerie autonome**, sans modifier le moteur d’exploitation Palier 4 :

1. sélectionner un **compte bancaire de référence** (journal / compte 512) ;
2. afficher les **flux trésorerie** du compte observé sur la période ;
3. rendre les **virements internes** visibles en trésorerie ;
4. garantir que virements internes et flux bilan **restent exclus** des KPI exploitation.

---

## 4. Gate MOA — conditions avant code

| # | Condition | Statut |
|---|---|---|
| G5-1 | Palier 4 gelé `19.0.4.9.0` | **OK** |
| G5-2 | Doctrine compte bancaire figée | **OK** — ticket doctrine |
| G5-3 | Cadrage Palier 5 validé MOA *(ce ticket)* | **OK** — Option C · S1 · bloc séparé |
| G5-4 | Arbitrages techniques §5 tranchés | **OK** |
| G5-5 | Recette TREF rédigée et acceptée | **OK** |
| G5-6 | GO MOA explicite « démarrage code Palier 5 » | **OK** |

---

## 5. Arbitrages à trancher *(cadrage — avant code)*

### 5.1 Journal bancaire vs compte 512

| Option | Modèle | Avantages | Risques |
|---|---|---|---|
| **A — Journal** | `reference_bank_journal_id` → `account.journal` (type `bank`) | Aligné UX Odoo · filtre naturel · un journal = un compte bancaire courant | Journal multi-comptes rare mais possible |
| **B — Compte 512** | `reference_bank_account_id` → `account.account` | POV comptable exact | Moins intuitif pour l’utilisateur MOA |
| **C — Hybride** | Journal + related `default_account_id` | Compromis recommandé en cadrage | Deux champs à maintenir |

**Proposition cadrage :** **Option C** — champ cockpit = journal bancaire ; compte 512 dérivé en related/compute.

### 5.2 Source des mouvements trésorerie

| Option | Source Odoo | Usage |
|---|---|---|
| **S1** | `account.move.line` sur compte 512 du journal | POV comptable · couvre toutes écritures |
| **S2** | `account.bank.statement.line` | Aligné relevé bancaire · peut manquer écritures non rapprochées |
| **S3** | Lecture seule `dorevia_cash_guard` | Tableau de bord transversal V2 — **pas** source primaire cockpit |

**Proposition cadrage :** **S1** pour le bloc cockpit Palier 5 ; **S3** en croisement ultérieur sans doublon.

### 5.3 Défaut société — compte courant GLC

| Élément | Proposition |
|---|---|
| Paramètre | `res.company` ou `ir.config_parameter` par société |
| Valeur GLC | Journal du **compte courant** |
| Comportement création cockpit | Pré-remplir `reference_bank_journal_id` |
| Refresh | Conserver le compte sélectionné (même logique que `activity_account_id`) |

### 5.4 Détection virement interne

Critères candidats *(à valider MOA)* :

- écriture **512 ↔ 512** ou **512 ↔ 53** sans impact analytique activité/financement ;
- compte **580** ;
- journal ou libellé métier dédié.

**Règle figée :** quel que soit le critère technique retenu, le mouvement est **visible en trésorerie** et **exclu** de Recette · Cumul RH · Dépense · Solde · financements.

### 5.5 Emplacement UI — bloc séparé

| Zone cockpit | Contenu | Modifiable par compte bancaire ? |
|---|---|---|
| **Synthèse / Détail** *(existant)* | KPI exploitation Palier 4 | **Non** |
| **Onglet ou bloc Trésorerie** *(nouveau)* | Entrées · sorties · virements · solde période | **Oui** |

**Interdit :** fusionner trésorerie et KPI exploitation dans un même agrégat ou un même graphique sans séparation visuelle explicite.

---

## 6. Périmètre

### Inclus (lot trésorerie Palier 5)

| # | Livrable |
|---|---|
| P5-1 | Champ `reference_bank_journal_id` sur `glc.coverage.cockpit` | **OK** |
| P5-2 | Défaut société = compte courant GLC | **OK** |
| P5-3 | Persistance du compte bancaire au refresh | **OK** |
| P5-4 | Agrégation flux trésorerie période (entrées / sorties / virements internes) | **OK** |
| P5-5 | Onglet ou bloc UI **Trésorerie** dédié | **OK** |
| P5-6 | Tests auto TREF-01 à TREF-05 | **OK** |
| P5-7 | Non-régression Palier 4 / Budget | **OK** |
| P5-8 | Recette manuelle Palier 5 | **OK** — [RECETTE_MANUELLE_PALIER_5_TRESORERIE_COMPTE_BANCAIRE_REFERENCE.md](./recette/RECETTE_MANUELLE_PALIER_5_TRESORERIE_COMPTE_BANCAIRE_REFERENCE.md) |
| P5-9 | Nettoyage nomenclature analytique legacy | **OK** — migration `19.0.5.0.1` |

### Exclus *(hors ce ticket ou lots ultérieurs)*

| Sujet | Report |
|---|---|
| Modification agrégats exploitation `_sum_*` Palier 4 | **Interdit** sans décision MOA |
| Budget multi-axes / réalisé non budgété par axe | Lot budget |
| Onglet Données exclues / à contrôler | Ticket réalignement §3.5 |
| Exports Excel / PDF | Palier 5 élargi |
| Scénarios budget multiples | Palier 5 élargi |
| Projections fin d’année | Palier 5 élargi |
| OCA Budget | Hors périmème GLC |
| Écriture ou modification comptable | Hors scope |

---

## 7. Architecture cible *(schéma)*

```text
glc.coverage.cockpit
├── Filtres communs
│   ├── company_id
│   ├── date_from / date_to
│   ├── activity_account_id        ← exploitation (Palier 4, inchangé)
│   ├── budget_scenario            ← exploitation (Palier 4, inchangé)
│   └── reference_bank_journal_id  ← NOUVEAU · trésorerie uniquement
│
├── Lecture EXPLOITATION (Palier 4 — gelée)
│   └── account.analytic.line · classes 6/7
│       → Recette · Cumul RH · Dépense · Solde
│       → INDÉPENDANT du compte bancaire de référence
│
└── Lecture TRÉSORERIE (Palier 5 — nouveau)
    └── move lines · compte 512 du journal de référence
        → Entrées · Sorties · Virements internes · Solde période
        → DÉPEND du compte bancaire de référence
```

---

## 8. Scénarios recette TREF *(à automatiser)*

| ID | Scénario | KPI exploitation | Lecture trésorerie |
|---|---|---|---|
| **TREF-01** | Encaissement client → crédit compte courant + analytique BAR | Recette BAR | Entrée compte courant |
| **TREF-02** | Paiement fournisseur → débit compte courant + analytique 626 | Dépense | Sortie compte courant |
| **TREF-03** | Virement compte courant → livret (580 ou 512↔512) | **Aucun** impact Recette / Dépense / Solde | Visible selon POV ; inverse si on observe le livret |
| **TREF-04** | Paie 645 rapprochée banque | Cumul RH | Sortie trésorerie |
| **TREF-05** | Changement compte de référence (courant → livret) | **Identiques** | Flux **recalculés** selon nouveau POV |

**Critère clé TREF-05 :** preuve formelle de l’invariant §2.

---

## 9. Critères d’acceptation *(implémentation future)*

- [x] **CA-P5-ISO** — Changement de `reference_bank_journal_id` : KPI exploitation **strictement identiques**
- [x] **CA-P5-FIELD** — Champ compte bancaire de référence · défaut compte courant GLC · persistance refresh
- [x] **CA-P5-POV** — Entrées / sorties lues depuis le POV du compte observé
- [x] **CA-P5-VIR** — Virements internes visibles en trésorerie · exclus KPI exploitation
- [x] **CA-P5-UI** — Bloc / onglet Trésorerie **séparé** de Synthèse et Détail
- [x] **CA-P5-TEST** — TREF-01 à TREF-05 automatisés
- [x] **CA-P5-NR** — post-install **95/95** · 0 failed · 0 error(s)
- [x] **CA-P5-DOC** — Recette Palier 5 + mise à jour PALIERS.md
- [x] **CA-P5-LEGACY** — nomenclature Activités GLC legacy nettoyée (`19.0.5.0.1`)

---

## 10. Séquence recommandée *(après GO cadrage)*

| Phase | Action | Livrable |
|---|---|---|
| **0** | Validation cadrage MOA *(ce ticket)* | GO cadrage |
| **1** | Paramètre société + champ cockpit | PR technique amorce |
| **2** | Agrégation trésorerie + détection virements | Backend + tests TREF |
| **3** | UI bloc Trésorerie | OWL / vue formulaire |
| **4** | Recette + non-régression 95 tests | **GO complet MOA Palier 5 trésorerie** |

**Règle de commit :** un commit / PR Palier 5 **ne mélange jamais** modification des agrégats exploitation Palier 4 et code trésorerie sans revue explicite de ce ticket.

---

## 11. Non-régression Palier 4

Toute PR Palier 5 doit confirmer :

```text
dorevia_glc_analytics : 93 tests · 0 failed
dorevia_glc_budget    : 14 tests · 0 failed
Total                 : 95 tests · 0 failed · 0 error(s)
```

Les domaines `_revenue_analytic_line_domain`, `_expense_analytic_line_domain`, `_payroll_analytic_line_domain` et les méthodes `_sum_*` exploitation **ne doivent pas** recevoir de filtre `journal_id` ou compte bancaire.

---

## 12. Verdict MOA attendu

| Verdict | Signification |
|---|---|
| **GO cadrage** | Arbitrages §5 validés · code autorisé · **`19.0.5.0.0`** |
| **GO technique serveur** | Rejeu auto **95/95** · TREF **7/7** · migration legacy **`19.0.5.0.1`** |
| **GO complet MOA** | GO technique serveur + recette navigateur §2 à §5 OK |
| **GO avec réserves** | Cadrage partiel · lot réduit (ex. champ seul, sans UI) |
| **NO GO** | Doctrine ou architecture à revoir |

**Statut actuel :** **GO complet MOA** — **`19.0.5.0.1`** · rejeu **95/95** + TREF **7/7** · précondition bancaire OK (`Compte Courant GLC`) · recette navigateur §2 à §5 OK · réserve legacy **levée**

### 12.1 Preuve MOA finale (2026-05-29)

**Période observée :** `13 avr. → 31 mai 2026`

| KPI exploitation | Compte Courant GLC | GLC - Livret Bleu | Verdict |
|---|---:|---:|---|
| Recette | `7 794,00 €` | `7 794,00 €` | Identique |
| Cumul RH | `0,00 €` | `0,00 €` | Identique |
| Dépense | `4 851,51 €` | `4 851,51 €` | Identique |
| Solde | `2 942,49 €` | `2 942,49 €` | Identique |

| Indicateur trésorerie | Compte Courant GLC | GLC - Livret Bleu | Verdict |
|---|---:|---:|---|
| Solde trésorerie période | `-1 627,11 €` | `30 000,00 €` | Recalculé selon le compte observé |

**Invariant confirmé :** le changement de compte bancaire conserve les KPI exploitation et recalcule uniquement l'onglet **Trésorerie**.

---

## 13. Liens tickets

| Ticket | Rôle |
|---|---|
| [TICKET_COCKPIT_COMPTE_BANCAIRE_REFERENCE.md](./TICKET_COCKPIT_COMPTE_BANCAIRE_REFERENCE.md) | **Doctrine MOA** — décision structurante (figée) |
| **Ce ticket** | **Cadrage + implémentation** Palier 5 trésorerie |
| [TICKET_COCKPIT_REALIGNEMENT_CONTROLE_GESTION.md](./TICKET_COCKPIT_REALIGNEMENT_CONTROLE_GESTION.md) | Palier 4 réaligné — **gelé** |

---

*Ticket ouvert post-GO livraison Palier 4 `19.0.4.9.0`. Lot trésorerie implémenté `19.0.5.0.0` · migration nomenclature `19.0.5.0.1` — GO complet MOA 2026-05-29 · **95/95** · recette navigateur §2 à §5 OK.*
