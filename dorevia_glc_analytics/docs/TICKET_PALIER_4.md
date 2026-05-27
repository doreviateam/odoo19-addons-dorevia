# Ticket Palier 4 — Cockpit couverture des salaires

**Module principal :** `dorevia_glc_analytics` *(extension)*  
**Dépendance :** `dorevia_glc_budget` (Palier 3)  
**Branche cible :** `feat/glc-cockpit-palier-4`  
**Version cible analytics :** `19.0.4.0.0`  
**Statut :** Cadrage — **ne pas démarrer avant gel Palier 3**

**Références :** [CADRAGE_BUDGET_COCKPIT.md](./CADRAGE_BUDGET_COCKPIT.md) · [TICKET_PALIER_3.md](./TICKET_PALIER_3.md) · [PALIERS.md](./PALIERS.md)

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
| Réalisé | `account.analytic.line` | mois × compte analytique × société × type produit/charge/financement |
| Prévisionnel | `glc.budget.line` | mois × compte analytique × type recette/charge/financement |
| Masse salariale ventilée | `glc.salary.allocation` (Palier 2) | complément lecture gestion si besoin |

**Doctrine :** exclure du réalisé d’exploitation les flux bilan (emprunt `164`, virements internes, etc.) — cf. [CADRAGE_BUDGET_COCKPIT.md](./CADRAGE_BUDGET_COCKPIT.md).

### Vigilance MOA — RH / Personnel

Le prévisionnel Palier 3 peut budgéter **RH / Personnel** comme ligne `expense`.

Le **réalisé** ne provient pas d’un compte historique unique `RH_PERSONNEL` : la masse salariale réelle devra être agrégée en Palier 4 à partir des **ventilations salariales Palier 2** (`glc.salary.allocation`) et/ou de la lecture comptable, selon règle MOA à figer en recette Palier 4.

> Point à valider explicitement en recette Palier 4 : formule d’agrégation de la masse salariale réelle vs ligne budgétaire RH / Personnel.

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

- [ ] Palier 3 gelé MOA (`dorevia_glc_budget`)
- [ ] Jeu de données budget + réalisé sur `glc-rgl-test-import`
- [ ] Validation MOA des formules d’agrégation et des seuils d’alerte
- [ ] Règle d’agrégation masse salariale réelle (ventilations Palier 2) validée MOA

---

## 7. Livrables prévisionnels

- Modèle ou wizard cockpit (vue pivot / dashboard Odoo 19)
- Filtres : société · année · mois · activité
- Bandeau synthèse + détail Activité × Mois
- Tests automatisés agrégations et alertes
- [RECETTE_MANUELLE_PALIER_4.md](./RECETTE_MANUELLE_PALIER_4.md) *(à rédiger au démarrage)*
