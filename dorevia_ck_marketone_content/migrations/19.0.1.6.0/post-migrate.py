# -*- coding: utf-8 -*-


def migrate(cr, version):
    from odoo import api, SUPERUSER_ID
    from odoo.addons.dorevia_ck_marketone_content.home_editorial import (
        bootstrap_home_editorial,
    )

    env = api.Environment(cr, SUPERUSER_ID, {})
    bootstrap_home_editorial(env)
