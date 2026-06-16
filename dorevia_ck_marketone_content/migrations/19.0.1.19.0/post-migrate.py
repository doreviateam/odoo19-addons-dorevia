# -*- coding: utf-8 -*-
"""Card home V1.1 — étiquettes, quantité nette, prix de référence, CTA enrichi."""


def migrate(cr, version):
    from odoo import api, SUPERUSER_ID
    from odoo.addons.dorevia_ck_marketone_content.home_featured import (
        bootstrap_home_featured_products,
    )

    env = api.Environment(cr, SUPERUSER_ID, {})
    bootstrap_home_featured_products(env)
