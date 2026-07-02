# -*- coding: utf-8 -*-
"""CK-HOME-POLISH-001 — Home : bloc Pro seul, newsletter neutralisée."""
import logging

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    from odoo import api, SUPERUSER_ID

    env = api.Environment(cr, SUPERUSER_ID, {})

    from odoo.addons.dorevia_ck_marketone_content.home_dual_engage import (
        bootstrap_home_dual_engage,
    )
    from odoo.addons.dorevia_ck_marketone_content.home_polish import (
        bootstrap_home_visual_polish,
    )

    bootstrap_home_dual_engage(env)
    bootstrap_home_visual_polish(env)

    _logger.info(
        'CK-HOME-POLISH-001 80.0 : newsletter retirée de la home · bloc Pro seul.'
    )
