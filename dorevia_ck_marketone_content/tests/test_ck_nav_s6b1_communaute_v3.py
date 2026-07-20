# -*- coding: utf-8 -*-
"""S6-B1 — Communauté racine éditoriale V3 (révocation S2, seq 55, URL #)."""

from odoo.tests import tagged
from odoo.tests.common import TransactionCase

from odoo.addons.dorevia_ck_marketone_content.nav_sync import (
    snapshot_ck_catalogue_navigation,
    sync_ck_catalogue_navigation_for_website,
)
from odoo.addons.dorevia_ck_marketone_content.nav_v22_config import (
    LEGACY_NAV_COUPS_LABEL,
    MANAGED_EDITORIAL_ROOT_NAMES,
    MANAGED_V22_ROOT_NAMES,
    NAV_CATALOGUE_BOUTIQUE_LABEL,
    NAV_CATALOGUE_COMMUNAUTE_SEQUENCE,
    NAV_CATALOGUE_FIRST_CATEGORY_SEQUENCE,
    NAV_CATALOGUE_PRODUCTEURS_LABEL,
    NAV_CATALOGUE_PRODUCTEURS_SEQUENCE,
    NAV_CATALOGUE_PROFESSIONNELS_LABEL,
    NAV_CATALOGUE_PROFESSIONNELS_SEQUENCE,
    NAV_CATALOGUE_PROFESSIONNELS_URL,
    NAV_CATALOGUE_RESERVED_ROOT_SEQUENCES,
    NAV_CATALOGUE_SEQUENCE_STEP,
    NAV_COMMUNAUTE_LABEL,
    NAV_COMMUNAUTE_URL,
)


@tagged('post_install', '-at_install', 'dorevia_ck_nav_s6b1')
class TestCkNavS6B1CommunauteV3(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.website = cls.env['website'].search([], limit=1)
        cls.Menu = cls.env['website.menu'].sudo()
        cls.root = cls.website.menu_id
        Category = cls.env['product.public.category'].sudo()
        Product = cls.env['product.template'].sudo()

        cls.epicerie = Category.create({
            'name': 'Épicerie S6B1',
            'sequence': 900,
            'ck_exposure_status': 'active',
        })
        cls.child_a = Category.create({
            'name': 'Rayon A S6B1',
            'parent_id': cls.epicerie.id,
            'sequence': 10,
            'ck_exposure_status': 'active',
        })
        cls.child_b = Category.create({
            'name': 'Rayon B S6B1',
            'parent_id': cls.epicerie.id,
            'sequence': 20,
            'ck_exposure_status': 'active',
        })
        for cat in (cls.epicerie, cls.child_a, cls.child_b):
            for idx in range(3):
                Product.create({
                    'name': f'Test S6B1 {cat.name} {idx}',
                    'sale_ok': True,
                    'is_published': True,
                    'website_published': True,
                    'public_categ_ids': [(4, cat.id)],
                })

        page = cls.env['website.page'].sudo().search([
            ('url', '=', NAV_CATALOGUE_PROFESSIONNELS_URL),
        ], limit=1)
        if page:
            page.write({'is_published': True})
        else:
            view = cls.env['ir.ui.view'].sudo().create({
                'name': 'Test Page S6B1 Pro',
                'type': 'qweb',
                'key': 'test.ck_nav_s6b1_pro',
                'arch': '<t t-name="test.ck_nav_s6b1"><div>/professionnels</div></t>',
            })
            cls.env['website.page'].sudo().create({
                'name': 'Professionnels S6B1',
                'url': NAV_CATALOGUE_PROFESSIONNELS_URL,
                'is_published': True,
                'website_id': cls.website.id,
                'view_id': view.id,
            })

    def _root_menu(self, name):
        return self.Menu.search([
            ('website_id', '=', self.website.id),
            ('parent_id', '=', self.root.id),
            ('name', '=', name),
        ], limit=1)

    def _sync(self):
        sync_ck_catalogue_navigation_for_website(self.env, self.website)

    def test_s6b1_config_editorial_set_and_not_in_v22_purge(self):
        self.assertIn(NAV_COMMUNAUTE_LABEL, MANAGED_EDITORIAL_ROOT_NAMES)
        self.assertNotIn(NAV_COMMUNAUTE_LABEL, MANAGED_V22_ROOT_NAMES)
        self.assertIn(NAV_CATALOGUE_COMMUNAUTE_SEQUENCE, NAV_CATALOGUE_RESERVED_ROOT_SEQUENCES)
        self.assertEqual(NAV_CATALOGUE_COMMUNAUTE_SEQUENCE, 55)
        self.assertEqual(NAV_COMMUNAUTE_URL, '#')

    def test_s6b1_create_communaute_if_absent(self):
        self.Menu.search([
            ('website_id', '=', self.website.id),
            ('parent_id', '=', self.root.id),
            ('name', '=', NAV_COMMUNAUTE_LABEL),
        ]).unlink()
        self._sync()
        menu = self._root_menu(NAV_COMMUNAUTE_LABEL)
        self.assertTrue(menu)
        self.assertEqual(menu.sequence, 55)
        self.assertEqual(menu.url, '#')

    def test_s6b1_reuse_without_duplicate(self):
        # Partir d'une seule entrée (éventuellement chrome V2.2) pour la reprise.
        self.Menu.search([
            ('website_id', '=', self.website.id),
            ('parent_id', '=', self.root.id),
            ('name', '=', NAV_COMMUNAUTE_LABEL),
        ]).unlink()
        existing = self.Menu.create({
            'name': NAV_COMMUNAUTE_LABEL,
            'url': '/legacy-communaute',
            'website_id': self.website.id,
            'parent_id': self.root.id,
            'sequence': 12,
            'ck_nav_css_class': 'ck-nav-n3-selection',
            'is_mega_menu': True,
        })
        self._sync()
        self.assertEqual(self._root_menu(NAV_COMMUNAUTE_LABEL).id, existing.id)
        self.assertEqual(
            self.Menu.search_count([
                ('website_id', '=', self.website.id),
                ('parent_id', '=', self.root.id),
                ('name', '=', NAV_COMMUNAUTE_LABEL),
            ]),
            1,
        )
        menu = self.Menu.browse(existing.id)
        self.assertEqual(menu.sequence, 55)
        self.assertEqual(menu.url, '#')
        self.assertFalse(menu.is_mega_menu)

    def test_s6b1_idempotent_two_bootstraps(self):
        self._sync()
        before = snapshot_ck_catalogue_navigation(self.env, self.website)
        self._sync()
        after = snapshot_ck_catalogue_navigation(self.env, self.website)
        self.assertEqual(after, before)
        self.assertEqual(
            self.Menu.search_count([
                ('website_id', '=', self.website.id),
                ('parent_id', '=', self.root.id),
                ('name', '=', NAV_COMMUNAUTE_LABEL),
            ]),
            1,
        )

    def test_s6b1_coups_de_coeur_still_purged(self):
        self.Menu.create({
            'name': LEGACY_NAV_COUPS_LABEL,
            'url': '#',
            'website_id': self.website.id,
            'parent_id': self.root.id,
            'sequence': 999,
        })
        self._sync()
        self.assertFalse(self._root_menu(LEGACY_NAV_COUPS_LABEL))
        self.assertTrue(self._root_menu(NAV_COMMUNAUTE_LABEL))

    def test_s6b1_global_order_and_no_side_effects(self):
        self._sync()
        boutique = self._root_menu(NAV_CATALOGUE_BOUTIQUE_LABEL)
        epicerie = self._root_menu(self.epicerie.name)
        communaute = self._root_menu(NAV_COMMUNAUTE_LABEL)
        producteurs = self._root_menu(NAV_CATALOGUE_PRODUCTEURS_LABEL)
        professionnels = self._root_menu(NAV_CATALOGUE_PROFESSIONNELS_LABEL)
        self.assertTrue(all([boutique, epicerie, communaute, producteurs, professionnels]))
        self.assertEqual(boutique.sequence, 10)
        self.assertEqual(epicerie.sequence, NAV_CATALOGUE_FIRST_CATEGORY_SEQUENCE)
        self.assertEqual(communaute.sequence, 55)
        self.assertEqual(producteurs.sequence, NAV_CATALOGUE_PRODUCTEURS_SEQUENCE)
        self.assertEqual(professionnels.sequence, NAV_CATALOGUE_PROFESSIONNELS_SEQUENCE)
        self.assertLess(epicerie.sequence, communaute.sequence)
        self.assertLess(communaute.sequence, producteurs.sequence)

    def test_s6b1_sequence_55_never_assigned_to_category_roots(self):
        """Plusieurs rayons exposables : aucun n'obtient la séquence 55."""
        Category = self.env['product.public.category'].sudo()
        Product = self.env['product.template'].sudo()
        extra_roots = []
        for idx, name in enumerate(('Boissons S6B1', 'Soin S6B1', 'Artisanat S6B1'), start=1):
            cat = Category.create({
                'name': name,
                'sequence': 910 + idx,
                'ck_exposure_status': 'active',
            })
            child = Category.create({
                'name': f'{name} enfant',
                'parent_id': cat.id,
                'sequence': 10,
                'ck_exposure_status': 'active',
            })
            for pidx in range(3):
                Product.create({
                    'name': f'Test S6B1 multi {name} {pidx}',
                    'sale_ok': True,
                    'is_published': True,
                    'website_published': True,
                    'public_categ_ids': [(4, cat.id), (4, child.id)],
                })
            extra_roots.append(cat)

        self._sync()
        self.assertEqual(self._root_menu(NAV_COMMUNAUTE_LABEL).sequence, 55)
        for cat in [self.epicerie, *extra_roots]:
            menu = self._root_menu(cat.name)
            self.assertTrue(menu, f'Racine catégorie « {cat.name} » attendue')
            self.assertNotEqual(
                menu.sequence,
                NAV_CATALOGUE_COMMUNAUTE_SEQUENCE,
                f'La séquence 55 est réservée à Communauté (pas « {cat.name} »)',
            )
            self.assertNotIn(menu.sequence, (
                10,
                NAV_CATALOGUE_COMMUNAUTE_SEQUENCE,
                NAV_CATALOGUE_PRODUCTEURS_SEQUENCE,
                NAV_CATALOGUE_PROFESSIONNELS_SEQUENCE,
            ))

    def test_s6b1_historical_writer_functions_still_importable(self):
        """A2 : sync_communaute_header / _sync_communaute présentes (migrations 39/40)."""
        from odoo.addons.dorevia_ck_marketone_content import nav_sync
        self.assertTrue(callable(nav_sync.sync_communaute_header))
        self.assertTrue(callable(nav_sync._sync_communaute))
