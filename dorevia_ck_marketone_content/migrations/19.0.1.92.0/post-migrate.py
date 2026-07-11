# -*- coding: utf-8 -*-
"""CODE-004 — opt-out discovery-pack : retrait section si ICP déjà False (sans SET ICP)."""
import logging

_logger = logging.getLogger(__name__)

DISCOVERY_PACK_BOOTSTRAP_ICP = 'ck.marketone.discovery_pack_bootstrap_enabled'


def migrate(cr, version):
    from odoo import api, SUPERUSER_ID

    env = api.Environment(cr, SUPERUSER_ID, {})
    param = env['ir.config_parameter'].sudo()
    if param.get_param(DISCOVERY_PACK_BOOTSTRAP_ICP, 'True') != 'False':
        return

    from odoo.addons.dorevia_ck_marketone_content.home_discovery_pack import (
        bootstrap_home_discovery_pack,
    )

    bootstrap_home_discovery_pack(env)
    _logger.info(
        'CODE-004 migration 92.0 : retrait section discovery-pack (ICP False préexistant).'
    )
