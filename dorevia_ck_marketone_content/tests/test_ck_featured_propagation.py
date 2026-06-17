# -*- coding: utf-8 -*-
"""Propagation BO → front de la section vedettes « Nos coups de cœur ».

Vérifie qu'une édition back-office d'un champ rendu sur la carte rafraîchit
automatiquement le SSR home, et que le scope curation (M1/D3) est respecté.
Champs réellement rendus : titre (nom), métadonnée (tags + format + prix réf),
prix, badge (ruban).
"""

from odoo.tests import tagged
from odoo.tests.common import TransactionCase

from odoo.addons.dorevia_ck_marketone_content.home_featured import (
    _ensure_featured_category,
    _get_featured_price_label,
    bootstrap_home_featured_products,
)

_TINY_PNG = (
    b'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAADElEQVR4nGP4z8AAAAMBAQDJ/pLvAAAAAElFTkSuQmCC'
)


@tagged('post_install', '-at_install', 'dorevia_ck_marketone_featured_propagation')
class TestCkFeaturedPropagation(TransactionCase):
    def _make_product(self, name, **vals):
        base = {
            'name': name,
            'is_published': True,
            'website_published': True,
            'sale_ok': True,
            'list_price': 4.0,
            'image_1920': _TINY_PNG,
        }
        base.update(vals)
        return self.env['product.template'].sudo().create(base)

    def _home_arch(self):
        page = self.env['website.page'].sudo().search([('url', '=', '/')], limit=1)
        return (page.view_id.arch_db or page.view_id.arch or '') if page and page.view_id else ''

    def test_rename_product_propagates_to_card_title(self):
        """Renommer un produit vedette met à jour le titre de la carte (champ `name`)."""
        cat = _ensure_featured_category(self.env)
        product = self._make_product('Alpha Vedette', public_categ_ids=[(4, cat.id)])
        bootstrap_home_featured_products(self.env)
        self.assertIn('Alpha Vedette', self._home_arch())

        product.write({'name': 'Omega Vedette'})
        arch = self._home_arch()
        self.assertIn('Omega Vedette', arch)
        self.assertNotIn('Alpha Vedette', arch)

    def test_rename_ribbon_propagates_to_badge(self):
        """Renommer le ruban e-commerce met à jour le badge de la carte."""
        cat = _ensure_featured_category(self.env)
        ribbon = self.env['product.ribbon'].sudo().create({'name': 'BadgeAvant'})
        self._make_product(
            'CK Vedette Badge',
            public_categ_ids=[(4, cat.id)],
            website_ribbon_id=ribbon.id,
        )
        bootstrap_home_featured_products(self.env)
        self.assertIn('BadgeAvant', self._home_arch())

        ribbon.write({'name': 'BadgeApres'})
        arch = self._home_arch()
        self.assertIn('BadgeApres', arch)
        self.assertNotIn('BadgeAvant', arch)

    def test_change_price_propagates(self):
        """Non-régression : un changement de prix met à jour le label prix SSR."""
        cat = _ensure_featured_category(self.env)
        product = self._make_product('CK Vedette Prix', list_price=4.0, public_categ_ids=[(4, cat.id)])
        bootstrap_home_featured_products(self.env)

        product.write({'list_price': 7.5})
        website = self.env['website'].search([], limit=1)
        expected = _get_featured_price_label(self.env, website, product.product_variant_id)
        self.assertIn(expected, self._home_arch())

    def test_rename_non_featured_product_does_not_rebuild(self):
        """Scope M1/D3 : renommer un produit hors « Coups de cœur » ne reconstruit pas la home."""
        cat = _ensure_featured_category(self.env)
        self._make_product('CK Curated In', public_categ_ids=[(4, cat.id)])
        outside = self._make_product('CK Hors Curation')
        bootstrap_home_featured_products(self.env)
        arch_before = self._home_arch()

        outside.write({'name': 'CK Hors Curation Renommé'})
        arch_after = self._home_arch()
        self.assertEqual(arch_before, arch_after)
        self.assertNotIn('CK Hors Curation', arch_after)

    # --- Cas variantes (product.product d'un template multi-variantes) ---

    def _make_two_variant_product(self, name, val_a='Salé', val_b='Sucré', **vals):
        attribute = self.env['product.attribute'].sudo().create({
            'name': f'{name} Saveur',
            'create_variant': 'always',
        })
        value_a = self.env['product.attribute.value'].sudo().create({
            'name': val_a, 'attribute_id': attribute.id,
        })
        value_b = self.env['product.attribute.value'].sudo().create({
            'name': val_b, 'attribute_id': attribute.id,
        })
        base = {
            'name': name,
            'is_published': True,
            'website_published': True,
            'sale_ok': True,
            'list_price': 3.0,
            'image_1920': _TINY_PNG,
            'attribute_line_ids': [(0, 0, {
                'attribute_id': attribute.id,
                'value_ids': [(6, 0, [value_a.id, value_b.id])],
            })],
        }
        base.update(vals)
        template = self.env['product.template'].sudo().create(base)
        return template, value_a, value_b

    def test_variant_attribute_value_rename_propagates_to_title(self):
        """Renommer la valeur d'attribut met à jour le titre de la card de CETTE variante."""
        cat = _ensure_featured_category(self.env)
        template, value_a, _value_b = self._make_two_variant_product(
            'CK Multi Titre', val_a='Piquant', val_b='Sucre',
            public_categ_ids=[(4, cat.id)],
        )
        bootstrap_home_featured_products(self.env)
        arch = self._home_arch()
        self.assertIn('Piquant', arch)
        self.assertIn('Sucre', arch)

        value_a.write({'name': 'Relevé'})
        arch = self._home_arch()
        self.assertIn('Relevé', arch)
        self.assertIn('Sucre', arch)        # l'autre variante intacte
        self.assertNotIn('Piquant', arch)   # ancien libellé remplacé

    def test_variant_specific_image_triggers_refresh(self):
        """Donner une image propre à une variante bascule l'URL image de sa card."""
        from odoo.addons.dorevia_ck_marketone_content.home_featured import (
            _featured_card_arch_chunk,
        )
        cat = _ensure_featured_category(self.env)
        template, _va, _vb = self._make_two_variant_product(
            'CK Multi Image', public_categ_ids=[(4, cat.id)],
        )
        bootstrap_home_featured_products(self.env)
        variant = template.product_variant_ids[0]
        arch = self._home_arch()
        chunk = _featured_card_arch_chunk(arch, variant)
        self.assertIn(f'/web/image/product.template/{template.id}/image_512', chunk)
        self.assertNotIn(f'/web/image/product.product/{variant.id}/image_512', chunk)

        variant.write({'image_variant_1920': _TINY_PNG})
        arch = self._home_arch()
        chunk = _featured_card_arch_chunk(arch, variant)
        self.assertIn(f'/web/image/product.product/{variant.id}/image_512', chunk)

    def test_variant_price_change_does_not_contaminate_other(self):
        """Changer le prix d'une variante n'affecte pas l'autre (isolation)."""
        cat = _ensure_featured_category(self.env)
        template, _va, _vb = self._make_two_variant_product(
            'CK Multi Prix', public_categ_ids=[(4, cat.id)],
        )
        bootstrap_home_featured_products(self.env)
        website = self.env['website'].search([], limit=1)
        variant_a, variant_b = template.product_variant_ids[0], template.product_variant_ids[1]
        price_b_before = _get_featured_price_label(self.env, website, variant_b)

        variant_a.product_template_attribute_value_ids[:1].write({'price_extra': 2.0})
        arch = self._home_arch()
        price_a_after = _get_featured_price_label(self.env, website, variant_a)
        price_b_after = _get_featured_price_label(self.env, website, variant_b)
        self.assertIn(price_a_after, arch)
        self.assertEqual(price_b_before, price_b_after)
        self.assertIn(price_b_after, arch)

    def test_each_variant_card_has_its_own_product_id(self):
        """Le panier ajoute la bonne variante : chaque card porte son data-product-id."""
        cat = _ensure_featured_category(self.env)
        template, _va, _vb = self._make_two_variant_product(
            'CK Multi Cart', public_categ_ids=[(4, cat.id)],
        )
        bootstrap_home_featured_products(self.env)
        arch = self._home_arch()
        for variant in template.product_variant_ids:
            self.assertIn(f'data-product-id="{variant.id}"', arch)
