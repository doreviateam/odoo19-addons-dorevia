# -*- coding: utf-8 -*-
{
    "name": "Dorevia GLC Analytique",
    "version": "19.0.1.0.0",
    "category": "Accounting/Accounting",
    "summary": "Socle analytique GLC — plans Activités et Financements.",
    "description": """
Palier 0 — Suivi d'activité GLC
================================

Installe la nomenclature analytique de pilotage pour l'association GLC :

* plan **GLC - Activités** (7 comptes pilotables) ;
* plan **GLC - Financements** (4 sources de ressources) ;
* champs métier sur les comptes analytiques ;
* groupes de sécurité de base.

Les paliers suivants (ventilation salariale, bénévolat, rapport CA) seront
ajoutés progressivement. Voir docs/PALIERS.md.
""",
    "author": "Dorevia",
    "license": "LGPL-3",
    "depends": [
        "account",
        "analytic",
    ],
    "data": [
        "security/glc_security.xml",
        "data/analytic_plan_data.xml",
        "data/analytic_account_data.xml",
        "views/account_analytic_account_views.xml",
        "views/glc_menus.xml",
    ],
    "installable": True,
    "application": False,
}
