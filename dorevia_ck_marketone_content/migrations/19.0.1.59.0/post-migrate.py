# -*- coding: utf-8 -*-
"""Rating-U2 — rebootstrap vedettes home pour injecter ck-card-rating dans le SSR gelé."""

from odoo.addons.dorevia_ck_marketone_content.home_featured import bootstrap_home_featured_products


def migrate(cr, version):
    env = __import__('odoo.api', fromlist=['Environment']).Environment(cr, 1, {})
    bootstrap_home_featured_products(env)
