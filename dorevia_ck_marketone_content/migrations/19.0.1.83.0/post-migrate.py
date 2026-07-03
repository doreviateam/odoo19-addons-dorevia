# -*- coding: utf-8 -*-
"""CATALOG-ARCHI-001 Lot A — ck_exposure_status + resync nav/footer catalogue.

Le nouveau champ ck_exposure_status prend le défaut 'active' pour toutes les
catégories existantes (posé par l'ORM à l'ajout de colonne) : aucune
régression de nav au déploiement — l'éligibilité réelle continue de dépendre
du nombre de produits qualifiés via _is_ck_exposable(). On resynchronise nav
et footer pour appliquer immédiatement la règle plus stricte (seuil 3), et on
journalise le résultat par catégorie racine pour traçabilité MOA.
"""
import logging

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    from odoo import api, SUPERUSER_ID

    env = api.Environment(cr, SUPERUSER_ID, {})

    from odoo.addons.dorevia_ck_marketone_content.nav_sync import (
        bootstrap_ck_catalogue_navigation,
    )
    from odoo.addons.dorevia_ck_marketone_content.footer_boutique import (
        bootstrap_footer_boutique_links,
    )

    bootstrap_ck_catalogue_navigation(env)
    bootstrap_footer_boutique_links(env)

    Category = env['product.public.category'].sudo()
    root_categories = Category.search([('parent_id', '=', False)], order='sequence, name')
    for category in root_categories:
        exposable = category._is_ck_exposable()
        count = category._ck_exposable_products_count()
        _logger.info(
            'CATALOG-ARCHI-001 Lot A : catégorie "%s" (id=%s) — statut=%s, '
            'produits qualifiés=%s, exposable=%s',
            category.name, category.id, category.ck_exposure_status, count, exposable,
        )
