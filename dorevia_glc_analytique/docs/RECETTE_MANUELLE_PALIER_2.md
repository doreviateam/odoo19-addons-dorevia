# Recette manuelle — dorevia_glc_analytique · Palier 2

**Module :** `dorevia_glc_analytique`  
**Version cible :** `19.0.3.0.0` (Palier 2)  
**Rôle testeur :** Gestionnaire GLC / MOA  
**Prérequis :** Palier 0 + Palier 1 validés MOA · [TICKET_PALIER_2.md](./TICKET_PALIER_2.md) implémenté  
**Références :** [REGLES_AFFECTATION.md](./REGLES_AFFECTATION.md) · [MATRICE_MIGRATION.md](./MATRICE_MIGRATION.md)

**Hors périmètre :** bénévolat, rapport CA complet, clôture, écritures comptables auto, `hr_payroll`.

**Statut document :** gelé pour exécution recette MOA sur `glc-rgl-test-import` (Palier 2).

---

## Contexte de recette

```text
URL  : http://localhost:18079
Base : glc-rgl-test-import
Module : dorevia_glc_analytique (Palier 2)
Version : 19.0.3.0.0
```

---

## Jeu de données de test (à préparer)

| Jeu | Description | Contrôle attendu |
|---|---|---|
| T1 | `glc.employee.cost.line` — coût + heures ref. | Coût horaire calculé |
| T2 | Ventilation `percent` 100 % sur 3 activités | Validation OK |
| T3 | Ventilation `percent` ≠ 100 % en brouillon | Brouillon OK |
| T3b | Ventilation `percent` ≠ 100 % à validation | Validation refusée |
| T4 | Ventilation `hours` + `reference_hours` > 0 | Montants = heures × coût horaire |
| T4b | Ventilation `hours` total ≠ référence à validation | Validation refusée |
| T5 | Ligne activité Financements | Refus / contrainte |
| T6 | Masse comptable vs total ventilé | Bandeau écart > 5 % si écart |

---

## Parcours nominal

| Pas | Action | Contrôles | OK | Observations |
|---|---|---|---|---|
| P2.1 | Menu **Coûts salariés mensuels** | Accès Gestionnaire GLC | ☑ | |
| P2.2 | Créer coût mensuel salarié test | `hourly_cost` OK | ☑ | 3000 / 150 = 20,00 |
| P2.3 | Menu **Ventilations salariales** | Formulaire + lignes | ☑ | |
| P2.4 | Ventilation T2 (100 % · 3 activités) | État `validated` | ☑ | |
| P2.5 | Ventilation T3b (60 % à validation) | Validation bloquée | ☑ | |
| P2.5bis | Ventilation T3 partielle en brouillon | Enregistrement OK | ☑ | |
| P2.6 | Ventilation T4 / T4b (heures) | Montants · validation si total = référence | ☑ | 100 h ref. · 80 h refusées |
| P2.7 | T5 Financements (`ADHESIONS`) | Refus | ☑ | |
| P2.8 | Bandeau écart masse comptable | Alerte si seuil | ☑ | Écart 50 % |
| P2.9 | Vérifier absence écriture comptable | Pas de `account.move` créé | ☑ | |
| P2.10 | Non-régression Palier 1 | Wizard anomalies OK | ☑ | |

---

## Critères d'acceptation (mapping ticket)

| CA | Pas recette | ☑ |
|---|---|---|
| CA1 | P2.1 / P2.3 | ☑ |
| CA2 | P2.2 | ☑ |
| CA3 | P2.4 | ☑ |
| CA4 | P2.5 / P2.5bis | ☑ |
| CA5 | P2.6 | ☑ |
| CA6 | P2.7 | ☑ |
| CA7 | P2.8 | ☑ |
| CA8 | P2.9 | ☑ |
| CA9 | P2.10 | ☑ |

---

## Verdict recette Palier 2

| Verdict | Condition |
|---|---|
| **GO MOA Palier 2** | P2.1–P2.10 OK · CA1–CA9 OK |
| **GO avec réserves** | Écarts mineurs UX · points vigilance documentés |
| **NO GO** | Écritures comptables générées · régression Palier 1 |

**Verdict :** ☑ **GO MOA Palier 2** · ☐ GO avec réserves · ☐ NO GO

**Testeur :** MOA GLC **Date :** 2026-05-27

**Commentaire MOA :**

```text
Recette exécutée sur glc-rgl-test-import (http://localhost:18079).
Module 19.0.3.0.0 · tests auto : 25/25.
Coût horaire, ventilations percent/hours, refus Financements,
bandeau écart masse comptable (50 %), absence écriture comptable,
non-régression Palier 1 conformes.
Warning Odoo domaine multi-société activity_account_id : non bloquant.
```

---

## Clôture recette — `glc-rgl-test-import` (2026-05-27)

| Contrôle | Résultat |
|---|---|
| Mise à jour module Docker (`19.0.3.0.0`) | OK |
| Redémarrage Odoo | OK |
| Tests automatisés (`/dorevia_glc_analytique`) | **25 post-tests, 0 échec, 0 erreur** |
| Menu **Coûts salariés mensuels** | OK |
| Menu **Ventilations salariales** | OK |
| Coût horaire `3000 / 150` | 20,00 OK |
| Ventilation `percent` 100 % (3 activités) | Validée OK |
| Ventilation `percent` partielle brouillon | OK |
| Validation `percent` à 60 % | Refusée OK |
| Ventilation `hours` 100 h référence | Montants + validation OK |
| Validation `hours` 80 h / 100 h | Refusée OK |
| Ligne Financements `ADHESIONS` | Refusée OK |
| Bandeau écart masse comptable | Alerte OK — écart 50 % |
| Absence écriture comptable à validation | OK |
| Non-régression Palier 1 (wizard anomalies) | OK |
| URL Odoo joignable | OK |

### Point de vigilance (non bloquant)

Warning Odoo sur le domaine multi-société de `glc.salary.allocation.line.activity_account_id`. Les tests et contrôles métier passent ; correction domaine prévue en maintenance légère post-recette.

> Aucun fichier du dépôt modifié lors de la recette. Fichier non suivi hors périmètre inchangé : `dorevia_ckreyol_marketone/static/src/interactions/marketone_shop_wishlist_cart_add.js`.

### Suite immédiate

- Palier 2 **validé MOA** — overlay ventilation salariale prêt pour usage courant.
- Merge **PR #26** · gel Palier 2.
- Prochain ticket : **Palier 3** — registre bénévole (branche dédiée).

## Après validation Palier 2

1. Alimenter le futur **solde de gestion** (Palier 4) via coûts salariés ventilés.
2. Cadrage **Palier 3** — registre bénévole, séparé.
3. Applicabilités **`optional`** maintenues — pas de `mandatory`.
