# -*- coding: utf-8 -*-
"""Axe B — libellés navigation + ruban Nouveau ! (S2 : nav pilotée par catégories)."""

from odoo.tests import tagged
from odoo.tests.common import TransactionCase

from odoo.addons.dorevia_ck_marketone_content.nav_sync import bootstrap_ck_navigation
from odoo.addons.dorevia_ck_marketone_content.nav_v22_config import (
    LEGACY_NAV_MAISON_LABEL,
    NAV_MAISON_LABEL,
)
from odoo.addons.dorevia_ck_marketone_content.ribbon_sync import (
    NOUVEAU_RIBBON_LABEL,
    francize_new_product_ribbon,
)


@tagged('post_install', '-at_install', 'dorevia_ck_nav_axe_b')
class TestCkNavAxeBLabels(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.website = cls.env['website'].search([], limit=1)
        cls.Menu = cls.env['website.menu'].sudo()
        cls.root = cls.website.menu_id
        cls.Category = cls.env['product.public.category'].sudo()

    def _menu_by_name(self, name):
        return self.Menu.search([
            ('website_id', '=', self.website.id),
            ('parent_id', '=', self.root.id),
            ('name', '=', name),
        ])

    def test_bootstrap_does_not_force_soin_label_without_category(self):
        """S2 : « Soin & Bien-être » n'est plus injecté par V2.2 — uniquement si catégorie exposable."""
        bootstrap_ck_navigation(self.env)

        self.assertFalse(
            self._menu_by_name(LEGACY_NAV_MAISON_LABEL),
            'Ancien libellé Maison & Bien-être absent',
        )
        soin = self._menu_by_name(NAV_MAISON_LABEL)
        cat = self.Category.search([
            ('name', '=', NAV_MAISON_LABEL),
            ('parent_id', '=', False),
        ], limit=1)
        if cat and cat._is_ck_exposable():
            self.assertEqual(len(soin), 1)
            self.assertIn('/shop/category/', soin.url)
            self.assertFalse(soin.is_mega_menu)
        else:
            self.assertFalse(soin)

    def test_francize_new_ribbon_renames_odoo_default(self):
        Ribbon = self.env['product.ribbon'].sudo()
        legacy = Ribbon.create({'name': 'New!'})
        francize_new_product_ribbon(self.env)
        self.assertEqual(legacy.name, NOUVEAU_RIBBON_LABEL)
