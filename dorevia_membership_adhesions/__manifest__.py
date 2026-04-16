# -*- coding: utf-8 -*-
{
    "name": "Dorevia — Menus Membres (adhésion & structure)",
    "version": "19.0.1.1.5",
    "category": "Membership",
    "summary": "Menu Adhésion (lignes) aligné sur la liste contact, organisation des menus Membres.",
    "author": "Dorevia",
    "license": "LGPL-3",
    "depends": ["membership", "membership_extension"],
    "data": [
        "views/membership_menu_reorganization.xml",
        "views/membership_line_menu_views.xml",
    ],
    "post_init_hook": "post_init_hook",
    "installable": True,
    "application": False,
}
