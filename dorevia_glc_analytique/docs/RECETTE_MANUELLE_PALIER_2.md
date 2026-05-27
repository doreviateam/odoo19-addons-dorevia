# Recette manuelle — dorevia_glc_analytique · Palier 2

**Module :** `dorevia_glc_analytique`  
**Version cible :** `19.0.3.0.0` (Palier 2 — à confirmer au release)  
**Rôle testeur :** Gestionnaire GLC / MOA  
**Prérequis :** Palier 0 + Palier 1 validés MOA · [TICKET_PALIER_2.md](./TICKET_PALIER_2.md) implémenté  
**Références :** [REGLES_AFFECTATION.md](./REGLES_AFFECTATION.md) · [MATRICE_MIGRATION.md](./MATRICE_MIGRATION.md)

**Hors périmètre :** bénévolat, rapport CA complet, clôture, écritures comptables auto, `hr_payroll`.

---

## Contexte de recette

```text
URL  : http://localhost:18079
Base : glc-rgl-test-import
Module : dorevia_glc_analytique (Palier 2)
```

---

## Jeu de données de test (à préparer)

| Jeu | Description | Contrôle attendu |
|---|---|---|
| T1 | `glc.employee.cost.line` — coût + heures ref. | Coût horaire calculé |
| T2 | Ventilation `percent` 100 % sur 3 activités | Validation OK |
| T3 | Ventilation `percent` ≠ 100 % | Validation refusée |
| T4 | Ventilation `hours` | Montants = heures × coût horaire |
| T5 | Ligne activité Financements | Refus / contrainte |
| T6 | Masse comptable vs total ventilé | Bandeau écart > 5 % si écart |

---

## Parcours nominal

| Pas | Action | Contrôles | OK | Observations |
|---|---|---|---|---|
| P2.1 | Menu **Coûts salariés mensuels** | Accès Gestionnaire GLC | ☐ | |
| P2.2 | Créer coût mensuel salarié test | `hourly_cost` OK | ☐ | |
| P2.3 | Menu **Ventilations salariales** | Formulaire + lignes | ☐ | |
| P2.4 | Ventilation T2 (100 %) | État `validated` | ☐ | |
| P2.5 | Ventilation T3 (≠ 100 %) | Validation bloquée | ☐ | |
| P2.6 | Ventilation T4 (heures) | Montants cohérents | ☐ | |
| P2.7 | T5 Financements | Refus | ☐ | |
| P2.8 | Bandeau écart masse comptable | Alerte si seuil | ☐ | |
| P2.9 | Vérifier absence écriture comptable | Pas de `account.move` créé | ☐ | |
| P2.10 | Non-régression Palier 1 | Wizard anomalies OK | ☐ | |

---

## Critères d'acceptation (mapping ticket)

| CA | Pas recette | ☐ |
|---|---|---|
| CA1 | P2.1 / P2.3 | ☐ |
| CA2 | P2.2 | ☐ |
| CA3 | P2.4 | ☐ |
| CA4 | P2.5 | ☐ |
| CA5 | P2.6 | ☐ |
| CA6 | P2.7 | ☐ |
| CA7 | P2.8 | ☐ |
| CA8 | P2.9 | ☐ |
| CA9 | P2.10 | ☐ |

---

## Verdict recette Palier 2

| Verdict | Condition |
|---|---|
| **GO MOA Palier 2** | P2.1–P2.10 OK · CA1–CA9 OK |
| **GO avec réserves** | Écarts mineurs UX · points vigilance documentés |
| **NO GO** | Écritures comptables générées · régression Palier 1 |

**Verdict :** ☐ GO MOA Palier 2 · ☐ GO avec réserves · ☐ NO GO

**Testeur :** __________________ **Date :** __________
