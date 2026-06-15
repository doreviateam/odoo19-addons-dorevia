# -*- coding: utf-8 -*-
{
    "name": "C-Kreyol Marketone — Thème CK",
    "version": "19.0.1.25.1",
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
    ],
    "data": [
        "views/snippets/snippet_groups.xml",
        "views/snippets/ck_snippet_hero.xml",
        "views/snippets/ck_snippet_category_links.xml",
        "views/snippets/ck_snippet_featured_products.xml",
        "views/snippets/ck_snippet_reassurance.xml",
        "views/snippets/ck_snippet_reassurance_m5.xml",
        "views/snippets/ck_snippet_shop_intro.xml",
        "views/snippets/ck_snippet_shop_pro_signal.xml",
        "views/snippets/ck_snippet_product_pro_signal.xml",
        "views/snippets/ck_snippet_pro_banner.xml",
        "views/snippets/snippets_registry.xml",
        "views/website_layout.xml",
        "views/website_header.xml",
        "views/website_sale_templates.xml",
        "views/website_sale_shop_compose.xml",
        "views/website_sale_product_compose.xml",
    ],
    "assets": {
        "web._assets_primary_variables": [
            "dorevia_ck_theme/static/src/scss/primary_variables.scss",
        ],
        "web._assets_frontend_helpers": [
            (
                "after",
                "website/static/src/scss/bootstrap_overridden.scss",
                "dorevia_ck_theme/static/src/scss/bootstrap_overridden.scss",
            ),
        ],
        "web.assets_frontend": [
            "dorevia_ck_theme/static/src/scss/website.scss",
            "dorevia_ck_theme/static/src/scss/website_header.scss",
            "dorevia_ck_theme/static/src/scss/website_sale.scss",
        ],
    },
    "installable": True,
    "application": False,
    "auto_install": False,
    "post_init_hook": "post_init_hook",
}
