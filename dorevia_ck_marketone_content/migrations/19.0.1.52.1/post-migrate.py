# -*- coding: utf-8 -*-
from odoo.addons.dorevia_ck_marketone_content.shop_filter_groups import bootstrap_ck_shop_filter_tags


def migrate(cr, version):
    from odoo import api, SUPERUSER_ID

    env = api.Environment(cr, SUPERUSER_ID, {})
    bootstrap_ck_shop_filter_tags(env)
