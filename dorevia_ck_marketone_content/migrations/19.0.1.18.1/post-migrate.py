# -*- coding: utf-8 -*-
"""Section 3 — chip origine réel : attribut « Origine » (no_variant) + réinjection."""


def migrate(cr, version):
    from odoo import api, SUPERUSER_ID
    from odoo.addons.dorevia_ck_marketone_content.catalog_origine import (
        bootstrap_origine_attribute,
    )
    from odoo.addons.dorevia_ck_marketone_content.home_featured import (
        bootstrap_home_featured_products,
    )

    env = api.Environment(cr, SUPERUSER_ID, {})
    bootstrap_origine_attribute(env)
    # Réinjecte la Section 3 pour que les chips « pays » reflètent l'attribut Origine.
    bootstrap_home_featured_products(env)
