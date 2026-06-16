# -*- coding: utf-8 -*-
import logging

from odoo import models
from odoo.http import request

_logger = logging.getLogger(__name__)


class IrHttp(models.AbstractModel):
    _inherit = 'ir.http'

    @classmethod
    def _pre_dispatch(cls, rule, args):
        cls._ck_maybe_refresh_home_featured_arch()
        return super()._pre_dispatch(rule, args)

    @classmethod
    def _ck_maybe_refresh_home_featured_arch(cls):
        """Reconstruit la section vedettes si l'arch home est périmée (étiquettes manquantes)."""
        if not request:
            return
        if not cls._ck_path_can_be_homepage():
            return
        env = request.env
        try:
            website = env['website'].get_current_website()
        except Exception:
            return
        if not website or not cls._ck_request_is_homepage(env, website):
            return
        from odoo.addons.dorevia_ck_marketone_content.home_featured import (
            _featured_arch_missing_product_labels,
            bootstrap_home_featured_products,
            get_curated_featured_variants,
        )

        page = env['website.page'].sudo().search([
            ('url', '=', '/'),
            ('website_id', '=', website.id),
        ], limit=1)
        if not page or not page.view_id:
            return
        arch = page.view_id.arch_db or ''
        variants = get_curated_featured_variants(env)
        if not _featured_arch_missing_product_labels(env, arch, variants):
            return
        if bootstrap_home_featured_products(env(su=True)):
            _logger.info('CK Section 3 : home reconstruite avant rendu (étiquettes produit).')
            page.view_id.invalidate_recordset(['arch_db'])

    @staticmethod
    def _ck_path_can_be_homepage():
        httprequest = getattr(request, 'httprequest', None)
        if not httprequest:
            return False
        path = (httprequest.path or '/').split('?')[0].rstrip('/') or '/'
        if path == '/':
            return True
        if path.startswith(('/odoo', '/web')):
            return False
        return path.count('/') == 1

    @staticmethod
    def _ck_request_is_homepage(env, website):
        path = (request.httprequest.path or '/').split('?')[0].rstrip('/') or '/'
        try:
            homepage = (website.homepage_url or '/').split('?')[0].rstrip('/') or '/'
        except Exception:
            return False
        if path == homepage:
            return True
        if homepage != '/' or path.count('/') != 1:
            return False
        lang_code = path[1:]
        return bool(env['res.lang'].sudo().search([
            ('url_code', '=', lang_code),
            ('active', '=', True),
        ], limit=1))
