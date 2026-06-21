# -*- coding: utf-8 -*-
"""Replay vedettes home — structure BEM commune card CK."""


def migrate(cr, version):
    from odoo import api, SUPERUSER_ID

    env = api.Environment(cr, SUPERUSER_ID, {})
    from odoo.addons.dorevia_ck_marketone_content.home_featured import (
        bootstrap_home_featured_products,
    )

    bootstrap_home_featured_products(env)
