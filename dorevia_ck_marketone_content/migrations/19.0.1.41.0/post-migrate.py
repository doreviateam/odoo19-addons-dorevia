# -*- coding: utf-8 -*-
"""Axe B — libellé navigation Soin & Bien-être + ruban « Nouveau ! »."""
from odoo.addons.dorevia_ck_marketone_content.nav_sync import bootstrap_ck_navigation
from odoo.addons.dorevia_ck_marketone_content.ribbon_sync import francize_new_product_ribbon


def migrate(cr, version):
    from odoo import api, SUPERUSER_ID

    env = api.Environment(cr, SUPERUSER_ID, {})
    francize_new_product_ribbon(env)
    bootstrap_ck_navigation(env)
