# -*- coding: utf-8 -*-
{
    "name": "Dorevia Cash Simulation — Achats",
    "version": "19.0.1.1.0",
    "category": "Accounting",
    "author": "Dorevia",
    "summary": "Simulation de trésorerie à partir de demandes de prix / commandes achat.",
    "description": """
Extension optionnelle de dorevia_cash_simulation permettant d'intégrer
des demandes de prix et commandes d'achat fournisseur comme hypothèses
de décaissement dans la projection Cash Guard, sans créer de facture
ni d'écriture comptable.
    """,
    "depends": [
        "purchase",
        "dorevia_cash_simulation",
    ],
    "data": [
        "views/purchase_order_views.xml",
        "views/cash_guard_views.xml",
    ],
    "installable": True,
    "auto_install": False,
    "license": "LGPL-3",
}
