# -*- coding: utf-8 -*-
from odoo.addons.dorevia_ck_marketone_content.hooks import (
    bootstrap_footer_legal_links,
    bootstrap_mentions_legales_page,
    bootstrap_privacy_page,
    bootstrap_terms_page,
)


def migrate(cr, version):
    from odoo import api, SUPERUSER_ID

    env = api.Environment(cr, SUPERUSER_ID, {})
    bootstrap_mentions_legales_page(env)
    bootstrap_privacy_page(env)
    bootstrap_terms_page(env)
    bootstrap_footer_legal_links(env)
