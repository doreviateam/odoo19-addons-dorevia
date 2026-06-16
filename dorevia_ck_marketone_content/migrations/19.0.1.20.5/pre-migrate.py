# -*- coding: utf-8 -*-
"""Sauvegarde des anciennes unités Selection avant passage Many2one."""


def migrate(cr, version):
    cr.execute(
        """
        SELECT EXISTS (
            SELECT 1
              FROM information_schema.columns
             WHERE table_name = 'product_template'
               AND column_name = 'ck_net_quantity_uom'
        )
        """
    )
    if not cr.fetchone()[0]:
        return

    cr.execute("DROP TABLE IF EXISTS _ck_card_uom_migration")
    cr.execute(
        """
        CREATE TABLE _ck_card_uom_migration AS
        SELECT id AS product_tmpl_id,
               ck_net_quantity_uom AS net_code,
               ck_reference_price_uom AS ref_code
          FROM product_template
         WHERE ck_net_quantity_uom IS NOT NULL
            OR ck_reference_price_uom IS NOT NULL
        """
    )
