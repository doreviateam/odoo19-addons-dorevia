# -*- coding: utf-8 -*-
"""Reprise Selection → dorevia.ck.card.uom + reconstruction home."""


def migrate(cr, version):
    from odoo import api, SUPERUSER_ID
    from odoo.addons.dorevia_ck_marketone_content.home_featured import (
        bootstrap_home_featured_products,
    )

    env = api.Environment(cr, SUPERUSER_ID, {})
    Uom = env['dorevia.ck.card.uom'].sudo()

    cr.execute(
        """
        SELECT EXISTS (
            SELECT 1
              FROM information_schema.tables
             WHERE table_name = '_ck_card_uom_migration'
        )
        """
    )
    if cr.fetchone()[0]:
        cr.execute(
            "SELECT product_tmpl_id, net_code, ref_code FROM _ck_card_uom_migration"
        )
        rows = cr.fetchall()
        for product_tmpl_id, net_code, ref_code in rows:
            vals = {}
            if net_code:
                net_uom = Uom.search([('code', '=', net_code)], limit=1)
                if net_uom:
                    vals['ck_net_quantity_uom_id'] = net_uom.id
            if ref_code:
                ref_uom = Uom.search([('code', '=', ref_code)], limit=1)
                if ref_uom:
                    vals['ck_reference_price_uom_id'] = ref_uom.id
            if vals:
                env['product.template'].browse(product_tmpl_id).write(vals)
        cr.execute("DROP TABLE _ck_card_uom_migration")

    bootstrap_home_featured_products(env)
    cr.commit()
