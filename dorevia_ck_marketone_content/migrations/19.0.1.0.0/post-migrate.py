# -*- coding: utf-8 -*-
from odoo.addons.dorevia_ck_marketone_content.hooks import bootstrap_all_marketone_content


def migrate(cr, version):
    from odoo import api, SUPERUSER_ID

    env = api.Environment(cr, SUPERUSER_ID, {})
    bootstrap_all_marketone_content(env)
