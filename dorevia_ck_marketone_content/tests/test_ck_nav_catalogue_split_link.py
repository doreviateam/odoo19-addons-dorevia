# -*- coding: utf-8 -*-
"""CK-NAV-005 — racines catalogue niveau 0 cliquables (desktop + mobile).

Les deux classes CSS (``ck-nav-universe-split__*`` en desktop,
``ck-nav-mobile-catalogue-split__*`` en mobile) ne sont posées que par les
deux nouvelles branches QWeb de ce ticket : leur seule présence dans le HTML
suffit à identifier sans ambiguïté le rendu concerné, sans avoir à isoler le
bloc ``#top_menu`` / ``#top_menu_collapse_mobile`` (dropdowns imbriqués
rendant une extraction par regex non fiable).
"""

import re

from odoo.tests import tagged
from odoo.tests.common import HttpCase

from odoo.addons.dorevia_ck_marketone_content.nav_sync import (
    sync_ck_catalogue_navigation_for_website,
)


@tagged('post_install', '-at_install', 'dorevia_ck_nav_catalogue')
class TestCkNavCatalogueSplitLink(HttpCase):

    def setUp(self):
        super().setUp()
        self.website = self.env['website'].search([], limit=1)
        Category = self.env['product.public.category'].sudo()
        Product = self.env['product.template'].sudo()

        # Racine AVEC sous-catégorie éligible — doit produire le split lien/toggle.
        self.cat_root = Category.create({'name': 'TestCat NAV005 Rayon', 'sequence': 950})
        self.cat_child = Category.create({
            'name': 'TestCat NAV005 Child',
            'parent_id': self.cat_root.id,
            'sequence': 10,
        })
        # CATALOG-ARCHI-001 : seuil d'exposition = 3 produits qualifiés / catégorie.
        for idx in range(3):
            Product.create({
                'name': f'Test Produit NAV005 Root {idx}',
                'sale_ok': True,
                'is_published': True,
                'website_published': True,
                'public_categ_ids': [(4, self.cat_root.id)],
            })
            Product.create({
                'name': f'Test Produit NAV005 Child {idx}',
                'sale_ok': True,
                'is_published': True,
                'website_published': True,
                'public_categ_ids': [(4, self.cat_child.id)],
            })

        # Racine SANS sous-catégorie — doit rester un lien simple (non-régression).
        self.cat_leaf = Category.create({'name': 'TestCat NAV005 Rayon Simple', 'sequence': 960})
        for idx in range(3):
            Product.create({
                'name': f'Test Produit NAV005 Leaf {idx}',
                'sale_ok': True,
                'is_published': True,
                'website_published': True,
                'public_categ_ids': [(4, self.cat_leaf.id)],
            })

        sync_ck_catalogue_navigation_for_website(self.env, self.website)
        self.env.flush_all()
        menu = self.env['website.menu'].sudo().search([
            ('website_id', '=', self.website.id),
            ('parent_id', '=', self.website.menu_id.id),
            ('name', '=', self.cat_root.name),
        ], limit=1)
        self.assertTrue(menu, 'Précondition : menu TestCat NAV005 Rayon après sync')
        self.assertTrue(menu.child_id, 'Précondition : enfants L2 sur le menu test')

    def _home_html(self):
        resp = self.url_open('/?qa_ts=nav005')
        self.assertEqual(resp.status_code, 200)
        return resp.text

    def _tag_with_class(self, html, css_class):
        match = re.search(r'<a\b[^>]*class="[^"]*%s[^"]*"[^>]*>' % re.escape(css_class), html)
        self.assertTrue(match, f'Balise <a> avec classe {css_class!r} introuvable')
        return match.group(0)

    def _href_of(self, tag):
        match = re.search(r'href="([^"]*)"', tag)
        self.assertTrue(match, 'Attribut href introuvable')
        return match.group(1)

    # --- Desktop ---

    def test_desktop_category_with_children_has_real_link(self):
        html = self._home_html()
        self.assertIn(self.cat_root.name, html)
        tag = self._tag_with_class(html, 'ck-nav-universe-split__link')
        href = self._href_of(tag)
        self.assertNotEqual(href, '#', 'Le libellé cliquable ne doit pas pointer vers #')
        self.assertIn('/shop/category/', href)
        self.assertIn('ck-nav-universe-split__toggle', html)

    def test_desktop_category_without_children_stays_simple_link(self):
        html = self._home_html()
        item = re.search(
            r'<a([^>]*)>\s*<span[^>]*>\s*%s\s*</span>' % re.escape(self.cat_leaf.name),
            html,
        )
        self.assertTrue(item, 'Catégorie sans enfant doit rester un lien simple')
        attrs = item.group(1)
        self.assertNotIn('dropdown-toggle', attrs)
        self.assertNotIn('ck-nav-universe-split', attrs)
        self.assertIn('href=', attrs)

    # --- Mobile ---

    def test_mobile_category_with_children_has_real_link(self):
        html = self._home_html()
        tag = self._tag_with_class(html, 'ck-nav-mobile-catalogue-split__link')
        href = self._href_of(tag)
        self.assertNotEqual(href, '#', 'Le libellé cliquable mobile ne doit pas pointer vers #')
        self.assertIn('/shop/category/', href)
        self.assertIn('ck-nav-mobile-catalogue-split__toggle', html)
