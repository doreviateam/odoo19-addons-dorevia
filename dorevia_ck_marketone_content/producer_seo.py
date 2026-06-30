# -*- coding: utf-8 -*-
"""SEO Producteurs CK — désindexation CMS legacy et helpers sitemap."""

import re

from .nos_producteurs_page import NOS_PRODUCTEURS_PAGE_URL

# Fiches dynamiques : /producteur/<slug>-<id>
_CANONICAL_PRODUCER_DETAIL_RE = re.compile(r'^/producteur/.+-\d+$')


def _clear_website_sitemap_cache(env):
    """Force la régénération du sitemap après changement d'indexation."""
    env['ir.attachment'].sudo().search([
        ('type', '=', 'binary'),
        ('url', '=like', '/sitemap-%'),
    ]).unlink()


def deindex_legacy_producer_cms_pages(env):
    """Retire du sitemap les pages CMS remplacées par les routes dynamiques CK."""
    Page = env['website.page'].sudo()
    legacy_urls = [NOS_PRODUCTEURS_PAGE_URL]
    legacy_urls += Page.search([
        ('url', '=like', '/producteur/%'),
    ]).mapped('url')

    to_deindex = Page.browse()
    for url in legacy_urls:
        normalized = (url or '').rstrip('/') or url
        if normalized == NOS_PRODUCTEURS_PAGE_URL:
            to_deindex |= Page.search([('url', '=', url)])
            continue
        if normalized.startswith('/producteur/') and not _CANONICAL_PRODUCER_DETAIL_RE.match(normalized):
            to_deindex |= Page.search([('url', '=', url)])

    if to_deindex:
        to_deindex.write({'website_indexed': False})
    _clear_website_sitemap_cache(env)
