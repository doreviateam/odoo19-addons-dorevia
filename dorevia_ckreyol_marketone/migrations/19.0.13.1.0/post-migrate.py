# -*- coding: utf-8 -*-
"""TICKET_MARKETONE_ORIGINE_REUNION_DEDUP — fusion valeurs Origines La Réunion / Reunion."""


def migrate(cr, version):
    from odoo import api, SUPERUSER_ID

    env = api.Environment(cr, SUPERUSER_ID, {})
    from odoo.addons.dorevia_ckreyol_marketone.models.marketone_origin_reunion_dedup import (
        marketone_dedup_reunion_origin_values,
    )

    marketone_dedup_reunion_origin_values(env)
