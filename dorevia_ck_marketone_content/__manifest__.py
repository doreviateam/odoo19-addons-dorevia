# -*- coding: utf-8 -*-
{
    "name": "C-Kreyol Marketone — Contenu démo",
    "version": "19.0.1.3.0",
    "category": "Website/Website",
    "summary": "Seed contenu CK Marketone — pages CMS, catalogue pilote, newsletter",
    "description": """
        Contenu métier optionnel pour l'instance CK Marketone (gouvernance MOA §4bis).

        Inclus : pages /professionnels, /contactus, /a-propos, /recettes, fiche producteur,
        enrichissements catalogue, mailing list newsletter.

        Le module ``dorevia_ck_theme`` reste un thème générique (tokens, SCSS, snippets, layout)
        déployable sans injection de contenu CK.
    """,
    "author": "Dorevia",
    "license": "LGPL-3",
    "depends": [
        "account",
        "dorevia_ck_theme",
        "website_sale",
        "website_crm",
        "mass_mailing",
        "website_mass_mailing",
    ],
    "data": [],
    "installable": True,
    "application": False,
    "auto_install": False,
    "post_init_hook": "post_init_hook",
}
