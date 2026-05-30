# Découpage en paliers — GLC Analytics

**Version module de référence :** **`19.0.14.1.0`**  
**État actuel :** [ETAT_MODULE_ACTUEL.md](./ETAT_MODULE_ACTUEL.md)  
**Release simplification :** [RELEASE_NOTE_19.0.14_SIMPLIFICATION_PILOTAGE.md](./RELEASE_NOTE_19.0.14_SIMPLIFICATION_PILOTAGE.md)

> La [spec V1.1](./README.md) reste le document cible long terme.  
> Le produit installé a été **simplifié en mai 2026** : réalisé analytique seul, sans overlay budget ni ventilation salariale.

---

## Vue d'ensemble

| Palier | Module | Objectif | Statut **aujourd'hui** |
|---|---|---|---|
| **0** | `dorevia_glc_analytics` | Socle analytique installable | **Actif** |
| **1** | `dorevia_glc_analytics` | Audit analytique (A1–A2, A4–A6) | **Actif** — menu **Audit** |
| **2** | `dorevia_glc_analytics` | Ventilation salariale overlay | **Retiré** `19.0.13.0.0` · [archive](./TICKET_PALIER_2.md) |
| **3** | ~~`dorevia_glc_budget`~~ | Budget prévisionnel mensuel | **Retiré** `19.0.14.0.0` · [archive](./TICKET_PALIER_3.md) |
| **4** | `dorevia_glc_analytics` | Contrôle de gestion (ex cockpit) | **Actif** — réalisé seul |
| **4bis** | `dorevia_glc_analytics` | UX cockpit · période libre · group_by | **Intégré** |
| **5** | `dorevia_glc_analytics` | Trésorerie · compte bancaire référence | **Actif** `19.0.5.0.1+` |
| **5bis** | `dorevia_glc_analytics` | Qualité comptable · suivi paiement (GQ-6) | **Actif** `19.0.7.0.2+` |
| **5ter** | `dorevia_glc_analytics` | Plan analytique unique (11 axes) | **Actif** `19.0.8.0.0+` |

---

## Palier 0 — Socle analytique

**Statut :** actif · gelé fonctionnellement

- Plan **`GLC - Activités`** — 11 axes (activités + financements)
- Extension `account.analytic.account` (type GLC, ordre, rapport)
- Groupes `Utilisateur GLC` / `Gestionnaire GLC`
- [Recette Palier 0](./RECETTE_MANUELLE_PALIER_0.md)

---

## Palier 1 — Audit analytique

**Statut :** actif · menu **Audit**

- Assistant période + liste anomalies
- Contrôles A1, A2, A4, A5, A6 (A3 financement retiré `19.0.13.0.0`)
- [Ticket Palier 1](./TICKET_PALIER_1.md) · [Recette Palier 1](./RECETTE_MANUELLE_PALIER_1.md)

---

## Palier 2 — Ventilation salariale *(retiré)*

**Statut :** **retiré** — PR #50 · `19.0.13.0.0`

Modèles supprimés : `glc.employee.cost.line`, `glc.salary.allocation`, `glc.salary.allocation.line`.

Documentation conservée à titre historique : [TICKET_PALIER_2.md](./TICKET_PALIER_2.md)

---

## Palier 3 — Budget prévisionnel *(retiré)*

**Statut :** **retiré** — PR #51 · module `dorevia_glc_budget` supprimé du dépôt

Documentation conservée : [TICKET_PALIER_3.md](./TICKET_PALIER_3.md)

---

## Palier 4 — Contrôle de gestion

**Statut :** actif · menu **Contrôle de gestion**

### Doctrine

| Indicateur | Source |
|---|---|
| Ressources | Analytique classe 7 |
| Cumul RH | Analytique paie classe 6 |
| Dépenses | Analytique charges classe 6 hors paie |
| Solde | `Ressources − Cumul RH − Dépenses` |

### Références

- [TICKET_COCKPIT_REALIGNEMENT_CONTROLE_GESTION.md](./TICKET_COCKPIT_REALIGNEMENT_CONTROLE_GESTION.md)
- [TICKET_COCKPIT_SOURCE_REALISE.md](./TICKET_COCKPIT_SOURCE_REALISE.md)
- [Recette période libre](./recette/RECETTE_MANUELLE_COCKPIT_GLC_PERIODE_LIBRE.md)

---

## Palier 5 — Trésorerie & enrichissements

**Livré :** compte bancaire de référence · onglet Trésorerie · KPI exploitation indépendants du compte observé.

**Non livré / reporté :** exports Excel/PDF · scénarios · bénévolat · rapport CA PDF.

- [TICKET_PALIER_5_TRESORERIE_COMPTE_BANCAIRE_REFERENCE.md](./TICKET_PALIER_5_TRESORERIE_COMPTE_BANCAIRE_REFERENCE.md)

---

## Structure module (actuelle)

```text
dorevia_glc_analytics/
├── models/
│   ├── account_analytic_account.py
│   ├── glc_analytic_anomaly_*.py
│   ├── glc_coverage_cockpit.py      # Contrôle de gestion
│   └── glc_coverage_cockpit_quality.py
├── views/
│   └── glc_menus.xml                # Pilotage GLC
├── static/src/js/                   # widgets synthèse + détail
└── tests/
```

---

## Paliers V1.1 reportés

| Sujet | Statut |
|---|---|
| Registre bénévole | Reporté |
| Rapport CA mensuel PDF | Reporté |
| Clôture analytique mensuelle | Reporté |
