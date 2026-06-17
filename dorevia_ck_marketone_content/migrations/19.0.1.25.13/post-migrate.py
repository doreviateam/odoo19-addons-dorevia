# -*- coding: utf-8 -*-
def migrate(cr, version):
    from odoo import api, SUPERUSER_ID

    env = api.Environment(cr, SUPERUSER_ID, {})
    from odoo.addons.dorevia_ck_marketone_content.home_featured import (
        bootstrap_home_featured_products,
    )

    # 25.13 : le prix par variante des cartes vedettes vient des règles pricelist
    # « fixed ». Leur édition n'était pas captée (aucun hook product.pricelist.item)
    # -> prix figé. Le nouveau hook propage désormais ; ce replay répare les
    # snapshots dont le prix pricelist a divergé.
    bootstrap_home_featured_products(env)
