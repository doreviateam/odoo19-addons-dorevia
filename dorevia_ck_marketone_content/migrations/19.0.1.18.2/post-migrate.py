# -*- coding: utf-8 -*-
"""Section 3 — fusion catégorie vedettes + réinjection home propre."""


def migrate(cr, version):
    from odoo import api, SUPERUSER_ID
    from odoo.addons.dorevia_ck_marketone_content.home_featured import (
        _ensure_featured_category,
        bootstrap_home_featured_products,
    )

    env = api.Environment(cr, SUPERUSER_ID, {})
    _ensure_featured_category(env)
    bootstrap_home_featured_products(env)
