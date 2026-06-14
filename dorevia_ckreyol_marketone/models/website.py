# -*- coding: utf-8 -*-
"""Extension ``website`` — canonical et robots portes Marketone (MOA D1–D6)."""

from urllib.parse import urlencode

from odoo import models
from odoo.http import request

from odoo.addons.dorevia_ckreyol_marketone.controllers.website_sale import (
    _marketone_is_shop_canonical_path,
    _marketone_seo_canonical_query_pairs,
    _marketone_shop_seo_noindex,
)


class Website(models.Model):
    _inherit = "website"

    def _get_canonical_url(self):
        """Rétablit la query whitelist sur ``/shop`` (Odoo natif supprime la QS)."""
        url = super()._get_canonical_url()
        if not request or not getattr(request, "httprequest", None):
            return url
        path = request.httprequest.path or ""
        if not _marketone_is_shop_canonical_path(path):
            return url
        params = _marketone_seo_canonical_query_pairs()
        if not params:
            return url
        separator = "&" if "?" in url else "?"
        return f"{url}{separator}{urlencode(params)}"

    def marketone_shop_seo_noindex(self):
        """Complète le flag layout ``no_index`` — porte + bruit / multi-origine.

        Nom public requis : QWeb n'appelle pas les méthodes ``_`` des extensions
        custom (contrairement aux API natives ``website._get_canonical_url``).
        """
        self.ensure_one()
        return _marketone_shop_seo_noindex()

    def marketone_shop_robots_content(self):
        """Contenu meta ``robots`` quand ``no_index`` est actif."""
        self.ensure_one()
        if self.marketone_shop_seo_noindex():
            return "noindex, follow"
        return "noindex"
