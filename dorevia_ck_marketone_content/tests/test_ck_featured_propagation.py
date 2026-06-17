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

    def test_variant_unlisted_field_write_repairs_stale_card(self):
        """Filet agnostique : tout write variante répare une card vedette périmée."""
        from odoo.addons.dorevia_ck_marketone_content.home_featured import (
            _featured_card_arch_chunk,
        )
        cat = _ensure_featured_category(self.env)
        product = self._make_product(
            'CK Vedette Filet', list_price=4.0, public_categ_ids=[(4, cat.id)],
        )
        variant = product.product_variant_id
        bootstrap_home_featured_products(self.env)
        page = self.env['website.page'].sudo().search([('url', '=', '/')], limit=1)
        # Simule un snapshot SSR figé (dérive BO non captée par un déclencheur connu).
        page.view_id.sudo().write({
            'arch_db': (page.view_id.arch_db or '').replace('4,00', '9,99'),
        })
        self.assertIn('9,99', self._home_arch())

        # Champ hors liste explicite (default_code) → doit déclencher la réparation
        # car le rendu attendu de la card diffère du snapshot.
        variant.write({'default_code': 'CK-FILET-1'})
        arch = self._home_arch()
        self.assertIn('4,00', _featured_card_arch_chunk(arch, variant))
        self.assertNotIn('9,99', arch)

    def test_variant_unlisted_field_write_keeps_fresh_snapshot(self):
        """Pas de sur-rebuild : un write hors rendu sur snapshot frais ne change rien."""
        cat = _ensure_featured_category(self.env)
        product = self._make_product(
            'CK Vedette Filet Noop', public_categ_ids=[(4, cat.id)],
        )
        variant = product.product_variant_id
        bootstrap_home_featured_products(self.env)
        before = self._home_arch()

        variant.write({'default_code': 'CK-FILET-NOOP'})
        self.assertEqual(before, self._home_arch())

    # --- Éligibilité : entrée / sortie de la grille vedette ---

    def test_template_unpublish_removes_its_variant_cards(self):
        """Dépublier le template retire toutes ses cards variantes de la grille.

        ``is_published`` / ``sale_ok`` délèguent au template en Odoo (pas de flag
        par-variante) : l'éligibilité est donc gérée au niveau template.
        """
        cat = _ensure_featured_category(self.env)
        template, _va, _vb = self._make_two_variant_product(
            'CK Multi Unpublish', public_categ_ids=[(4, cat.id)],
        )
        variant_a, variant_b = template.product_variant_ids[0], template.product_variant_ids[1]
        bootstrap_home_featured_products(self.env)
        arch = self._home_arch()
        self.assertIn(f'data-product-id="{variant_a.id}"', arch)
        self.assertIn(f'data-product-id="{variant_b.id}"', arch)

        template.write({'website_published': False})
        arch = self._home_arch()
        self.assertNotIn(f'data-product-id="{variant_a.id}"', arch)
        self.assertNotIn(f'data-product-id="{variant_b.id}"', arch)

    def test_template_republish_restores_its_variant_cards(self):
        """Re-publier le template restaure ses cards variantes."""
        cat = _ensure_featured_category(self.env)
        template, _va, _vb = self._make_two_variant_product(
            'CK Multi Republish', public_categ_ids=[(4, cat.id)],
        )
        variant_a, variant_b = template.product_variant_ids[0], template.product_variant_ids[1]
        bootstrap_home_featured_products(self.env)
        template.write({'website_published': False})
        self.assertNotIn(f'data-product-id="{variant_a.id}"', self._home_arch())

        template.write({'website_published': True})
        arch = self._home_arch()
        self.assertIn(f'data-product-id="{variant_a.id}"', arch)
        self.assertIn(f'data-product-id="{variant_b.id}"', arch)

    def test_template_sale_ok_false_removes_its_cards(self):
        """Template non vendable (sale_ok=False) → retiré de la grille vedette."""
        cat = _ensure_featured_category(self.env)
        template, _va, _vb = self._make_two_variant_product(
            'CK Multi SaleOk', public_categ_ids=[(4, cat.id)],
        )
        variant_a, variant_b = template.product_variant_ids[0], template.product_variant_ids[1]
        bootstrap_home_featured_products(self.env)
        self.assertIn(f'data-product-id="{variant_a.id}"', self._home_arch())

        template.write({'sale_ok': False})
        arch = self._home_arch()
        self.assertNotIn(f'data-product-id="{variant_a.id}"', arch)
        self.assertNotIn(f'data-product-id="{variant_b.id}"', arch)

    # --- Contenu : tags, prix simultané, image, isolation inter-template ---

    def test_variant_additional_tag_propagates_to_labels(self):
        """Ajouter une étiquette propre à une variante l'affiche dans sa ligne méta."""
        from odoo.addons.dorevia_ck_marketone_content.home_featured import (
            _featured_card_arch_chunk,
        )
        cat = _ensure_featured_category(self.env)
        template, _va, _vb = self._make_two_variant_product(
            'CK Multi Tag', public_categ_ids=[(4, cat.id)],
        )
        variant_a, variant_b = template.product_variant_ids[0], template.product_variant_ids[1]
        tag = self.env['product.tag'].sudo().create({'name': 'EditionLimitee'})
        bootstrap_home_featured_products(self.env)

        variant_a.write({'additional_product_tag_ids': [(4, tag.id)]})
        arch = self._home_arch()
        self.assertIn('EditionLimitee', _featured_card_arch_chunk(arch, variant_a))
        self.assertNotIn('EditionLimitee', _featured_card_arch_chunk(arch, variant_b))

    def test_two_variants_simultaneous_price_change_are_distinct(self):
        """Modifier le prix des deux variantes : chaque card reflète son propre prix."""
        from odoo.addons.dorevia_ck_marketone_content.home_featured import (
            _featured_card_arch_chunk,
        )
        cat = _ensure_featured_category(self.env)
        template, _va, _vb = self._make_two_variant_product(
            'CK Multi Dual Price', public_categ_ids=[(4, cat.id)],
        )
        variant_a, variant_b = template.product_variant_ids[0], template.product_variant_ids[1]
        bootstrap_home_featured_products(self.env)
        website = self.env['website'].search([], limit=1)

        variant_a.product_template_attribute_value_ids[:1].write({'price_extra': 1.0})
        variant_b.product_template_attribute_value_ids[:1].write({'price_extra': 2.0})
        arch = self._home_arch()
        label_a = _get_featured_price_label(self.env, website, variant_a)
        label_b = _get_featured_price_label(self.env, website, variant_b)
        self.assertNotEqual(label_a, label_b)
        self.assertIn(label_a, _featured_card_arch_chunk(arch, variant_a))
        self.assertIn(label_b, _featured_card_arch_chunk(arch, variant_b))

    def test_variant_image_clear_reverts_to_template(self):
        """Retirer l'image propre d'une variante rebascule la card sur l'image template."""
        from odoo.addons.dorevia_ck_marketone_content.home_featured import (
            _featured_card_arch_chunk,
        )
        cat = _ensure_featured_category(self.env)
        template, _va, _vb = self._make_two_variant_product(
            'CK Multi Image Clear', public_categ_ids=[(4, cat.id)],
        )
        variant = template.product_variant_ids[0]
        bootstrap_home_featured_products(self.env)

        variant.write({'image_variant_1920': _TINY_PNG})
        chunk = _featured_card_arch_chunk(self._home_arch(), variant)
        self.assertIn(f'/web/image/product.product/{variant.id}/image_512', chunk)

        variant.write({'image_variant_1920': False})
        chunk = _featured_card_arch_chunk(self._home_arch(), variant)
        self.assertIn(f'/web/image/product.template/{template.id}/image_512', chunk)
        self.assertNotIn(f'/web/image/product.product/{variant.id}/image_512', chunk)

    def test_variant_change_keeps_other_template_card_identical(self):
        """Isolation inter-template : éditer une variante n'altère pas les autres cards."""
        from odoo.addons.dorevia_ck_marketone_content.home_featured import (
            _featured_card_arch_chunk,
        )
        cat = _ensure_featured_category(self.env)
        template_a, _a1, _a2 = self._make_two_variant_product(
            'CK Iso A', public_categ_ids=[(4, cat.id)],
        )
        other = self._make_product('CK Iso B', list_price=6.0, public_categ_ids=[(4, cat.id)])
        other_variant = other.product_variant_id
        bootstrap_home_featured_products(self.env)
        before = _featured_card_arch_chunk(self._home_arch(), other_variant)
        self.assertTrue(before)

        template_a.product_variant_ids[0].write({'lst_price': 9.0})
        after = _featured_card_arch_chunk(self._home_arch(), other_variant)
        self.assertEqual(before, after)

    def test_simple_product_price_change_regression(self):
        """Non-régression produit simple : changement de prix propagé à la card."""
        from odoo.addons.dorevia_ck_marketone_content.home_featured import (
            _featured_card_arch_chunk,
        )
        cat = _ensure_featured_category(self.env)
        product = self._make_product(
            'CK Simple Regress', list_price=4.0, public_categ_ids=[(4, cat.id)],
        )
        variant = product.product_variant_id
        bootstrap_home_featured_products(self.env)
        website = self.env['website'].search([], limit=1)

        variant.write({'lst_price': 8.5})
        expected = _get_featured_price_label(self.env, website, variant)
        self.assertIn(expected, _featured_card_arch_chunk(self._home_arch(), variant))
