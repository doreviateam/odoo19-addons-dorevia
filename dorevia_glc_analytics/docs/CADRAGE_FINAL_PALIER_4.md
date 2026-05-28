# Cadrage final Palier 4 — Cockpit couverture des salaires

**Date :** 2026-05-27  
**Statut :** **Validé MOA (Option A)** — invariants I1–I7 acceptés · PR #32  
**Gate développement :** branche `feat/glc-cockpit-palier-4` ouverte uniquement après **GO MOA explicite** (G7)

**Références :** [AUDIT_GLC_ANALYTICS_BUDGET_AVANT_PALIER_4.md](./AUDIT_GLC_ANALYTICS_BUDGET_AVANT_PALIER_4.md) · [TICKET_PALIER_4.md](./TICKET_PALIER_4.md) · [CADRAGE_BUDGET_COCKPIT.md](./CADRAGE_BUDGET_COCKPIT.md)

---

## 1. Contexte

Le socle Paliers 0–3 est **gelé et validé MOA** :

| Élément | Statut |
|---|---|
| `dorevia_glc_analytics` (Paliers 0–2) | Gelé |
| `dorevia_glc_budget` (Palier 3) | Gelé |
| Audit officiel (PR #29) | Mergé |
| Maintenance P2 pré-Palier 4 (PR #30) | Mergée |
| Règle RH / Personnel (PR #31) | Figée |
| Tests recette (`glc-rgl-test-import`) | 39 tests, 0 échec |

Le Palier 4 est **cadré et validé MOA** (invariants I1–I7). Le développement cockpit reste **en attente du GO explicite** (G7).

---

## 2. Invariants non négociables

Ces règles sont **structurantes** pour toute implémentation Palier 4. Aucune dérogation sans décision MOA explicite.

### I1 — Source prévisionnelle : `glc.budget.line`

| Attribut | Valeur |
|---|---|
| Modèle | `glc.budget.line` (Palier 3) |
| Filtre | budget `validated` ou `archived` (scénario retenu en recette : `initial` par défaut) |
| Agrégation | mois × compte analytique × type `revenue` / `expense` / `funding` × société |

**Interdit :** recalculer ou resaisir le prévisionnel dans le cockpit ; modifier le module `dorevia_glc_budget`.

### I2 — Source réalisé cockpit : `account.analytic.line` (révision MOA 2026-05-28 · raffiné `19.0.4.8.0`)

| Attribut | Valeur |
|---|---|
| Modèle | `account.analytic.line` |
| Règle de remontée | **date dans la période** + **montant non nul** + **GL classe 6 ou 7** + **distribution analytique exploitable** |
| Périmètre analytique | **tous les comptes analytiques, tous plans** (Activités GLC, Financements GLC, autres) — hors codes legacy / `RH_PERSONNEL` |
| Origines | facture client/fournisseur · OD · rapprochement bancaire · caisse |
| Agrégation | mois × compte analytique × société × nature comptable (classe 6 / classe 7) |

**Règle :** la présence ou l'absence d'une facture **n'est pas** un critère d'inclusion.

**Mapping familles cockpit (cartographie GL × plan analytique) :**

| Compte GL | Compte analytique | Famille cockpit | Sens |
|---|---|---|---|
| **7xxx** | Plan **Activités GLC** *(toute activité)* | **RECETTES** | + |
| **7xxx** | Plan **Financements GLC** *(SUBVENTIONS, ADHESIONS, DONS, RESSOURCES_PROPRES)* | **RESSOURCES / FINANCEMENTS** | + |
| **7xxx** | **Tout autre plan analytique** | **RECETTES** *(classe 7 = entrée)* | + |
| **631 / 633 / 641 / 645** | **Tout plan analytique exploitable** | **SALAIRES** | − |
| **6xxx hors payroll** | **Tout plan analytique exploitable** | **DÉPENSES** | − |

**Tous les plans analytiques** sont pris en compte par défaut. Le filtre par plan (Activités GLC / Financements GLC / …) est une **option UX ultérieure**, pas une limite de calcul.

**Exclusions (I5) :** classes **1xx / 4xx / 5xx** (164, 401, 411, 467, 512, 53), lettrage seul, lignes sans analytique exploitable, comptes legacy / `RH_PERSONNEL`.

**Défense en profondeur (cumulée) :**

1. `account_type` ∈ income / income_other / expense / expense_direct_cost / expense_depreciation
2. **garde-fou explicite** : `general_account_id.code` commence par `6` ou `7`
3. exclusion préfixes `164` + codes analytiques legacy
4. exclusion préfixes payroll (631/633/641/645) des DÉPENSES

### I3 — Palier 2 ventilations salariales : rôle contrôle (R2 — révision MOA 2026-05-28)

| Attribut | Valeur |
|---|---|
| Modèle | `glc.salary.allocation` + `glc.salary.allocation.line` |
| Rôle cockpit | **Contrôle / ventilation RH / analyse d'écart** — **pas** source primaire du réalisé |
| Bandeau écart Palier 2 | Informatif (masse comptable vs ventilée) |

**Invariant révisé :**

> Le réalisé cockpit **SALAIRES** provient des `account.analytic.line` portant un compte 631/633/641/645 et une distribution analytique activité. Les ventilations Palier 2 **ne suralimentent pas** le cockpit.

| Donnée cockpit | Source |
|---|---|
| Masse salariale réalisée | `account.analytic.line` (comptes payroll + analytique activité) |
| Ventilations Palier 2 | Contrôle RH — bandeau écart informatif |
| Ligne budgétaire RH / Personnel | `glc.budget.line` type `expense` (I1) |

### I4 — Pas de double comptage (révision MOA 2026-05-28)

Règle opérationnelle :

```text
Réalisé cockpit (toutes familles) = account.analytic.line charge/produit + analytique
Palier 2 = contrôle uniquement — jamais additionné au réalisé cockpit
Anti-doublon : une charge mois × société × activité × famille = comptée une seule fois
```

Les ventilations Palier 2 validées **ne sont plus agrégées** dans `payroll_realized` du cockpit.

### I5 — Exclusion des flux bilan / trésorerie

Le cockpit lit l’**exploitation**, pas la trésorerie ni le bilan.

Flux **exclus** du réalisé cockpit (doctrine [CADRAGE_BUDGET_COCKPIT.md](./CADRAGE_BUDGET_COCKPIT.md)) :

| Flux | Exemple |
|---|---|
| Emprunts / dette financière | compte `164`, remboursement de capital |
| Virements internes | transferts entre comptes bancaires |
| Compte courant / livret | mouvements de trésorerie internes |
| Reprise de solde | écritures d’ouverture / reprise |
| Transfert bancaire pur | sans impact activité GLC |

Ces flux ne doivent **pas** alimenter le plan **Activités GLC** ni fausser les KPI de couverture.

**Hors périmètre Palier 4 :** bloc trésorerie, soldes bancaires, échéancier emprunts (→ Palier 5).

### I6 — Alertes rouge / orange / vert

Seuils de gestion **figés** pour la V1 cockpit :

| Statut | Condition |
|---|---|
| **Rouge** | Ressources disponibles < masse salariale (RH / Personnel) |
| **Orange** | Ressources ≥ masse salariale mais < masse salariale + frais généraux |
| **Vert** | Ressources ≥ masse salariale + frais généraux |

Avec :

```text
Recettes d’activité = BAR + PRESTATIONS + PRIVATISATIONS
Financements        = SUBVENTIONS (+ adhésions si retenu en recette)
Ressources          = Recettes d’activité + Financements
Masse salariale     = account.analytic.line comptes 631/633/641/645 + analytique (I2/I3 révisés)
Frais généraux      = axe analytique Frais généraux (I2)
```

### I7 — Palier 3 inchangé dans le Palier 4

| Règle | Détail |
|---|---|
| Module `dorevia_glc_budget` | **Gelé** — aucune évolution fonctionnelle dans le Palier 4 |
| Modèles Palier 3 | `glc.budget`, `glc.budget.line` consommés en **lecture seule** |
| Workflow Palier 3 | inchangé (`draft` → `validated` → `archived`) |
| Développement Palier 4 | extension `dorevia_glc_analytics` uniquement (cockpit) |

---

## 3. Périmètre V1 cockpit (rappel)

**Inclus :**

- vue synthèse + détail Activité × Mois ;
- croisement réalisé (I2 révisé) vs budget (I1) ;
- KPI couverture et écarts ;
- bandeau alerte rouge / orange / vert (I6) ;
- filtres : société · année · mois · activité ;
- tests automatisés agrégations et alertes.

**Exclus (→ Palier 5) :**

- graphiques multi-scénarios, exports Excel/PDF ;
- comparaison initial / révisé / atterrissage ;
- commentaires de gestion, projections fin d’année ;
- trésorerie, OCA Budget.

---

## 4. Gate MOA — ouverture développement

| # | Condition | Statut |
|---|---|---|
| G1 | Socle Paliers 0–3 gelé sur `main` | ✅ Validé |
| G2 | Audit officiel mergé (PR #29) | ✅ Validé |
| G3 | Maintenance P2 mergée (PR #30) | ✅ Validé |
| G4 | Règle RH / Personnel figée (PR #31) | ✅ Validé |
| G5 | **Invariants I1–I7 validés MOA** (ce document) | ✅ Validé (2026-05-27 · Option A) |
| G6 | Jeu de données recette budget + réalisé + ventilations | ✅ Validé (2026-05-27 · fonctionnel pour démarrage) |
| G7 | **GO MOA explicite** ouverture `feat/glc-cockpit-palier-4` | ✅ Validé (2026-05-27) |

---

## 5. Décision MOA

**Option A — GO cadrage final** : **validée MOA (2026-05-27)**.

Les invariants I1–I7 sont acceptés tels quels. Prochaine étape : confirmation G6 (jeu de données recette) puis **GO explicite G7** pour ouvrir `feat/glc-cockpit-palier-4`.

---

*Palier 4 livré et gelé MOA sur `main` — version `19.0.4.0.0` · PR #33 mergée.*  
*Révision I2/I3/I4 source réalisé cockpit — MOA validée 2026-05-28 · `19.0.4.7.0` · [TICKET_COCKPIT_SOURCE_REALISE.md](./TICKET_COCKPIT_SOURCE_REALISE.md).*  
*Raffinement I2 doctrine classe 6/7 (toute activité, tous plans) — MOA validée 2026-05-28 · `19.0.4.8.1` · [TICKET_COCKPIT_DOCTRINE_CLASSE_6_7.md](./TICKET_COCKPIT_DOCTRINE_CLASSE_6_7.md).*
