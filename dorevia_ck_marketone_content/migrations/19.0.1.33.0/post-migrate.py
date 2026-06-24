# -*- coding: utf-8 -*-
"""Ticket Dev — Homepage CK : simplification CTA cards « Nos coups de cœur ».

Retire le CTA secondaire "Voir le produit" des cards homepage ; navigation
portée par l'image (cover) et un nouveau lien dédié sur le titre. Section
figée en SSR dans arch_db : sans ce re-bake, la home continuerait de servir
l'ancien markup avec les deux CTA.
"""

from odoo.addons.dorevia_ck_marketone_content.home_featured import bootstrap_home_featured_products


def migrate(cr, version):
    from odoo import api, SUPERUSER_ID

    env = api.Environment(cr, SUPERUSER_ID, {})
    bootstrap_home_featured_products(env)
