# -*- coding: utf-8 -*-
"""S6-B2bis — purge chirurgicale de la racine technique Blog → /blog."""

from odoo.tests import tagged
from odoo.tests.common import TransactionCase

from odoo.addons.dorevia_ck_marketone_content.nav_sync import (
    snapshot_ck_catalogue_navigation,
    sync_ck_catalogue_navigation_for_website,
)
from odoo.addons.dorevia_ck_marketone_content.nav_v22_config import (
    LEGACY_NAV_COUPS_LABEL,
    NAV_BLOG_DEFAULT_LABEL,
    NAV_CATALOGUE_COMMUNAUTE_SEQUENCE,
    NAV_CATALOGUE_PROFESSIONNELS_URL,
    NAV_COMMUNAUTE_LABEL,
    NAV_COMMUNAUTE_MAGAZINE_LABEL,
    NAV_COMMUNAUTE_RECETTES_LABEL,
    NAV_COMMUNAUTE_URL,
)


@tagged('post_install', '-at_install', 'dorevia_ck_nav_s6b2bis')
class TestCkNavS6B2bisPurgeBlogRoot(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.website = cls.env['website'].search([], limit=1)
        cls.Menu = cls.env['website.menu'].sudo()
        cls.root = cls.website.menu_id
        Category = cls.env['product.public.category'].sudo()
        Product = cls.env['product.template'].sudo()

        cls.epicerie = Category.create({
            'name': 'Épicerie S6B2bis',
            'sequence': 901,
            'ck_exposure_status': 'active',
        })
        cls.child_a = Category.create({
            'name': 'Rayon A S6B2bis',
            'parent_id': cls.epicerie.id,
            'sequence': 10,
            'ck_exposure_status': 'active',
        })
        cls.child_b = Category.create({
            'name': 'Rayon B S6B2bis',
            'parent_id': cls.epicerie.id,
            'sequence': 20,
            'ck_exposure_status': 'active',
        })
        for cat in (cls.epicerie, cls.child_a, cls.child_b):
            for idx in range(3):
                Product.create({
                    'name': f'Test S6B2bis {cat.name} {idx}',
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
                'name': 'Test Page S6B2bis Pro',
                'type': 'qweb',
                'key': 'test.ck_nav_s6b2bis_pro',
                'arch': '<t t-name="test.ck_nav_s6b2bis"><div>/professionnels</div></t>',
            })
            cls.env['website.page'].sudo().create({
                'name': 'Professionnels S6B2bis',
                'url': NAV_CATALOGUE_PROFESSIONNELS_URL,
                'is_published': True,
                'website_id': cls.website.id,
                'view_id': view.id,
            })

        # Parent hors arbre CK : Default Main Menu (website_id False) si présent,
        # sinon racine website.menu sans website / autre parent.
        cls.default_main = cls.Menu.search([
            ('name', '=', 'Default Main Menu'),
            ('website_id', '=', False),
        ], limit=1)
        if not cls.default_main:
            cls.default_main = cls.Menu.search([
                ('website_id', '=', False),
                ('parent_id', '=', False),
            ], limit=1)
        if not cls.default_main:
            cls.default_main = cls.Menu.create({
                'name': 'Default Main Menu',
                'url': '/',
                'website_id': False,
                'sequence': 0,
            })

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

    def _create_ck_blog_root(self, url='/blog', **extra):
        vals = {
            'name': NAV_BLOG_DEFAULT_LABEL,
            'url': url,
            'website_id': self.website.id,
            'parent_id': self.root.id,
            'sequence': 98,
        }
        vals.update(extra)
        return self.Menu.create(vals)

    # 1 — racine CK Blog + /blog → supprimée
    def test_01_ck_blog_root_slash_blog_purged(self):
        blog = self._create_ck_blog_root(url='/blog')
        blog_id = blog.id
        self._sync()
        self.assertFalse(self.Menu.browse(blog_id).exists())
        self.assertFalse(self._root_menu(NAV_BLOG_DEFAULT_LABEL))

    # 2 — variante /blog/ → supprimée (normalisation)
    def test_02_ck_blog_root_slash_blog_trailing_slash_purged(self):
        blog = self._create_ck_blog_root(url='/blog/')
        blog_id = blog.id
        self._sync()
        self.assertFalse(self.Menu.browse(blog_id).exists())

    # 3 — Blog hors arbre CK → intact
    def test_03_blog_outside_ck_tree_intact(self):
        outside = self.Menu.create({
            'name': NAV_BLOG_DEFAULT_LABEL,
            'url': '/blog',
            'website_id': False,
            'parent_id': self.default_main.id,
            'sequence': 50,
        })
        outside_id = outside.id
        self._sync()
        self.assertTrue(self.Menu.browse(outside_id).exists())
        self.assertEqual(outside.name, NAV_BLOG_DEFAULT_LABEL)
        self.assertEqual((outside.url or '').rstrip('/'), '/blog')
        self.assertEqual(outside.parent_id.id, self.default_main.id)
        self.assertFalse(outside.website_id)

    # 4 — Blog racine autre URL → préservé
    def test_04_blog_root_other_url_preserved(self):
        blog = self._create_ck_blog_root(url='/actualites')
        blog_id = blog.id
        self._sync()
        self.assertTrue(self.Menu.browse(blog_id).exists())
        kept = self.Menu.browse(blog_id)
        self.assertEqual(kept.name, NAV_BLOG_DEFAULT_LABEL)
        self.assertEqual(kept.url, '/actualites')

    # 5 — Magazine et Recettes enfants Communauté → préservés
    def test_05_magazine_recettes_children_preserved(self):
        self._create_ck_blog_root(url='/blog')
        self._sync()
        communaute = self._root_menu(NAV_COMMUNAUTE_LABEL)
        self.assertTrue(communaute)
        self.assertTrue(self._child_menu(communaute, NAV_COMMUNAUTE_MAGAZINE_LABEL))
        self.assertTrue(self._child_menu(communaute, NAV_COMMUNAUTE_RECETTES_LABEL))
        self.assertFalse(self._root_menu(NAV_BLOG_DEFAULT_LABEL))

    # 6 — Communauté seq 55, url #
    def test_06_communaute_seq_55_url_hash(self):
        self._create_ck_blog_root(url='/blog')
        self._sync()
        menu = self._root_menu(NAV_COMMUNAUTE_LABEL)
        self.assertTrue(menu)
        self.assertEqual(menu.sequence, NAV_CATALOGUE_COMMUNAUTE_SEQUENCE)
        self.assertEqual(menu.sequence, 55)
        self.assertEqual(menu.url, NAV_COMMUNAUTE_URL)
        self.assertEqual(menu.url, '#')

    # 7 — pas de doublon / réapparition après deux bootstraps
    def test_07_no_reappear_after_two_bootstraps(self):
        blog = self._create_ck_blog_root(url='/blog')
        blog_id = blog.id
        self._sync()
        self.assertFalse(self.Menu.browse(blog_id).exists())
        snap1 = snapshot_ck_catalogue_navigation(self.env, self.website)
        self._sync()
        snap2 = snapshot_ck_catalogue_navigation(self.env, self.website)
        self.assertEqual(snap1, snap2)
        self.assertFalse(self._root_menu(NAV_BLOG_DEFAULT_LABEL))
        self.assertEqual(
            self.Menu.search_count([
                ('website_id', '=', self.website.id),
                ('parent_id', '=', self.root.id),
                ('name', '=', NAV_COMMUNAUTE_LABEL),
            ]),
            1,
        )

    # 8 — Coups de cœur toujours absent
    def test_08_coups_de_coeur_still_purged(self):
        self.Menu.create({
            'name': LEGACY_NAV_COUPS_LABEL,
            'url': '#',
            'website_id': self.website.id,
            'parent_id': self.root.id,
            'sequence': 999,
        })
        self._create_ck_blog_root(url='/blog')
        self._sync()
        self.assertFalse(self._root_menu(LEGACY_NAV_COUPS_LABEL))
        self.assertFalse(self._root_menu(NAV_BLOG_DEFAULT_LABEL))
        self.assertTrue(self._root_menu(NAV_COMMUNAUTE_LABEL))

    # 9 — Blog racine avec marqueur CK → préservé
    def test_09_blog_root_with_ck_marker_preserved(self):
        with_css = self._create_ck_blog_root(
            url='/blog',
            ck_nav_css_class='ck-nav-editorial-blog',
        )
        with_css_id = with_css.id

        marker_cat = self.env['product.public.category'].sudo().create({
            'name': 'Marqueur Blog S6B2bis',
            'sequence': 902,
            'ck_exposure_status': 'active',
        })
        for idx in range(3):
            self.env['product.template'].sudo().create({
                'name': f'Test S6B2bis marker {idx}',
                'sale_ok': True,
                'is_published': True,
                'website_published': True,
                'public_categ_ids': [(4, marker_cat.id)],
            })
        with_categ = self._create_ck_blog_root(
            url='/blog',
            sequence=97,
            ck_nav_category_id=marker_cat.id,
        )
        with_categ_id = with_categ.id
        self._sync()
        self.assertTrue(
            self.Menu.browse(with_css_id).exists(),
            'Blog /blog avec ck-nav-* doit être préservé',
        )
        self.assertTrue(
            self.Menu.browse(with_categ_id).exists(),
            'Blog /blog avec ck_nav_category_id éligible doit être préservé',
        )

    # 10 — comptes exposables enfants Épicerie inchangés
    def test_10_epicerie_exposable_child_counts_unchanged(self):
        self._create_ck_blog_root(url='/blog')
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
