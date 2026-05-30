# -*- coding: utf-8 -*-
{
    "name": "Dorevia GLC Analytics",
    "version": "19.0.14.2.0",
    "category": "Accounting/Accounting",
    "summary": "Pilotage GLC — contrôle de gestion sur réalisé analytique.",
    "description": """
Suivi d'activité GLC
====================

Navigation : Facturation → Pilotage GLC

* **Contrôle de gestion** — réalisé comptable (Ressources · Cumul RH · Dépenses · Solde) ;
* **Axes analytiques** — paramétrage plan GLC (11 axes) ;
* **Audit** — contrôles analytiques A1–A2, A4–A6.

Socle :

* plan **GLC - Activités** unique ;
* trésorerie cockpit (compte bancaire de référence) ;
* qualité comptable & suivi paiement (GQ-6).

Documentation à jour : docs/ETAT_MODULE_ACTUEL.md · docs/PALIERS.md
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
