# -*- coding: utf-8 -*-
def migrate(cr, version):
    from odoo import api, SUPERUSER_ID

    env = api.Environment(cr, SUPERUSER_ID, {})
    from odoo.addons.dorevia_ck_marketone_content.home_polish import (
        bootstrap_home_visual_polish,
    )

    # 25.14 : polish visuel home — espacements pt48, coffret, newsletter FR
    bootstrap_home_visual_polish(env)
