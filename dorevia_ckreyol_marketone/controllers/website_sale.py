# -*- coding: utf-8 -*-
"""Portes catalogue Marketone — extension native ``WebsiteSale`` (Odoo 19)."""

from odoo.fields import Domain
from odoo.http import request, route

from odoo.addons.website_sale.controllers.main import WebsiteSale

MARKETONE_MODE_FEATURED = "featured"
MARKETONE_MODE_ORIGIN = "origin"
MARKETONE_MODE_PRIORITY = ("pack", "promo", "featured", "origin", "collection")
MARKETONE_IMPLEMENTED_MODES = frozenset({MARKETONE_MODE_FEATURED, MARKETONE_MODE_ORIGIN})

MARKETONE_FEATURED_PARAM = "dorevia_ckreyol_marketone.featured_public_category_id"
MARKETONE_ORIGIN_PARAM = "marketone_origin"
MARKETONE_CATEGORY_PARAM = "marketone_category"

MARKETONE_FEATURED_CANONICAL_QUERY = "/shop?marketone_mode=featured"
MARKETONE_ORIGIN_CANONICAL_QUERY = "/shop?marketone_mode=origin"


class MarketoneRedirectBareShop(Exception):
    """Repli vers ``/shop`` sans paramètres porte (origine invalide)."""


def _marketone_mode_values(mapping):
    """Valeurs ``marketone_mode`` depuis post ou query HTTP."""
    values = []
    if request and getattr(request, "httprequest", None):
        values.extend(request.httprequest.args.getlist("marketone_mode"))
    raw = (mapping or {}).get("marketone_mode")
    if raw:
        if isinstance(raw, (list, tuple)):
            values.extend(raw)
        else:
            values.append(raw)
    out = []
    seen = set()
    for item in values:
        if item and item not in seen:
            seen.add(item)
            out.append(item)
    return out


def _marketone_effective_mode(mapping):
    """Un seul mode actif — priorité C3.4 sur les modes implémentés."""
    modes = set(_marketone_mode_values(mapping))
    for mode in MARKETONE_MODE_PRIORITY:
        if mode in modes and mode in MARKETONE_IMPLEMENTED_MODES:
            return mode
    return None


def _marketone_read_origin_slugs(mapping):
    values = []
    if request and getattr(request, "httprequest", None):
        values.extend(request.httprequest.args.getlist(MARKETONE_ORIGIN_PARAM))
    raw = (mapping or {}).get(MARKETONE_ORIGIN_PARAM)
    if raw:
        if isinstance(raw, (list, tuple)):
            values.extend(raw)
        else:
            values.append(raw)
    out = []
    seen = set()
    for item in values:
        if item and item not in seen:
            seen.add(item)
            out.append(item)
    return out


def _marketone_read_category_slugs(mapping):
    """Slugs facette catégories depuis la query (répétable)."""
    values = []
    if request and getattr(request, "httprequest", None):
        values.extend(request.httprequest.args.getlist(MARKETONE_CATEGORY_PARAM))
    raw = (mapping or {}).get(MARKETONE_CATEGORY_PARAM)
    if raw:
        if isinstance(raw, (list, tuple)):
            values.extend(raw)
        else:
            values.append(raw)
    out = []
    seen = set()
    for item in values:
        if item and item not in seen:
            seen.add(item)
            out.append(item)
    return out


def _marketone_category_slugs_for_request(mapping, path_category=None):
    """Slugs actifs : query d'abord, sinon catégorie chemin si principale."""
    slugs = _marketone_read_category_slugs(mapping)
    if slugs:
        return slugs
    if not path_category:
        return []
    ir_http = request.env["ir.http"].sudo()
    return [ir_http._slug(path_category)]


def _marketone_resolve_category_facet(mapping, path_category=None):
    """(categories, facet_requested, facet_invalid)."""
    website = request.website if request else None
    slugs = _marketone_category_slugs_for_request(mapping, path_category=path_category)
    if not slugs:
        return (
            request.env["product.public.category"].browse(),
            False,
            False,
        )
    categories = request.env["product.public.category"]._marketone_resolve_primary_categories_from_slugs(
        slugs, website=website
    )
    ir_http = request.env["ir.http"].sudo()
    want = set(slugs)
    got = {ir_http._slug(rec) for rec in categories}
    return (categories, True, want != got)


def _marketone_apply_category_facet_options(options, mapping, path_category=None):
    """Facette sidebar principales — OU via ``_search_get_detail``."""
    categories, facet_requested, facet_invalid = _marketone_resolve_category_facet(
        mapping, path_category=path_category
    )
    if not facet_requested:
        return
    if facet_invalid:
        options["marketone_category_invalid"] = True
        return
    options["marketone_public_category_ids"] = list(categories.ids)


def _marketone_resolve_featured_public_category(env):
    raw = env["ir.config_parameter"].sudo().get_param(MARKETONE_FEATURED_PARAM)
    if not raw or not str(raw).strip().isdigit():
        return env["product.public.category"].browse()
    return env["product.public.category"].sudo().browse(int(raw)).exists()


def _marketone_resolve_origin_profiles(mapping):
    """(profiles, facet_requested, facet_invalid)."""
    slugs = _marketone_read_origin_slugs(mapping)
    if not slugs:
        return (
            request.env["marketone.shop.origin"].browse(),
            False,
            False,
        )
    website = request.website if request else None
    profiles = (
        request.env["marketone.shop.origin"]
        .sudo()
        ._marketone_resolve_published_slugs(slugs, website=website)
    )
    return (profiles, True, not profiles)


def _marketone_apply_mode_options(options, mapping):
    """Injecte les options featured / origin selon le mode effectif unique."""
    mode = _marketone_effective_mode(mapping)
    if mode == MARKETONE_MODE_FEATURED:
        category_rec = _marketone_resolve_featured_public_category(request.env)
        options["marketone_featured_only"] = True
        if category_rec:
            options["marketone_featured_category_id"] = category_rec.id
        else:
            options["marketone_featured_category_invalid"] = True
        return

    if mode != MARKETONE_MODE_ORIGIN:
        return

    profiles, facet_requested, facet_invalid = _marketone_resolve_origin_profiles(
        mapping
    )
    if facet_invalid:
        raise MarketoneRedirectBareShop()
    options["marketone_origin_mode"] = True
    if facet_requested:
        options["marketone_origin_attribute_value_ids"] = (
            profiles.mapped("attribute_value_id").ids
        )
    else:
        options["marketone_origin_only"] = True


def _marketone_canonical_category_slugs(mapping, path_category=None):
    website = request.website if request else None
    categories, requested, _invalid = _marketone_resolve_category_facet(
        mapping, path_category=path_category
    )
    if not requested or not categories:
        return []
    ir_http = request.env["ir.http"].sudo()
    return sorted({ir_http._slug(rec) for rec in categories})


class WebsiteSaleMarketone(WebsiteSale):
    """Portes catalogue : Incontournables (6.1) et Origines (6.2)."""

    @route()
    def shop(self, page=0, category=None, search="", min_price=0.0, max_price=0.0, tags="", **post):
        try:
            return super().shop(
                page=page,
                category=category,
                search=search,
                min_price=min_price,
                max_price=max_price,
                tags=tags,
                **post,
            )
        except MarketoneRedirectBareShop:
            return request.redirect("/shop", code=302)

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
        _marketone_apply_category_facet_options(
            options, post, path_category=category
        )
        _marketone_apply_mode_options(options, post)
        return options

    def _get_shop_domain(
        self,
        search,
        category,
        attribute_value_dict,
        search_in_description=True,
    ):
        mapping = request.httprequest.args
        query_categories, facet_requested, facet_invalid = _marketone_resolve_category_facet(
            mapping, path_category=category
        )
        path_category = None if facet_requested else category

        domain = super()._get_shop_domain(
            search,
            path_category,
            attribute_value_dict,
            search_in_description=search_in_description,
        )

        if facet_requested:
            if facet_invalid:
                return Domain.AND([domain, Domain([("id", "=", 0)])])
            domain = Domain.AND(
                [
                    domain,
                    Domain([("public_categ_ids", "in", query_categories.ids)]),
                ]
            )

        mode = _marketone_effective_mode(mapping)
        if mode == MARKETONE_MODE_FEATURED:
            category_rec = _marketone_resolve_featured_public_category(request.env)
            if not category_rec:
                return Domain.AND([domain, Domain([("id", "=", 0)])])
            return Domain.AND(
                [
                    domain,
                    Domain([("public_categ_ids", "in", [category_rec.id])]),
                ]
            )
        if mode != MARKETONE_MODE_ORIGIN:
            return domain
        profiles, origin_facet_requested, _invalid = _marketone_resolve_origin_profiles(
            mapping
        )
        if origin_facet_requested and profiles:
            value_ids = profiles.mapped("attribute_value_id").ids
            return Domain.AND(
                [
                    domain,
                    Domain([("attribute_line_ids.value_ids", "in", value_ids)]),
                ]
            )
        return domain

    def _get_additional_shop_values(self, values, **kwargs):
        result = super()._get_additional_shop_values(values, **kwargs)
        path_category = (values or {}).get("category")
        result["marketone_primary_public_categories"] = request.env[
            "product.public.category"
        ]._marketone_primary_public_categories(website=request.website)
        result["marketone_shop_sidebar_active_category_slugs"] = (
            _marketone_canonical_category_slugs(kwargs, path_category=path_category)
        )
        mode = _marketone_effective_mode(kwargs)
        search_count = (values or {}).get("search_count") or 0

        result["marketone_featured_mode"] = mode == MARKETONE_MODE_FEATURED
        result["marketone_featured_empty"] = False
        result["marketone_featured_category"] = request.env[
            "product.public.category"
        ].browse()
        if result["marketone_featured_mode"]:
            category_rec = _marketone_resolve_featured_public_category(request.env)
            result["marketone_featured_category"] = category_rec
            result["marketone_featured_empty"] = not category_rec or not search_count

        result["marketone_origin_mode"] = mode == MARKETONE_MODE_ORIGIN
        result["marketone_origin_empty"] = False
        result["marketone_origin_profiles"] = request.env[
            "marketone.shop.origin"
        ].browse()
        result["marketone_origin_title"] = "Origines"
        result["marketone_culture_url"] = False
        if result["marketone_origin_mode"]:
            profiles, facet_requested, _invalid = _marketone_resolve_origin_profiles(
                kwargs
            )
            result["marketone_origin_profiles"] = profiles
            if len(profiles) == 1:
                result["marketone_origin_title"] = (
                    profiles[0].display_name_visitor or "Origines"
                )
            result["marketone_origin_empty"] = bool(
                facet_requested and profiles and not search_count
            )
            if facet_requested and len(profiles) == 1:
                result["marketone_culture_url"] = profiles[
                    0
                ]._marketone_culture_url()
        return result

    @route(
        "/incontournables",
        type="http",
        auth="public",
        website=True,
        sitemap=False,
    )
    def marketone_incontournables_redirect(self, **kwargs):
        return request.redirect(MARKETONE_FEATURED_CANONICAL_QUERY, code=301)

    @route(
        "/origines",
        type="http",
        auth="public",
        website=True,
        sitemap=False,
    )
    def marketone_origines_redirect(self, **kwargs):
        return request.redirect(MARKETONE_ORIGIN_CANONICAL_QUERY, code=301)
