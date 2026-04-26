# -*- coding: utf-8 -*-
"""Migration 19.0.1.9.7 : réinjecte les binaires image des 4 fiches vitrine.

Les enregistrements sont en ``noupdate`` : un simple changement de fichier
data ne met pas à jour les produits déjà créés. On relit les PNG sous
``static/src/img/selection/`` (banque alignée sur ``docs/assets`` MVP02).
"""
import base64
import os

from odoo.api import Environment, SUPERUSER_ID

MOD = "dorevia_ckreyol_marketplace"
SHOWCASE = (
    (f"{MOD}.product_template_ckr_sel_crepes", "static/src/img/selection/ckr_sel_crepes.png"),
    (f"{MOD}.product_template_ckr_sel_biere", "static/src/img/selection/ckr_sel_biere.png"),
    (f"{MOD}.product_template_ckr_sel_sucre", "static/src/img/selection/ckr_sel_sucre.png"),
    (f"{MOD}.product_template_ckr_sel_chips", "static/src/img/selection/ckr_sel_chips.png"),
)


def migrate(cr, version):
    from odoo.modules.module import get_module_path

    env = Environment(cr, SUPERUSER_ID, {})
    root = get_module_path("dorevia_ckreyol_marketplace")
    if not root:
        return
    for xmlid, rel in SHOWCASE:
        p = env.ref(xmlid, raise_if_not_found=False)
        if not p:
            continue
        full = os.path.join(root, rel)
        if not os.path.isfile(full):
            continue
        with open(full, "rb") as f:
            p.sudo().write({"image_1920": base64.b64encode(f.read())})
