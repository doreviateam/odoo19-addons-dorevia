# -*- coding: utf-8 -*-
"""CK-UNIVERSE-BANNER-001 Lot A — banner éditorial niveau 0.

Réécriture complète (note_09_reponse.md §1.7) : l'ancienne version de ce
fichier affirmait explicitement l'absence de bannière (Shop-U3). La cible
Lot A la réintroduit sur les catégories e-commerce niveau 0 uniquement.
"""
import base64
from html import unescape
import re

from odoo.tests import tagged
from odoo.tests.common import HttpCase, TransactionCase

# PNG transparent 1x1 — suffisant pour peupler image_1920 sans dépendre d'un
# asset externe.
_ONE_PIXEL_PNG = base64.b64encode(
    b'\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01\x00\x00\x00\x01'
    b'\x08\x06\x00\x00\x00\x1f\x15\xc4\x89\x00\x00\x00\nIDATx\x9cc\x00\x01'
    b'\x00\x00\x05\x00\x01\r\n-\xb4\x00\x00\x00\x00IEND\xaeB`\x82'
)

UNIVERSE_TITLES = {
    'epicerie': 'Épicerie créole',
    'boissons': 'Boissons des îles',
    'soin': 'Soin & bien-être créole',
    'artisanat': 'Artisanat & culture',
}


@tagged('post_install', '-at_install', 'dorevia_ck_universe_banner')
class TestCkShopUniverseBannerHttp(HttpCase):

    def _shop_html(self, path):
        resp = self.url_open(path)
        self.assertEqual(resp.status_code, 200, path)
        return resp.text

    def _visible_h1_texts(self, page_html):
        return [
            unescape(re.sub(r'\s+', ' ', m.group(1)).strip())
            for m in re.finditer(
                r'<h1\b[^>]*>([\s\S]*?)</h1>',
                page_html,
                flags=re.IGNORECASE,
            )
            if 'd-none' not in m.group(0) and 'visually-hidden' not in m.group(0)
        ]

    def _root_category_for_universe(self, universe):
        Category = self.env['product.public.category'].sudo()
        category = Category.search([('ck_universe', '=', universe)], limit=1)
        if not category:
            self.skipTest(f"Catégorie racine univers '{universe}' absente sur instance seed.")
        return category

    def _slug(self, category):
        return self.env['ir.http'].sudo()._slug(category)

    def test_universe_root_categories_show_banner(self):
        """Q1 — banner présent sur les 4 univers niveau 0, résolution dynamique (ajustement #4)."""
        for universe, expected_title in UNIVERSE_TITLES.items():
            with self.subTest(universe=universe):
                category = self._root_category_for_universe(universe)
                html = self._shop_html(f'/shop/category/{self._slug(category)}')
                self.assertIn('ck-univers-banner', html, universe)
                self.assertNotIn('ck-shop-intro--title-only', html, universe)
                h1_texts = self._visible_h1_texts(html)
                self.assertEqual(len(h1_texts), 1, f'{universe}: un seul H1 attendu, trouvé {h1_texts!r}')
                self.assertIn(expected_title, h1_texts[0])

    def test_shop_general_no_banner(self):
        """Q2 — pas de banner sur /shop général, fallback H1 compact conservé."""
        html = self._shop_html('/shop')
        self.assertNotIn('ck-univers-banner', html)
        self.assertIn('ck-shop-intro--title-only', html)
        h1_texts = self._visible_h1_texts(html)
        self.assertEqual(len(h1_texts), 1, f'un seul H1 attendu, trouvé {h1_texts!r}')
        self.assertIn('Boutique C-Kréyòl', h1_texts[0])

    def test_subcategory_no_banner_inherits_parent_universe_h1(self):
        """Q3 — pas de banner sur sous-catégorie, H1 compact hérité de l'univers parent."""
        root = self._root_category_for_universe('epicerie')
        child = self.env['product.public.category'].sudo().search(
            [('parent_id', '=', root.id)], limit=1)
        if not child:
            vals = {'name': 'CK Note09 sous-catégorie éphémère', 'parent_id': root.id}
            if 'is_published' in self.env['product.public.category']._fields:
                vals['is_published'] = True
            if 'website_published' in self.env['product.public.category']._fields:
                vals['website_published'] = True
            child = self.env['product.public.category'].sudo().create(vals)
            self.addCleanup(child.sudo().unlink)
        html = self._shop_html(f'/shop/category/{self._slug(child)}')
        self.assertNotIn('ck-univers-banner', html)
        self.assertIn('ck-shop-intro--title-only', html)
        h1_texts = self._visible_h1_texts(html)
        self.assertEqual(len(h1_texts), 1)
        self.assertIn('Épicerie créole', h1_texts[0])
        self.assertNotIn('o_wsale_shop_title', html)

    def test_shop_no_native_duplicate_h1(self):
        html = self._shop_html('/shop')
        self.assertEqual(html.count('o_wsale_shop_title'), 0)
        self.assertEqual(html.count('o_wsale_category_title'), 0)

    def _create_root_category(self, name, universe, with_image, with_subtitle):
        Category = self.env['product.public.category'].sudo()
        vals = {
            'name': name,
            'parent_id': False,
            'ck_universe': universe,
        }
        if with_image:
            vals['image_1920'] = _ONE_PIXEL_PNG
        if with_subtitle:
            vals['ck_subtitle'] = 'Une accroche de test courte.'
        if 'is_published' in Category._fields:
            vals['is_published'] = True
        if 'website_published' in Category._fields:
            vals['website_published'] = True
        category = Category.create(vals)
        product = self.env['product.template'].sudo().create({
            'name': f'Produit QA {name}',
            'type': 'consu',
            'sale_ok': True,
            'is_published': True,
            'website_published': True,
            'public_categ_ids': [(4, category.id)],
        })
        self.addCleanup(category.unlink)
        self.addCleanup(product.unlink)
        return category

    def test_banner_with_image_and_subtitle(self):
        """Q4 + Q6 (présent) — image et accroche rendues quand renseignées."""
        category = self._create_root_category(
            'CK Note09 univers avec image', 'epicerie', with_image=True, with_subtitle=True)
        html = self._shop_html(f'/shop/category/{self._slug(category)}')
        self.assertIn('ck-univers-banner', html)
        self.assertNotIn('ck-univers-banner--no-image', html)
        self.assertIn('<img', html)
        self.assertIn('aria-hidden="true"', html)
        self.assertIn('ck-univers-banner__subtitle', html)

    def test_banner_fallback_without_image_or_subtitle(self):
        """Q5 + Q6 (absent) — fallback fond clair CK, pas de bloc accroche vide."""
        category = self._create_root_category(
            'CK Note09 univers sans image', 'boissons', with_image=False, with_subtitle=False)
        html = self._shop_html(f'/shop/category/{self._slug(category)}')
        self.assertIn('ck-univers-banner', html)
        self.assertIn('ck-univers-banner--no-image', html)
        self.assertNotIn('ck-univers-banner__subtitle', html)
        h1_texts = self._visible_h1_texts(html)
        self.assertEqual(len(h1_texts), 1)


class TestCkShopUniverseBanner(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Category = cls.env['product.public.category'].sudo()
        cls.View = cls.env['ir.ui.view'].sudo()

    def test_shop_banner_fallback_has_no_optional_blocks(self):
        banner = self.Category.get_ck_shop_banner()

        self.assertEqual(banner['title'], 'Boutique C-Kréyòl')
        self.assertEqual(
            banner['phrase'],
            'Produits créoles sélectionnés, aux origines identifiées, pour découvrir '
            'des saveurs, des soins et des savoir-faire issus des territoires.',
        )
        self.assertIsNone(banner['subtitle'])
        self.assertIsNone(banner['image_url'])
        self.assertNotIn('families', banner)
        self.assertNotIn('highlights', banner)

    def test_rayon_template_renders_banner_and_compact_fallback(self):
        arch = self.env.ref(
            'dorevia_ck_marketone_content.website_sale_rayon_editorial'
        ).arch_db

        self.assertIn('ck-univers-banner', arch)
        self.assertIn('ck_univers_banner', arch)
        self.assertIn('ck-shop-intro--title-only', arch)
        self.assertIn("ck_rayon['title']", arch)
        self.assertNotIn('ck-rayon-families', arch)
        self.assertNotIn('ck-rayon-header__highlights', arch)

    def test_native_shop_title_hidden_only_when_ck_rayon_active(self):
        arch = self.env.ref(
            'dorevia_ck_marketone_content.website_sale_rayon_editorial_hide_native_title'
        ).arch_db

        self.assertIn("//header[@id='o_wsale_products_header']/h1[1]", arch)
        self.assertIn("//h1[hasclass('o_wsale_shop_title')]", arch)
        self.assertIn('not ck_rayon', arch)
        self.assertNotIn('<attribute name="t-if">False</attribute>', arch)

    def test_featured_wishlist_ssr_is_user_neutral(self):
        arch = self.env.ref(
            'dorevia_ck_marketone_content.ck_featured_card_wishlist_button'
        ).arch_db

        self.assertIn('<t t-set="in_wish" t-value="False"/>', arch)
        self.assertNotIn('_is_in_wishlist()', arch)
