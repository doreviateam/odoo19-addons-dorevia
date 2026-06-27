# -*- coding: utf-8 -*-
from odoo.tests.common import TransactionCase


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

    def test_rayon_template_uses_optional_block_guards(self):
        arch = self.env.ref(
            'dorevia_ck_marketone_content.website_sale_rayon_editorial'
        ).arch_db

        self.assertIn("ck_rayon.get('families')", arch)
        self.assertIn("ck_rayon.get('highlights')", arch)
        self.assertIn("ck_rayon.get('proof')", arch)

    def test_native_shop_title_hidden_when_ck_rayon_is_active(self):
        arch = self.env.ref(
            'dorevia_ck_marketone_content.website_sale_rayon_editorial_hide_native_title'
        ).arch_db

        self.assertIn("//h1[hasclass('o_wsale_shop_title')]", arch)
        self.assertEqual(arch.count('<attribute name="t-if">False</attribute>'), 3)

    def test_featured_wishlist_ssr_is_user_neutral(self):
        arch = self.env.ref(
            'dorevia_ck_marketone_content.ck_featured_card_wishlist_button'
        ).arch_db

        self.assertIn('<t t-set="in_wish" t-value="False"/>', arch)
        self.assertNotIn('_is_in_wishlist()', arch)
