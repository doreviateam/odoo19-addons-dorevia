# -*- coding: utf-8 -*-
"""CATALOG-ARCHI-001 Lot C — décision de routage catégorie.

Logique isolée du contrôleur (cf. note_11.md Risque 3 : éviter de disperser
la matrice statut → route dans plusieurs méthodes/templates).

Le filtrage sitemap ne vit pas ici : website_sale enregistre la route
/shop/category/<...> pour plusieurs classes contrôleur de sa chaîne
d'héritage, dont certaines pointent vers sitemap_shop non filtré en plus de
la nôtre — passer un sitemap= personnalisé sur notre seule route ne suffit
donc pas (fusion avec les autres résultats non filtrés). Voir
models/website.py::Website._enumerate_pages pour le filtrage réel, appliqué
en aval sur le flux déjà fusionné.
"""
from odoo.addons.website_sale.const import SHOP_PATH

CK_CATEGORY_REDIRECT_STATUSES = ('promise', 'hidden')
CK_SITEMAP_CATEGORY_PREFIX = f'{SHOP_PATH}/category/'


def ck_category_route_action(category):
    """Matrice V1 note_11.md §2/§5 — action de routage pour une catégorie.

    Retourne un dict :
    - {'action': 'render'} — laisser la route standard s'exécuter (200).
    - {'action': 'redirect', 'url': str, 'code': 301|302}
    - {'action': 'notfound'}
    """
    status = category.ck_exposure_status
    if status == 'active':
        return {'action': 'render'}
    if status in CK_CATEGORY_REDIRECT_STATUSES:
        return {'action': 'redirect', 'url': SHOP_PATH, 'code': 302}
    if status == 'draft':
        return {'action': 'notfound'}
    if status == 'archived':
        replacement = category.ck_replacement_category_id
        if replacement:
            from .nav_mega_menu import _category_shop_url
            url = _category_shop_url(category.env, replacement)
            return {'action': 'redirect', 'url': url or SHOP_PATH, 'code': 301}
        return {'action': 'notfound'}
    return {'action': 'render'}
