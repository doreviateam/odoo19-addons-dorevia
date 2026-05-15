# -*- coding: utf-8 -*-
"""Migration 19.0.1.10.5 (pré) — sauvegarde ``featured_collection_id``.

Exécuté **avant** le chargement des data du module : le retrait du XML
``ckr_featured_collection_parameter`` peut entraîner la suppression de
l'enregistrement ``ir.config_parameter`` (cleanup ``ir.model.data``).
On copie la valeur courante vers une clé technique temporaire ; le
``post-migration`` la réinjecte.
"""
from odoo.api import Environment, SUPERUSER_ID

KEY = "dorevia_ckreyol_marketplace.featured_collection_id"
BAK = "dorevia_ckreyol_marketplace.__featured_collection_id_mig_backup"


def migrate(cr, version):
    env = Environment(cr, SUPERUSER_ID, {})
    ICP = env["ir.config_parameter"].sudo()
    cur = ICP.search([("key", "=", KEY)], limit=1)
    if not cur:
        return
    ICP.set_param(BAK, cur.value)
