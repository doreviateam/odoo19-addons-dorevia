#!/usr/bin/env python3
"""Phase 3 — déploiement portable · dorevia_ck_marketone.

La composition shop (intro, réassurance M5, signal Pro) est portée par le module
``dorevia_ck_theme`` (``views/website_sale_shop_compose.xml``).

Le seed catégorie BO est porté par ``dorevia_ck_marketone_content``.

Sur une nouvelle base :

  odoo -d MA_BASE -i dorevia_ck_marketone_content -u dorevia_ck_theme --stop-after-init
  docker restart <conteneur-odoo>

Usage :
  docker exec -i sandbox-odoo19-odoo-1 odoo shell -d MA_BASE --no-http \\
    < docs/design/maquette_01.2/scripts/ck_phase3_configure.py
"""
from odoo.addons.dorevia_ck_marketone_content.hooks import bootstrap_epicerie_category
from odoo.addons.dorevia_ck_theme.hooks import remove_legacy_phase3_script_view

print('Phase 3 portable path: odoo -d <db> -i dorevia_ck_marketone_content -u dorevia_ck_theme --stop-after-init')
cat_ok = bootstrap_epicerie_category(env)
remove_legacy_phase3_script_view(env)
print(f'bootstrap_epicerie_category: {cat_ok}')
print('remove_legacy_phase3_script_view: OK')
