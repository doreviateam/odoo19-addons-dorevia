# -*- coding: utf-8 -*-
"""BO polish — quantité nette vide au lieu de 0,00 par défaut."""


def migrate(cr, version):
    cr.execute(
        """
        UPDATE product_template
           SET ck_net_quantity = NULL
         WHERE ck_net_quantity IS NOT NULL
           AND ck_net_quantity = 0
        """
    )
