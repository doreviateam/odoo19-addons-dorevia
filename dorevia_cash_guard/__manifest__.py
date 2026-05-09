# -*- coding: utf-8 -*-
{
    "name": "Dorevia Cash Guard",
    "version": "19.0.1.0.0",
    "category": "Accounting",
    "summary": "Projection et garde-fou de tresorerie.",
    "description": """
Module de securite tresorerie pour Odoo 19 CE.

Fonctions principales:
- point de tresorerie sur periode;
- flux previsionnels et simules;
- calcul du solde initial, final et minimum;
- statut de risque safe/warning/risk.
""",
    "author": "Dorevia",
    "license": "LGPL-3",
    "depends": ["account", "base_account_budget", "mail"],
    "data": [
        "security/ir.model.access.csv",
        "data/sequence.xml",
        "views/cash_guard_views.xml",
        "views/menus.xml",
    ],
    "installable": True,
    "application": False,
}
