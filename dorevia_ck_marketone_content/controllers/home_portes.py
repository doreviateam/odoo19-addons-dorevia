# -*- coding: utf-8 -*-
"""Portes home CK — redirections publiques sans dépendre de dorevia_ckreyol_marketone."""

from odoo import http
from odoo.http import request

# Aligné Chantier B / Lot 6.3b lorsque le module marketone est installé.
KITS_CANONICAL_QUERY = '/shop?marketone_mode=pack'


class CkHomePortesController(http.Controller):

    @http.route('/kits', type='http', auth='public', website=True, sitemap=False)
    def kits_redirect(self, **kwargs):
        """Porte coffrets home — 301 vers la collection pack du shop."""
        return request.redirect(KITS_CANONICAL_QUERY, code=301)
