# -*- coding: utf-8 -*-
"""Galettes MOA — vraie photo produit sur install existante (fin de la zone beige).

Rejoue le bootstrap catalogue vedettes : le chemin d'update de
_ensure_galettes_separate_product remplace le placeholder crème par
ck_hero_crepe_manioc.webp sans écraser une vraie photo BO existante.
"""


def migrate(cr, version):
    from odoo import api, SUPERUSER_ID

    env = api.Environment(cr, SUPERUSER_ID, {})
    from odoo.addons.dorevia_ck_marketone_content.catalog_manioc_variants import (
        bootstrap_catalog_vedettes_products,
    )

    bootstrap_catalog_vedettes_products(env)
