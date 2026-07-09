# -*- coding: utf-8 -*-
"""Homepage site-specific — neutralise la page / globale (install fraîche QA)."""


def migrate(cr, version):
    from odoo import api, SUPERUSER_ID

    env = api.Environment(cr, SUPERUSER_ID, {})
    from odoo.addons.dorevia_ck_marketone_content.home_hero import bootstrap_home_hero
    from odoo.addons.dorevia_ck_marketone_content.home_page import (
        bootstrap_website_homepage_binding,
    )

    bootstrap_home_hero(env)
    bootstrap_website_homepage_binding(env)
