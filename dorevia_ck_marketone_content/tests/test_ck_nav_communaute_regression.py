# -*- coding: utf-8 -*-
"""Non-régression Communauté — S2 : bootstrap V3 ne réintroduit pas le mega V2.2."""

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
    NAV_CATALOGUE_BOUTIQUE_LABEL,
    NAV_CATALOGUE_PRODUCTEURS_LABEL,
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
        cls.Category = cls.env['product.public.category'].sudo()

    def _menu_by_name(self, name):
        return self.Menu.search([
            ('website_id', '=', self.website.id),
            ('parent_id', '=', self.root.id),
            ('name', '=', name),
        ], limit=1)

    def _category_exposable(self, name):
        cat = self.Category.search([
            ('name', '=', name),
            ('parent_id', '=', False),
        ], limit=1)
        return bool(cat and cat._is_ck_exposable())

    def test_sync_communaute_does_not_unpublish_seed_products(self):
        ensure_moa_seed_catalog_published(self.env)
        before = count_moa_seed_published_products(self.env)
        if before < MOA_SEED_MIN_PUBLISHED_COUNT:
            self.skipTest('Catalogue seed MOA incomplet sur cette instance.')

        sync_communaute_header(self.env)

        after = count_moa_seed_published_products(self.env)
        self.assertEqual(after, before)

    def test_moa_seed_catalog_has_seven_published_after_guard(self):
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

    def test_bootstrap_v3_communaute_root_and_coups_purged(self):
        """S6-B1 A1 — révocation S2 : Communauté racine V3 ; Coups de cœur reste purgé.

        Remplace ``test_bootstrap_v3_does_not_restore_v22_selection_menus``
        (arbitrage MOA 2026-07-20 — mandat S6-B1 amendé). Assertion chirurgicale :
        un seul des deux libellés S2 change de statut.
        """
        ensure_moa_seed_catalog_published(self.env)
        # Injecter Coups de cœur pour vérifier la purge persistante.
        self.Menu.create({
            'name': LEGACY_NAV_COUPS_LABEL,
            'url': '#',
            'website_id': self.website.id,
            'parent_id': self.root.id,
            'sequence': 999,
        })
        bootstrap_ck_navigation(self.env)

        communaute = self._menu_by_name(NAV_COMMUNAUTE_LABEL)
        self.assertTrue(communaute, 'Communauté doit persister comme racine V3')
        self.assertEqual(communaute.url, '#')
        self.assertFalse(self._menu_by_name(LEGACY_NAV_COUPS_LABEL))
        self.assertTrue(self._menu_by_name(NAV_CATALOGUE_BOUTIQUE_LABEL))
        self.assertTrue(self._menu_by_name(NAV_CATALOGUE_PRODUCTEURS_LABEL))

        for label in (NAV_BOISSONS_LABEL, NAV_MAISON_LABEL, NAV_ARTISANAT_LABEL):
            menu = self._menu_by_name(label)
            if self._category_exposable(label):
                self.assertTrue(menu, msg=f'« {label} » exposable doit être en nav catalogue')
                self.assertFalse(menu.is_mega_menu)
            else:
                self.assertFalse(
                    menu,
                    msg=f'« {label} » non exposable ne doit pas être réintroduit en mega V2.2',
                )
