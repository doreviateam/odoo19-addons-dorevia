# -*- coding: utf-8 -*-
{
    "name": "Dorevia Cash Flow",
    "version": "19.0.2.3.14",
    "category": "Accounting",
    "summary": "Trajectoire de trésorerie : restitution graphique à partir des projections Cash Guard.",
    "description": """
Lecture graphique de la trajectoire de trésorerie (constaté + projeté 90 j)
à partir des données déjà calculées par Dorevia Cash Guard.
Voir README.md et docs/SPEC_CASH_FLOW_TRAJECTORY.md ; ticket V1.1 : docs/TICKET_CASH_FLOW_V1_1_TRAJECTOIRE_REFERENCE.md.
""",
    "author": "Dorevia",
    "license": "LGPL-3",
    "depends": [
        "account",
        "dorevia_cash_guard",
        "web",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/cash_flow_trajectory_views.xml",
        "views/menus.xml",
        "views/cash_guard_bridge_menus.xml",
    ],
    "assets": {
        "web.assets_backend": [
            "dorevia_cash_flow/static/src/trajectory_chart/trajectory_chart_action.xml",
            "dorevia_cash_flow/static/src/trajectory_chart/trajectory_chart_action.js",
        ],
    },
    "installable": True,
    "application": False,
}
