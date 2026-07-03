# -*- coding: utf-8 -*-
"""Extension contrôleur shop — injection des variables rebond (Note 07 Lot C)
et gouvernance des routes catégories (CATALOG-ARCHI-001 Lot C)."""

from odoo.http import request, route
from werkzeug.exceptions import NotFound

from odoo.addons.website_sale.const import SHOP_PATH
from odoo.addons.website_sale.controllers.main import WebsiteSale

from odoo.addons.dorevia_ck_marketone_content.ck_category_routing import (
    ck_category_route_action,
)
from odoo.addons.dorevia_ck_marketone_content.shop_filter_groups import (
    build_ck_shop_filter_tag_groups,
    ck_shop_filter_active_tag_ids,
)
from odoo.addons.dorevia_ck_marketone_content.shop_rebound import (
    CK_REBOUND_CTA_LABEL,
    CK_REBOUND_CTA_URL,
    CK_REBOUND_MESSAGE,
    ck_should_show_rebound,
    ck_sparse_grid_class,
)
from odoo.addons.dorevia_ck_marketone_content.shop_toolbar import (
    filter_ck_toolbar_categories,
)


class CkWebsiteSaleController(WebsiteSale):

    @route(
        [
            SHOP_PATH,
            f'{SHOP_PATH}/page/<int:page>',
            f'{SHOP_PATH}/category/<model("product.public.category"):category>',
            f'{SHOP_PATH}/category/<model("product.public.category"):category>/page/<int:page>',
        ],
        type='http',
        auth='public',
        website=True,
        sitemap=WebsiteSale.sitemap_shop,
        handle_params_access_error=lambda e, **kwargs: NotFound.code,
    )
    def shop(self, page=0, category=None, search='', min_price=0.0, max_price=0.0, tags='', **post):
        """CATALOG-ARCHI-001 Lot C — 200/301/302/404 selon ck_exposure_status.

        Redéclaration minimale (note_11.md Risque 3) : la décision de
        routage est isolée dans ck_category_route_action(), aucune logique
        de statut dispersée ici. `/shop` (category=None) n'est jamais
        gouverné comme une catégorie (note_10.md §13.1).

        Le sitemap réutilise WebsiteSale.sitemap_shop tel quel : le filtrage
        website_indexed se fait en aval sur le flux déjà fusionné (voir
        models/website.py::Website._enumerate_pages), pas ici — website_sale
        enregistre cette route pour plusieurs classes contrôleur de sa
        chaîne d'héritage, donc un sitemap= propre à cette seule route ne
        suffirait pas à exclure quoi que ce soit (fusion avec les autres
        résultats non filtrés au niveau du générateur de sitemap).
        """
        if category and not isinstance(category, str):
            action = ck_category_route_action(category)
            if action['action'] == 'redirect':
                return request.redirect(action['url'], code=action['code'])
            if action['action'] == 'notfound':
                raise NotFound()
        return super().shop(
            page=page, category=category, search=search,
            min_price=min_price, max_price=max_price, tags=tags, **post,
        )

    def _get_additional_shop_values(self, values, **kwargs):
        result = super()._get_additional_shop_values(values, **kwargs)
        result['ck_show_rebound'] = ck_should_show_rebound(values, kwargs)
        result['ck_sparse_grid_class'] = ck_sparse_grid_class(values)
        if result['ck_show_rebound']:
            result.update({
                'ck_rebound_message': CK_REBOUND_MESSAGE,
                'ck_rebound_cta_url': CK_REBOUND_CTA_URL,
                'ck_rebound_cta_label': CK_REBOUND_CTA_LABEL,
            })
        for key in ('categories', 'category_entries'):
            if key in values:
                result[key] = filter_ck_toolbar_categories(values[key])
        all_tags = values.get('all_tags')
        if all_tags is not None:
            active_tag_ids = ck_shop_filter_active_tag_ids(values, kwargs)
            grouped_tags = all_tags.filtered('ck_shop_filter_group')
            result['all_tags'] = grouped_tags
            result['ck_shop_filter_tag_groups'] = build_ck_shop_filter_tag_groups(
                grouped_tags,
                active_tag_ids=active_tag_ids,
            )
            result['ck_shop_filter_has_active'] = bool(
                active_tag_ids
                or values.get('attrib_set')
                or values.get('min_price')
                or values.get('max_price')
            )
        return result
