# -*- coding: utf-8 -*-
"""Univers Culture — pages territoire ``/culture/<slug>`` (v1)."""

from werkzeug.exceptions import NotFound

from odoo.http import request, route

from odoo.addons.website.controllers.main import Website


class MarketoneCulture(Website):
    """Page territoire Culture — hors ``/shop``, lien vers porte Origines."""

    @route(
        ["/culture/<string:slug>"],
        type="http",
        auth="public",
        website=True,
        sitemap=False,
    )
    def culture_territory(self, slug, **kwargs):
        website = request.website
        profile = (
            request.env["marketone.shop.origin"]
            .sudo()
            ._marketone_resolve_published_slug(slug, website=website)
        )
        if not profile:
            raise NotFound()
        return request.render(
            "dorevia_ckreyol_marketone.marketone_culture_territory",
            {
                "culture_profile": profile,
                "culture_shop_url": profile._marketone_origin_shop_url(),
            },
        )
