# -*- coding: utf-8 -*-
"""Migration 19.0.1.10.65 : renomme Offrir → Idées cadeaux au menu principal.

``post_init_hook`` ne s'exécute pas à l'upgrade ; on réutilise la fonction
idempotente ``_sync_ckr_menus`` pour aligner URL ``/offrir`` et libellé.
"""

from odoo.api import Environment, SUPERUSER_ID

from odoo.addons.dorevia_ckreyol_marketplace.hooks import _sync_ckr_menus


def migrate(cr, version):
    env = Environment(cr, SUPERUSER_ID, {})
    _sync_ckr_menus(env)
