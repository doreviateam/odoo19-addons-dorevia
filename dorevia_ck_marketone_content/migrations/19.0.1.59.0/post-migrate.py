# -*- coding: utf-8 -*-
"""Rating-U2 — rebootstrap vedettes home pour injecter ck-card-rating dans le SSR gelé.

Les cards home sont des fragments HTML statiques freezés dans l'arch de la page
au bootstrap.  Ce post-migrate reconstruit la section vedettes pour que la ligne
rating (★ 4,8 · 12 avis) apparaisse sans action manuelle après l'upgrade.
"""
from odoo.addons.dorevia_ck_marketone_content.home_featured import bootstrap_home_featured_products


def migrate(cr, version):
    from odoo import api, SUPERUSER_ID

    env = api.Environment(cr, SUPERUSER_ID, {})
    bootstrap_home_featured_products(env)
