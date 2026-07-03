# -*- coding: utf-8 -*-
{
    "name": "C-Kreyol Marketone — Contenu démo",
    "version": "19.0.1.83.0",
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
        "website_sale_wishlist",
        "website_crm",
        "mass_mailing",
        "website_mass_mailing",
    ],
    "data": [
        "security/ir.model.access.csv",
        "data/website_sale_product_comment.xml",
        "data/ck_card_uom_data.xml",
        "data/ck_product_badge_data.xml",
        "views/ck_card_uom_views.xml",
        "views/ck_product_badge_views.xml",
        "views/res_partner_views.xml",
        "views/product_template_views.xml",
        "views/website_sale_product_card.xml",
        "views/website_sale_home_featured_wishlist.xml",
        "views/website_sale_product_page.xml",
        "views/website_sale_product_page_v11.xml",
        "views/product_public_category_views.xml",
        "views/website_sale_rayon_editorial.xml",
        "views/website_sale_category_tiles.xml",
        "views/website_sale_shop_rebound.xml",
        "views/website_producers_list.xml",
        "views/website_producer_detail.xml",
        "views/website_sale_shop_sparse_grid.xml",
        "views/product_tag_views.xml",
        "views/website_sale_shop_filter_drawer.xml",
        "views/ck_mega_menu_visual_block_views.xml",
        "views/ck_mega_menu_rayon_visual_views.xml",
        "views/website_nav_ck_v1.xml",
        "views/website_nav_ck_shop_v2.xml",
        "views/website_nav_ck_v22.xml",
        "data/ck_public_category_coups_de_coeur.xml",
        "data/ck_product_ribbon_coups_de_coeur.xml",
        "data/website_sale_config.xml",
        "data/website_cookies_config.xml",
        "data/ck_cron.xml",
    ],
    "installable": True,
    "application": False,
    "auto_install": False,
    "post_init_hook": "post_init_hook",
    "assets": {
        "web.assets_frontend": [
            "dorevia_ck_marketone_content/static/src/js/ck_featured_cart_add.js",
            "dorevia_ck_marketone_content/static/src/js/ck_shop_filter_offcanvas.js",
            "dorevia_ck_marketone_content/static/src/js/ck_product_page_anchors.js",
        ],
    },
}
