# -*- coding: utf-8 -*-
from odoo import api, SUPERUSER_ID


def migrate(cr, version):
  env = api.Environment(cr, SUPERUSER_ID, {})
  from odoo.addons.dorevia_ck_marketone_content.hooks import bootstrap_all_marketone_content
  bootstrap_all_marketone_content(env)
