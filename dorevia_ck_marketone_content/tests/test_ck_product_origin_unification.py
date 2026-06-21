# -*- coding: utf-8 -*-
"""Unification origine produit — attribut « Origines » source unique (Option A fallback)."""

from odoo.tests import tagged
from odoo.tests.common import TransactionCase

from odoo.addons.dorevia_ck_marketone_content.ck_product_origin import (
    ck_card_origin_and_transversal_tags,
    ck_is_geographic_origin_name,
    ck_origin_from_attribute,
)
from odoo.addons.dorevia_ck_marketone_content.home_featured import (
    FEATURED_CATEGORY_NAME,
    _get_featured_card_metadata_line,
    _get_featured_labels_line,
)
from odoo.addons.dorevia_ck_marketone_content.product_page_details import (
    build_ck_product_page_detail_sections,
)


@tagged('post_install', '-at_install', 'dorevia_ck_product_origin')
class TestCkProductOriginUnification(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.website = cls.env['website'].search([], limit=1)
        cls.card_uom_g = cls.env['dorevia.ck.card.uom'].sudo().search(
            [('code', '=', 'g')], limit=1,
        )
        cls.card_uom_kg = cls.env['dorevia.ck.card.uom'].sudo().search(
            [('code', '=', 'kg')], limit=1,
        )

    def _make_product(self, **kwargs):
        values = {
            'name': 'CK Origine QA',
            'type': 'consu',
            'list_price': 3.6,
            'sale_ok': True,
            'is_published': True,
        }
        values.update(kwargs)
        return self.env['product.template'].sudo().create(values)

    def _ensure_origin_attribute(self, origin_name):
        attr = self.env['product.attribute'].sudo().search([
            ('name', 'ilike', 'origines'),
        ], limit=1)
        if not attr:
            attr = self.env['product.attribute'].sudo().create({
                'name': 'Origines',
                'create_variant': 'no_variant',
            })
        value = self.env['product.attribute.value'].sudo().search([
            ('attribute_id', '=', attr.id),
            ('name', '=', origin_name),
        ], limit=1)
        if not value:
            value = self.env['product.attribute.value'].sudo().create({
                'name': origin_name,
                'attribute_id': attr.id,
            })
        return attr, value

    def _set_origin_attribute(self, template, origin_name):
        attr, value = self._ensure_origin_attribute(origin_name)
        template.write({
            'attribute_line_ids': [(5, 0, 0), (0, 0, {
                'attribute_id': attr.id,
                'value_ids': [(6, 0, [value.id])],
            })],
        })

    def test_case1_origin_from_attribute_not_tags(self):
        """Attribut « Origines » prioritaire ; tag transversal conservé."""
        guadeloupe = self.env['product.tag'].sudo().create({
            'name': 'Guadeloupe',
            'sequence': 10,
        })
        epicerie = self.env['product.tag'].sudo().create({
            'name': 'Épicerie',
            'sequence': 20,
        })
        product = self._make_product(
            product_tag_ids=[(6, 0, [guadeloupe.id, epicerie.id])],
            ck_net_quantity=100,
            ck_net_quantity_uom_id=self.card_uom_g.id,
            ck_reference_price_uom_id=self.card_uom_kg.id,
            ck_show_reference_price=True,
        )
        self._set_origin_attribute(product, 'Guadeloupe')
        variant = product.product_variant_id
        labels = _get_featured_labels_line(product, variant)
        self.assertEqual(labels, 'Guadeloupe · Épicerie')
        metadata = _get_featured_card_metadata_line(self.env, self.website, variant)
        self.assertEqual(metadata, 'Guadeloupe · Épicerie · 100 g · 36,00\xa0€/kg')
        self.assertEqual(ck_origin_from_attribute(product), 'Guadeloupe')

    def test_case2_option_a_fallback_geographic_tag(self):
        """Sans attribut : fallback temporaire sur étiquette géographique."""
        reunion = self.env['product.tag'].sudo().create({
            'name': 'Réunion',
            'sequence': 1,
        })
        product = self._make_product(
            product_tag_ids=[(6, 0, [reunion.id])],
        )
        variant = product.product_variant_id
        self.assertEqual(_get_featured_labels_line(product, variant), 'Réunion')
        self.assertEqual(ck_origin_from_attribute(product), '')

    def test_case2_option_a_no_origin_for_transversal_tags_only(self):
        """Sans attribut ni tag géographique : pas d'origine affichée."""
        epicerie = self.env['product.tag'].sudo().create({'name': 'Épicerie', 'sequence': 1})
        artisanal = self.env['product.tag'].sudo().create({'name': 'Artisanal', 'sequence': 2})
        coup = self.env['product.tag'].sudo().create({'name': FEATURED_CATEGORY_NAME, 'sequence': 0})
        product = self._make_product(
            product_tag_ids=[(6, 0, [coup.id, epicerie.id, artisanal.id])],
        )
        variant = product.product_variant_id
        self.assertEqual(_get_featured_labels_line(product, variant), 'Épicerie · Artisanal')

    def test_case3_transversal_tags_not_geographic(self):
        self.assertFalse(ck_is_geographic_origin_name('Épicerie'))
        self.assertFalse(ck_is_geographic_origin_name('Artisanal'))
        self.assertTrue(ck_is_geographic_origin_name('Martinique'))
        origin, tags = ck_card_origin_and_transversal_tags(
            ['Épicerie', 'Coup de cœur', 'Artisanal'],
            '',
        )
        self.assertEqual(origin, '')
        self.assertEqual(tags, ['Épicerie', 'Coup de cœur', 'Artisanal'])

    def test_attribute_dedupes_geographic_tag(self):
        """Tag géographique redondant masqué quand l'attribut est renseigné."""
        guadeloupe_tag = self.env['product.tag'].sudo().create({'name': 'Guadeloupe'})
        martinique_tag = self.env['product.tag'].sudo().create({'name': 'Martinique'})
        epicerie = self.env['product.tag'].sudo().create({'name': 'Épicerie'})
        product = self._make_product(
            product_tag_ids=[(6, 0, [guadeloupe_tag.id, martinique_tag.id, epicerie.id])],
        )
        self._set_origin_attribute(product, 'Guadeloupe')
        labels = _get_featured_labels_line(product)
        self.assertEqual(labels, 'Guadeloupe · Épicerie')

    def test_case4_product_page_uses_shared_origin_helper(self):
        """Fiche produit — section origine depuis attribut partagé."""
        product = self._make_product()
        self._set_origin_attribute(product, 'Martinique')
        sections = build_ck_product_page_detail_sections(product)
        producer = next(
            (section for section in sections if section['key'] == 'origin_producer'),
            None,
        )
        self.assertIsNotNone(producer)
        self.assertIn('Martinique', str(producer['body']))

    def test_case5_shop_origin_filter_is_native_attribute(self):
        """Filtre boutique Origine = facettes attributs Odoo natif (si attribut configuré)."""
        attr = self.env['product.attribute'].sudo().search([
            ('name', 'ilike', 'origines'),
        ], limit=1)
        if not attr:
            self.skipTest('Attribut « Origines » non configuré sur l’instance — filtre shop absent.')
        self.assertIn(attr.create_variant, ('no_variant', 'always'))
        view = self.env['ir.ui.view'].sudo().search([
            ('key', '=', 'website_sale.products_attributes'),
        ], limit=1)
        self.assertTrue(view, 'Facette attributs shop Odoo native attendue.')
