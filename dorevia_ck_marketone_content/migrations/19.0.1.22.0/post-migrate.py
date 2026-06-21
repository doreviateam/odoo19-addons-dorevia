# -*- coding: utf-8 -*-
"""PR-2 H3 — fige les empreintes des pages CMS existantes (baseline anti-écrasement).

Pose uniquement ``ck_seed_arch.{view_key}`` = empreinte de l'arch courante.
AUCUNE écriture d'arch : on capture l'état courant comme baseline.

Précondition : exécuter avant toute édition MOA importante des pages CMS (cas
actuel — pages code-seedées). Une page déjà éditée avant le freeze serait figée
comme baseline et donc réécrasable au prochain bootstrap.
"""


def migrate(cr, version):
    from odoo import api, SUPERUSER_ID
    from odoo.addons.dorevia_ck_marketone_content.home_arch import _arch_fingerprint
    from odoo.addons.dorevia_ck_marketone_content.hooks import (
        CONTACTUS_VIEW_KEY,
        A_PROPOS_VIEW_KEY,
        PROFESSIONNELS_VIEW_KEY,
        PRODUCER_VIEW_KEY,
        RECIPES_VIEW_KEY,
    )
    from odoo.addons.dorevia_ck_marketone_content.legal_pages import (
        LEGAL_PAGE_VIEW_KEY,
        PRIVACY_PAGE_VIEW_KEY,
        TERMS_PAGE_VIEW_KEY,
    )

    env = api.Environment(cr, SUPERUSER_ID, {})
    param = env['ir.config_parameter'].sudo()
    View = env['ir.ui.view'].sudo()
    for view_key in (
        CONTACTUS_VIEW_KEY,
        A_PROPOS_VIEW_KEY,
        PROFESSIONNELS_VIEW_KEY,
        PRODUCER_VIEW_KEY,
        RECIPES_VIEW_KEY,
        LEGAL_PAGE_VIEW_KEY,
        PRIVACY_PAGE_VIEW_KEY,
        TERMS_PAGE_VIEW_KEY,
    ):
        view = View.search([('key', '=', view_key)], limit=1)
        if view:
            param.set_param(
                f'ck_seed_arch.{view_key}',
                _arch_fingerprint(view.arch_db or view.arch or ''),
            )
