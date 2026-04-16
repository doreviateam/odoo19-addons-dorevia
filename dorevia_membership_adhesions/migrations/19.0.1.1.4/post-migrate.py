# -*- coding: utf-8 -*-
"""Réaligne le libellé du menu racine membership sur toutes les langues actives.

Le ``post_init_hook`` ne s'exécute qu'à l'installation : une base déjà en « Assos »
peut garder des traductions ``fr_FR`` obsolètes après changement XML / ``fr.po``.
Ce script force « AssoS » comme le hook initial.
"""

import logging

from odoo import SUPERUSER_ID, api

from odoo.addons.dorevia_membership_adhesions.hooks import sync_root_app_menu_name

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    env = api.Environment(cr, SUPERUSER_ID, {})
    _logger.info(
        "post-migrate dorevia_membership_adhesions 19.0.1.1.4 : menu racine → AssoS (toutes langues)"
    )
    sync_root_app_menu_name(env)
