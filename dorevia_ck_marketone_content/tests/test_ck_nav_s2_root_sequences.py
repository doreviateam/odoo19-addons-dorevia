# -*- coding: utf-8 -*-
"""S2 — ordre déterministe des racines (collision séquence vs personnalisation BO)."""

from odoo.tests import tagged
from odoo.tests.common import TransactionCase

from odoo.addons.dorevia_ck_marketone_content.nav_sync import (
    snapshot_ck_catalogue_navigation,
    sync_ck_catalogue_navigation_for_website,
)
from odoo.addons.dorevia_ck_marketone_content.nav_v22_config import (
    NAV_CATALOGUE_BOUTIQUE_LABEL,
    NAV_CATALOGUE_FIRST_CATEGORY_SEQUENCE,
    NAV_CATALOGUE_PRODUCTEURS_LABEL,
    NAV_CATALOGUE_PRODUCTEURS_SEQUENCE,
    NAV_CATALOGUE_PROFESSIONNELS_LABEL,
    NAV_CATALOGUE_PROFESSIONNELS_SEQUENCE,
    NAV_CATALOGUE_PROFESSIONNELS_URL,
)


@tagged('post_install', '-at_install', 'dorevia_ck_nav_s2')
class TestCkNavS2RootSequences(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.website = cls.env['website'].search([], limit=1)
        cls.Menu = cls.env['website.menu'].sudo()
        cls.root = cls.website.menu_id
        Category = cls.env['product.public.category'].sudo()
        Product = cls.env['product.template'].sudo()

        cls.epicerie = Category.search([
            ('name', '=', 'Épicerie'),
            ('parent_id', '=', False),
        ], limit=1)
        if not cls.epicerie:
            cls.epicerie = Category.create({'name': 'Épicerie', 'sequence': 100})
        if cls.epicerie.ck_exposure_status != 'active':
            cls.epicerie.write({'ck_exposure_status': 'active'})

        cls.sucree = Category.search([
            ('name', '=', 'Épicerie sucrée'),
            ('parent_id', '=', cls.epicerie.id),
        ], limit=1)
        if not cls.sucree:
            cls.sucree = Category.create({
                'name': 'Épicerie sucrée',
                'parent_id': cls.epicerie.id,
                'sequence': 10,
            })
        cls.salee = Category.search([
            ('name', '=', 'Épicerie salée'),
            ('parent_id', '=', cls.epicerie.id),
        ], limit=1)
        if not cls.salee:
            cls.salee = Category.create({
                'name': 'Épicerie salée',
                'parent_id': cls.epicerie.id,
                'sequence': 20,
            })
        # Placer Épicerie en tête des racines exposables (créneau canonique 20).
        cls.epicerie.write({'sequence': 1})
        for cat in (cls.epicerie, cls.sucree, cls.salee):
            if cat.ck_exposure_status != 'active':
                cat.write({'ck_exposure_status': 'active'})
            while cat._ck_exposable_products_count() < 3:
                Product.create({
                    'name': f'Test S2 seq {cat.name} {cat._ck_exposable_products_count()}',
                    'sale_ok': True,
                    'is_published': True,
                    'website_published': True,
                    'public_categ_ids': [(4, cat.id)],
                })

    def _root_menu(self, name):
        return self.Menu.search([
            ('website_id', '=', self.website.id),
            ('parent_id', '=', self.root.id),
            ('name', '=', name),
        ], limit=1)

    def _ensure_pro_page(self, published=True):
        page = self.env['website.page'].sudo().search([
            ('url', '=', NAV_CATALOGUE_PROFESSIONNELS_URL),
        ], limit=1)
        if page:
            page.write({'is_published': published})
            return page
        if not published:
            return page
        view = self.env['ir.ui.view'].sudo().create({
            'name': 'Test Page S2 Seq Pro',
            'type': 'qweb',
            'key': 'test.ck_nav_s2_seq_pro',
            'arch': '<t t-name="test.ck_nav_s2_seq"><div>/professionnels</div></t>',
        })
        return self.env['website.page'].sudo().create({
            'name': 'Professionnels S2 Seq',
            'url': NAV_CATALOGUE_PROFESSIONNELS_URL,
            'is_published': True,
            'website_id': self.website.id,
            'view_id': view.id,
        })

    def _sync(self):
        sync_ck_catalogue_navigation_for_website(self.env, self.website)

    def _ordered_managed_names(self):
        names = []
        for menu in self.Menu.search([
            ('website_id', '=', self.website.id),
            ('parent_id', '=', self.root.id),
        ], order='sequence, id'):
            if menu.name in (
                NAV_CATALOGUE_BOUTIQUE_LABEL,
                self.epicerie.name,
                NAV_CATALOGUE_PRODUCTEURS_LABEL,
                NAV_CATALOGUE_PROFESSIONNELS_LABEL,
            ):
                names.append(menu.name)
        return names

    def test_s2_fresh_canonical_root_sequences(self):
        self._ensure_pro_page(published=True)
        self._sync()
        epicerie = self._root_menu(self.epicerie.name)
        producteurs = self._root_menu(NAV_CATALOGUE_PRODUCTEURS_LABEL)
        professionnels = self._root_menu(NAV_CATALOGUE_PROFESSIONNELS_LABEL)
        self.assertEqual(epicerie.sequence, NAV_CATALOGUE_FIRST_CATEGORY_SEQUENCE)
        self.assertEqual(producteurs.sequence, NAV_CATALOGUE_PRODUCTEURS_SEQUENCE)
        self.assertEqual(professionnels.sequence, NAV_CATALOGUE_PROFESSIONNELS_SEQUENCE)
        self.assertEqual(
            self._ordered_managed_names(),
            [
                NAV_CATALOGUE_BOUTIQUE_LABEL,
                self.epicerie.name,
                NAV_CATALOGUE_PRODUCTEURS_LABEL,
                NAV_CATALOGUE_PROFESSIONNELS_LABEL,
            ],
        )

    def test_s2_inherited_collision_epicerie_producteurs_20(self):
        """Dette héritée Épicerie=20 ∩ Producteurs=20 → normalisation canonique."""
        self._ensure_pro_page(published=True)
        self._sync()
        epicerie = self._root_menu(self.epicerie.name)
        producteurs = self._root_menu(NAV_CATALOGUE_PRODUCTEURS_LABEL)
        # Simule l'état QA refusé (collision + ordre dépendant des ids)
        epicerie.write({'sequence': 20})
        producteurs.write({'sequence': 20})
        self.assertEqual(epicerie.sequence, producteurs.sequence)

        self._sync()
        epicerie = self._root_menu(self.epicerie.name)
        producteurs = self._root_menu(NAV_CATALOGUE_PRODUCTEURS_LABEL)
        self.assertEqual(epicerie.sequence, NAV_CATALOGUE_FIRST_CATEGORY_SEQUENCE)
        self.assertEqual(producteurs.sequence, NAV_CATALOGUE_PRODUCTEURS_SEQUENCE)
        self.assertNotEqual(epicerie.sequence, producteurs.sequence)
        self.assertEqual(
            self._ordered_managed_names(),
            [
                NAV_CATALOGUE_BOUTIQUE_LABEL,
                self.epicerie.name,
                NAV_CATALOGUE_PRODUCTEURS_LABEL,
                NAV_CATALOGUE_PROFESSIONNELS_LABEL,
            ],
        )

        before = snapshot_ck_catalogue_navigation(self.env, self.website)
        self._sync()
        after = snapshot_ck_catalogue_navigation(self.env, self.website)
        self.assertEqual(after, before, 'Idempotence après réparation de collision')

    def test_s2_bo_category_sequence_preserved_outside_reserved(self):
        """BO catégorie hors {10,60,70} préservée ; racines fixes toujours 60/70."""
        self._ensure_pro_page(published=True)
        self._sync()
        epicerie = self._root_menu(self.epicerie.name)
        epicerie.write({'sequence': 22})
        # Tentative BO sur racines fixes — annulée (créneaux réservés).
        self._root_menu(NAV_CATALOGUE_PRODUCTEURS_LABEL).write({'sequence': 55})
        self._root_menu(NAV_CATALOGUE_PROFESSIONNELS_LABEL).write({'sequence': 85})
        self._sync()
        self.assertEqual(self._root_menu(self.epicerie.name).sequence, 22)
        self.assertEqual(
            self._root_menu(NAV_CATALOGUE_PRODUCTEURS_LABEL).sequence,
            NAV_CATALOGUE_PRODUCTEURS_SEQUENCE,
        )
        self.assertEqual(
            self._root_menu(NAV_CATALOGUE_PROFESSIONNELS_LABEL).sequence,
            NAV_CATALOGUE_PROFESSIONNELS_SEQUENCE,
        )
        self.assertEqual(
            self._ordered_managed_names(),
            [
                NAV_CATALOGUE_BOUTIQUE_LABEL,
                self.epicerie.name,
                NAV_CATALOGUE_PRODUCTEURS_LABEL,
                NAV_CATALOGUE_PROFESSIONNELS_LABEL,
            ],
        )

    def test_s2_cascade_collision_resolved_in_one_pass(self):
        """NO GO Garant 6afb44d : Producteurs=20 ∩ Épicerie=20 + rayon BO=60.

        Un seul sync doit :
        - lever la collision 20 ;
        - imposer Producteurs=60 ;
        - déplacer le rayon BO hors du créneau réservé 60 ;
        - être idempotent au 2ᵉ sync.
        """
        self._ensure_pro_page(published=True)
        Category = self.env['product.public.category'].sudo()
        Product = self.env['product.template'].sudo()
        rayon = Category.create({
            'name': 'Rayon BO S2 Seq',
            'sequence': 500,
            'ck_exposure_status': 'active',
        })
        for idx in range(3):
            Product.create({
                'name': f'Test S2 rayon BO {idx}',
                'sale_ok': True,
                'is_published': True,
                'website_published': True,
                'public_categ_ids': [(4, rayon.id)],
            })
        self._sync()
        epicerie = self._root_menu(self.epicerie.name)
        producteurs = self._root_menu(NAV_CATALOGUE_PRODUCTEURS_LABEL)
        rayon_menu = self._root_menu(rayon.name)
        self.assertTrue(rayon_menu)

        # État Garant : collision 20 + personnalisation BO unique à 60
        epicerie.write({'sequence': 20})
        producteurs.write({'sequence': 20})
        rayon_menu.write({'sequence': 60})

        self._sync()
        epicerie = self._root_menu(self.epicerie.name)
        producteurs = self._root_menu(NAV_CATALOGUE_PRODUCTEURS_LABEL)
        rayon_menu = self._root_menu(rayon.name)
        self.assertEqual(epicerie.sequence, NAV_CATALOGUE_FIRST_CATEGORY_SEQUENCE)
        self.assertEqual(producteurs.sequence, NAV_CATALOGUE_PRODUCTEURS_SEQUENCE)
        self.assertNotEqual(rayon_menu.sequence, NAV_CATALOGUE_PRODUCTEURS_SEQUENCE)
        self.assertNotEqual(rayon_menu.sequence, epicerie.sequence)
        sequences = {
            epicerie.sequence,
            producteurs.sequence,
            rayon_menu.sequence,
            self._root_menu(NAV_CATALOGUE_PROFESSIONNELS_LABEL).sequence,
        }
        self.assertEqual(len(sequences), 4, 'Aucune collision résiduelle après 1 sync')

        before = snapshot_ck_catalogue_navigation(self.env, self.website)
        self._sync()
        after = snapshot_ck_catalogue_navigation(self.env, self.website)
        self.assertEqual(after, before, 'Idempotence dès le premier sync convergent')

    def test_s2_professionnels_absent_and_reappear_deterministic(self):
        self._ensure_pro_page(published=False)
        self._sync()
        self.assertFalse(self._root_menu(NAV_CATALOGUE_PROFESSIONNELS_LABEL))
        self.assertEqual(
            self._ordered_managed_names(),
            [
                NAV_CATALOGUE_BOUTIQUE_LABEL,
                self.epicerie.name,
                NAV_CATALOGUE_PRODUCTEURS_LABEL,
            ],
        )
        self.assertEqual(
            self._root_menu(NAV_CATALOGUE_PRODUCTEURS_LABEL).sequence,
            NAV_CATALOGUE_PRODUCTEURS_SEQUENCE,
        )

        self._ensure_pro_page(published=True)
        self._sync()
        pro = self._root_menu(NAV_CATALOGUE_PROFESSIONNELS_LABEL)
        self.assertTrue(pro)
        self.assertEqual(pro.sequence, NAV_CATALOGUE_PROFESSIONNELS_SEQUENCE)
        self.assertEqual(
            self._ordered_managed_names(),
            [
                NAV_CATALOGUE_BOUTIQUE_LABEL,
                self.epicerie.name,
                NAV_CATALOGUE_PRODUCTEURS_LABEL,
                NAV_CATALOGUE_PROFESSIONNELS_LABEL,
            ],
        )

    def test_s2_root_order_stable_without_orm_id_tiebreak(self):
        """Même avec Producteurs.id < Épicerie.id, l'ordre suit les séquences."""
        self._ensure_pro_page(published=True)
        self._sync()
        epicerie = self._root_menu(self.epicerie.name)
        producteurs = self._root_menu(NAV_CATALOGUE_PRODUCTEURS_LABEL)
        # Force collision puis sync : l'ordre ne doit plus dépendre de id
        if producteurs.id < epicerie.id:
            pass  # cas QA typique
        epicerie.write({'sequence': 20})
        producteurs.write({'sequence': 20})
        self._sync()
        ordered = self.Menu.search([
            ('website_id', '=', self.website.id),
            ('parent_id', '=', self.root.id),
            ('name', 'in', [self.epicerie.name, NAV_CATALOGUE_PRODUCTEURS_LABEL]),
        ], order='sequence, id')
        self.assertEqual(
            ordered.mapped('name'),
            [self.epicerie.name, NAV_CATALOGUE_PRODUCTEURS_LABEL],
        )
        self.assertLess(ordered[0].sequence, ordered[1].sequence)
