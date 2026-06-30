# -*- coding: utf-8 -*-
"""Producteurs SEO V1 — sitemap dynamique, désindexation CMS legacy."""
from odoo.addons.dorevia_ck_marketone_content.producer_seo import deindex_legacy_producer_cms_pages


def migrate(cr, version):
    from odoo import api, SUPERUSER_ID

    env = api.Environment(cr, SUPERUSER_ID, {})
    deindex_legacy_producer_cms_pages(env)
