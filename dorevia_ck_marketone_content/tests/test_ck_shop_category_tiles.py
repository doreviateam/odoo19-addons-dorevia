# -*- coding: utf-8 -*-
"""Tests Note 07 Lot B — shop_category_tiles.get_ck_category_family_tiles."""

from odoo.tests import tagged
from odoo.tests.common import TransactionCase

from odoo.addons.dorevia_ck_marketone_content.shop_category_tiles import (
    get_ck_category_family_tiles,
)


@tagged('post_install', '-at_install', 'dorevia_ck_shop_note07_tiles')
class TestCkShopCategoryTiles(TransactionCase):

    def _make_category(self, name, parent=None):
        return self.env['product.public.category'].sudo().create({
            'name': name,
            'parent_id': parent.id if parent else False,
        })

    def _make_published_product(self, name, category):
        return self.env['product.template'].sudo().create({
            'name': name,
            'type': 'consu',
            'list_price': 5.0,
            'is_published': True,
            'public_categ_ids': [(4, category.id)],
        })

    def test_tiles_returns_children_with_published_products(self):
        parent = self._make_category('Épices')
        child_with = self._make_category('Piment', parent)
        child_empty = self._make_category('Poivre', parent)
        self._make_published_product('Piment doux', child_with)

        tiles = parent.get_ck_category_family_tiles()
        labels = [t['label'] for t in tiles]
        self.assertIn('Piment', labels)
        self.assertNotIn('Poivre', labels)

    def test_tiles_empty_when_no_children(self):
        cat = self._make_category('Catégorie sans enfant')
        self.assertEqual(cat.get_ck_category_family_tiles(), [])

    def test_tiles_empty_when_category_is_none(self):
        self.assertEqual(get_ck_category_family_tiles(self.env, None), [])

    def test_tile_structure(self):
        parent = self._make_category('Boissons')
        child = self._make_category('Jus', parent)
        product = self._make_published_product('Jus goyave', child)

        tiles = parent.get_ck_category_family_tiles()
        self.assertEqual(len(tiles), 1)
        tile = tiles[0]
        self.assertEqual(tile['label'], 'Jus')
        self.assertIn('/shop/category/', tile['url'])
        self.assertIn(str(product.id), tile['image_url'])

    def test_tile_image_none_when_no_product_image(self):
        parent = self._make_category('Artisanat')
        child = self._make_category('Vannerie', parent)
        product = self._make_published_product('Panier', child)
        product.image_1920 = False

        tiles = parent.get_ck_category_family_tiles()
        self.assertEqual(len(tiles), 1)

    def test_unpublished_products_excluded(self):
        parent = self._make_category('Soins')
        child = self._make_category('Savons', parent)
        product = self.env['product.template'].sudo().create({
            'name': 'Savon coco non publié',
            'type': 'consu',
            'list_price': 5.0,
            'is_published': False,
            'public_categ_ids': [(4, child.id)],
        })
        self.assertFalse(product.is_published)
        tiles = parent.get_ck_category_family_tiles()
        self.assertEqual(tiles, [], 'Sous-catégorie sans produit publié ne doit pas générer de tuile')
