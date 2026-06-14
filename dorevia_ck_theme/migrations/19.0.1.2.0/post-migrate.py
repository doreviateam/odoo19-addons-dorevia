# -*- coding: utf-8 -*-

from odoo.addons.dorevia_ck_theme.hooks import (
    is_marketone_content_installed,
    remove_legacy_phase3_script_view,
)


def migrate(cr, version):
    from odoo import api, SUPERUSER_ID

    env = api.Environment(cr, SUPERUSER_ID, {})
    if not is_marketone_content_installed(env):
        remove_legacy_phase3_script_view(env)
        return
    from odoo.addons.dorevia_ck_marketone_content.hooks import (
        bootstrap_epicerie_category,
        bootstrap_published_products,
    )

    bootstrap_epicerie_category(env)
    bootstrap_published_products(env)
    remove_legacy_phase3_script_view(env)
