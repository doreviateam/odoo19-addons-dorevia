# -*- coding: utf-8 -*-

"""Initialise date de situation pour les points existants (alignée sur le début d'exercice)."""


def migrate(cr, version):
    cr.execute(
        """
        UPDATE dorevia_cash_guard
        SET situation_date = date_from
        WHERE situation_date IS NULL
          AND date_from IS NOT NULL
        """
    )
