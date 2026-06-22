# -*- coding: utf-8 -*-
"""Nav-Shop — seed L2 recette + re-sync navigation."""

from odoo.addons.dorevia_ck_marketone_content.nav_shop_l2_seed import seed_nav_shop_l2_categories
from odoo.addons.dorevia_ck_marketone_content.nav_sync import bootstrap_ck_navigation


def migrate(cr, version):
    from odoo import api, SUPERUSER_ID

    env = api.Environment(cr, SUPERUSER_ID, {})
    seed_nav_shop_l2_categories(env)
    bootstrap_ck_navigation(env)
