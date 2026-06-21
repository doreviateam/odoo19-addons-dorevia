# -*- coding: utf-8 -*-
"""Hero — crêpes manioc : visuel recadré centré, crop carrousel stable."""


def migrate(cr, version):
    from odoo import api, SUPERUSER_ID

    env = api.Environment(cr, SUPERUSER_ID, {})
    from odoo.addons.dorevia_ck_marketone_content.home_hero import (
        normalize_homepage_hero_crepe,
    )

    normalize_homepage_hero_crepe(env)
