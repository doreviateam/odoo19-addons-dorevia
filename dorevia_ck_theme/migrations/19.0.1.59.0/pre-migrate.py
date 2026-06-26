# -*- coding: utf-8 -*-
"""Logo SVG header — purge les vues logo obsolètes avant rechargement du registre.

* layout_ck_header_brand_v22 : xpath sur .ck-header__brand (baseline texte, retirée)
* layout_ck_header_brand : ancien héritage sur option_header_brand_logo (19.0.1.58.0)

Les deux sont recréées / remplacées par website_header_brand.xml (héritage direct
sur placeholder_header_brand + asset ck-logo.svg).
"""


def migrate(cr, version):
    for key in (
        'dorevia_ck_theme.layout_ck_header_brand_v22',
        'dorevia_ck_theme.layout_ck_header_brand',
    ):
        cr.execute("DELETE FROM ir_ui_view WHERE key = %s", (key,))
