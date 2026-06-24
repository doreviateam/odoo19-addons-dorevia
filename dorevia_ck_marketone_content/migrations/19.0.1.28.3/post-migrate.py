# -*- coding: utf-8 -*-
"""Champ En vedette — migration catégorie Coups de cœur → ck_is_featured."""


def migrate(cr, version):
    from odoo import api, SUPERUSER_ID
    from odoo.addons.dorevia_ck_marketone_content.home_featured import (
        bootstrap_home_featured_products,
        migrate_coups_de_coeur_category_to_ck_is_featured,
    )

    env = api.Environment(cr, SUPERUSER_ID, {})
    migrate_coups_de_coeur_category_to_ck_is_featured(env)
    bootstrap_home_featured_products(env)
