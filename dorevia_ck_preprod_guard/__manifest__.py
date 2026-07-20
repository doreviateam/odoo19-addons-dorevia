# -*- coding: utf-8 -*-
{
    "name": "Dorevia CK — Soft-launch préprod guard",
    "version": "19.0.1.2.0",
    "category": "Website/Website",
    "summary": "Protections UX soft-launch P1 + Option B (bandeau, CTA achat, CTA login) — réservé préproduction CK",
    "description": """
Module technique soft-launch CK (R3-3 / Option B).
Réservé à la préproduction (preprod-ck.doreviateam.com / ck_marketone_preprod).
auto_install=False — ne jamais inclure dans un déploiement production.
""",
    "author": "Dorevia",
    "license": "LGPL-3",
    "depends": ["website_sale", "portal"],
    "data": [
        "views/ck_soft_launch_p1.xml",
        "views/ck_soft_launch_auth_cta.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
    "pre_init_hook": "pre_init_hook",
}
