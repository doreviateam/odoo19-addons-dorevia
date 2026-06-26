# -*- coding: utf-8 -*-
"""Tests Micro-lot 3B — drawer filtres boutique (regroupement tags)."""

from odoo.tests import tagged
from odoo.tests.common import HttpCase, TransactionCase

from odoo.addons.dorevia_ck_marketone_content.shop_filter_groups import (
    AGRICULTURE_BIO_TAG_NAME,
    BIEN_ETRE_TAG_NAME,
    CK_SHOP_FILTER_GROUP_ORIGIN,
    CK_SHOP_FILTER_GROUP_PREFERENCE,
    CK_SHOP_FILTER_GROUP_PRODUCER,
    GUADELOUPE_TAG_NAME,
    bootstrap_ck_shop_filter_tags,
    ck_infer_shop_filter_group,
)


@tagged('post_install', '-at_install', 'dorevia_ck_shop_filter_drawer')
class TestCkShopFilterGroups(TransactionCase):

    def test_infer_groups(self):
        self.assertEqual(ck_infer_shop_filter_group('Guadeloupe'), CK_SHOP_FILTER_GROUP_ORIGIN)
        self.assertEqual(ck_infer_shop_filter_group('Dominique (Ile)'), CK_SHOP_FILTER_GROUP_ORIGIN)
        self.assertEqual(ck_infer_shop_filter_group('Komla'), CK_SHOP_FILTER_GROUP_PRODUCER)
        self.assertEqual(ck_infer_shop_filter_group('Sans Gluten'), CK_SHOP_FILTER_GROUP_PREFERENCE)
        self.assertFalse(ck_infer_shop_filter_group('Bien-être'))

    def test_bootstrap_classifies_tags(self):
        bootstrap_ck_shop_filter_tags(self.env)
        Tag = self.env['product.tag'].sudo()
        guadeloupe = Tag.search([('name', '=', GUADELOUPE_TAG_NAME)], limit=1)
        if guadeloupe:
            self.assertEqual(guadeloupe.ck_shop_filter_group, CK_SHOP_FILTER_GROUP_ORIGIN)
            self.assertTrue(guadeloupe.visible_to_customers)
        bien_etre = Tag.search([('name', '=', BIEN_ETRE_TAG_NAME)], limit=1)
        if bien_etre:
            self.assertFalse(bien_etre.visible_to_customers)
        bio = Tag.search([('name', '=', AGRICULTURE_BIO_TAG_NAME)], limit=1)
        self.assertTrue(bio)
        self.assertEqual(bio.ck_shop_filter_group, CK_SHOP_FILTER_GROUP_PREFERENCE)


@tagged('post_install', '-at_install', 'dorevia_ck_shop_filter_drawer', 'dorevia_ck_shop_s1')
class TestCkShopFilterDrawerHttp(HttpCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        bootstrap_ck_shop_filter_tags(cls.env)

    def _drawer_html(self, path='/shop'):
        return self.url_open(path).text

    def _offcanvas_block(self, html):
        start = html.find('id="o_wsale_offcanvas"')
        self.assertGreater(start, -1, 'Offcanvas introuvable')
        end = html.find('</aside>', start)
        self.assertGreater(end, start, 'Fin offcanvas introuvable')
        return html[start:end]

    def test_drawer_three_sections(self):
        drawer = self._offcanvas_block(self._drawer_html())
        self.assertIn('Origines', drawer)
        self.assertIn('Producteurs', drawer)
        self.assertIn('Préférences', drawer)
        self.assertNotIn('Origines &amp; préférences', drawer)
        self.assertNotIn('Origines & préférences', drawer)

    def test_guadeloupe_in_origines_section(self):
        drawer = self._offcanvas_block(self._drawer_html())
        origin_block = drawer.split('o_wsale_offcanvas_ck_tags_origin', 1)[-1]
        origin_block = origin_block.split('o_wsale_offcanvas_ck_tags_producer', 1)[0]
        self.assertIn('Guadeloupe', origin_block)

    def test_bien_etre_not_in_drawer(self):
        drawer = self._offcanvas_block(self._drawer_html())
        self.assertNotIn('>Bien-être<', drawer)
        self.assertNotIn('>Bien-etre<', drawer)

    def test_agriculture_bio_in_preferences(self):
        drawer = self._offcanvas_block(self._drawer_html())
        pref_block = drawer.split('o_wsale_offcanvas_ck_tags_preference', 1)[-1]
        self.assertIn(AGRICULTURE_BIO_TAG_NAME, pref_block)

    def test_reset_button_top_french(self):
        drawer = self._offcanvas_block(self._drawer_html())
        self.assertIn('Réinitialiser les filtres', drawer)
        self.assertNotIn('Clear Filters', drawer)

    def test_tag_filter_url_still_works(self):
        Tag = self.env['product.tag'].sudo()
        Product = self.env['product.template'].sudo()
        tags = Tag.search([
            ('ck_shop_filter_group', '!=', False),
            ('visible_to_customers', '=', True),
        ])
        tag = tags.filtered(
            lambda candidate: Product.search_count([
                ('is_published', '=', True),
                ('product_tag_ids', 'in', candidate.id),
            ])
        )[:1]
        if not tag:
            self.skipTest('Aucun tag filtrable rattaché à un produit publié.')
        tag = tag[0]
        response = self.url_open(f'/shop?tags={tag.id}')
        self.assertEqual(response.status_code, 200)
        html = response.text
        self.assertIn('oe_product', html)
        drawer = self._offcanvas_block(html)
        self.assertIn(f'tag_{tag.id}', drawer)

    def test_producers_section_contains_known_producer(self):
        drawer = self._offcanvas_block(self._drawer_html())
        producer_block = drawer.split('o_wsale_offcanvas_ck_tags_producer', 1)[-1]
        producer_block = producer_block.split('o_wsale_offcanvas_ck_tags_preference', 1)[0]
        self.assertTrue(
            any(name in producer_block for name in ('Komla', 'La Platine', 'Rwan Ltd')),
            msg='Au moins un producteur attendu',
        )
