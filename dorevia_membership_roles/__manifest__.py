# -*- coding: utf-8 -*-
{
    "name": "Dorevia — Rôles de membre",
    "version": "19.0.2.0.2",
    "category": "Membership",
    "summary": "Rôles associatifs sur les contacts, indépendants de l'adhésion.",
    "author": "Dorevia",
    "license": "LGPL-3",
    "depends": ["membership"],
    "data": [
        "security/membership_role_security.xml",
        "security/ir.model.access.csv",
        "views/membership_role_views.xml",
        "views/res_partner_views.xml",
        "views/res_partner_search_views.xml",
        "data/membership_role_data.xml",
    ],
    "installable": True,
    "application": False,
}
