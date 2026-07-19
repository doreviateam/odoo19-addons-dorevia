# -*- coding: utf-8 -*-
"""S2 — normaliser collisions de séquences racines (Épicerie/Producteurs)."""
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
        'S2 NAV sequences : bootstrap_ck_catalogue_navigation sur %s site(s) '
        'après upgrade 19.0.1.97.0',
        count,
    )
