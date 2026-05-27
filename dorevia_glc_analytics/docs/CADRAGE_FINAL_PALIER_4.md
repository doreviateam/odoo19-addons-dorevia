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

### I2 — Source réalisé analytique : `account.analytic.line`

| Attribut | Valeur |
|---|---|
| Modèle | `account.analytic.line` |
| Périmètre | réalisé d’**exploitation** hors masse salariale (cf. I3) |
| Agrégation | mois × compte analytique × société × nature produit / charge / financement |

**Interdit :** inclure dans ce flux les montants déjà couverts par les ventilations salariales Palier 2 (cf. I3).

### I3 — Source masse salariale réalisée : ventilations Palier 2

| Attribut | Valeur |
|---|---|
| Modèle | `glc.salary.allocation` + `glc.salary.allocation.line` |
| États retenus | `validated`, `locked` uniquement |
| Montant | somme de `glc.salary.allocation.line.amount` |
| Agrégation | mois de ventilation × activité GLC × société |

**Invariant RH / Personnel (figé MOA, PR #31) :**

> La masse salariale réalisée du cockpit est calculée **prioritairement** depuis les ventilations salariales Palier 2 validées ou verrouillées, **sans double comptage** avec les anciennes écritures analytiques RH historiques sur `account.analytic.line`.

| Donnée cockpit | Source | Exclusion |
|---|---|---|
| Masse salariale réalisée | Ventilations Palier 2 | Écritures analytiques RH historiques |
| Ligne budgétaire RH / Personnel | `glc.budget.line` type `expense` | — |
| Écart masse comptable vs ventilée | Bandeau Palier 2 | **Informatif uniquement** — pas source cockpit |

### I4 — Pas de double comptage RH

Règle opérationnelle :

```text
Réalisé cockpit (charges salariales) = ventilations Palier 2 (I3)
Réalisé cockpit (autres charges/recettes) = account.analytic.line (I2)
```

Les écritures analytiques portant sur des comptes / axes RH historiques **ne sont pas additionnées** aux ventilations Palier 2 pour le même périmètre temporel et société.

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
Masse salariale     = agrégat ventilations Palier 2 (I3)
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
- croisement réalisé (I2 + I3) vs budget (I1) ;
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

*Document validé MOA — Palier 4 en développement (`feat/glc-cockpit-palier-4`).*
