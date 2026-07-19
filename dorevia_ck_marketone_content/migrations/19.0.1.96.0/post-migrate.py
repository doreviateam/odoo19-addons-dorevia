# -*- coding: utf-8 -*-
"""S2 — Navigation catalogue V3 unique autorité ; resync après neutralisation V1/V2.2."""
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
        'S2 NAV V3 : bootstrap_ck_catalogue_navigation sur %s site(s) après upgrade 19.0.1.96.0',
        count,
    )
