# PV de recette — V1.0.1 + V1.1 — Scénario porté par Cash Guard

**Date** : 12 mai 2026
**Environnement** : `tenant_o8`
**Run** : `RECETTE CASH SIM V101 20260512-002`
**Projection** : id `1305`

---

## 1. Décision

**GO V1.0.1 + V1.1**

La nouvelle doctrine est validée : la simulation est un scénario porté par la projection Cash Guard, et non plus un état diffus sur les devis ou les commandes achat.

---

## 2. Versions installées

| Module | Version |
| ------ | ------- |
| `dorevia_cash_simulation` | `19.0.1.0.1` |
| `dorevia_cash_simulation_purchase` | `19.0.1.1.0` |
| `purchase` | installé |

---

## 3. Tests automatisés

```text
Total : 30 tests
Failed : 0
Errors : 0
```

Note : 30 tests exécutés au lieu des 28 initialement planifiés (16 + 14 avec les 2 tests ajoutés sur la contrainte élargie).

---

## 4. Corrections de recette

Deux micro-corrections appliquées pendant la recette pour passer les prérequis :

| Fichier | Correction |
| ------- | ---------- |
| `dorevia_cash_simulation/models/cash_guard.py` | Compatibilité `situation_date=None, **kwargs` sur `_manual_line_net_by_week_index` |
| `dorevia_cash_simulation/tests/test_cash_simulation.py` | Helper `_create_quote` : `validity_date=False` explicitement supporté |
| `dorevia_cash_simulation_purchase/models/cash_guard.py` | Même compatibilité `situation_date=None, **kwargs` |

---

## 5. Recette fonctionnelle

| # | Test | Résultat |
| - | ---- | -------- |
| 1 | Simulation OFF : champs vidés, projection prudente | OK |
| 2 | Simulation ON sans document (ni devis ni achat) : blocage | OK |
| 2bis | Simulation ON avec achats seuls (P1) : impact −500 € | OK |
| 3 | Simulation ON avec D1 + D2 : impact +3 000 € | OK |
| 4 | D4 confirmé : reste dans M2M, exclu du calcul et smart button | OK |
| 5 | D3 hors période : exclu | OK |
| 6 | D1 + P1 : impact net +500 € | OK |
| 7 | P2 confirmé : reste dans M2M, exclu du calcul et smart button | OK |
| 8 | Retour OFF : devis et achats vidés, projection prudente | OK |

---

## 6. Tests complémentaires

| Test | Résultat |
| ---- | -------- |
| Aucun effet comptable automatique | OK |
| `sale.order` ne porte plus de champs `cash_simulation_*` | OK |
| `purchase.order` ne porte plus de champs `cash_simulation_*` | OK |

---

## 7. Doctrine validée

- La simulation est portée par la projection Cash Guard, pas par les devis.
- Les devis / achats sont sélectionnés explicitement dans le scénario (Many2many).
- Les documents sélectionnés restent soumis aux règles d'éligibilité.
- Les objets `sale.order` et `purchase.order` ne sont plus pollués par des champs de simulation.
- Le toggle OFF vide le scénario et revient en projection prudente.
- Le mode simulation ON exige au moins un document (devis ou achat).

---

## 8. Limites V1.0.1 + V1.1

| Limite | Statut |
| ------ | ------ |
| Les simulations impactent `projected_balance` et `risk_status`, pas `inflow_amount` / `outflow_amount` | Accepté |
| Pas de conversion multi-devise | Accepté |
| Pas d'éclatement selon conditions de paiement | Accepté |
| Le toggle est unique pour ventes + achats (pas de granularité séparée) | Accepté |
| Les colonnes techniques V1.0.0 (`cash_simulation_ok`, etc.) restent en base, nettoyage ultérieur par migration SQL | Accepté |

---

## 9. Branche et commit

```text
Branche : feature/shop-mvp22-visible-wave1
Commit recette : 8d6c476
```
