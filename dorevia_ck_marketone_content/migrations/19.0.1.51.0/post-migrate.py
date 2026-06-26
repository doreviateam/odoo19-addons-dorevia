# -*- coding: utf-8 -*-
from odoo.addons.dorevia_ck_marketone_content.shop_toolbar import purge_ck_qa_public_categories


def migrate(cr, version):
    from odoo import api, SUPERUSER_ID

    env = api.Environment(cr, SUPERUSER_ID, {})
    purge_ck_qa_public_categories(env)
