# -*- coding: utf-8 -*-
from odoo.addons.dorevia_ck_marketone_content.hooks import (
    bootstrap_footer_legal_link,
    bootstrap_mentions_legales_page,
)


def migrate(cr, version):
    from odoo import api, SUPERUSER_ID

    env = api.Environment(cr, SUPERUSER_ID, {})
    bootstrap_mentions_legales_page(env)
    bootstrap_footer_legal_link(env)
