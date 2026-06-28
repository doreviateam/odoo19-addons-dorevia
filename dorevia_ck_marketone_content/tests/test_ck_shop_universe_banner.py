# -*- coding: utf-8 -*-
from html import unescape
import re

from odoo.tests import tagged
from odoo.tests.common import HttpCase, TransactionCase

from odoo.addons.dorevia_ck_marketone_content.hooks import EPICERIE_CATEGORY_NAME


@tagged('post_install', '-at_install', 'dorevia_ck_shop_u3')
class TestCkShopUniverseBannerHttp(HttpCase):

    SHOP_PATHS = (
        ('/shop', 'Boutique C-Kréyòl'),
        ('/shop/category/epicerie-1', 'Épicerie créole'),
        ('/shop/category/boissons-123', 'Boissons des îles'),
        ('/shop/category/soin-bien-etre-2', 'Soin & bien-être créole'),
        ('/shop/category/artisanat-3', 'Artisanat & culture'),
    )

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

    def test_shop_pages_single_ck_h1_without_editorial_banner(self):
        for path, expected_title in self.SHOP_PATHS:
            with self.subTest(path=path):
                html = self._shop_html(path)
                self.assertNotIn('ck-rayon-banner', html, path)
                self.assertNotIn('ck-rayon-families', html, path)
                self.assertNotIn('ck-rayon-header__highlights', html, path)
                self.assertIn('ck-shop-intro--title-only', html, path)
                h1_texts = self._visible_h1_texts(html)
                self.assertEqual(
                    len(h1_texts), 1,
                    f'{path}: un seul H1 attendu, trouvé {h1_texts!r}',
                )
                self.assertIn(expected_title, h1_texts[0])

    def test_subcategory_inherits_parent_universe_h1(self):
        root = self.env['product.public.category'].sudo().search(
            [('ck_universe', '=', 'epicerie')],
            limit=1,
        )
        if not root:
            root = self.env['product.public.category'].sudo().search(
                [('name', '=', EPICERIE_CATEGORY_NAME)],
                limit=1,
            )
        if not root:
            self.skipTest('Catégorie Épicerie absente sur instance seed.')
        child = self.env['product.public.category'].sudo().search(
            [('parent_id', '=', root.id)],
            limit=1,
        )
        if not child:
            vals = {
                'name': 'CK Shop-U3 sous-catégorie éphémère',
                'parent_id': root.id,
            }
            if 'website_published' in self.env['product.public.category']._fields:
                vals['website_published'] = True
            child = self.env['product.public.category'].sudo().create(vals)
            self.addCleanup(child.sudo().unlink)
        slug = self.env['ir.http'].sudo()._slug(child)
        html = self._shop_html(f'/shop/category/{slug}')
        h1_texts = self._visible_h1_texts(html)
        self.assertEqual(len(h1_texts), 1)
        self.assertIn('Épicerie créole', h1_texts[0])
        self.assertNotIn('o_wsale_shop_title', html)

    def test_shop_no_native_duplicate_h1(self):
        html = self._shop_html('/shop')
        self.assertEqual(html.count('o_wsale_shop_title'), 0)
        self.assertEqual(html.count('o_wsale_category_title'), 0)


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
        self.assertNotIn('families', banner)
        self.assertNotIn('highlights', banner)

    def test_rayon_template_renders_compact_title_only(self):
        arch = self.env.ref(
            'dorevia_ck_marketone_content.website_sale_rayon_editorial'
        ).arch_db

        self.assertIn('ck-shop-intro--title-only', arch)
        self.assertIn("ck_rayon['title']", arch)
        self.assertNotIn('ck-rayon-banner', arch)
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
