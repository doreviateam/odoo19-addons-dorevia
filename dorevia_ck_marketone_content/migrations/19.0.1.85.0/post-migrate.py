# -*- coding: utf-8 -*-
"""CATALOG-ARCHI-001 Lot C — routage catégories + noindex + sitemap filtré.

Aucun backfill de données requis (ck_replacement_category_id est optionnel,
website_indexed est calculé non stocké) — cette migration journalise
uniquement l'impact réel par catégorie racine pour traçabilité MOA/QA.
"""
import logging

from odoo.addons.dorevia_ck_marketone_content.ck_category_routing import (
    ck_category_route_action,
)

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    from odoo import api, SUPERUSER_ID

    env = api.Environment(cr, SUPERUSER_ID, {})

    Category = env['product.public.category'].sudo()
    categories = Category.search([], order='parent_id, sequence, name')
    for category in categories:
        action = ck_category_route_action(category)
        _logger.info(
            'CATALOG-ARCHI-001 Lot C : catégorie "%s" (id=%s) — statut=%s, '
            'route=%s, website_indexed=%s',
            category.name, category.id, category.ck_exposure_status,
            action, category.website_indexed,
        )
