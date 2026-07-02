# -*- coding: utf-8 -*-
"""CK-HOME-001B hotfix — fuite markup dual + porte /kits."""
import logging

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    from odoo import api, SUPERUSER_ID

    env = api.Environment(cr, SUPERUSER_ID, {})

    from odoo.addons.dorevia_ck_marketone_content.home_discovery_pack import (
        bootstrap_home_discovery_pack,
    )
    from odoo.addons.dorevia_ck_marketone_content.home_dual_engage import (
        bootstrap_home_dual_engage,
    )

    bootstrap_home_dual_engage(env)
    bootstrap_home_discovery_pack(env)
    cr.commit()

    _logger.info(
        'CK-HOME-001B hotfix 77.0 : home coffrets/dual sans fuite markup + /kits actif.'
    )
