# -*- coding: utf-8 -*-
{
    "name": "C-Kreyol — Site e-commerce (Odoo 19)",
    "version": "19.0.1.0.0",
    "category": "Dorevia",
    "summary": "Thème d’accueil, charte et pages stub pour la vitrine / boutique C-Kreyol (La Platine)",
    "description": """
        Module initial pour **https://c-kreyol.doreviateam.com** : remplace le contenu de la page
        d’accueil par une landing proche de la maquette ``Zedocs/odoo19/c-kreyol/c-kreyol.html``,
        charge une charte SCSS (latérite, typo Cormorant / IBM Plex Mono / Inter), ajoute des menus
        et des pages brouillon (espace pro, revendeurs).

        Dépend de **website_sale** pour disposer du catalogue ``/shop`` dès l’installation.

        Désinstaller le module pour retrouver l’accueil standard du thème.
    """,
    "author": "Dorevia Team",
    "license": "LGPL-3",
    "depends": ["website", "website_sale"],
    "data": [
        "views/ckreyol_homepage_templates.xml",
        "views/ckreyol_footer_templates.xml",
        "data/ckreyol_stub_pages.xml",
        "data/ckreyol_menus.xml",
    ],
    "assets": {
        "web.assets_frontend": [
            "dorevia_website_c_kreyol/static/src/scss/ckreyol_branding.scss",
        ],
    },
    "installable": True,
    "application": False,
}
