# -*- coding: utf-8 -*-
"""Axe B — libellés navigation Soin & Bien-être + ruban Nouveau !."""

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

    def _menu_by_name(self, name):
        return self.Menu.search([
            ('website_id', '=', self.website.id),
            ('parent_id', '=', self.root.id),
            ('name', '=', name),
        ])

    def test_bootstrap_exposes_soin_bien_etre_nav_label(self):
        bootstrap_ck_navigation(self.env)

        soin = self._menu_by_name(NAV_MAISON_LABEL)
        self.assertEqual(len(soin), 1, msg='Une seule entrée Soin & Bien-être attendue')
        self.assertIn('/shop/category/', soin.url)
        self.assertFalse(self._menu_by_name(LEGACY_NAV_MAISON_LABEL))

    def test_francize_new_ribbon_renames_odoo_default(self):
        Ribbon = self.env['product.ribbon'].sudo()
        legacy = Ribbon.create({'name': 'New!'})
        francize_new_product_ribbon(self.env)
        self.assertEqual(legacy.name, NOUVEAU_RIBBON_LABEL)
