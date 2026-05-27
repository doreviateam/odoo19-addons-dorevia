# Ticket Palier 4 — Cockpit couverture des salaires

**Module principal :** `dorevia_glc_analytics` *(extension)*  
**Dépendance :** `dorevia_glc_budget` (Palier 3)  
**Branche cible :** `feat/glc-cockpit-palier-4`  
**Version cible analytics :** `19.0.4.0.0`  
**Statut :** **Recette MOA validée** (2026-05-27 · `glc-rgl-test-import`) · [PR #33](https://github.com/doreviateam/odoo19-addons-dorevia/pull/33) — merge en attente

**Références :** [CADRAGE_FINAL_PALIER_4.md](./CADRAGE_FINAL_PALIER_4.md) · [CADRAGE_BUDGET_COCKPIT.md](./CADRAGE_BUDGET_COCKPIT.md) · [TICKET_PALIER_3.md](./TICKET_PALIER_3.md) · [PALIERS.md](./PALIERS.md)

---

## 1. Objectif

Créer le **tableau de bord de pilotage** répondant à la question MOA :

> Génère-t-on assez de recettes pour couvrir les salaires — puis les frais généraux ?

Croisement :

```text
réalisé analytique  vs  budget prévisionnel  vs  alertes de couverture
```

---

## 2. Sources de données

| Flux | Source | Agrégation |
|---|---|---|
| Réalisé (hors masse salariale) | `account.analytic.line` | mois × compte analytique × société × type produit/charge/financement |
| Prévisionnel | `glc.budget.line` | mois × compte analytique × type recette/charge/financement |
| Masse salariale réalisée | `glc.salary.allocation` (Palier 2) | **source prioritaire** — ventilations `validated` / `locked` |

**Doctrine :** exclure du réalisé d’exploitation les flux bilan (emprunt `164`, virements internes, etc.) — cf. [CADRAGE_BUDGET_COCKPIT.md](./CADRAGE_BUDGET_COCKPIT.md).

### Règle MOA figée — RH / Personnel

Le prévisionnel Palier 3 peut budgéter **RH / Personnel** comme ligne `expense`.

Pour le cockpit Palier 4, la **masse salariale réalisée** doit être agrégée **prioritairement** depuis les **ventilations salariales Palier 2** (`glc.salary.allocation` en état `validated` ou `locked`), afin d’éviter tout **double comptage** avec les écritures analytiques historiques RH sur `account.analytic.line`.

| Donnée cockpit | Source retenue | Exclusion |
|---|---|---|
| Masse salariale réalisée | Somme des montants ventilés Palier 2 (`glc.salary.allocation.line.amount`) | Écritures analytiques RH historiques sur le même périmètre |
| Ligne budgétaire RH / Personnel | `glc.budget.line` type `expense` | — |

> Cette règle est **figée MOA** avant démarrage dev cockpit. Toute lecture comptable complémentaire (écart masse comptable vs ventilée) reste **informatif** (bandeau Palier 2), pas une source d’agrégation cockpit.

---

## 3. Indicateurs attendus

### Ressources

```text
Recettes d’activité = BAR + PRESTATIONS + PRIVATISATIONS
Financements = SUBVENTIONS (+ adhésions si retenu)
Ressources disponibles = Recettes d’activité + Financements
```

### Charges

```text
Masse salariale = RH / Personnel (axe ou agrégat ventilé)
Charges fixes = RH / Personnel + Frais généraux
```

### KPI cockpit

- taux de couverture des salaires ;
- solde après salaires ;
- solde après salaires + frais généraux ;
- écart budget / réalisé par mois et par activité ;
- tendance mensuelle ;
- statut alerte rouge / orange / vert.

---

## 4. Alertes de gestion

| Statut | Condition |
|---|---|
| Rouge | Ressources disponibles < RH / Personnel |
| Orange | Ressources ≥ RH / Personnel mais < RH / Personnel + Frais généraux |
| Vert | Ressources ≥ RH / Personnel + Frais généraux |

---

## 5. Hors périmètre Palier 4 (→ Palier 5)

- Graphiques avancés multi-scénarios ;
- export Excel / PDF ;
- commentaires de gestion par mois ;
- comparaison budget initial / révisé / atterrissage ;
- projections fin d’année ;
- bloc trésorerie ;
- intégration OCA Budget.

---

## 6. Prérequis livraison

- [x] Palier 3 gelé MOA (`dorevia_glc_budget`)
- [x] Jeu de données budget + réalisé sur `glc-rgl-test-import`
- [x] Validation MOA des formules d’agrégation et des seuils d’alerte — recette P4.1–P4.6
- [x] Règle d’agrégation masse salariale réelle (ventilations Palier 2) figée MOA — cf. §2
- [x] Invariants I1–I7 validés MOA — [CADRAGE_FINAL_PALIER_4.md](./CADRAGE_FINAL_PALIER_4.md) (Option A · 2026-05-27)
- [x] Jeu de données recette budget + réalisé + ventilations (G6)
- [x] **GO MOA explicite** ouverture branche `feat/glc-cockpit-palier-4` (G7)

---

## 7. Livrables prévisionnels

- Modèle ou wizard cockpit (vue pivot / dashboard Odoo 19)
- Filtres : société · année · mois · activité
- Bandeau synthèse + détail Activité × Mois
- Tests automatisés agrégations et alertes
- [RECETTE_MANUELLE_PALIER_4.md](./RECETTE_MANUELLE_PALIER_4.md) — **validée MOA** (2026-05-27)
