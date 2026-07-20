# -*- coding: utf-8 -*-
"""S6-B2 — enfants Magazine / Recettes sous Communauté (child_menus + env.ref)."""

from odoo.tests import tagged
from odoo.tests.common import TransactionCase

from odoo.addons.dorevia_ck_marketone_content.nav_sync import (
    _communaute_child_menus,
    _resolve_blog_website_url,
    snapshot_ck_catalogue_navigation,
    sync_ck_catalogue_navigation_for_website,
)
from odoo.addons.dorevia_ck_marketone_content.nav_v22_config import (
    LEGACY_NAV_COUPS_LABEL,
    NAV_CATALOGUE_BOUTIQUE_LABEL,
    NAV_CATALOGUE_FIRST_CATEGORY_SEQUENCE,
    NAV_CATALOGUE_PRODUCTEURS_LABEL,
    NAV_CATALOGUE_PRODUCTEURS_SEQUENCE,
    NAV_CATALOGUE_PROFESSIONNELS_LABEL,
    NAV_CATALOGUE_PROFESSIONNELS_SEQUENCE,
    NAV_CATALOGUE_PROFESSIONNELS_URL,
    NAV_COMMUNAUTE_LABEL,
    NAV_COMMUNAUTE_MAGAZINE_LABEL,
    NAV_COMMUNAUTE_MAGAZINE_SEQUENCE,
    NAV_COMMUNAUTE_RECETTES_LABEL,
    NAV_COMMUNAUTE_RECETTES_SEQUENCE,
    NAV_COMMUNAUTE_URL,
    XMLID_CK_BLOG_MAGAZINE,
    XMLID_CK_BLOG_RECETTES,
)


@tagged('post_install', '-at_install', 'dorevia_ck_nav_s6b2')
class TestCkNavS6B2CommunauteBlogChildren(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.website = cls.env['website'].search([], limit=1)
        cls.Menu = cls.env['website.menu'].sudo()
        cls.root = cls.website.menu_id
        Category = cls.env['product.public.category'].sudo()
        Product = cls.env['product.template'].sudo()

        cls.epicerie = Category.create({
            'name': 'Épicerie S6B2',
            'sequence': 900,
            'ck_exposure_status': 'active',
        })
        cls.child_a = Category.create({
            'name': 'Rayon A S6B2',
            'parent_id': cls.epicerie.id,
            'sequence': 10,
            'ck_exposure_status': 'active',
        })
        cls.child_b = Category.create({
            'name': 'Rayon B S6B2',
            'parent_id': cls.epicerie.id,
            'sequence': 20,
            'ck_exposure_status': 'active',
        })
        for cat in (cls.epicerie, cls.child_a, cls.child_b):
            for idx in range(3):
                Product.create({
                    'name': f'Test S6B2 {cat.name} {idx}',
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
                'name': 'Test Page S6B2 Pro',
                'type': 'qweb',
                'key': 'test.ck_nav_s6b2_pro',
                'arch': '<t t-name="test.ck_nav_s6b2"><div>/professionnels</div></t>',
            })
            cls.env['website.page'].sudo().create({
                'name': 'Professionnels S6B2',
                'url': NAV_CATALOGUE_PROFESSIONNELS_URL,
                'is_published': True,
                'website_id': cls.website.id,
                'view_id': view.id,
            })

        cls.blog_magazine = cls.env.ref(XMLID_CK_BLOG_MAGAZINE)
        cls.blog_recettes = cls.env.ref(XMLID_CK_BLOG_RECETTES)

    def _root_menu(self, name):
        return self.Menu.search([
            ('website_id', '=', self.website.id),
            ('parent_id', '=', self.root.id),
            ('name', '=', name),
        ], limit=1)

    def _child_menu(self, parent, name):
        return self.Menu.search([
            ('website_id', '=', self.website.id),
            ('parent_id', '=', parent.id),
            ('name', '=', name),
        ], limit=1)

    def _sync(self):
        sync_ck_catalogue_navigation_for_website(self.env, self.website)

    def test_s6b2_blogs_xmlids_exist(self):
        self.assertEqual(self.blog_magazine.name, NAV_COMMUNAUTE_MAGAZINE_LABEL)
        self.assertEqual(self.blog_recettes.name, NAV_COMMUNAUTE_RECETTES_LABEL)
        self.assertFalse(self.env['blog.post'].sudo().search_count([
            ('blog_id', 'in', (self.blog_magazine.id, self.blog_recettes.id)),
        ]))

    def test_s6b2_magazine_recettes_children_created(self):
        self._sync()
        communaute = self._root_menu(NAV_COMMUNAUTE_LABEL)
        self.assertTrue(communaute)
        magazine = self._child_menu(communaute, NAV_COMMUNAUTE_MAGAZINE_LABEL)
        recettes = self._child_menu(communaute, NAV_COMMUNAUTE_RECETTES_LABEL)
        self.assertTrue(magazine)
        self.assertTrue(recettes)
        self.assertEqual(magazine.sequence, NAV_COMMUNAUTE_MAGAZINE_SEQUENCE)
        self.assertEqual(recettes.sequence, NAV_COMMUNAUTE_RECETTES_SEQUENCE)
        self.assertEqual(
            self.Menu.search_count([
                ('website_id', '=', self.website.id),
                ('parent_id', '=', communaute.id),
            ]),
            2,
        )

    def test_s6b2_survive_two_bootstraps_no_duplicate(self):
        """S6-B2-BLOC-1 : enfants gérés survivent à deux bootstraps sans doublon."""
        self._sync()
        communaute = self._root_menu(NAV_COMMUNAUTE_LABEL)
        mag_id = self._child_menu(communaute, NAV_COMMUNAUTE_MAGAZINE_LABEL).id
        rec_id = self._child_menu(communaute, NAV_COMMUNAUTE_RECETTES_LABEL).id
        before = snapshot_ck_catalogue_navigation(self.env, self.website)
        self._sync()
        after = snapshot_ck_catalogue_navigation(self.env, self.website)
        self.assertEqual(after, before)
        communaute = self._root_menu(NAV_COMMUNAUTE_LABEL)
        self.assertEqual(
            self.Menu.search_count([
                ('website_id', '=', self.website.id),
                ('parent_id', '=', self.root.id),
                ('name', '=', NAV_COMMUNAUTE_LABEL),
            ]),
            1,
        )
        self.assertEqual(
            self.Menu.search_count([
                ('website_id', '=', self.website.id),
                ('parent_id', '=', communaute.id),
                ('name', '=', NAV_COMMUNAUTE_MAGAZINE_LABEL),
            ]),
            1,
        )
        self.assertEqual(
            self.Menu.search_count([
                ('website_id', '=', self.website.id),
                ('parent_id', '=', communaute.id),
                ('name', '=', NAV_COMMUNAUTE_RECETTES_LABEL),
            ]),
            1,
        )
        self.assertEqual(self._child_menu(communaute, NAV_COMMUNAUTE_MAGAZINE_LABEL).id, mag_id)
        self.assertEqual(self._child_menu(communaute, NAV_COMMUNAUTE_RECETTES_LABEL).id, rec_id)

    def test_s6b2_urls_from_env_ref_not_hardcoded(self):
        expected_mag = _resolve_blog_website_url(self.env, XMLID_CK_BLOG_MAGAZINE)
        expected_rec = _resolve_blog_website_url(self.env, XMLID_CK_BLOG_RECETTES)
        self.assertTrue(expected_mag.startswith('/blog/'))
        self.assertTrue(expected_rec.startswith('/blog/'))
        self.assertIn(str(self.blog_magazine.id), expected_mag)
        self.assertIn(str(self.blog_recettes.id), expected_rec)
        # Pas d'ID inventé / figure en dur hors enregistrement résolu
        specs = {s['name']: s for s in _communaute_child_menus(self.env)}
        self.assertEqual(specs[NAV_COMMUNAUTE_MAGAZINE_LABEL]['url'], expected_mag)
        self.assertEqual(specs[NAV_COMMUNAUTE_RECETTES_LABEL]['url'], expected_rec)

        self._sync()
        communaute = self._root_menu(NAV_COMMUNAUTE_LABEL)
        self.assertEqual(
            self._child_menu(communaute, NAV_COMMUNAUTE_MAGAZINE_LABEL).url,
            expected_mag,
        )
        self.assertEqual(
            self._child_menu(communaute, NAV_COMMUNAUTE_RECETTES_LABEL).url,
            expected_rec,
        )

    def test_s6b2_unmanaged_child_purged(self):
        self._sync()
        communaute = self._root_menu(NAV_COMMUNAUTE_LABEL)
        unmanaged = self.Menu.create({
            'name': 'Orphelin S6B2',
            'url': '/blog/orphan',
            'website_id': self.website.id,
            'parent_id': communaute.id,
            'sequence': 99,
        })
        unmanaged_id = unmanaged.id
        self._sync()
        self.assertFalse(self.Menu.browse(unmanaged_id).exists())
        self.assertTrue(self._child_menu(communaute, NAV_COMMUNAUTE_MAGAZINE_LABEL))
        self.assertTrue(self._child_menu(communaute, NAV_COMMUNAUTE_RECETTES_LABEL))

    def test_s6b2_communaute_seq_55_url_hash(self):
        self._sync()
        menu = self._root_menu(NAV_COMMUNAUTE_LABEL)
        self.assertEqual(menu.sequence, 55)
        self.assertEqual(menu.url, NAV_COMMUNAUTE_URL)
        self.assertEqual(menu.url, '#')

    def test_s6b2_global_order_unchanged(self):
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

    def test_s6b2_coups_de_coeur_still_purged(self):
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

    def test_s6b2_epicerie_category_child_counts_unchanged(self):
        self._sync()
        epicerie_menu = self._root_menu(self.epicerie.name)
        self.assertTrue(epicerie_menu)
        before_names = sorted(epicerie_menu.child_id.mapped('name'))
        before_count = len(epicerie_menu.child_id)
        self._sync()
        epicerie_menu = self._root_menu(self.epicerie.name)
        self.assertEqual(len(epicerie_menu.child_id), before_count)
        self.assertEqual(sorted(epicerie_menu.child_id.mapped('name')), before_names)
        self.assertEqual(before_count, 2)

    def test_s6b2_idempotence_complete(self):
        self._sync()
        snap1 = snapshot_ck_catalogue_navigation(self.env, self.website)
        self._sync()
        snap2 = snapshot_ck_catalogue_navigation(self.env, self.website)
        self._sync()
        snap3 = snapshot_ck_catalogue_navigation(self.env, self.website)
        self.assertEqual(snap1, snap2)
        self.assertEqual(snap2, snap3)
