# -*- coding: utf-8 -*-
{
    "name": "C-Kreyol Marketone — Contenu démo",
    "version": "19.0.1.26.1",
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
    "data": [
        "security/ir.model.access.csv",
        "data/ck_card_uom_data.xml",
        "views/ck_card_uom_views.xml",
        "views/product_template_views.xml",
        "views/website_sale_product_card.xml",
        "views/website_sale_product_page.xml",
        "views/website_nav_ck_v1.xml",
        "data/ck_public_category_coups_de_coeur.xml",
        "data/ck_product_ribbon_coups_de_coeur.xml",
        "data/ck_cron.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
    "post_init_hook": "post_init_hook",
    "assets": {
        "web.assets_frontend": [
            "dorevia_ck_marketone_content/static/src/js/ck_featured_cart_add.js",
        ],
    },
}
