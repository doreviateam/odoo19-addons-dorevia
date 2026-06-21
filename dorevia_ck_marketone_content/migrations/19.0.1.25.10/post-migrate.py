# -*- coding: utf-8 -*-
"""Propagation BO→front variantes — rebootstrap home après extension des déclencheurs.

Réaligne les cards vedettes (par variante : titre = valeur d'attribut, image variante)
après l'ajout de l'image variante aux déclencheurs et de l'override
``product.attribute.value`` (renommage de valeur d'attribut).
"""


def migrate(cr, version):
    from odoo import api, SUPERUSER_ID
    from odoo.addons.dorevia_ck_marketone_content.home_featured import (
        bootstrap_home_featured_products,
    )

    env = api.Environment(cr, SUPERUSER_ID, {})
    bootstrap_home_featured_products(env)
