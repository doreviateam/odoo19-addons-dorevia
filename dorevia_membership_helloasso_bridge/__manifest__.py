# -*- coding: utf-8 -*-
{
    "name": "Dorevia — Pont HelloAsso → Membership",
    "version": "19.0.1.7.15",
    "category": "Membership",
    "summary": "Service pont : pivot dorevia.helloasso.payment → membership.membership_line (sans facture, idempotent).",
    "author": "Dorevia",
    "license": "LGPL-3",
    "depends": [
        "account",
        "utm",
        "membership",
        "membership_extension",
        "dorevia_helloasso_payment",
        "dorevia_helloasso_members",
    ],
    "data": [
        "views/helloasso_account_views.xml",
        "views/helloasso_account_tree_bridge.xml",
        "views/helloasso_payment_membership_v2_views.xml",
    ],
    "installable": True,
    "application": False,
}
