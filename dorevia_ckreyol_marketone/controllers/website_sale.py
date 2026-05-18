# -*- coding: utf-8 -*-
"""Porte catalogue Incontournables — extension native ``WebsiteSale`` (Odoo 19)."""

from odoo.fields import Domain
from odoo.http import request, route

from odoo.addons.website_sale.controllers.main import WebsiteSale

MARKETONE_MODE_FEATURED = "featured"
MARKETONE_FEATURED_PARAM = "dorevia_ckreyol_marketone.featured_public_category_id"
MARKETONE_FEATURED_CANONICAL_QUERY = "/shop?marketone_mode=featured"


def _marketone_featured_mode_from_mapping(mapping):
    """Retourne ``featured`` si whitelist, sinon ``None`` (params inconnus ignorés)."""
    mode = (mapping or {}).get("marketone_mode")
    if isinstance(mode, list):
        mode = mode[0] if mode else None
    if mode == MARKETONE_MODE_FEATURED:
        return MARKETONE_MODE_FEATURED
    return None


def _marketone_resolve_featured_public_category(env):
    """Catégorie publique configurée pour la porte Incontournables."""
    raw = env["ir.config_parameter"].sudo().get_param(MARKETONE_FEATURED_PARAM)
    if not raw or not str(raw).strip().isdigit():
        return env["product.public.category"].browse()
    category = env["product.public.category"].sudo().browse(int(raw)).exists()
    return category


class WebsiteSaleMarketone(WebsiteSale):
    """Une porte catalogue : ``marketone_mode=featured`` + alias ``/incontournables``."""

    def _get_search_options(
        self,
        category=None,
        attribute_value_dict=None,
        tags=None,
        min_price=0.0,
        max_price=0.0,
        conversion_rate=1,
        **post,
    ):
        options = super()._get_search_options(
            category=category,
            attribute_value_dict=attribute_value_dict,
            tags=tags,
            min_price=min_price,
            max_price=max_price,
            conversion_rate=conversion_rate,
            **post,
        )
        if _marketone_featured_mode_from_mapping(post) == MARKETONE_MODE_FEATURED:
            category_rec = _marketone_resolve_featured_public_category(request.env)
            options["marketone_featured_only"] = True
            if category_rec:
                options["marketone_featured_category_id"] = category_rec.id
            else:
                options["marketone_featured_category_invalid"] = True
        return options

    def _get_shop_domain(
        self,
        search,
        category,
        attribute_value_dict,
        search_in_description=True,
    ):
        domain = super()._get_shop_domain(
            search,
            category,
            attribute_value_dict,
            search_in_description=search_in_description,
        )
        mode = _marketone_featured_mode_from_mapping(request.httprequest.args)
        if mode != MARKETONE_MODE_FEATURED:
            return domain
        category_rec = _marketone_resolve_featured_public_category(request.env)
        if not category_rec:
            return Domain.AND([domain, Domain([("id", "=", 0)])])
        return Domain.AND(
            [
                domain,
                Domain([("public_categ_ids", "in", [category_rec.id])]),
            ]
        )

    def _get_additional_shop_values(self, values, **kwargs):
        result = super()._get_additional_shop_values(values, **kwargs)
        featured_mode = (
            _marketone_featured_mode_from_mapping(kwargs) == MARKETONE_MODE_FEATURED
        )
        result["marketone_featured_mode"] = featured_mode
        result["marketone_featured_empty"] = False
        result["marketone_featured_category"] = request.env[
            "product.public.category"
        ].browse()
        if featured_mode:
            category_rec = _marketone_resolve_featured_public_category(request.env)
            result["marketone_featured_category"] = category_rec
            search_count = (values or {}).get("search_count") or 0
            result["marketone_featured_empty"] = not category_rec or not search_count
        return result

    @route(
        "/incontournables",
        type="http",
        auth="public",
        website=True,
        sitemap=False,
    )
    def marketone_incontournables_redirect(self, **kwargs):
        """Alias SEO — redirection permanente vers l'URL canonique de la porte."""
        return request.redirect(MARKETONE_FEATURED_CANONICAL_QUERY, code=301)
