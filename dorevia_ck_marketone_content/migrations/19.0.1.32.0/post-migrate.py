# -*- coding: utf-8 -*-
"""Ticket Dev — Homepage CK « Nos coups de cœur » en grille de 4 cards.

FEATURED_CURATED_MAX passe de 8 à 4. La section homepage est une bake SSR
figée dans arch_db (pas un rendu QWeb live) : sans ce re-bake, la home
continuerait de servir l'ancien arch à 8 cartes malgré le changement de code.
"""

from odoo.addons.dorevia_ck_marketone_content.home_featured import bootstrap_home_featured_products


def migrate(cr, version):
    from odoo import api, SUPERUSER_ID

    env = api.Environment(cr, SUPERUSER_ID, {})
    bootstrap_home_featured_products(env)
