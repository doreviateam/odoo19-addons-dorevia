# -*- coding: utf-8 -*-
{
    "name": "Dorevia GLC Analytics",
    "version": "19.0.4.9.0",
    "category": "Accounting/Accounting",
    "summary": "Socle analytique GLC — cockpit pilotage d'exploitation.",
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
* overlay de gestion — pas d'écriture comptable ni analytique paie ;
* rôle **contrôle / comparaison RH** vis-à-vis du cockpit (pas source du réalisé).

Palier 4 — Cockpit pilotage d'exploitation GLC :

* réalisé = écritures comptables analytiques (classes 6/7, tous axes exploitables) ;
* budget Palier 3 = comparaison prévisionnelle (périmètre partiel — voir ticket réalignement) ;
* synthèse graphique + détail par axe analytique (Recette · Cumul RH · Dépense · Solde) ;
* alertes couverture masse salariale (héritage Palier 4).

Palier 4bis — Finition UX cockpit (wording MOA, tableau de bord).

Doctrine et évolutions : docs/TICKET_COCKPIT_REALIGNEMENT_CONTROLE_GESTION.md

Les paliers suivants (bénévolat, rapport CA) seront ajoutés progressivement.
Voir docs/PALIERS.md.
""",
    "author": "Dorevia",
    "license": "LGPL-3",
    "depends": [
        "web",
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
        "data/glc_coverage_cockpit_cron.xml",
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
    "assets": {
        "web.assets_backend": [
            "dorevia_glc_analytics/static/src/js/glc_coverage_cockpit_form_view.esm.js",
            "dorevia_glc_analytics/static/src/js/glc_coverage_detail_widget.esm.js",
            "dorevia_glc_analytics/static/src/js/glc_coverage_synthesis_widget.esm.js",
            "dorevia_glc_analytics/static/src/xml/glc_coverage_detail_widget.xml",
            "dorevia_glc_analytics/static/src/xml/glc_coverage_synthesis_widget.xml",
            "dorevia_glc_analytics/static/src/scss/glc_coverage_detail_widget.scss",
            "dorevia_glc_analytics/static/src/scss/glc_coverage_synthesis_widget.scss",
        ],
    },
}
