# -*- coding: utf-8 -*-
"""Force la reconstruction home pour réinjecter les étiquettes produit sur les cards."""


def migrate(cr, version):
    from odoo import api, SUPERUSER_ID
    from odoo.addons.dorevia_ck_marketone_content.home_featured import (
        bootstrap_home_featured_products,
    )

    env = api.Environment(cr, SUPERUSER_ID, {})
    bootstrap_home_featured_products(env)
