# -*- coding: utf-8 -*-
"""Hooks dorevia_ck_theme — maintenance technique uniquement.

Le thème ne seed plus de contenu métier. Pages CMS, catalogue, newsletter :
module ``dorevia_ck_marketone_content`` (gouvernance MOA §4bis).
"""

LEGACY_PHASE3_VIEW_KEY = 'ck_marketone_phase3.shop_compose'
MARKETONE_CONTENT_MODULE = 'dorevia_ck_marketone_content'


def is_marketone_content_installed(env):
    """True si le module contenu CK est installé en base (pas seulement présent addons path)."""
    return bool(env['ir.module.module'].sudo().search([
        ('name', '=', MARKETONE_CONTENT_MODULE),
        ('state', '=', 'installed'),
    ], limit=1))


def remove_legacy_phase3_script_view(env):
    """Retire la vue shell ad hoc si elle coexiste avec l'héritage module."""
    legacy = env['ir.ui.view'].sudo().search([('key', '=', LEGACY_PHASE3_VIEW_KEY)])
    if legacy:
        legacy.unlink()


def post_init_hook(env):
    remove_legacy_phase3_script_view(env)
