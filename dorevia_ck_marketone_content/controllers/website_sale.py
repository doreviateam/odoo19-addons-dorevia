# -*- coding: utf-8 -*-
"""Extension contrôleur shop — injection des variables rebond (Note 07 Lot C)."""

from odoo.addons.website_sale.controllers.main import WebsiteSale

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
