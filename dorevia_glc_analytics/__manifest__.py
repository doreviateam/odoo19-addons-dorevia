# -*- coding: utf-8 -*-
{
    "name": "Dorevia GLC Analytics",
    "version": "19.0.4.1.0",
    "category": "Accounting/Accounting",
    "summary": "Socle analytique GLC — plans Activités et Financements.",
    "description": """
Suivi d'activité GLC
====================

Palier 0 — Socle analytique :

* plan **GLC - Activités** (7 comptes pilotables) ;
* plan **GLC - Financements** (4 sources de ressources) ;
* champs métier sur les comptes analytiques ;
* groupes de sécurité de base.

Palier 1 — Contrôles non bloquants :

* assistant **Anomalies analytiques GLC** (contrôles A1–A6) ;
* mapping explicite pour le contrôle A3 ;
* synthèse poids STRUCTURE (bandeau, pas ligne à ligne).

Palier 2 — Ventilation salariale :

* coûts salariés mensuels (`glc.employee.cost.line`) ;
* ventilations par activité (`glc.salary.allocation`) ;
* overlay de gestion — pas d'écriture comptable ni analytique paie.

Palier 4 — Cockpit couverture des salaires :

* agrégation réalisé analytique + ventilations Palier 2 + budget Palier 3 ;
* alertes rouge / orange / vert ;
* détail Activité × Mois.

Palier 4bis — Finition UX cockpit (wording MOA, présentation GLC).

Les paliers suivants (bénévolat, rapport CA) seront ajoutés progressivement.
Voir docs/PALIERS.md.
""",
    "author": "Dorevia",
    "license": "LGPL-3",
    "depends": [
        "account",
        "analytic",
        "hr",
    ],
    "data": [
        "security/glc_security.xml",
        "security/ir.model.access.csv",
        "data/analytic_plan_data.xml",
        "data/analytic_account_data.xml",
        "data/ir_config_parameter_data.xml",
        "views/account_analytic_account_views.xml",
        "views/glc_account_funding_rule_views.xml",
        "views/glc_analytic_anomaly_views.xml",
        "views/glc_employee_cost_line_views.xml",
        "views/glc_salary_allocation_views.xml",
        "views/glc_coverage_cockpit_views.xml",
        "views/glc_menus.xml",
    ],
    "installable": True,
    "application": False,
    "pre_init_hook": "pre_init_hook",
}
