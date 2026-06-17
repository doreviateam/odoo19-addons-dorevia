# -*- coding: utf-8 -*-
def migrate(cr, version):
    from odoo import api, SUPERUSER_ID

    env = api.Environment(cr, SUPERUSER_ID, {})
    from odoo.addons.dorevia_ck_marketone_content.home_featured import (
        bootstrap_home_featured_products,
    )

    # 25.12 : l'arch_db de la home est un champ traduit (jsonb par langue).
    # Le rebuild ne reconstruisait que la langue source (en_US), laissant
    # l'entrée fr_FR servie figée. On reconstruit désormais chaque langue ;
    # ce bootstrap répare les snapshots fr existants.
    bootstrap_home_featured_products(env)
