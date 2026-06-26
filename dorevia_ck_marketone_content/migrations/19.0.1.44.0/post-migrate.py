# -*- coding: utf-8 -*-
"""MOA-2 — UOM card Jus Mont-Pelé (l/l) et Pâte de manioc (kg/kg).

Périmètre 19.0.1.44.0 uniquement — ne touche pas aux produits corrigés en 43.0
ni à la catégorie « Coups de cœur ».
"""


def migrate(cr, version):
    from odoo import api, SUPERUSER_ID

    from odoo.addons.dorevia_ck_marketone_content.axe_c_bo_sync import (
        apply_moa2_bo_corrections,
    )

    env = api.Environment(cr, SUPERUSER_ID, {})
    apply_moa2_bo_corrections(env)
