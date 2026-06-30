# -*- coding: utf-8 -*-
"""Routes publiques /producteurs et /producteur/<slug> — Sprint Producteurs CK V1."""

from collections import defaultdict

from odoo import http
from odoo.http import request

from odoo.addons.dorevia_ck_marketone_content.models.res_partner import _CK_PRODUCER_IMAGE_SIZES
from odoo.addons.dorevia_ck_marketone_content.nav_v22_config import NAV_PRODUCTEURS_URL
from odoo.addons.dorevia_ck_marketone_content.nos_producteurs_page import NOS_PRODUCTEURS_PAGE_URL


class CkProducersController(http.Controller):

    @http.route(NOS_PRODUCTEURS_PAGE_URL, type='http', auth='public', website=True, sitemap=False)
    def ck_nos_producteurs_legacy_redirect(self, **kwargs):
        """301 — ancienne page CMS /nos-producteurs vers l'annuaire dynamique."""
        return request.redirect(NAV_PRODUCTEURS_URL, code=301)

    @http.route(
        '/ck/producteur/<int:producer_id>/image/<string:field>',
        type='http',
        auth='public',
        website=True,
        sitemap=False,
    )
    def ck_producer_image(self, producer_id, field, **kwargs):
        """Image producteur accessible au visiteur anonyme (ck_is_producer uniquement)."""
        size = _CK_PRODUCER_IMAGE_SIZES.get(field)
        if not size:
            raise request.not_found()
        producer = request.env['res.partner'].sudo().browse(producer_id)
        if not producer.exists() or not producer.ck_is_producer or not producer.ck_producer_website_image:
            raise request.not_found()
        stream = request.env['ir.binary'].sudo()._get_image_stream_from(
            producer,
            'ck_producer_website_image',
            width=size,
            height=size,
        )
        return stream.get_response()

    @http.route('/producteurs', type='http', auth='public', website=True, sitemap=True)
    def ck_producers_list(self, **kwargs):
        producers = request.env['res.partner'].sudo().search(
            [('ck_is_producer', '=', True)],
            order='name asc',
        )
        published_products = request.env['product.template'].sudo().search([
            ('ck_producer_id', 'in', producers.ids),
            ('is_published', '=', True),
            ('sale_ok', '=', True),
        ])
        producer_counts = defaultdict(int)
        for product in published_products:
            producer_counts[product.ck_producer_id.id] += 1

        return request.render(
            'dorevia_ck_marketone_content.ck_producers_list_page',
            {
                'producers': producers,
                'producer_counts': producer_counts,
            },
        )

    @http.route('/producteur/<string:producer_slug>', type='http', auth='public', website=True, sitemap=False)
    def ck_producer_detail(self, producer_slug, **kwargs):
        try:
            producer_id = int(producer_slug.rsplit('-', 1)[-1])
        except (ValueError, IndexError):
            raise request.not_found()

        producer = request.env['res.partner'].sudo().browse(producer_id)
        if not producer.exists() or not producer.ck_is_producer:
            raise request.not_found()

        canonical_slug = producer.get_ck_producer_url().rsplit('/', 1)[-1]
        if producer_slug != canonical_slug:
            return request.redirect(f'/producteur/{canonical_slug}', code=301)

        products = producer.get_ck_producer_products()
        meta_description = (
            producer.ck_producer_short_description
            or f'Découvrez {producer.name}, producteur partenaire C-Kréyòl.'
        )
        return request.render(
            'dorevia_ck_marketone_content.ck_producer_detail_page',
            {
                'producer': producer,
                'products': products,
                'meta_description': meta_description,
            },
        )
