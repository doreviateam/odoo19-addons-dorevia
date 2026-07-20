# -*- coding: utf-8 -*-
"""CK-NAV-003 — Navigation catalogue dynamique depuis product.public.category."""

from odoo.tests import tagged
from odoo.tests.common import TransactionCase

from odoo.addons.dorevia_ck_marketone_content.nav_sync import (
    bootstrap_ck_catalogue_navigation,
    snapshot_ck_catalogue_navigation,
    sync_ck_catalogue_navigation_for_website,
)
from odoo.addons.dorevia_ck_marketone_content.nav_sync import (
    NAV_CSS_DESKTOP_UNIVERSE_CHILD,
    NAV_CSS_MOBILE_UNIVERS_GROUP,
    NAV_CSS_MOBILE_UNIVERSE_CHILD,
)
from odoo.addons.dorevia_ck_marketone_content.nav_v22_config import (
    NAV_CATALOGUE_BOUTIQUE_LABEL,
    NAV_CATALOGUE_BOUTIQUE_SEQUENCE,
    NAV_CATALOGUE_BOUTIQUE_URL,
    NAV_CATALOGUE_PRODUCTEURS_LABEL,
    NAV_CATALOGUE_PRODUCTEURS_URL,
    NAV_CATALOGUE_PROFESSIONNELS_URL,
    NAV_CSS_ESPACE_PRO,
    NAV_CSS_MEGA_PRODUCT,
    NAV_CSS_N3_GROUP_END,
    NAV_CSS_N3_RAYON,
    NAV_CSS_N3_RELATION,
    NAV_CSS_N3_SELECTION,
    NAV_CSS_PRODUCTEURS,
    NAV_CSS_SHOP_ROOT,
)

# Classes menu canoniques S2 (icône Accueil) — autorisées sur website.menu.
_CK_NAV_CSS_CANONICAL = frozenset({NAV_CSS_SHOP_ROOT})

# Marqueurs V1 / V2.2 / mega / groupes mobiles — interdits après sync V3.
_CK_NAV_CSS_LEGACY_FORBIDDEN = frozenset({
    NAV_CSS_N3_RAYON,
    NAV_CSS_N3_SELECTION,
    NAV_CSS_N3_RELATION,
    NAV_CSS_N3_GROUP_END,
    NAV_CSS_PRODUCTEURS,
    NAV_CSS_ESPACE_PRO,
    NAV_CSS_MEGA_PRODUCT,
    NAV_CSS_DESKTOP_UNIVERSE_CHILD,
    NAV_CSS_MOBILE_UNIVERS_GROUP,
    NAV_CSS_MOBILE_UNIVERSE_CHILD,
    'ck-nav-desktop-universe',
})


@tagged('post_install', '-at_install', 'dorevia_ck_nav_catalogue')
class TestCkNavCatalogueSync(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.website = cls.env['website'].search([], limit=1)
        cls.Menu = cls.env['website.menu'].sudo()
        cls.root = cls.website.menu_id

        Category = cls.env['product.public.category'].sudo()

        # Catégorie racine A — avec produit publié + deux sous-catégories
        cls.cat_a = Category.create({'name': 'TestCat NAV003 Rayon A', 'sequence': 900})
        cls.cat_a_child1 = Category.create({
            'name': 'TestCat NAV003 Child A1',
            'parent_id': cls.cat_a.id,
            'sequence': 10,
        })
        cls.cat_a_child2 = Category.create({
            'name': 'TestCat NAV003 Child A2',
            'parent_id': cls.cat_a.id,
            'sequence': 20,
        })

        # Catégorie racine B — avec produit publié, pas de sous-catégories
        cls.cat_b = Category.create({'name': 'TestCat NAV003 Rayon B', 'sequence': 910})

        # Catégorie racine vide — sans produit publié
        cls.cat_vide = Category.create({'name': 'TestCat NAV003 Vide', 'sequence': 920})

        # Sous-catégorie de niveau 3 — ne doit pas apparaître dans le header
        cls.cat_l3 = Category.create({
            'name': 'TestCat NAV003 Level 3',
            'parent_id': cls.cat_a_child1.id,
            'sequence': 10,
        })

        Product = cls.env['product.template'].sudo()

        # Produit dans cat_a et cat_a_child1
        cls.prod_a = Product.create({
            'name': 'Test Produit NAV003 A',
            'sale_ok': True,
            'is_published': True,
            'website_published': True,
            'public_categ_ids': [(4, cls.cat_a.id), (4, cls.cat_a_child1.id)],
        })

        # Produit dans cat_a_child2
        cls.prod_a2 = Product.create({
            'name': 'Test Produit NAV003 A2',
            'sale_ok': True,
            'is_published': True,
            'website_published': True,
            'public_categ_ids': [(4, cls.cat_a_child2.id)],
        })

        # Produit dans cat_b (pas de sous-catégorie)
        cls.prod_b = Product.create({
            'name': 'Test Produit NAV003 B',
            'sale_ok': True,
            'is_published': True,
            'website_published': True,
            'public_categ_ids': [(4, cls.cat_b.id)],
        })

        # CATALOG-ARCHI-001 Lot A : seuil d'exposition = 3 produits qualifiés
        # (CK_CATEGORY_ACTIVE_MIN_PRODUCTS), évalué via _is_ck_exposable() sur
        # CHAQUE catégorie individuellement (racine ET sous-catégories, cf.
        # _get_ck_nav_child_categories). Les extras doivent donc être ajoutés
        # sur cat_a_child1/child2 (pas seulement sur cat_a) pour que les deux
        # sous-catégories restent éligibles dans les tests structurels
        # ci-dessous (idempotence, séquences, etc.) qui ne portent pas sur le
        # seuil lui-même (couvert par test_ck_catalog_exposure.py). cat_b n'a
        # pas de sous-catégorie : ses extras vont directement dessus.
        for idx in range(2):
            Product.create({
                'name': f'Test Produit NAV003 A1 extra {idx}',
                'sale_ok': True,
                'is_published': True,
                'website_published': True,
                'public_categ_ids': [(4, cls.cat_a_child1.id)],
            })
            Product.create({
                'name': f'Test Produit NAV003 A2 extra {idx}',
                'sale_ok': True,
                'is_published': True,
                'website_published': True,
                'public_categ_ids': [(4, cls.cat_a_child2.id)],
            })
            Product.create({
                'name': f'Test Produit NAV003 B extra {idx}',
                'sale_ok': True,
                'is_published': True,
                'website_published': True,
                'public_categ_ids': [(4, cls.cat_b.id)],
            })

        # Produit dans cat_l3 uniquement (niveau 3)
        cls.prod_l3 = Product.create({
            'name': 'Test Produit NAV003 L3',
            'sale_ok': True,
            'is_published': True,
            'website_published': True,
            'public_categ_ids': [(4, cls.cat_l3.id)],
        })

    def _root_menu(self, name):
        return self.Menu.search([
            ('website_id', '=', self.website.id),
            ('parent_id', '=', self.root.id),
            ('name', '=', name),
        ], limit=1)

    def _sync(self):
        sync_ck_catalogue_navigation_for_website(self.env, self.website)

    def _ensure_page(self, url, published=True):
        page = self.env['website.page'].sudo().search([('url', '=', url)], limit=1)
        if page:
            page.write({'is_published': published})
        else:
            view = self.env['ir.ui.view'].sudo().create({
                'name': f'Test Page {url}',
                'type': 'qweb',
                'key': f'test.ck_nav003_{url.strip("/").replace("/", "_")}',
                'arch': f'<t t-name="test.ck_nav003"><div>{url}</div></t>',
            })
            self.env['website.page'].sudo().create({
                'name': f'Test {url}',
                'url': url,
                'is_published': published,
                'website_id': self.website.id,
                'view_id': view.id,
            })

    # --- Boutique fixe ---

    def test_catalogue_nav_boutique_fixed(self):
        self._sync()
        menu = self._root_menu(NAV_CATALOGUE_BOUTIQUE_LABEL)
        self.assertTrue(menu, 'Boutique doit exister')
        self.assertEqual(menu.url, NAV_CATALOGUE_BOUTIQUE_URL)
        self.assertEqual(menu.sequence, NAV_CATALOGUE_BOUTIQUE_SEQUENCE)
        self.assertFalse(menu.is_mega_menu)
        self.assertIn(
            'ck-nav-shop-root',
            (menu.ck_nav_css_class or '').split(),
            'Boutique doit porter ck-nav-shop-root (icône maison header/drawer)',
        )

    # --- Catégories racines éligibles ---

    def test_catalogue_nav_root_categories_present(self):
        self._sync()
        self.assertTrue(
            self._root_menu(self.cat_a.name),
            f'{self.cat_a.name} doit être en racine nav',
        )
        self.assertTrue(
            self._root_menu(self.cat_b.name),
            f'{self.cat_b.name} doit être en racine nav',
        )

    def test_catalogue_nav_empty_category_hidden(self):
        self._sync()
        self.assertFalse(
            self._root_menu(self.cat_vide.name),
            'Catégorie sans produit publié doit être absente',
        )

    # --- Sous-catégories (niveau 2) ---

    def test_catalogue_nav_child_categories(self):
        self._sync()
        parent = self._root_menu(self.cat_a.name)
        self.assertTrue(parent)

        child1 = self.Menu.search([
            ('parent_id', '=', parent.id),
            ('name', '=', self.cat_a_child1.name),
        ], limit=1)
        child2 = self.Menu.search([
            ('parent_id', '=', parent.id),
            ('name', '=', self.cat_a_child2.name),
        ], limit=1)
        self.assertTrue(child1, 'Sous-catégorie A1 doit être enfant du menu parent')
        self.assertTrue(child2, 'Sous-catégorie A2 doit être enfant du menu parent')

    def test_catalogue_nav_child_sequence_order(self):
        self._sync()
        parent = self._root_menu(self.cat_a.name)
        self.assertTrue(parent)
        child1 = self.Menu.search([('parent_id', '=', parent.id), ('name', '=', self.cat_a_child1.name)], limit=1)
        child2 = self.Menu.search([('parent_id', '=', parent.id), ('name', '=', self.cat_a_child2.name)], limit=1)
        self.assertTrue(child1 and child2)
        self.assertLess(child1.sequence, child2.sequence, 'A1 doit précéder A2 (sequence)')

    def test_catalogue_nav_no_children_for_simple_category(self):
        """Catégorie sans sous-catégorie éligible : lien simple, pas de dropdown."""
        self._sync()
        parent = self._root_menu(self.cat_b.name)
        self.assertTrue(parent)
        self.assertFalse(parent.child_id, f'{self.cat_b.name} ne doit pas avoir de sous-menus')

    # --- Profondeur maximale 2 ---

    def test_catalogue_nav_depth_limited_to_2(self):
        self._sync()
        # Le niveau 3 (cat_l3) ne doit pas apparaître dans website.menu
        l3_in_menu = self.Menu.search([
            ('website_id', '=', self.website.id),
            ('name', '=', self.cat_l3.name),
        ])
        self.assertFalse(l3_in_menu, 'Les catégories niveau 3 ne doivent pas être dans le header')

    # --- Méga-menu et CSS ---

    def test_catalogue_nav_no_megamenu(self):
        self._sync()
        root_menus = self.Menu.search([
            ('website_id', '=', self.website.id),
            ('parent_id', '=', self.root.id),
        ])
        mega = root_menus.filtered('is_mega_menu')
        self.assertFalse(mega, 'Aucun mega-menu en racine après catalogue sync')

    def test_catalogue_nav_no_legacy_css(self):
        """S2 : ck-nav-shop-root est canonique ; les marqueurs V1/V2.2 restent interdits."""
        self._sync()
        all_nav_menus = self.Menu.search([('website_id', '=', self.website.id)])
        boutique = self._root_menu(NAV_CATALOGUE_BOUTIQUE_LABEL)
        self.assertTrue(boutique)
        boutique_tokens = set((boutique.ck_nav_css_class or '').split())
        self.assertIn(
            NAV_CSS_SHOP_ROOT,
            boutique_tokens,
            'Boutique doit porter ck-nav-shop-root (icône Accueil)',
        )

        for menu in all_nav_menus:
            tokens = set((menu.ck_nav_css_class or '').split())
            forbidden = tokens & _CK_NAV_CSS_LEGACY_FORBIDDEN
            self.assertFalse(
                forbidden,
                f'Menu « {menu.name} » : marqueurs CSS legacy interdits {sorted(forbidden)}',
            )
            unexpected = {
                token for token in tokens
                if token.startswith('ck-nav-') and token not in _CK_NAV_CSS_CANONICAL
            }
            self.assertFalse(
                unexpected,
                f'Menu « {menu.name} » : classes ck-nav-* non canoniques {sorted(unexpected)}',
            )

    # --- Séquences ---

    def test_catalogue_nav_boutique_before_categories(self):
        self._sync()
        boutique = self._root_menu(NAV_CATALOGUE_BOUTIQUE_LABEL)
        cat_a = self._root_menu(self.cat_a.name)
        self.assertTrue(boutique and cat_a)
        self.assertLess(boutique.sequence, cat_a.sequence, 'Boutique doit précéder les catégories')

    def test_catalogue_nav_preserves_admin_sequence_on_resync(self):
        """CK-NAV-003b : une séquence modifiée en BO ne doit pas être écrasée au resync."""
        self._sync()
        cat_a_menu = self._root_menu(self.cat_a.name)
        self.assertTrue(cat_a_menu)

        cat_a_menu.write({'sequence': 12345})
        self._sync()

        cat_a_menu_reloaded = self._root_menu(self.cat_a.name)
        self.assertEqual(
            cat_a_menu_reloaded.sequence, 12345,
            'La séquence modifiée manuellement en BO doit survivre au resync',
        )
        # name/url restent pilotés par la catégorie source
        self.assertEqual(cat_a_menu_reloaded.name, self.cat_a.name)

    def test_catalogue_nav_producteurs_uses_reserved_sequence(self):
        """S2 : Producteurs occupe le créneau réservé 60 (pas de BO libre sur 60)."""
        from odoo.addons.dorevia_ck_marketone_content.nav_v22_config import (
            NAV_CATALOGUE_PRODUCTEURS_SEQUENCE,
        )
        self._sync()
        producteurs_menu = self._root_menu(NAV_CATALOGUE_PRODUCTEURS_LABEL)
        self.assertTrue(producteurs_menu)

        producteurs_menu.write({'sequence': 54321})
        self._sync()

        producteurs_menu_reloaded = self._root_menu(NAV_CATALOGUE_PRODUCTEURS_LABEL)
        self.assertEqual(
            producteurs_menu_reloaded.sequence,
            NAV_CATALOGUE_PRODUCTEURS_SEQUENCE,
            'Producteurs doit retrouver le créneau réservé 60 au resync',
        )

    def test_catalogue_nav_new_category_gets_default_sequence_without_disturbing_existing(self):
        """CK-NAV-003b : une nouvelle catégorie prend sa séquence par défaut sans perturber les autres."""
        self._sync()
        cat_a_menu = self._root_menu(self.cat_a.name)
        cat_a_menu.write({'sequence': 12345})

        Category = self.env['product.public.category'].sudo()
        cat_new = Category.create({'name': 'TestCat NAV003 Rayon Nouveau', 'sequence': 905})
        Product = self.env['product.template'].sudo()
        for idx in range(3):
            Product.create({
                'name': f'Test Produit NAV003 Nouveau {idx}',
                'sale_ok': True,
                'is_published': True,
                'website_published': True,
                'public_categ_ids': [(4, cat_new.id)],
            })

        self._sync()

        cat_a_menu_reloaded = self._root_menu(self.cat_a.name)
        self.assertEqual(
            cat_a_menu_reloaded.sequence, 12345,
            'La catégorie existante ne doit pas être perturbée par un nouvel item',
        )
        cat_new_menu = self._root_menu(cat_new.name)
        self.assertTrue(cat_new_menu, 'La nouvelle catégorie doit apparaître au menu')

    # --- Producteurs fixe (route contrôleur, pas de website.page) ---

    def test_catalogue_nav_producteurs_fixed(self):
        self._sync()
        menu = self._root_menu(NAV_CATALOGUE_PRODUCTEURS_LABEL)
        self.assertTrue(menu, 'Producteurs doit toujours être présent en nav catalogue')
        self.assertEqual(menu.url, NAV_CATALOGUE_PRODUCTEURS_URL)
        self.assertFalse(menu.is_mega_menu)
        self.assertFalse(
            menu.ck_nav_css_class and 'ck-nav-' in menu.ck_nav_css_class,
            'Producteurs sans CSS legacy',
        )

    # --- Professionnels conditionnel ---

    def test_catalogue_nav_professionnels_present_if_page_published(self):
        self._ensure_page(NAV_CATALOGUE_PROFESSIONNELS_URL, published=True)
        self._sync()
        self.assertTrue(
            self._root_menu('Professionnels'),
            'Professionnels doit être présent si /professionnels est publiée',
        )

    def test_catalogue_nav_professionnels_absent_if_page_unpublished(self):
        self._ensure_page(NAV_CATALOGUE_PROFESSIONNELS_URL, published=False)
        self._sync()
        self.assertFalse(
            self._root_menu('Professionnels'),
            'Professionnels doit être absent si /professionnels non publiée',
        )

    # --- Nettoyage V2.2 ---

    def test_catalogue_nav_removes_nav002_stale_items(self):
        # Injecter des libellés V2.2 qui ne sont PAS des catégories catalogue éligibles.
        # S6-B1 : Communauté n'est plus un stale — racine éditoriale V3.
        stale_names = ('Tous nos produits', 'Espace pro', 'Nos producteurs')
        stale_menu_ids = []
        for name in stale_names:
            stale_menu = self.Menu.create({
                'name': name,
                'url': '#',
                'website_id': self.website.id,
                'parent_id': self.root.id,
                'sequence': 999,
                'is_mega_menu': True,
                'ck_nav_css_class': 'ck-nav-test-stale',
            })
            stale_menu_ids.append(stale_menu.id)
        self._sync()
        self.assertFalse(
            self.Menu.browse(stale_menu_ids).exists(),
            'Les anciennes entrées V2.2 injectées doivent être supprimées',
        )
        for name in stale_names:
            self.assertFalse(self._root_menu(name), f'« {name} » V2.2 ne doit pas survivre')

    def test_catalogue_nav_keeps_communaute_as_v3_root(self):
        """S6-B1 : Communauté préexistante reprise, non purgée."""
        self.Menu.search([
            ('website_id', '=', self.website.id),
            ('parent_id', '=', self.root.id),
            ('name', '=', 'Communauté'),
        ]).unlink()
        existing = self.Menu.create({
            'name': 'Communauté',
            'url': '#',
            'website_id': self.website.id,
            'parent_id': self.root.id,
            'sequence': 999,
        })
        self._sync()
        menu = self._root_menu('Communauté')
        self.assertTrue(menu, 'Communauté doit être présente après NAV-003 sync')
        self.assertEqual(menu.id, existing.id)
        self.assertEqual(menu.sequence, 55)
        self.assertEqual(menu.url, '#')
        self.assertEqual(
            self.Menu.search_count([
                ('website_id', '=', self.website.id),
                ('parent_id', '=', self.root.id),
                ('name', '=', 'Communauté'),
            ]),
            1,
        )

    def test_catalogue_nav_removes_espace_pro(self):
        self.Menu.create({
            'name': 'Espace pro',
            'url': '#',
            'website_id': self.website.id,
            'parent_id': self.root.id,
            'sequence': 999,
        })
        self._sync()
        self.assertFalse(
            self._root_menu('Espace pro'),
            'Espace pro doit être absent après NAV-003 sync',
        )

    # --- Idempotence ---

    def test_catalogue_nav_idempotent(self):
        self._sync()
        before = snapshot_ck_catalogue_navigation(self.env, self.website)
        self._sync()
        after = snapshot_ck_catalogue_navigation(self.env, self.website)
        self.assertEqual(after, before, 'Deux sync V3 doivent produire le même état structuré')
        boutique_count = self.Menu.search_count([
            ('website_id', '=', self.website.id),
            ('parent_id', '=', self.root.id),
            ('name', '=', NAV_CATALOGUE_BOUTIQUE_LABEL),
        ])
        self.assertEqual(boutique_count, 1, 'Une seule entrée Boutique après double sync')

        cat_count = self.Menu.search_count([
            ('website_id', '=', self.website.id),
            ('parent_id', '=', self.root.id),
            ('name', '=', self.cat_a.name),
        ])
        self.assertEqual(cat_count, 1, 'Une seule entrée catégorie A après double sync')

    def test_catalogue_nav_idempotent_children(self):
        self._sync()
        self._sync()
        parent = self._root_menu(self.cat_a.name)
        self.assertTrue(parent)
        child1_count = self.Menu.search_count([
            ('parent_id', '=', parent.id),
            ('name', '=', self.cat_a_child1.name),
        ])
        self.assertEqual(child1_count, 1, 'Une seule sous-catégorie A1 après double sync')

    def test_catalogue_nav_stable_identity_on_category_rename(self):
        """S2 : renommage catégorie → même menu (ck_nav_category_id), pas de doublon."""
        self._sync()
        menu_before = self._root_menu(self.cat_a.name)
        self.assertTrue(menu_before)
        menu_id = menu_before.id
        self.cat_a.write({'name': 'TestCat NAV003 Rayon A Renamed'})
        self._sync()
        menu_after = self.Menu.browse(menu_id)
        self.assertTrue(menu_after.exists())
        self.assertEqual(menu_after.name, 'TestCat NAV003 Rayon A Renamed')
        self.assertEqual(menu_after.ck_nav_category_id.id, self.cat_a.id)
        self.assertEqual(
            self.Menu.search_count([
                ('website_id', '=', self.website.id),
                ('parent_id', '=', self.root.id),
                ('ck_nav_category_id', '=', self.cat_a.id),
            ]),
            1,
        )

    # --- Nettoyage stale sur resync ---

    def test_catalogue_nav_removes_stale_category_on_resync(self):
        """Une catégorie dépubliée (plus de produits) doit disparaître au resync."""
        self._sync()
        self.assertTrue(self._root_menu(self.cat_a.name))

        # Dépublier les produits de cat_a (mais pas cat_a_child1/child2)
        # On crée une catégorie temporaire publiée puis la dépublie
        cat_tmp = self.env['product.public.category'].sudo().create({
            'name': 'TestCat NAV003 Tmp',
            'sequence': 930,
        })
        Product = self.env['product.template'].sudo()
        prods_tmp = Product.browse()
        for idx in range(3):
            prods_tmp |= Product.create({
                'name': f'Test Produit NAV003 Tmp {idx}',
                'sale_ok': True,
                'is_published': True,
                'website_published': True,
                'public_categ_ids': [(4, cat_tmp.id)],
            })
        self._sync()
        self.assertTrue(self._root_menu(cat_tmp.name))

        # Dépublier tous les produits (catégorie redevient vide)
        prods_tmp.write({'is_published': False, 'website_published': False})
        self._sync()
        self.assertFalse(
            self._root_menu(cat_tmp.name),
            'Catégorie devenue vide doit disparaître au resync',
        )

    # --- Bootstrap ---

    def test_catalogue_nav_bootstrap_returns_count(self):
        count = bootstrap_ck_catalogue_navigation(self.env)
        self.assertGreaterEqual(count, 1, 'bootstrap doit retourner >= 1 site synchronisé')

    # --- category_id sur menus catalogue ---

    def test_catalogue_nav_category_id_set_on_root_entries(self):
        self._sync()
        cat_menu = self._root_menu(self.cat_a.name)
        self.assertTrue(cat_menu)
        self.assertEqual(
            cat_menu.ck_nav_category_id.id,
            self.cat_a.id,
            'ck_nav_category_id doit être renseigné sur les entrées catalogue racines',
        )
