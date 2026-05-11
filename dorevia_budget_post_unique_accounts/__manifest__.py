# -*- coding: utf-8 -*-
{
    "name": "Dorevia — Unicité des comptes sur les postes budgétaires",
    "version": "19.0.1.0.0",
    "category": "Accounting",
    "summary": "Un compte ne peut être lié qu’à un seul poste budgétaire actif par société.",
    "description": """
Chaque compte comptable ne peut appartenir qu’à un seul poste budgétaire **actif**
(`account.budget.post`) pour une même société. Les postes archivés libèrent les comptes
pour une réaffectation.
""",
    "author": "Dorevia",
    "license": "LGPL-3",
    "depends": ["base_account_budget"],
    "data": [
        "views/account_budget_post_views.xml",
    ],
    "installable": True,
    "application": False,
}
