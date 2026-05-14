# SCENARIO_MANUEL_LOT_C — `dorevia_cash_guard`

Objectif : valider manuellement le Lot C (seed optionnel documentaire + cron optionnel) avant clôture V1.

Contexte de recette :

- URL : `http://localhost:18079`
- Base : `tenant_o8` *(lettre **o**, pas `tenant_08` avec un zéro)*
- Module : `dorevia_cash_guard`

---

## 1. Préparation commune

1. Mettre à jour le module :
   - `-u dorevia_cash_guard`
2. Vérifier que l’instance dispose d’au moins un journal `bank` ou `cash`.
3. Vérifier qu’un utilisateur manager Cash Guard est disponible pour les opérations d’administration.

Attendu :

- upgrade sans erreur bloquante ;
- module accessible dans Odoo.

## C1 — Sans cron (baseline sûre)

## 2. Référentiel postes budgétaires (livrable documentaire)

1. Ouvrir :
   - `docs/REFERENTIEL_POSTES_BUDGETAIRES_V1.md`
2. Vérifier la présence des 20 postes standards.
3. Vérifier le format par poste :
   - `code`
   - `nom`
   - `famille entrée/sortie`
   - `sens cash par défaut`
   - `ordre`
   - `description métier`
   - `comptes comptables suggérés`

Attendu :

- référentiel documentaire complet disponible ;
- structure homogène sur les 20 postes.

---

## 3. Politique seed (non automatique)

1. Vérifier que `budget_post_seed.xml` n’est pas chargé automatiquement par le manifest.
2. Vérifier que le principe de mapping manuel est documenté (SPEC/TICKETS/référentiel).
3. Vérifier qu’aucun poste n’est injecté automatiquement sans validation mapping.

Attendu :

- pas de seed automatique ;
- mapping comptes validé manuellement dans l’instance avant toute activation seed.

## 4. Contrôle cron en état par défaut (inactif)

1. Vérifier l’existence du cron :
   - `Cash Guard - Recompute Open Points`
2. Vérifier qu’il est **désactivé par défaut**.
3. Vérifier la fréquence :
   - intervalle `1` jour (`daily`).

Attendu :

- cron présent ;
- cron inactif par défaut ;
- périodicité quotidienne correcte.

---

## C2 — Cron actif (test dynamique)

## 5. Activation et périmètre cron : uniquement points ouverts

1. Activer temporairement le cron `Cash Guard - Recompute Open Points`.
2. Préparer trois points :
   - un `draft`
   - un `validated`
   - un `closed`
3. Exécuter le cron (manuel ou “Run Manually”).
4. Vérifier le périmètre traité.

Attendu :

- les points `draft` et `validated` sont inclus dans le recalcul ;
- les points `closed` sont exclus ;
- aucune modification non attendue des points clôturés.
- le cron peut ensuite être remis à l’état inactif par défaut.

---

## 6. Non-régression fonctionnelle rapide

Après activation manuelle ponctuelle du cron :

1. Ouvrir un point `draft` et vérifier cohérence des indicateurs (`initial_balance`, `forecast_final_balance`, `forecast_min_balance`, `risk_status`).
2. Vérifier qu’un point `closed` reste non modifiable par un user non manager.

Attendu :

- recalcul stable sur points ouverts ;
- règles de sécurité/workflow Lot B toujours respectées.

---

## 7. Verdict recette Lot C

| Contrôle | Résultat | Commentaire |
| --- | --- | --- |
| Upgrade module | OK / KO | |
| Référentiel documentaire 20 postes présent | OK / KO | |
| Format complet par poste respecté | OK / KO | |
| Seed non automatique | OK / KO | |
| Mapping comptes manuel explicitement requis | OK / KO | |
| Cron présent | OK / KO | |
| Cron désactivé par défaut | OK / KO | |
| Cron quotidien (1 jour) | OK / KO | |
| Cron inclut `draft` et `validated` | OK / KO | |
| Cron exclut `closed` | OK / KO | |
| Non-régression indicateurs de trésorerie | OK / KO | |

## Verdict

- [ ] GO Lot C
- [ ] NO GO Lot C

Commentaires :

```text
...
```
