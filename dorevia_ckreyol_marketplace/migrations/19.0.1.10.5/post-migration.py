# -*- coding: utf-8 -*-
"""Migration 19.0.1.10.5 (post) — restaure ``featured_collection_id`` si besoin.

Réinjecte la valeur sauvegardée en pré-migration puis supprime la clé
technique de backup.
"""
from odoo.api import Environment, SUPERUSER_ID

KEY = "dorevia_ckreyol_marketplace.featured_collection_id"
BAK = "dorevia_ckreyol_marketplace.__featured_collection_id_mig_backup"


def migrate(cr, version):
    env = Environment(cr, SUPERUSER_ID, {})
    ICP = env["ir.config_parameter"].sudo()
    bak = ICP.search([("key", "=", BAK)], limit=1)
    if not bak:
        return
    val = bak.value
    bak.unlink()
    ICP.set_param(KEY, val)
