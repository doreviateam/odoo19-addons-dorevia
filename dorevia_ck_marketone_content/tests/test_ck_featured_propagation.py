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
