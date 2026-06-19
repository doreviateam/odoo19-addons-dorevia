# -*- coding: utf-8 -*-
"""Lot 1 fiche produit — retire l'ancienne vue chips hors bloc achat."""


def migrate(cr, version):
    cr.execute(
        "DELETE FROM ir_ui_view WHERE key = %s",
        ('dorevia_ck_theme.product_ck_chips',),
    )
