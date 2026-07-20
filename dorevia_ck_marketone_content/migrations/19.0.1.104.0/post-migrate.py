# -*- coding: utf-8 -*-
"""S6-B2bis — purge chirurgicale racine Blog → /blog (navigation CK)."""
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
        'S6-B2bis Blog root purge : bootstrap_ck_catalogue_navigation sur %s site(s) '
        'après 19.0.1.104.0',
        count,
    )
