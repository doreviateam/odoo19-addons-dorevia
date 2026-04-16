# -*- coding: utf-8 -*-
{
    "name": "Dorevia — connecteur Vault (V1)",
    "version": "19.0.1.0.2",
    "category": "Accounting/Accounting",
    "summary": "Envoi minimal des factures client postées vers une cible HTTP (chaîne source locale).",
    "author": "Dorevia",
    "depends": ["base", "account"],
    "data": [
        "data/ir_config_parameter.xml",
        "views/res_config_settings_views.xml",
        "views/account_move_views.xml",
        "views/account_payment_views.xml",
    ],
    "installable": True,
    "application": False,
    "license": "LGPL-3",
}
