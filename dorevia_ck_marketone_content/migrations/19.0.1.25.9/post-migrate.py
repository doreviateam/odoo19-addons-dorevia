# -*- coding: utf-8 -*-
"""Propagation BO→front vedettes — rebootstrap home après extension des déclencheurs.

Réaligne les cartes « Coups de cœur » (titre, label catégorie, badge ruban) sur le
BO courant après l'ajout de `name`/`description_sale` aux déclencheurs template et
des overrides catégorie/ruban (renommages désormais propagés).
"""


def migrate(cr, version):
    from odoo import api, SUPERUSER_ID
    from odoo.addons.dorevia_ck_marketone_content.home_featured import (
        bootstrap_home_featured_products,
    )

    env = api.Environment(cr, SUPERUSER_ID, {})
    bootstrap_home_featured_products(env)
