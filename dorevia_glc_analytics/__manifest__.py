# -*- coding: utf-8 -*-
{
    "name": "Dorevia GLC Analytics",
    "version": "19.0.13.0.0",
    "category": "Accounting/Accounting",
    "summary": "Socle analytique GLC — cockpit pilotage d'exploitation.",
    "description": """
Suivi d'activité GLC
====================

Palier 0 — Socle analytique :

* plan **GLC - Activités** unique (11 axes : activités + financements) ;
* champs métier sur les comptes analytiques ;
* groupes de sécurité de base.

Palier 1 — Contrôles non bloquants :

* assistant **Anomalies analytiques GLC** (contrôles A1–A2, A4–A6) ;
* synthèse poids STRUCTURE (bandeau, pas ligne à ligne).

Palier 4 — Cockpit pilotage d'exploitation GLC :

* réalisé = écritures comptables analytiques (classes 6/7, tous axes exploitables) ;
* synthèse graphique + détail par axe analytique (Ressources · Cumul RH · Dépenses · Solde) ;
* alertes couverture masse salariale (héritage Palier 4).

Palier 4bis — Finition UX cockpit (wording MOA, tableau de bord).

Palier 5 — Trésorerie cockpit (compte bancaire de référence, lecture séparée).

Lot GQ-6 — Qualité comptable & suivi paiement (onglets Contrôles qualité · Tiers & paiements).

Doctrine et évolutions : docs/TICKET_PALIER_5_TRESORERIE_COMPTE_BANCAIRE_REFERENCE.md

Les paliers suivants (bénévolat, rapport CA) seront ajoutés progressivement.
Voir docs/PALIERS.md.
""",
    "author": "Dorevia",
    "license": "LGPL-3",
    "depends": [
        "web",
        "account",
        "analytic",
    ],
    "data": [
        "security/glc_security.xml",
        "security/ir.model.access.csv",
        "data/analytic_plan_data.xml",
        "data/analytic_account_data.xml",
        "data/ir_config_parameter_data.xml",
        "data/glc_coverage_cockpit_cron.xml",
        "views/account_analytic_account_views.xml",
        "views/glc_analytic_anomaly_views.xml",
        "views/res_company_views.xml",
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
