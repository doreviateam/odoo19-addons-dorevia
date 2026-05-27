# -*- coding: utf-8 -*-
{
    "name": "Dorevia GLC Budget",
    "version": "19.0.1.0.0",
    "category": "Accounting/Accounting",
    "summary": "Budget prévisionnel GLC — saisie mensuelle par axe analytique.",
    "description": """
Budget prévisionnel GLC — Palier 3
==================================

* en-têtes de budget annuel par société et scénario ;
* lignes mensuelles par compte analytique GLC ;
* types recette / charge / financement ;
* overlay de gestion — aucune écriture comptable ni analytique.

Consommé ultérieurement par le cockpit Palier 4.
Voir dorevia_glc_analytics/docs/TICKET_PALIER_3.md.
""",
    "author": "Dorevia",
    "license": "LGPL-3",
    "depends": [
        "dorevia_glc_analytics",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/glc_budget_views.xml",
        "views/glc_budget_menus.xml",
    ],
    "installable": True,
    "application": False,
}
