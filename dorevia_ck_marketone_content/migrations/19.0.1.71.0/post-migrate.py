# -*- coding: utf-8 -*-
"""CK-PROD-001 — Passe Tambour Gro Ka en mode « Sur commande »."""
import logging

_logger = logging.getLogger(__name__)

TAMBOUR_GROKA_NAME = 'Tambour Gro Ka'


def migrate(cr, version):
    from odoo import api, SUPERUSER_ID

    env = api.Environment(cr, SUPERUSER_ID, {})
    product = env['product.template'].search(
        [('name', '=', TAMBOUR_GROKA_NAME)], limit=1,
    )
    if not product:
        _logger.warning(
            'CK-PROD-001 : produit « %s » introuvable — migration ignorée.',
            TAMBOUR_GROKA_NAME,
        )
        return
    if product.ck_availability_mode != 'order':
        product.ck_availability_mode = 'order'
        _logger.info('CK-PROD-001 : « %s » passé en mode order.', TAMBOUR_GROKA_NAME)
