# -*- coding: utf-8 -*-


def migrate(cr, version):
    from odoo import api, SUPERUSER_ID
    from odoo.addons.dorevia_ck_marketone_content.catalog_manioc_variants import (
        bootstrap_catalog_vedettes_products,
    )
    from odoo.addons.dorevia_ck_marketone_content.home_featured import (
        bootstrap_home_featured_products,
    )
    from odoo.addons.dorevia_ck_marketone_content.hooks import bootstrap_published_products

    env = api.Environment(cr, SUPERUSER_ID, {})
    bootstrap_catalog_vedettes_products(env)
    bootstrap_published_products(env)
    bootstrap_home_featured_products(env)
