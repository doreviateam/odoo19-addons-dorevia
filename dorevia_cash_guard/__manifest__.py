# -*- coding: utf-8 -*-
{
    "name": "Dorevia Cash Guard",
    "version": "19.0.5.6.2",
    "category": "Accounting",
    "summary": "Projection de trésorerie : constat + factures ouvertes engagées.",
    "description": """
Cash Guard mesure l'impact des entrées et sorties de cash engagées sur la trésorerie
afin d'anticiper les mesures nécessaires.

Doctrine : trésorerie constatée ± flux engagés (factures ouvertes) = projection.

Fonctions principales :
- document de projection sur une période ;
- suivi de trésorerie (constaté / situation / projeté) ;
- détail projection : pièces expliquant les tensions ;
- statut par période (confort / vigilance / tension / risque) ;
- flux complémentaires (saisie manuelle / simulation, optionnel).
""",
    "author": "Dorevia",
    "license": "LGPL-3",
    "depends": [
        "account",
        "base_account_budget",
        "base_accounting_kit",
        "dorevia_budget_post_unique_accounts",
        "mail",
        "web",
    ],
    "data": [
        "security/dorevia_cash_guard_security.xml",
        "security/ir.model.access.csv",
        "data/sequence.xml",
        "data/cash_guard_cron.xml",
        "views/cash_guard_views.xml",
        "views/menus.xml",
    ],
    "installable": True,
    "application": False,
    "assets": {
        "web.assets_backend": [
            "dorevia_cash_guard/static/src/js/cash_guard_form_controller.esm.js",
        ],
    },
}
