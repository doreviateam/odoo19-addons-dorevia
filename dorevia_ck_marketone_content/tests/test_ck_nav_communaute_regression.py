# -*- coding: utf-8 -*-
"""Non-régression — ticket Navigation Communauté (catalogue + menus rayons)."""

from odoo.tests import tagged
from odoo.tests.common import TransactionCase

from odoo.addons.dorevia_ck_marketone_content.catalog_seed_guard import (
    MOA_SEED_MIN_PUBLISHED_COUNT,
    MOA_SEED_PUBLISHED_PRODUCT_NAMES,
    count_moa_seed_published_products,
    ensure_moa_seed_catalog_published,
)
from odoo.addons.dorevia_ck_marketone_content.nav_sync import (
    bootstrap_ck_navigation,
    sync_communaute_header,
)
from odoo.addons.dorevia_ck_marketone_content.nav_v22_config import (
    LEGACY_NAV_COUPS_LABEL,
    NAV_ARTISANAT_LABEL,
    NAV_BOISSONS_LABEL,
    NAV_COMMUNAUTE_LABEL,
    NAV_MAISON_LABEL,
)


@tagged('post_install', '-at_install', 'dorevia_ck_nav_communaute')
class TestCkNavCommunauteRegression(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.website = cls.env['website'].search([], limit=1)
        cls.Menu = cls.env['website.menu'].sudo()
        cls.root = cls.website.menu_id
        cls.Template = cls.env['product.template'].sudo()

    def _menu_by_name(self, name):
        return self.Menu.search([
            ('website_id', '=', self.website.id),
            ('parent_id', '=', self.root.id),
            ('name', '=', name),
        ], limit=1)

    def test_sync_communaute_does_not_unpublish_seed_products(self):
        ensure_moa_seed_catalog_published(self.env)
        before = count_moa_seed_published_products(self.env)
        self.assertGreaterEqual(before, MOA_SEED_MIN_PUBLISHED_COUNT)

        sync_communaute_header(self.env)

        after = count_moa_seed_published_products(self.env)
        self.assertEqual(after, before)

    def test_moa_seed_catalog_has_seven_published_after_guard(self):
        # Simule une dépublication accidentelle (rollback TransactionCase en fin).
        seed_products = self.Template.search([
            ('name', 'in', list(MOA_SEED_PUBLISHED_PRODUCT_NAMES)),
        ])
        if len(seed_products) < MOA_SEED_MIN_PUBLISHED_COUNT:
            self.skipTest('Catalogue seed MOA incomplet sur cette instance.')
        seed_products.write({'is_published': False, 'website_published': False})

        ensure_moa_seed_catalog_published(self.env)

        count = count_moa_seed_published_products(self.env)
        self.assertGreaterEqual(
            count,
            MOA_SEED_MIN_PUBLISHED_COUNT,
            msg='Les 7 produits seed MOA doivent être republiés',
        )

    def test_rayon_menus_restored_after_guard_and_bootstrap(self):
        ensure_moa_seed_catalog_published(self.env)
        sync_communaute_header(self.env)
        bootstrap_ck_navigation(self.env)

        self.assertTrue(self._menu_by_name(NAV_COMMUNAUTE_LABEL))
        self.assertFalse(self._menu_by_name(LEGACY_NAV_COUPS_LABEL))

        for label in (NAV_BOISSONS_LABEL, NAV_MAISON_LABEL, NAV_ARTISANAT_LABEL):
            menu = self._menu_by_name(label)
            self.assertTrue(
                menu,
                msg=f'Entrée menu rayon « {label} » attendue après bootstrap',
            )
