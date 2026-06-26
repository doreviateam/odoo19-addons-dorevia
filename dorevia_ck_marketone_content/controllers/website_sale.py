# -*- coding: utf-8 -*-
"""Extension contrôleur shop — injection des variables rebond (Note 07 Lot C)."""

from odoo.addons.website_sale.controllers.main import WebsiteSale

from odoo.addons.dorevia_ck_marketone_content.shop_rebound import (
    CK_REBOUND_CTA_LABEL,
    CK_REBOUND_CTA_URL,
    CK_REBOUND_MESSAGE,
    ck_should_show_rebound,
)


class CkWebsiteSaleController(WebsiteSale):

    def _get_additional_shop_values(self, values, **kwargs):
        result = super()._get_additional_shop_values(values, **kwargs)
        result['ck_show_rebound'] = ck_should_show_rebound(values, kwargs)
        if result['ck_show_rebound']:
            result.update({
                'ck_rebound_message': CK_REBOUND_MESSAGE,
                'ck_rebound_cta_url': CK_REBOUND_CTA_URL,
                'ck_rebound_cta_label': CK_REBOUND_CTA_LABEL,
            })
        return result
