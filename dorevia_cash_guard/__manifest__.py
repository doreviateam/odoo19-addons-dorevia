# -*- coding: utf-8 -*-
{
    "name": "Dorevia Cash Guard",
    "version": "19.0.5.0.2",
    "category": "Accounting",
    "summary": "Projection de trésorerie à partir du constat et des factures ouvertes.",
    "description": """
Cash Guard visualise la projection de trésorerie à partir de la trésorerie constatée et des
factures ouvertes déjà engagées dans Odoo (pièces postées, résidu à l’échéance).

Périmètre actuel : projection — pas une prévision métier complète (budget, récurrences,
simulations avancées : évolutions ultérieures).

Fonctions principales :
- document de projection sur une période ;
- flux complémentaires (saisie manuelle / simulation) ;
- soldes et statut de vigilance (safe / warning / risk).
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
