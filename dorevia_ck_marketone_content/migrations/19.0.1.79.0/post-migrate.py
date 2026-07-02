# -*- coding: utf-8 -*-
"""CK-HOME-001B — CTA Coffrets sans stretched-link (clic Découvrir → /kits)."""
import logging

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    from odoo import api, SUPERUSER_ID

    env = api.Environment(cr, SUPERUSER_ID, {})

    from odoo.addons.dorevia_ck_marketone_content.home_discovery_pack import (
        bootstrap_home_discovery_pack,
    )

    bootstrap_home_discovery_pack(env)

    _logger.info(
        'CK-HOME-001B hotfix 79.0 : bloc coffrets sans stretched-link · CTA /kits cliquable.'
    )
