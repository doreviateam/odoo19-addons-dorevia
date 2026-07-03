# -*- coding: utf-8 -*-
"""CATALOG-ARCHI-001 Lot B — qualification produit + signalement orphelins.

ck_is_orphan est un champ calculé stocké : recalculé automatiquement par
l'ORM à l'ajout de la colonne. On journalise ici le résultat pour
traçabilité MOA/QA (produits orphelins existants + produits non qualifiés
actuellement cochés « Afficher sur l'accueil »).
"""
import logging

_logger = logging.getLogger(__name__)


def migrate(cr, version):
    from odoo import api, SUPERUSER_ID

    env = api.Environment(cr, SUPERUSER_ID, {})

    Product = env['product.template'].sudo()
    orphans = Product.search([('ck_is_orphan', '=', True)])
    if orphans:
        _logger.info(
            'CATALOG-ARCHI-001 Lot B : %s produit(s) orphelin(s) détecté(s) — %s',
            len(orphans), ', '.join(orphans.mapped('name')),
        )
    else:
        _logger.info('CATALOG-ARCHI-001 Lot B : aucun produit orphelin détecté.')

    featured = Product.search([('ck_is_featured', '=', True)])
    unqualified = featured.filtered(lambda p: not p._is_ck_qualified_for_public_exposure())
    if unqualified:
        _logger.info(
            'CATALOG-ARCHI-001 Lot B : %s produit(s) « Afficher sur l\'accueil » non '
            'qualifié(s) (fiche minimale incomplète), désormais exclu(s) des '
            'coups de cœur : %s',
            len(unqualified), ', '.join(unqualified.mapped('name')),
        )
