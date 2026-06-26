# -*- coding: utf-8 -*-
"""Axe C — corrections BO catalogue (blocs D partiel + E).

Périmètre 19.0.1.43.0 :
- UOM card g/kg + prix de référence : Confiture, Manio Crackers, Galettes, Savon.
- Chapeau Panama : ck_show_reference_price=False, UOM card vidées.
- fr_FR : sous-catégories publiques, Galettes de manioc, attribut Origine / Guadeloupe.

Exclus (autres livrables) :
- Jus Mont-Pelé, Pâte de manioc → 19.0.1.44.0 après MOA-2.
- Catégorie « Coups de cœur » → ticket XML data (noupdate / retrait record).
"""


def migrate(cr, version):
    from odoo import api, SUPERUSER_ID

    from odoo.addons.dorevia_ck_marketone_content.axe_c_bo_sync import (
        apply_axe_c_bo_corrections,
    )

    env = api.Environment(cr, SUPERUSER_ID, {})
    apply_axe_c_bo_corrections(env)
