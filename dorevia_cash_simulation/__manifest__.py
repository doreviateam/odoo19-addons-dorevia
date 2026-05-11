# -*- coding: utf-8 -*-
{
    "name": "Dorevia Cash Simulation",
    "version": "19.0.1.0.0",
    "category": "Accounting",
    "author": "Dorevia",
    "summary": "Simulation de trésorerie à partir de devis clients.",
    "description": """
Extension optionnelle de dorevia_cash_guard permettant d'intégrer
des devis clients comme hypothèses d'encaissement dans la projection
de trésorerie, sans les confondre avec les flux réels.
    """,
    "depends": [
        "sale_management",
        "dorevia_cash_guard",
    ],
    "data": [
        "views/sale_order_views.xml",
        "views/cash_guard_views.xml",
    ],
    "installable": True,
    "auto_install": False,
    "license": "LGPL-3",
}
