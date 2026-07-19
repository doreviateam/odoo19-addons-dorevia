# -*- coding: utf-8 -*-
"""S2 — assignation atomique des séquences racines (anti-cascade)."""
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
        'S2 NAV atomic sequences : bootstrap sur %s site(s) après 19.0.1.98.0',
        count,
    )
