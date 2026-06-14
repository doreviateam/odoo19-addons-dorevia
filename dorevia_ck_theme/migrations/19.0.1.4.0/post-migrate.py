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
        bootstrap_a_propos_page,
        bootstrap_contactus_page,
        bootstrap_epicerie_category,
        bootstrap_professionnels_page,
        bootstrap_published_products,
    )

    bootstrap_epicerie_category(env)
    bootstrap_published_products(env)
    bootstrap_professionnels_page(env)
    bootstrap_contactus_page(env)
    bootstrap_a_propos_page(env)
    remove_legacy_phase3_script_view(env)
