# -*- coding: utf-8 -*-
"""CK-HOME-001B — vedettes visibles + visuel coffret qualifié."""
import logging

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    from odoo import api, SUPERUSER_ID

    env = api.Environment(cr, SUPERUSER_ID, {})

    from odoo.addons.dorevia_ck_marketone_content.catalog_discovery_pack import (
        bootstrap_catalog_discovery_pack_product,
    )
    from odoo.addons.dorevia_ck_marketone_content.home_discovery_pack import (
        bootstrap_home_discovery_pack,
    )
    from odoo.addons.dorevia_ck_marketone_content.home_featured import (
        bootstrap_home_featured_products,
    )

    bootstrap_catalog_discovery_pack_product(env)
    bootstrap_home_featured_products(env)
    bootstrap_home_discovery_pack(env)
    cr.commit()

    _logger.info(
        'CK-HOME-001B : vedettes SSR avec <img> produit + coffret sans fallback beige.'
    )
