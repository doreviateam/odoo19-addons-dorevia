# -*- coding: utf-8 -*-
# QA C6 — Convention de versionnage : le numéro de version est incrémenté à
# chaque livraison (y compris assets/SCSS/JS sans changement de schéma DB). Seuls
# les changements nécessitant une post-migration disposent d'un dossier dédié
# sous migrations/ ; les écarts entre la version et le dernier dossier de
# migration sont donc normaux (bumps « assets-only »).
{
    "name": "C-Kreyol Marketone — Thème CK",
    "version": "19.0.1.38.3",
    "category": "Theme/eCommerce",
    "summary": "Thème CK générique — tokens, layout, snippets Website Builder",
    "description": """
        Module thème C-Kreyol — périmètre strict ticket
        ``dorevia_ck_theme_01_socle_tokens_layout_snippets``.

        Odoo 19 CE · snippets first · pas de surcouche autonome.

        Inclus : tokens SCSS, layout léger, snippets éditables, héritages QWeb minimaux.

        Exclus : seed contenu métier (module ``dorevia_ck_marketone_content``),
        origines/collections custom, B2B custom, catalogue parallèle.

        Référence : ``dorevia_ck_marketone/docs/design/ticket_dorevia_ck_theme_01_socle_tokens_layout_snippets.md``
    """,
    "author": "Dorevia",
    "license": "LGPL-3",
    "depends": [
        "website",
        "website_sale",
        "website_sale_comparison",
    ],
    "data": [
        "views/snippets/snippet_groups.xml",
        "views/snippets/ck_snippet_hero.xml",
        "views/snippets/ck_snippet_hero_slide.xml",
        "views/snippets/ck_snippet_category_links.xml",
        "views/snippets/ck_snippet_featured_products.xml",
        "views/snippets/ck_snippet_univers_card.xml",
        "views/snippets/ck_snippet_univers_cards.xml",
        "views/snippets/ck_snippet_reassurance.xml",
        "views/snippets/ck_snippet_reassurance_m5.xml",
        "views/snippets/ck_snippet_shop_intro.xml",
        "views/snippets/ck_snippet_shop_pro_signal.xml",
        "views/snippets/ck_snippet_product_pro_signal.xml",
        "views/snippets/ck_snippet_pro_banner.xml",
        "views/snippets/snippets_registry.xml",
        "views/website_layout.xml",
        "views/website_header.xml",
        "views/website_header_h1.xml",
        "views/website_nav_ck_v1.xml",
        "views/website_sale_templates.xml",
        "views/website_sale_product_card.xml",
        "views/website_sale_product_page.xml",
        "views/website_sale_shop_compose.xml",
        "views/website_sale_product_compose.xml",
    ],
    "assets": {
        "web._assets_frontend_helpers": [
            (
                "before",
                "website/static/src/scss/bootstrap_overridden.scss",
                "dorevia_ck_theme/static/src/scss/ck_tokens.scss",
            ),
            (
                "after",
                "website/static/src/scss/bootstrap_overridden.scss",
                "dorevia_ck_theme/static/src/scss/bootstrap_overridden.scss",
            ),
        ],
        "web.assets_frontend": [
            (
                "before",
                "web/static/lib/bootstrap/scss/_variables.scss",
                "dorevia_ck_theme/static/src/scss/frontend_bootstrap_variables.scss",
            ),
            "dorevia_ck_theme/static/src/scss/website_fonts.scss",
            "dorevia_ck_theme/static/src/scss/product_card.scss",
            "dorevia_ck_theme/static/src/scss/product_page.scss",
            "dorevia_ck_theme/static/src/scss/website.scss",
            "dorevia_ck_theme/static/src/scss/website_header.scss",
            "dorevia_ck_theme/static/src/scss/website_sale.scss",
            "dorevia_ck_theme/static/src/js/ck_hero_carousel_pause.js",
            "dorevia_ck_theme/static/src/js/ck_nav_shop_header.js",
        ],
        "website.website_builder_assets": [
            "dorevia_ck_theme/static/src/js/ck_hero_plugin.js",
            "dorevia_ck_theme/static/src/js/ck_hero_option_plugin.js",
            "dorevia_ck_theme/static/src/js/ck_hero_builder_plugin.js",
            "dorevia_ck_theme/static/src/js/ck_univers_plugin.js",
            "dorevia_ck_theme/static/src/js/ck_univers_option_plugin.js",
            "dorevia_ck_theme/static/src/js/ck_univers_builder_plugin.js",
        ],
    },
    "installable": True,
    "application": False,
    "auto_install": False,
    "post_init_hook": "post_init_hook",
}
