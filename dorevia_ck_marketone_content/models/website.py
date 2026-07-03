# -*- coding: utf-8 -*-
"""CATALOG-ARCHI-001 Lot C — filtrage sitemap catégories via website_indexed.

NB technique : website_sale enregistre la route /shop/category/<...> pour
CHAQUE classe contrôleur de la chaîne d'héritage (dont plusieurs pointent
vers la même fonction sitemap_shop non filtrée, en plus de la nôtre) — la
génération du sitemap (website._enumerate_pages) fusionne les résultats de
TOUTES les fonctions sitemap enregistrées pour un même chemin, donc un
sitemap= personnalisé sur notre seule route ne suffit pas à exclure une
catégorie (l'union avec sitemap_shop non filtré la referait apparaître).
On filtre donc en aval, sur le flux final déjà fusionné, ce qui est robuste
quel que soit le nombre de règles concurrentes.
"""
from odoo import models

from ..ck_category_routing import CK_SITEMAP_CATEGORY_PREFIX


class Website(models.Model):
    _inherit = 'website'

    def _enumerate_pages(self, query_string=None, force=False):
        Category = self.env['product.public.category'].sudo()
        for entry in super()._enumerate_pages(query_string=query_string, force=force):
            loc = entry.get('loc') or ''
            if loc.startswith(CK_SITEMAP_CATEGORY_PREFIX):
                category_id = self._ck_category_id_from_sitemap_loc(loc)
                category = Category.browse(category_id) if category_id else Category.browse()
                if category and not category.website_indexed:
                    continue
            yield entry

    @staticmethod
    def _ck_category_id_from_sitemap_loc(loc):
        """Extrait l'id depuis un slug '/shop/category/<name>-<id>' — 0 si non résolu."""
        tail = loc.rsplit('-', 1)[-1]
        return int(tail) if tail.isdigit() else 0
