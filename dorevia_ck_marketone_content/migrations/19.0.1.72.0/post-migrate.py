# -*- coding: utf-8 -*-
"""CK-NAV-002 — Passage navigation V1 (3 liens plats, mega-menus mis en réserve)."""
import logging
_logger = logging.getLogger(__name__)


def migrate(cr, version):
    from odoo import api, SUPERUSER_ID
    env = api.Environment(cr, SUPERUSER_ID, {})
    from odoo.addons.dorevia_ck_marketone_content.nav_sync import bootstrap_ck_navigation_v1
    count = bootstrap_ck_navigation_v1(env)
    _logger.info('CK-NAV-002 : navigation V1 installée pour %s site(s).', count)
