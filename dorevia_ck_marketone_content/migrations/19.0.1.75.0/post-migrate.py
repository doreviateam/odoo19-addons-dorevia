# -*- coding: utf-8 -*-
"""CK-HOME-001A — repositionnement hero home : titre, kicker, sous-titre, CTA producteurs."""
import logging

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    from odoo import api, SUPERUSER_ID

    env = api.Environment(cr, SUPERUSER_ID, {})

    from odoo.addons.dorevia_ck_marketone_content.home_hero import bootstrap_home_hero

    bootstrap_home_hero(env)
    cr.commit()

    _logger.info(
        'CK-HOME-001A : hero home repositionné (titre, kicker, sous-titre, '
        'CTA secondaire /producteurs).'
    )
