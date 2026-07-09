# -*- coding: utf-8 -*-
"""Hero MOA — visuels sandbox (crêpe / pâte manioc / marché) sur install existante."""


def migrate(cr, version):
    from odoo import api, SUPERUSER_ID

    env = api.Environment(cr, SUPERUSER_ID, {})
    from odoo.addons.dorevia_ck_marketone_content.home_hero import bootstrap_home_hero

    bootstrap_home_hero(env)
