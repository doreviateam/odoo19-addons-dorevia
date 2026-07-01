# -*- coding: utf-8 -*-
"""CK-NAV-003 — Navigation catalogue dynamique depuis product.public.category."""
import logging

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    from odoo import api, SUPERUSER_ID

    env = api.Environment(cr, SUPERUSER_ID, {})

    from odoo.addons.dorevia_ck_marketone_content.nav_sync import (
        bootstrap_ck_catalogue_navigation,
    )

    count = bootstrap_ck_catalogue_navigation(env)
    _logger.info(
        'CK-NAV-003 : navigation catalogue synchronisée pour %s site(s).',
        count,
    )
