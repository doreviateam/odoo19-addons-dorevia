# -*- coding: utf-8 -*-
"""Migration 19.0.1.21.0 — Section 4 Acheter par univers (3 cards visuelles)."""


def migrate(cr, version):
    from odoo import api, SUPERUSER_ID

    env = api.Environment(cr, SUPERUSER_ID, {})
    from odoo.addons.dorevia_ck_marketone_content.home_univers import bootstrap_home_univers

    if not bootstrap_home_univers(env):
        raise RuntimeError(
            'CK univers migration 21.0: bootstrap_home_univers a échoué'
        )
