# -*- coding: utf-8 -*-
"""Portes catalogue Marketone — extension native ``WebsiteSale`` (Odoo 19)."""

from datetime import date

from odoo.fields import Domain
from odoo.http import request, route
from odoo.tools import float_round, formatLang

from odoo.addons.website.controllers.main import QueryURL
from odoo.addons.website_sale.controllers.main import WebsiteSale

MARKETONE_MODE_FEATURED = "featured"
MARKETONE_MODE_ORIGIN = "origin"
MARKETONE_MODE_PRIORITY = ("pack", "promo", "featured", "origin", "collection")
MARKETONE_IMPLEMENTED_MODES = frozenset({MARKETONE_MODE_FEATURED, MARKETONE_MODE_ORIGIN})

MARKETONE_FEATURED_PARAM = "dorevia_ckreyol_marketone.featured_public_category_id"
MARKETONE_ORIGIN_PARAM = "marketone_origin"
MARKETONE_CATEGORY_PARAM = "marketone_category"
MARKETONE_COLLECTION_PARAM = "marketone_collection"

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


def _marketone_read_collection_slugs(mapping):
    """Slugs facette collections depuis la query (répétable)."""
    values = []
    if request and getattr(request, "httprequest", None):
        values.extend(request.httprequest.args.getlist(MARKETONE_COLLECTION_PARAM))
    raw = (mapping or {}).get(MARKETONE_COLLECTION_PARAM)
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


def _marketone_resolve_collection_facet(mapping):
    """(collections, facet_requested) — slugs invalides ignorés (Lot B B2)."""
    slugs = _marketone_read_collection_slugs(mapping)
    if not slugs:
        return (
            request.env["marketone.shop.collection"].browse(),
            False,
        )
    website = request.website if request else None
    collections = request.env[
        "marketone.shop.collection"
    ]._marketone_resolve_published_slugs(slugs, website=website)
    return (collections, True)


def _marketone_apply_collection_facet_options(options, mapping):
    """Facette sidebar collections — OU via ``_search_get_detail``."""
    if "collection" in _marketone_sidebar_facet_omit_get():
        return
    collections, facet_requested = _marketone_resolve_collection_facet(mapping)
    if not facet_requested or not collections:
        return
    options["marketone_collection_ids"] = list(collections.ids)


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


def _marketone_sidebar_facet_omit_get():
    """Facettes neutralisées (ex. comptage catégories sidebar — relaxation multi OR)."""
    omit = getattr(request, "_marketone_sidebar_facet_omit", None) if request else None
    return frozenset(omit) if omit else frozenset()


def _marketone_apply_category_facet_options(options, mapping, path_category=None):
    """Facette sidebar principales — OU via ``_search_get_detail``."""
    if "category" in _marketone_sidebar_facet_omit_get():
        return
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


def _marketone_canonical_collection_slugs(mapping):
    collections, requested = _marketone_resolve_collection_facet(mapping)
    if not requested or not collections:
        return []
    return list(collections.mapped("slug"))


def _marketone_attrib_values_to_query_list(attrib_values):
    """Dict ``attrib_values`` Odoo → liste ``attribute_values`` pour ``keep()``."""
    items = []
    for attr_id, value_ids in (attrib_values or {}).items():
        for value_id in value_ids:
            items.append(f"{attr_id}-{value_id}")
    return items


def _marketone_is_filtering_by_price(values):
    """Aligné ``website_sale.products`` — ``isFilteringByPrice``.

    Sans ``available_min_price`` / ``available_max_price``, les bornes catalogue
    ne doivent pas être traitées comme un filtre prix actif (R1 UX-1).
    """
    if not values or "min_price" not in values:
        return False
    if "available_min_price" not in values or "available_max_price" not in values:
        return False
    min_price = float_round(values.get("min_price") or 0.0, 2)
    max_price = float_round(values.get("max_price") or 0.0, 2)
    available_min = float_round(values["available_min_price"] or 0.0, 2)
    available_max = float_round(values["available_max_price"] or 0.0, 2)
    return min_price != available_min or max_price != available_max


def _marketone_should_preserve_price_in_urls(values, kwargs):
    """True seulement si le prix est un filtre **explicite** (chip Prix / query / slider actif).

    Odoo remplit souvent ``values['min_price']`` avec les bornes du jeu filtré
    (ex. un seul produit à 6,80 €) sans filtre prix utilisateur — ne pas propager
    ces valeurs dans les ``remove_url`` des autres facettes (R1).
    """
    if _marketone_is_filtering_by_price(values):
        return True
    if request and getattr(request, "httprequest", None):
        args = request.httprequest.args
        for key in ("min_price", "max_price"):
            raw = args.get(key)
            if raw is None or raw == "":
                continue
            try:
                if float(raw):
                    return True
            except (TypeError, ValueError):
                return True
    return False


def _marketone_price_chip_label(env, values):
    """Libellé chip prix — préfixe « Prix » (MOA UX-1)."""
    currency = request.website.currency_id
    min_p = values.get("min_price") or 0.0
    max_p = values.get("max_price") or 0.0
    min_label = formatLang(env, min_p, currency_obj=currency, digits=0)
    max_label = formatLang(env, max_p, currency_obj=currency, digits=0)
    if min_label == max_label:
        return f"Prix : {min_label}"
    return f"Prix : {min_label} — {max_label}"


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
        _marketone_apply_collection_facet_options(options, post)
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
        omit_category = "category" in _marketone_sidebar_facet_omit_get()
        query_categories, facet_requested, facet_invalid = _marketone_resolve_category_facet(
            mapping, path_category=category
        )
        if omit_category:
            facet_requested = False
            path_category = None
        else:
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

        omit_collection = "collection" in _marketone_sidebar_facet_omit_get()
        query_collections, collection_facet_requested = _marketone_resolve_collection_facet(
            mapping
        )
        if omit_collection:
            collection_facet_requested = False
        if collection_facet_requested and query_collections:
            product_ids = list(set(query_collections.mapped("product_ids").ids))
            if product_ids:
                domain = Domain.AND(
                    [domain, Domain([("id", "in", product_ids)])]
                )
            else:
                domain = Domain.AND([domain, Domain([("id", "=", 0)])])

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

    def _shop_get_query_url_kwargs(
        self, search, min_price, max_price, order=None, tags=None, **kwargs
    ):
        """Inclure facettes Marketone + ``attribute_values`` courants dans ``keep()``."""
        result = super()._shop_get_query_url_kwargs(
            search, min_price, max_price, order=order, tags=tags, **kwargs
        )
        raw_attrib = kwargs.get("attribute_values")
        if raw_attrib:
            if isinstance(raw_attrib, (list, tuple)):
                result["attribute_values"] = list(raw_attrib)
            else:
                result["attribute_values"] = raw_attrib
        elif request and getattr(request, "httprequest", None):
            args_vals = request.httprequest.args.getlist("attribute_values")
            if args_vals:
                result["attribute_values"] = args_vals
        slugs = _marketone_read_category_slugs(kwargs)
        if slugs:
            result[MARKETONE_CATEGORY_PARAM] = slugs
        coll_slugs = _marketone_canonical_collection_slugs(kwargs)
        if coll_slugs:
            result[MARKETONE_COLLECTION_PARAM] = coll_slugs
        return result

    def _marketone_shop_search_product_without_facets(self, values, kwargs, omit_facets):
        """``search_product`` aligné grille, sans facettes listées (sidebar C4)."""
        website = request.website
        current = values or {}
        wk = dict(kwargs or {})
        for key in ("search", "tags", "min_price", "max_price", "order"):
            if current.get(key) is not None and wk.get(key) in (None, ""):
                wk[key] = current.get(key)
        search = (
            wk.get("search")
            or current.get("original_search")
            or current.get("search")
            or ""
        )
        min_price = wk.get("min_price")
        if min_price in (None, ""):
            min_price = current.get("min_price") or 0.0
        max_price = wk.get("max_price")
        if max_price in (None, ""):
            max_price = current.get("max_price") or 0.0
        if not _marketone_should_preserve_price_in_urls(current, wk):
            min_price = 0.0
            max_price = 0.0
        attribute_value_dict = current.get("attrib_values") or {}
        if not attribute_value_dict:
            raw_attrib = wk.get("attribute_values")
            if raw_attrib:
                attribute_value_dict = self._get_attribute_value_dict(raw_attrib)
        tags = wk.get("tags")
        if tags is None:
            tags = current.get("tags")
        company_currency = website.company_id.sudo().currency_id
        conversion_rate = request.env["res.currency"]._get_conversion_rate(
            company_currency,
            website.currency_id,
            website.company_id,
            date.today(),
        )
        post = dict(wk)
        for key in (
            "tags",
            "min_price",
            "max_price",
            "search",
            "category",
            "attribute_values",
            "attribute_value_dict",
            "conversion_rate",
            "display_currency",
            "order",
        ):
            post.pop(key, None)
        try:
            request._marketone_sidebar_facet_omit = frozenset(omit_facets)
            options = self._get_search_options(
                category=None,
                attribute_value_dict=attribute_value_dict,
                tags=tags,
                min_price=float(min_price or 0),
                max_price=float(max_price or 0),
                conversion_rate=conversion_rate,
                display_currency=website.currency_id,
                **post,
            )
            if search:
                post["search"] = search
            _fuzzy, _count, search_product = self._shop_lookup_products(
                options, post, search, website
            )
            return search_product
        finally:
            if hasattr(request, "_marketone_sidebar_facet_omit"):
                delattr(request, "_marketone_sidebar_facet_omit")

    def _marketone_shop_search_product_without_category_facet(self, values, kwargs):
        return self._marketone_shop_search_product_without_facets(
            values, kwargs, {"category"}
        )

    def _marketone_shop_search_product_without_collection_facet(self, values, kwargs):
        return self._marketone_shop_search_product_without_facets(
            values, kwargs, {"collection"}
        )

    def _marketone_shop_keep_url(self, values, kwargs, path_category=None, **overrides):
        """URL catalogue via ``QueryURL`` + ``_shop_get_query_url_kwargs`` (UX-1 chips)."""
        vals = values or {}
        mapping = dict(kwargs or {})
        search = (
            mapping.pop("search", None)
            or vals.get("search")
            or vals.get("original_search")
            or ""
        )
        preserve_price = _marketone_should_preserve_price_in_urls(vals, mapping)
        min_price = mapping.pop("min_price", None)
        if min_price is None:
            min_price = (vals.get("min_price") or 0.0) if preserve_price else 0.0
        max_price = mapping.pop("max_price", None)
        if max_price is None:
            max_price = (vals.get("max_price") or 0.0) if preserve_price else 0.0
        tags = mapping.pop("tags", None)
        if tags is None:
            tags = vals.get("tags") or ""
        if "attribute_values" not in overrides:
            attr_list = _marketone_attrib_values_to_query_list(
                vals.get("attrib_values")
            )
            if attr_list and not mapping.get("attribute_values"):
                mapping["attribute_values"] = attr_list
        url = self._get_shop_path(path_category)
        url_kwargs = self._shop_get_query_url_kwargs(
            search, min_price, max_price, tags=tags, **mapping
        )
        price_override = "min_price" in overrides or "max_price" in overrides
        if not preserve_price and not price_override:
            url_kwargs.pop("min_price", None)
            url_kwargs.pop("max_price", None)
        for key, value in overrides.items():
            if value in (0, None, "", False) or value == []:
                url_kwargs.pop(key, None)
            else:
                url_kwargs[key] = value
        return QueryURL(url, **url_kwargs)()

    def _marketone_build_active_filter_chips(self, values, kwargs):
        """Chips filtres actifs — Collections → Catégories → Origines → Prix."""
        vals = values or {}
        mapping = kwargs or {}
        env = request.env
        ir_http = env["ir.http"].sudo()
        path_category = vals.get("category")
        chips = []
        attrib_values = {
            int(attr_id): list(value_ids)
            for attr_id, value_ids in (vals.get("attrib_values") or {}).items()
        }
        active_attrib_query = _marketone_attrib_values_to_query_list(attrib_values)

        collections, coll_requested = _marketone_resolve_collection_facet(mapping)
        if coll_requested and collections:
            for coll in collections.sorted("name"):
                coll_slug = coll.slug
                remaining = [
                    other.slug
                    for other in collections
                    if other.id != coll.id
                ]
                chips.append(
                    {
                        "type": "collection",
                        "label": coll.name,
                        "remove_url": self._marketone_shop_keep_url(
                            vals,
                            mapping,
                            path_category,
                            marketone_collection=remaining or 0,
                            attribute_values=active_attrib_query or None,
                        ),
                        "key": coll_slug,
                    }
                )

        categories, cat_requested, _cat_invalid = _marketone_resolve_category_facet(
            mapping, path_category=path_category
        )
        if cat_requested and categories:
            for cat in categories.sorted("name"):
                slug = ir_http._slug(cat)
                remaining = [
                    ir_http._slug(other)
                    for other in categories
                    if other.id != cat.id
                ]
                path_for_url = path_category
                if (
                    path_for_url
                    and ir_http._slug(path_for_url) == slug
                    and slug not in remaining
                ):
                    path_for_url = None
                chips.append(
                    {
                        "type": "category",
                        "label": cat.name,
                        "remove_url": self._marketone_shop_keep_url(
                            vals,
                            mapping,
                            path_for_url,
                            marketone_category=remaining or 0,
                            attribute_values=active_attrib_query or None,
                        ),
                        "key": slug,
                    }
                )

        origin_attr = env.ref(
            "dorevia_ckreyol_marketone.marketone_product_attribute_origin",
            raise_if_not_found=False,
        )
        if origin_attr and origin_attr.id in attrib_values:
            for value_id in list(attrib_values[origin_attr.id]):
                val = env["product.attribute.value"].browse(value_id)
                if not val.exists():
                    continue
                new_attrib = {
                    attr_id: list(vids) for attr_id, vids in attrib_values.items()
                }
                new_attrib[origin_attr.id] = [
                    vid for vid in new_attrib[origin_attr.id] if vid != value_id
                ]
                if not new_attrib[origin_attr.id]:
                    new_attrib.pop(origin_attr.id, None)
                attr_list = _marketone_attrib_values_to_query_list(new_attrib)
                chips.append(
                    {
                        "type": "origin",
                        "label": val.name,
                        "remove_url": self._marketone_shop_keep_url(
                            vals,
                            mapping,
                            path_category,
                            attribute_values=attr_list or 0,
                        ),
                        "key": f"{origin_attr.id}-{value_id}",
                    }
                )

        if _marketone_should_preserve_price_in_urls(vals, mapping):
            chips.append(
                {
                    "type": "price",
                    "label": _marketone_price_chip_label(env, vals),
                    "remove_url": self._marketone_shop_keep_url(
                        vals,
                        mapping,
                        path_category,
                        min_price=0,
                        max_price=0,
                        attribute_values=active_attrib_query or None,
                    ),
                    "key": "price",
                }
            )
        return chips

    def _get_additional_shop_values(self, values, **kwargs):
        result = super()._get_additional_shop_values(values, **kwargs)
        path_category = (values or {}).get("category")
        active_categories, _facet_requested, _facet_invalid = (
            _marketone_resolve_category_facet(kwargs, path_category=path_category)
        )
        search_for_categories = self._marketone_shop_search_product_without_category_facet(
            values, kwargs
        )
        result["marketone_primary_public_categories"] = request.env[
            "product.public.category"
        ]._marketone_primary_public_categories_for_shop(
            search_for_categories,
            active_category_ids=active_categories.ids,
            website=request.website,
        )
        active_slugs = _marketone_canonical_category_slugs(
            kwargs, path_category=path_category
        )
        result["marketone_shop_sidebar_active_category_slugs"] = active_slugs
        result["marketone_has_category_filter"] = bool(active_slugs)
        active_collections, _coll_requested = _marketone_resolve_collection_facet(
            kwargs
        )
        search_for_collections = (
            self._marketone_shop_search_product_without_collection_facet(
                values, kwargs
            )
        )
        result["marketone_shop_collections"] = request.env[
            "marketone.shop.collection"
        ]._marketone_collections_for_shop(
            search_for_collections,
            active_collection_ids=active_collections.ids,
            website=request.website,
        )
        collection_slugs = _marketone_canonical_collection_slugs(kwargs)
        result["marketone_shop_sidebar_active_collection_slugs"] = collection_slugs
        result["marketone_has_collection_filter"] = bool(collection_slugs)
        origin_attr = request.env.ref(
            "dorevia_ckreyol_marketone.marketone_product_attribute_origin",
            raise_if_not_found=False,
        )
        result["marketone_origin_attribute_id"] = origin_attr.id if origin_attr else False
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

        chips = self._marketone_build_active_filter_chips(values, kwargs)
        result["marketone_active_filter_chips"] = chips
        result["marketone_show_filter_state_bar"] = bool(chips)
        result["marketone_search_count"] = search_count
        result["marketone_reset_filters_url"] = self._marketone_shop_keep_url(
            values,
            kwargs,
            values.get("category") if values else None,
            attribute_values=0,
            tags=0,
            min_price=0,
            max_price=0,
            marketone_category=0,
            marketone_collection=0,
        )
        result["marketone_has_active_filters"] = bool(chips)
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
