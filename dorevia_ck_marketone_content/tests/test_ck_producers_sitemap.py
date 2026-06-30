# -*- coding: utf-8 -*-
"""Tests SEO / Sitemap — Producteurs CK V1."""

from odoo.tests import tagged
from odoo.tests.common import HttpCase, TransactionCase

from odoo.addons.dorevia_ck_marketone_content.controllers.producers import ck_sitemap_producers
from odoo.addons.dorevia_ck_marketone_content.nos_producteurs_page import NOS_PRODUCTEURS_PAGE_URL
from odoo.addons.dorevia_ck_marketone_content.producer_seo import (
    _clear_website_sitemap_cache,
    deindex_legacy_producer_cms_pages,
)


def _make_producer(env, name='Distillerie Sitemap', **kwargs):
    vals = {'name': name, 'ck_is_producer': True}
    vals.update(kwargs)
    return env['res.partner'].sudo().create(vals)


def _make_product(env, producer, name='Produit Sitemap', published=True, sale_ok=True):
    return env['product.template'].sudo().create({
        'name': name,
        'type': 'consu',
        'list_price': 5.0,
        'sale_ok': sale_ok,
        'is_published': published,
        'ck_producer_id': producer.id,
    })


def _sitemap_locs(env):
    website = env['website'].search([], limit=1)
    return {page['loc'] for page in website.sudo()._enumerate_pages()}


@tagged('post_install', '-at_install', 'dorevia_ck_producers_seo_v1')
class TestCkProducersSitemapModel(TransactionCase):
    """Fonction ck_sitemap_producers — éligibilité et URLs canoniques."""

    def test_sitemap_function_yields_canonical_url_only(self):
        producer = _make_producer(self.env, name='SARL La Platine Sitemap')
        _make_product(self.env, producer, name='Rhum Sitemap')
        locs = {entry['loc'] for entry in ck_sitemap_producers(self.env, None, None)}
        canonical = producer.get_ck_producer_url()
        self.assertIn(canonical, locs)
        obsolete = f'/producteur/ancien-slug-{producer.id}'
        self.assertNotIn(obsolete, locs)

    def test_sitemap_function_excludes_producer_without_published_products(self):
        producer = _make_producer(self.env, name='Sans Produit Sitemap')
        locs = {entry['loc'] for entry in ck_sitemap_producers(self.env, None, None)}
        self.assertNotIn(producer.get_ck_producer_url(), locs)

    def test_sitemap_function_excludes_non_producer_partner(self):
        partner = self.env['res.partner'].sudo().create({
            'name': 'Fournisseur Sitemap',
            'ck_is_producer': False,
        })
        _make_product(self.env, partner, name='Produit Fournisseur')
        locs = {entry['loc'] for entry in ck_sitemap_producers(self.env, None, None)}
        self.assertFalse(any(str(partner.id) in loc for loc in locs))

    def test_deindex_legacy_cms_pages_removes_nos_producteurs(self):
        website = self.env['website'].search([], limit=1)
        Page = self.env['website.page'].sudo()
        page = Page.search([
            ('website_id', '=', website.id),
            ('url', '=', NOS_PRODUCTEURS_PAGE_URL),
        ], limit=1)
        if page:
            page.write({'website_indexed': True})
        deindex_legacy_producer_cms_pages(self.env)
        if page:
            self.assertFalse(page.website_indexed)
        locs = _sitemap_locs(self.env)
        self.assertNotIn(NOS_PRODUCTEURS_PAGE_URL, locs)


@tagged('post_install', '-at_install', 'dorevia_ck_producers_seo_v1')
class TestCkProducersSitemapHttp(HttpCase):
    """Sitemap Odoo — annuaire et fiches producteurs indexables."""

    FR_HEADERS = {'Accept-Language': 'fr-FR,fr;q=0.9'}

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        deindex_legacy_producer_cms_pages(cls.env)
        cls.producer = cls.env['res.partner'].sudo().create({
            'name': 'SARL La Platine',
            'ck_is_producer': True,
        })
        cls.product = cls.env['product.template'].sudo().create({
            'name': 'Rhum Sitemap HTTP',
            'type': 'consu',
            'list_price': 12.0,
            'sale_ok': True,
            'is_published': True,
            'ck_producer_id': cls.producer.id,
        })
        cls.canonical_url = cls.producer.get_ck_producer_url()

    def test_sitemap_contains_producteurs_list(self):
        locs = _sitemap_locs(self.env)
        self.assertIn('/producteurs', locs)

    def test_sitemap_contains_canonical_producer_detail(self):
        locs = _sitemap_locs(self.env)
        self.assertIn(self.canonical_url, locs)
        obsolete = f'/producteur/ancien-nom-{self.producer.id}'
        self.assertNotIn(obsolete, locs)

    def test_sitemap_excludes_legacy_nos_producteurs(self):
        locs = _sitemap_locs(self.env)
        self.assertNotIn(NOS_PRODUCTEURS_PAGE_URL, locs)

    def test_sitemap_excludes_non_producer_partner(self):
        partner = self.env['res.partner'].sudo().create({
            'name': 'Fournisseur HTTP Sitemap',
            'ck_is_producer': False,
        })
        self.env['product.template'].sudo().create({
            'name': 'Produit Non Producteur',
            'type': 'consu',
            'list_price': 3.0,
            'sale_ok': True,
            'is_published': True,
            'ck_producer_id': partner.id,
        })
        locs = _sitemap_locs(self.env)
        self.assertFalse(any(f'-{partner.id}' in loc and loc.startswith('/producteur/') for loc in locs))

    def test_sitemap_excludes_producer_without_published_products(self):
        empty_producer = self.env['res.partner'].sudo().create({
            'name': 'Producteur Vide Sitemap',
            'ck_is_producer': True,
        })
        locs = _sitemap_locs(self.env)
        self.assertNotIn(empty_producer.get_ck_producer_url(), locs)

    def test_sitemap_xml_endpoint_lists_producer_pages(self):
        _clear_website_sitemap_cache(self.env)
        resp = self.url_open('/sitemap.xml', headers=self.FR_HEADERS)
        self.assertEqual(resp.status_code, 200)
        body = resp.text
        self.assertIn('/producteurs', body)
        self.assertIn(self.canonical_url.replace('&', '&amp;'), body)
        self.assertNotIn(NOS_PRODUCTEURS_PAGE_URL, body)

    def test_legacy_nos_producteurs_redirect_still_301(self):
        resp = self.url_open(
            NOS_PRODUCTEURS_PAGE_URL,
            allow_redirects=False,
            headers=self.FR_HEADERS,
        )
        self.assertEqual(resp.status_code, 301)
        self.assertIn('/producteurs', resp.headers.get('Location', ''))
