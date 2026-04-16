# -*- coding: utf-8 -*-
"""Réaligne le libellé du menu racine membership (``ROOT_MEMBERSHIP_APP_MENU_LABEL``) sur toutes les langues."""

import logging

from odoo import SUPERUSER_ID, api

from odoo.addons.dorevia_membership_adhesions.hooks import (
    ROOT_MEMBERSHIP_APP_MENU_LABEL,
    sync_root_app_menu_name,
)

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    _logger.info(
        "post-migrate dorevia_membership_adhesions 19.0.1.1.5 : menu racine → %s (toutes langues)",
        ROOT_MEMBERSHIP_APP_MENU_LABEL,
    )
    sync_root_app_menu_name(env)
