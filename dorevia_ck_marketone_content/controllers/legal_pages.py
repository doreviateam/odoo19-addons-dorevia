# -*- coding: utf-8 -*-
"""Route /terms — priorité CMS CK sur la page CGV comptabilité Odoo (account)."""

from odoo import http
from odoo.http import request

from odoo.addons.account.controllers.terms import TermsController
from odoo.addons.dorevia_ck_marketone_content.legal_pages import TERMS_PAGE_URL


class CkMarketoneLegalPagesController(TermsController):
    @http.route()
    def terms_conditions(self, **kwargs):
        """Sert la page CMS CK /terms (CGV recette interne MOA)."""
        page = request.env['website.page'].sudo().search([
            ('url', '=', TERMS_PAGE_URL),
            ('website_id', 'in', [False, request.website.id]),
        ], order='website_id desc', limit=1)
        if page:
            response = page._get_response(request)
            if response:
                return response
        return super().terms_conditions(**kwargs)
