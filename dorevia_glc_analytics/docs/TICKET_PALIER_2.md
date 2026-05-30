# Ticket Palier 2 — Ventilation salariale mensuelle


> **Document historique** — ne décrit plus le produit installé depuis **`19.0.13.0.0`** / **`19.0.14.0.0`**. État actuel : [ETAT_MODULE_ACTUEL.md](./ETAT_MODULE_ACTUEL.md).

---

**Module :** `dorevia_glc_analytics`  
**Branche cible :** `feat/glc-analytique-palier-2`  
**Version cible :** `19.0.3.0.0`  
**Statut :** Validé MOA — gelé (recette 2026-05-27 · PR #26)  
**Prérequis :**
- Palier 0 gelé : socle analytique
- Palier 1 gelé : assistant anomalies analytiques (PR #25 mergée)
- Applicabilités maintenues en `optional`
- Pas de durcissement `mandatory`

**Références :** [PALIERS.md](./PALIERS.md) · [REGLES_AFFECTATION.md](./REGLES_AFFECTATION.md) · [MATRICE_MIGRATION.md](./MATRICE_MIGRATION.md) · [spec V1.1 §8.2 / §9.2](./README.md)

---

## 1. Contexte

Le Palier 1 permet d’identifier les anomalies analytiques sur les écritures comptables.

Le Palier 2 traite un sujet différent : **la masse salariale**.

Dans la doctrine GLC, un salaire n’est pas une activité. C’est une ressource consommée par plusieurs activités.

Le compte historique `RH_PERSONNEL` ne doit **pas** être conservé comme activité pilotable. Les coûts salariés doivent être ventilés mensuellement vers les activités réelles :

- `STRUCTURE`
- `BAR`
- `PRESTATIONS`
- `RESIDENCES`
- `MISSIONS`
- `PRIVATISATIONS`
- `LOCATION_RADIO`

> **Interdit** : comptes du plan `GLC - Financements` · compte « salaire » / `RH_PERSONNEL` dans le plan Activités cible.

---

## 2. Objectif Palier 2

Créer un mécanisme de **ventilation salariale mensuelle** permettant au gestionnaire GLC d’affecter le coût salarié chargé d’un mois aux activités GLC.

Le résultat alimente les futurs calculs de **coût complet** (Palier 4) et le rapport CA mensuel, **sans modifier la comptabilité générale**.

---

## 3. Doctrine d’architecture

### 3.1 Pas d’écriture comptable

Le Palier 2 ne génère **aucune** écriture comptable (`account.move`).

### 3.2 Pas d’écriture analytique de paie

Le Palier 2 ne crée **pas** d’`analytic_distribution` sur les lignes de paie. Le contrôle A4 (Palier 1) reste la règle côté comptabilité.

### 3.3 Overlay de gestion uniquement

La ventilation salariale est une **donnée de gestion**, rattachée au mois, au salarié et aux activités.

### 3.4 Source de vérité comptable inchangée

Les salaires restent lus dans la comptabilité générale : comptes `631*`, `633*`, `641*`, `645*`, etc.

La ventilation sert à expliquer comment cette masse salariale est **consommée** par les activités.

### 3.5 Applicabilités analytiques

**Inchangées** : plans GLC en `optional`. Aucun passage `mandatory` dans ce palier.

---

## 4. Modèles attendus

### 4.1 `glc.salary.allocation`

Objet principal de ventilation mensuelle.

| Champ | Description |
|---|---|
| `company_id` | Société |
| `period_date` | Premier jour du mois concerné (clé de période) |
| `employee_id` | Salarié (`hr.employee`) |
| `employee_cost_line_id` | Coût mensuel chargé de référence |
| `cost_amount` | Coût mensuel chargé ventilable (related ou saisi) |
| `currency_id` | Devise |
| `method` | `percent` ou `hours` |
| `line_ids` | Lignes de ventilation |
| `total_percent` | Total pourcentage (computed) |
| `total_hours` | Total heures (computed) |
| `allocated_amount` | Montant total ventilé (computed) |
| `state` | `draft` / `to_check` / `validated` / `locked` |
| `validated_by` | Validateur |
| `validated_date` | Date validation |
| `note` | Commentaire |

**Contrainte d’unicité :** `(company_id, employee_id, period_date)` — une ventilation par salarié et par mois.

### 4.2 `glc.salary.allocation.line`

Ligne de ventilation par activité.

| Champ | Description |
|---|---|
| `allocation_id` | Ventilation parente |
| `activity_account_id` | Compte analytique du plan `GLC - Activités` |
| `percent` | Pourcentage affecté (si méthode `percent`) |
| `hours` | Heures affectées (si méthode `hours`) |
| `amount` | Montant calculé |
| `note` | Commentaire |

**Contraintes :**

- l’activité doit appartenir au plan `GLC - Activités` ;
- **interdit** : comptes du plan `GLC - Financements` ;
- pas de doublon d’activité sur une même ventilation.

### 4.3 `glc.employee.cost.line`

Historique mensuel du coût salarié chargé.

| Champ | Description |
|---|---|
| `company_id` | Société |
| `employee_id` | Salarié |
| `period_date` | Premier jour du mois |
| `cost_amount` | Coût mensuel chargé |
| `reference_hours` | Heures mensuelles de référence — **obligatoire et > 0** si méthode `hours` sur la ventilation liée |
| `hourly_cost` | Coût horaire calculé (stored computed) |
| `currency_id` | Devise |
| `source` | `manual` (V1 — pas d’import paie auto) |
| `note` | Commentaire |

**Formule :**

```text
Coût horaire = coût mensuel chargé / heures mensuelles de référence
```

**Contrainte d’unicité :** `(company_id, employee_id, period_date)`.

**Définition V1 du coût mensuel chargé :** salaire brut + charges patronales + avantages en nature (à valider avec la paie GLC). **Saisie manuelle** prioritaire — **pas** d’import paie automatique ni de lien `hr_payroll` en V1 (évolution V2).

### 4.4 Montants ventilés par activité

**Méthode `percent` :**

```text
Montant activité = coût mensuel chargé × pourcentage activité / 100
```

**Méthode `hours` :**

```text
Montant activité = heures activité × coût horaire
```

---

## 5. Workflow et statuts

| État | Description | Actions |
|---|---|---|
| `draft` | Saisie en cours | Édition libre |
| `to_check` | Soumis au contrôle | Édition gestionnaire ; contrôles totaux |
| `validated` | Ventilation validée MOA / gestionnaire | Lecture seule sauf déverrouillage contrôlé |
| `locked` | Mois verrouillé (préparation Palier 5) | Aucune modification |

**Règles de validation (gel MOA) :**

| Méthode | Brouillon (`draft` / `to_check`) | Validation (`validated`) |
|---|---|---|
| `percent` | Ventilation **partielle** autorisée (total `< 100 %`) | **Refusée** si somme des `percent` ≠ **100 %** (tolérance 0,01 pt) |
| `hours` | Ventilation **partielle** autorisée (total heures `< reference_hours`) | **Refusée** si somme des `hours` ≠ **`reference_hours`** du coût mensuel lié |

**Prérequis méthode `hours` :**

- `glc.employee.cost.line.reference_hours` **obligatoire** et **strictement > 0** ;
- impossible de valider une ventilation `hours` sans coût mensuel lié conforme.

**Aucune génération** d’écriture comptable (`account.move`) ni analytique (`analytic_distribution`) à la validation.

---

## 6. Interface attendue (minimal Palier 2)

| Écran | Description |
|---|---|
| ***(retiré — coûts salariés)*** | Liste / formulaire `glc.employee.cost.line` |
| ***(retiré — ventilations)*** | Liste / formulaire `glc.salary.allocation` + lignes inline |
| **Synthèse mois** | Bandeau : total ventilé vs masse comptable paie |

**Menus proposés** (sous `Facturation → Pilotage GLC`) :

- `*(retiré — coûts salariés)*`
- `*(retiré — ventilations)*`

**Groupe :** Gestionnaire GLC (CRUD) · Utilisateur GLC (lecture seule, option MOA).

---

## 7. Contrôle vs masse salariale comptable

Comparaison **informative** (bandeau / smart button), **non bloquante** — aucun impact sur validation comptable ni sur la validation des ventilations salariales :

```text
Masse salariale comptable du mois =
Somme |balance| des lignes comptes 631*, 633*, 641*, 645* (pièces validées, période)

Total ventilé validé du mois =
Somme allocated_amount des glc.salary.allocation en état validated/locked

Écart % = |masse comptable − total ventilé| / masse comptable × 100
```

**Seuil alerte :** `dorevia_glc_analytics.salary_allocation_variance_pct` (défaut documenté : **5 %** — cf. [MATRICE_MIGRATION.md](./MATRICE_MIGRATION.md) §5).

> La masse comptable est une **lecture agrégée** ; la ventilation est **par salarié**. L’écart est un signal de contrôle, pas une écriture d’ajustement.

---

## 8. Lien Palier 1

| Sujet | Palier 1 | Palier 2 |
|---|---|---|
| Paie avec `analytic_distribution` | Anomalie **A4** | Toujours interdit — pas de contournement |
| `RH_PERSONNEL` post-bascule | Anomalie **A5** | Remplacé par ventilation overlay |
| Applicabilités | `optional` | Inchangées |

Aucune modification du wizard anomalies Palier 1 dans ce ticket, sauf documentation croisée si besoin.

---

## 9. Dépendances techniques

| Dépendance | Motif |
|---|---|
| `account` | Lecture masse salariale comptable (Palier 0) |
| `analytic` | Comptes activités cibles (Palier 0) |
| **`hr`** | `employee_id` → **`hr.employee`** (validé MOA — pas `res.partner`) |

**Nouveau dans `__manifest__.py` :** `"hr"` (validé MOA — module RH installé sur instance GLC).

---

## 10. Sécurité

- `ir.model.access.csv` : droits sur `glc.salary.allocation`, `.line`, `glc.employee.cost.line`
- Données salariales sensibles : accès **Gestionnaire GLC** minimum pour coûts nominatifs
- Rapport CA futur (Palier 4) : **pas de détail nominatif salarié** dans le PDF

---

## 11. Hors périmètre Palier 2

- Écritures comptables ou analytiques automatiques
- Intégration `hr_payroll` / bulletins / **import paie automatique**
- **Timesheets salariés** (`hr_timesheet` ou équivalent) — hors Palier 2
- Registre bénévole (reporté post-cockpit — cf. [PALIERS.md](./PALIERS.md))
- Contrôle de gestion (Palier 4)
- Rapport CA / coût complet affiché (Palier 4 — consomme les données Palier 2)
- Clôture analytique mensuelle (reportée post-cockpit)
- Reclassement rétroactif massif des écritures paie historiques
- Passage applicabilités en `mandatory`
- Fichiers hors périmètre CK MarketOne

---

## 12. Critères d’acceptation

| ID | Critère |
|---|---|
| CA1 | Menus Coûts salariés / Ventilations visibles pour Gestionnaire GLC |
| CA2 | Création `glc.employee.cost.line` avec coût horaire calculé |
| CA3 | Ventilation `percent` — total 100 % → validation possible |
| CA4 | Ventilation `percent` — total ≠ 100 % → validation refusée (partiel OK en brouillon) |
| CA5 | Ventilation `hours` — `reference_hours` > 0 · montants = heures × coût horaire · validation si total heures = référence |
| CA6 | Activité Financements refusée sur ligne de ventilation |
| CA7 | Bandeau écart masse comptable vs total ventilé (seuil 5 %) — **informatif, non bloquant** |
| CA8 | Aucune écriture comptable / analytique paie générée · tests auto verts |
| CA9 | Non-régression Palier 0 + Palier 1 (17 tests anomalies) |

---

## 13. Documentation attendue

- [ ] Mettre à jour [PALIERS.md](./PALIERS.md)
- [ ] [RECETTE_MANUELLE_PALIER_2.md](./RECETTE_MANUELLE_PALIER_2.md)
- [ ] Croiser [REGLES_AFFECTATION.md](./REGLES_AFFECTATION.md) § paie / ventilation
- [ ] Croiser [MATRICE_MIGRATION.md](./MATRICE_MIGRATION.md) § `RH_PERSONNEL`

---

## 14. Règle de livraison

```text
Branche : feat/glc-analytique-palier-2
Base    : main (post merge PR #25)

Ne pas mélanger avec :
- Palier 1 (gelé)
- Palier 3+ (tickets séparés)
```

**Séquence :**

1. ~~Validation MOA du présent cadrage~~ — **GO MOA 2026-05-27**
2. Développement Palier 2 sur branche dédiée
3. Recette MOA sur `glc-rgl-test-import`
4. Merge PR Palier 2

---

## 15. Décisions MOA gelées (cadrage validé)

| # | Décision |
|---|---|
| D1 | **Doctrine** — pas d’écriture comptable, pas d’écriture analytique de paie, overlay de gestion uniquement |
| D2 | **Applicabilités** — restent `optional`, aucun `mandatory` |
| D3 | **Salarié** — porté par `hr.employee`, pas `res.partner` · dépendance `hr` validée |
| D4 | **`reference_hours`** — obligatoire et **> 0** pour toute ventilation en méthode `hours` |
| D5 | **Méthode `percent`** — validation uniquement si total = **100 %** |
| D6 | **Méthode `hours`** — validation uniquement si total heures = **heures de référence** |
| D7 | **Ventilation partielle** — autorisée en brouillon, **refusée à la validation** |
| D8 | **Masse salariale comptable** — contrôle **informatif, non bloquant** |
| D9 | **Aucune génération** d’écriture comptable ou analytique à la validation |

### Points ouverts (non bloquants Palier 2)

- Définition exacte du coût mensuel chargé avec la paie GLC (brut + charges + AN).
- Périmètre fin des comptes `631/633/641/645` sur le plan comptable GLC.
- Première ventilation rétroactive mois pilote : calibrage vs officiel (cf. matrice migration).

---

## Annexe — activités cibles ventilation

| Code | Libellé |
|---|---|
| `STRUCTURE` | Structure & Administration |
| `BAR` | Bar, Restauration & Cuisine |
| `PRESTATIONS` | Prestations & Animations |
| `RESIDENCES` | Résidences artistiques |
| `MISSIONS` | Déplacements & Missions |
| `PRIVATISATIONS` | Privatisation d'espace |
| `LOCATION_RADIO` | Location Radio Grand Lieu |
