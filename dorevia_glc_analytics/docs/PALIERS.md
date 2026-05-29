# Découpage en paliers — GLC Analytics & Budget

**Version :** V1.1 (référence fonctionnelle) + cadrage Budget / Cockpit (2026-05-27)  
**Doctrine de livraison :** la spec V1.1 reste le document cible ; le développement avance par paliers installables.

> GLC pilote ses activités avec deux axes : **ce que l'association fait**, et **ce qui finance ce qu'elle fait**.  
> Après le Palier 2, la priorité MOA est un **cockpit de soutenabilité économique** (couverture des salaires).

**Cadrage détaillé :** [CADRAGE_BUDGET_COCKPIT.md](./CADRAGE_BUDGET_COCKPIT.md)  
**Release note jalon :** [RELEASE_NOTE_GLC_ANALYTICS_BUDGET_PALIERS_0_4.md](./RELEASE_NOTE_GLC_ANALYTICS_BUDGET_PALIERS_0_4.md)

---

## Vue d'ensemble

| Palier | Module | Objectif | Statut |
|---|---|---|---|
| **0** | `dorevia_glc_analytics` | Socle analytique installable | **Validé MOA · gelé** |
| **1** | `dorevia_glc_analytics` | Règles d'affectation et contrôles | **Validé MOA · gelé** · [PR #25](https://github.com/doreviateam/odoo19-addons-dorevia/pull/25) |
| **2** | `dorevia_glc_analytics` | Ventilation salariale | **Validé MOA · gelé** · [PR #26](https://github.com/doreviateam/odoo19-addons-dorevia/pull/26) |
| **3** | `dorevia_glc_budget` | Budget prévisionnel mensuel par axe analytique | **Validé MOA** (2026-05-27 · `glc-rgl-test-import`) · [PR #28](https://github.com/doreviateam/odoo19-addons-dorevia/pull/28) |
| **4** | `dorevia_glc_analytics` (+ budget) | Cockpit pilotage d'exploitation GLC | **GO livraison MOA · gelé** · **`19.0.4.9.0`** · [TICKET réalignement](./TICKET_COCKPIT_REALIGNEMENT_CONTROLE_GESTION.md) |
| **4bis** | `dorevia_glc_analytics` | Finition UX cockpit + période libre + UX-GROUPBY | **Intégré Palier 4 réaligné** (`19.0.4.9.0`) · [TICKET_PALIER_4BIS.md](./TICKET_PALIER_4BIS.md) |
| **5** | extensions | Trésorerie · exports · scénarios | **GO complet MOA** · lot trésorerie **`19.0.5.0.1`** (2026-05-29) · [TICKET_PALIER_5](./TICKET_PALIER_5_TRESORERIE_COMPTE_BANCAIRE_REFERENCE.md) |
| **5bis** | `dorevia_glc_analytics` | Qualité comptable · analytique · suivi paiement (GQ-6) | **GO MOA · mergé** · **`19.0.7.0.2`** · [PR #45](https://github.com/doreviateam/odoo19-addons-dorevia/pull/45) |
| **5ter** | `dorevia_glc_analytics` | Nomenclature plan analytique unique | **`19.0.8.0.0`** · [ETAT_NOMENCLATURE_ANALYTIQUE.md](./ETAT_NOMENCLATURE_ANALYTIQUE.md) |

### Paliers V1.1 reportés (post-cockpit)

Éléments de la [spec V1.1](./README.md) repoussés après Budget / Cockpit :

| Sujet | Référence spec | Statut |
|---|---|---|
| Registre bénévole | §7.3, §9.3 | Reporté |
| Rapport CA mensuel PDF | §11 | Partiellement couvert par Palier 4 |
| Clôture analytique mensuelle | §8.7 | Reporté |

---

## Palier 0 — Socle analytique installable

**Ticket :** Installer le socle analytique GLC : plans, comptes, sécurité minimale, documentation et tests.  
**Statut :** **Gelé MOA**

### Livrables

- Plan analytique **`GLC - Activités`** unique (**11 axes** : activités + financements)
- ~~Plan analytique `GLC - Financements`~~ → archivé depuis **`19.0.8.0.0`** · voir [ETAT_NOMENCLATURE_ANALYTIQUE.md](./ETAT_NOMENCLATURE_ANALYTIQUE.md)
- Extension légère `account.analytic.account` (type, ordre, rapport)
- Groupes de sécurité de base (`Utilisateur GLC`, `Gestionnaire GLC`)
- Applicabilités Odoo 19 **non bloquantes** (`optional`)
- Tests d'installation et de nomenclature
- [Recette manuelle Palier 0](./RECETTE_MANUELLE_PALIER_0.md)

---

## Palier 1 — Règles d'affectation et contrôles

**Ticket :** [TICKET_PALIER_1.md](./TICKET_PALIER_1.md)  
**Recette :** [RECETTE_MANUELLE_PALIER_1.md](./RECETTE_MANUELLE_PALIER_1.md)  
**Statut :** **Gelé MOA**

### Livrables

- Wizard + liste **Anomalies analytiques GLC**
- Contrôles A1–A6
- Paramètres : date de bascule, seuil STRUCTURE
- Tests automatisés — **non bloquant**

---

## Palier 2 — Ventilation salariale

**Ticket :** [TICKET_PALIER_2.md](./TICKET_PALIER_2.md)  
**Recette :** [RECETTE_MANUELLE_PALIER_2.md](./RECETTE_MANUELLE_PALIER_2.md)  
**Statut :** **Gelé MOA** (2026-05-27 · `glc-rgl-test-import` · version `19.0.3.0.0`)

### Livrables

- `glc.salary.allocation` + lignes
- `glc.employee.cost.line`
- Ventilation `percent` / `hours`
- Bandeau écart masse comptable (informatif)
- **Pas d'écriture comptable ni analytique**

**Règle gelée :** overlay de gestion uniquement.

---

## Palier 3 — Budget prévisionnel GLC

**Module :** `dorevia_glc_budget` *(nouveau — pas OCA Budget)*  
**Ticket :** [TICKET_PALIER_3.md](./TICKET_PALIER_3.md)

### Objectif

Saisir une trajectoire prévisionnelle simple, **mois par mois**, par axe analytique GLC, en préparation du cockpit Palier 4.

### Livrables

- `glc.budget` — en-tête (année, société, scénario, statut)
- `glc.budget.line` — lignes mensuelles (axe analytique, type recette/charge/financement, montant)
- Workflow brouillon / validé / archivé
- Tests automatisés + recette MOA

### Règles gelées proposées

- aucune écriture comptable ;
- aucune écriture analytique ;
- comptes Financements autorisés pour lignes `funding` ;
- module léger, séparé de `dorevia_glc_analytics`.

---

## Palier 4 — Cockpit pilotage d'exploitation GLC

**Ticket :** [TICKET_PALIER_4.md](./TICKET_PALIER_4.md) · [TICKET_COCKPIT_REALIGNEMENT_CONTROLE_GESTION.md](./TICKET_COCKPIT_REALIGNEMENT_CONTROLE_GESTION.md)  
**Recette :** [RECETTE_MANUELLE_PALIER_4.md](./RECETTE_MANUELLE_PALIER_4.md) · [Recette période libre](./recette/RECETTE_MANUELLE_COCKPIT_GLC_PERIODE_LIBRE.md)  
**Statut :** **GO livraison MOA · gelé** (2026-05-28) · **`19.0.4.9.0`** — grammaire Recette · Cumul RH · Dépense · Solde

### Objectif

Tableau de bord **Activité × Mois × Produits / Charges / Solde** avec :

```text
Couverture des salaires
Couverture salaires + frais généraux
Écart prévu / réalisé
Alerte de gestion (rouge / orange / vert)
```

### Sources

| Donnée | Source |
|---|---|
| Réalisé | `account.analytic.line` |
| Prévisionnel | `glc.budget.line` |

---

## Palier 5 — Enrichissements de pilotage

Hors périmètre immédiat Palier 4 :

- graphiques avancés ;
- export Excel / PDF ;
- commentaires de gestion ;
- comparaison budget initial / révisé / atterrissage ;
- scénarios multiples ;
- projections fin d'année ;
- **bloc trésorerie** — compte bancaire de référence (défaut GLC : compte courant), lecture entrées / sorties / virements internes depuis le POV du compte observé ;
- intégration OCA Budget si besoin futur.

**Doctrine trésorerie figée MOA (2026-05-28) :** triple lecture — compte bancaire de référence (POV trésorerie) · compte comptable (nature) · compte analytique (qualification métier). Virements internes visibles en trésorerie, exclus des KPI exploitation.

> **Invariant Palier 5 :** un cockpit = période + compte bancaire de référence + lecture trésorerie séparée. Les KPI exploitation ne changent jamais quand on change de compte bancaire.

**Ticket cadrage :** [TICKET_PALIER_5_TRESORERIE_COMPTE_BANCAIRE_REFERENCE.md](./TICKET_PALIER_5_TRESORERIE_COMPTE_BANCAIRE_REFERENCE.md) · **Doctrine :** [TICKET_COCKPIT_COMPTE_BANCAIRE_REFERENCE.md](./TICKET_COCKPIT_COMPTE_BANCAIRE_REFERENCE.md) · **Recette :** [RECETTE_MANUELLE_PALIER_5_TRESORERIE_COMPTE_BANCAIRE_REFERENCE.md](./recette/RECETTE_MANUELLE_PALIER_5_TRESORERIE_COMPTE_BANCAIRE_REFERENCE.md)

**Lot trésorerie livré `19.0.5.0.1` (2026-05-29) :** compte bancaire de référence · param société · onglet Trésorerie S1 · tests TREF **7/7** · rejeu cockpit+budget **70/70** · post-install **95/95** · migration nomenclature Activités GLC legacy · recette navigateur §2 à §5 **OK**.

**Preuve MOA finale :** sur `13 avr. → 31 mai 2026`, `Compte Courant GLC` et `GLC - Livret Bleu` conservent les KPI exploitation identiques (Recette `7 794,00 €` · Cumul RH `0,00 €` · Dépense `4 851,51 €` · Solde `2 942,49 €`) tandis que le solde trésorerie change selon le compte observé (`-1 627,11 €` vs `30 000,00 €`).

**Reste Palier 5 (non livré) :** exports Excel/PDF · scénarios budget · projections · commentaires de gestion.

---

## Décision de cadrage MOA (2026-05-27)

Après validation du Palier 2 :

- **Palier 3** : module `dorevia_glc_budget` — prévisionnel mensuel simple.
- **Palier 4** : cockpit couverture des salaires — réalisé vs budget vs alertes.
- **Palier 5** : enrichissements (exports, scénarios, trésorerie).

Le module **`dorevia_glc_analytics`** reste le socle du réalisé analytique, des coûts salariés et des ventilations salariales.

---

## Décisions d'architecture validées

| Sujet | Décision |
|---|---|
| Modèle activité | Réutiliser `account.analytic.account` |
| Plans analytiques | `GLC - Activités` et `GLC - Financements` |
| Compte comptable | = nature juridique/comptable |
| Compte analytique | = activité / destination métier |
| Compte bancaire de référence | = point de vue trésorerie cockpit (défaut GLC : compte courant) — [TICKET_COCKPIT_COMPTE_BANCAIRE_REFERENCE.md](./TICKET_COCKPIT_COMPTE_BANCAIRE_REFERENCE.md) |
| Flux bilan | N'alimentent pas l'analytique d'exploitation |
| Budget GLC | Module séparé `dorevia_glc_budget`, pas OCA Budget |
| Ventilation salariale | Overlay — pas d'écriture paie analytique |
| Applicabilités | `optional` par défaut — pas de `mandatory` sans décision MOA |

---

## Migration — doctrine

Cf. [MATRICE_MIGRATION.md](./MATRICE_MIGRATION.md) :

1. Inventorier les 9 comptes actuels (Phase 0 métier)
2. Date de bascule + mois pilote non officiel
3. `RH_PERSONNEL` → ventilation salariale Palier 2, pas de solde migré
4. Premier cockpit officiel après validation budget + réalisé mois pilote

---

## Structure modules (vision)

```text
dorevia_glc_analytics/          # Paliers 0–2 · cockpit Palier 4
├── data/
├── security/
├── models/
│   ├── account_analytic_account.py
│   ├── glc_salary_allocation.py
│   └── glc_* (cockpit Palier 4)
├── views/
├── wizard/                     # Palier 1 (anomalies)
└── tests/

dorevia_glc_budget/             # Palier 3
├── models/
│   ├── glc_budget.py
│   └── glc_budget_line.py
├── views/
├── security/
└── tests/
```

**Prochaine livraison = commit Palier 5 trésorerie `19.0.5.0.1`** (GO technique MOA 2026-05-29 · **95/95**) · puis exports / scénarios Palier 5 élargi.
