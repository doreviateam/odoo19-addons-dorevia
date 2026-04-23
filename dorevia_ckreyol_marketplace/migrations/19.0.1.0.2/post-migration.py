# -*- coding: utf-8 -*-
"""Migration 19.0.1.0.2 : resynchronise les menus C-Kreyol.

Odoo ne rejoue pas `post_init_hook` lors d un simple upgrade
(`-u dorevia_ckreyol_marketplace`). Pour que les modifications du
hook (purge natifs, creation Option B, nettoyage website.page) se
propagent a chaque upgrade, on duplique l appel ici.

La fonction cible est idempotente, rejouer ne cree pas de doublons.
"""

from odoo.api import Environment, SUPERUSER_ID

from odoo.addons.dorevia_ckreyol_marketplace.hooks import _sync_ckr_menus


def migrate(cr, version):
    env = Environment(cr, SUPERUSER_ID, {})
    _sync_ckr_menus(env)
