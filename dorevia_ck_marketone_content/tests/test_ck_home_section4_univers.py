# -*- coding: utf-8 -*-
"""Tests hooks Section 4 — Acheter par univers · 3 cards visuelles."""

from odoo.tests import tagged
from odoo.tests.common import TransactionCase

from odoo.addons.dorevia_ck_marketone_content.home_discovery_pack import (
    DISCOVERY_PACK_SECTION_MARKER,
)
from odoo.addons.dorevia_ck_marketone_content.home_featured import (
    FEATURED_SECTION_MARKER,
)
from odoo.addons.dorevia_ck_marketone_content.home_univers import (
    UNIVERS_CARD_SNIPPET,
    UNIVERS_EDITABLE_MEDIA_MARKER,
    UNIVERS_INTRO,
    UNIVERS_SECTION_MARKER,
    UNIVERS_TITLE,
    bootstrap_home_univers,
    build_home_univers_arch,
    univers_arch_is_valid,
)
from odoo.addons.dorevia_ck_marketone_content.hooks import (
    bootstrap_home_discovery_pack,
    bootstrap_home_featured_products,
)


@tagged('post_install', '-at_install', 'dorevia_ck_marketone_home_section4')
class TestCkHomeSection4UniversHooks(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        from odoo.addons.dorevia_ck_marketone_content.hooks import bootstrap_epicerie_category

        bootstrap_epicerie_category(cls.env)
        Category = cls.env['product.public.category'].sudo()
        for name in ('Épicerie', 'Maison & bien-être', 'Artisanat'):
            if not Category.search([('name', '=', name)], limit=1):
                Category.create({'name': name})
        bootstrap_epicerie_category(cls.env)
        bootstrap_home_featured_products(cls.env)

    def _homepage_arch(self):
        page = self.env['website.page'].search([('url', '=', '/')], limit=1)
        self.assertTrue(page)
        arch = page.view_id.arch_db
        if isinstance(arch, dict):
            arch = next(iter(arch.values()))
        return arch

    def setUp(self):
        super().setUp()
        bootstrap_home_featured_products(self.env)

    def test_build_univers_arch_markers(self):
        arch = build_home_univers_arch(self.env)
        self.assertIn(UNIVERS_SECTION_MARKER, arch)
        self.assertIn(UNIVERS_TITLE, arch)
        self.assertIn(UNIVERS_INTRO, arch)
        self.assertEqual(arch.count('ck-univers-card--'), 3)
        self.assertIn('Épicerie créole', arch)
        self.assertIn('Soin &amp; bien-être', arch)
        self.assertIn('Artisanat &amp; culture', arch)
        self.assertIn("Voir l'épicerie", arch)
        self.assertNotIn('Packs & découvertes', arch)
        self.assertNotIn('route-hint', arch)
        self.assertEqual(arch.count(f'data-snippet="{UNIVERS_CARD_SNIPPET}"'), 3)
        self.assertEqual(arch.count(UNIVERS_EDITABLE_MEDIA_MARKER), 3)
        self.assertEqual(arch.count('ck-univers-card__cover'), 3)
        self.assertIn('ck_univers_epicerie.jpg?v=5', arch)
        self.assertIn('ck-univers-card--epicerie o_editable', arch)
        self.assertNotIn('data-snippet="s_ck_univers_cards"', arch.split('ck-univers-cards__grid')[0])

    def test_bootstrap_injects_univers_after_featured(self):
        self.assertTrue(bootstrap_home_univers(self.env))
        arch = self._homepage_arch()
        self.assertTrue(univers_arch_is_valid(arch))
        featured_pos = arch.find(FEATURED_SECTION_MARKER)
        univers_pos = arch.find(UNIVERS_SECTION_MARKER)
        self.assertGreater(featured_pos, 0)
        self.assertGreater(univers_pos, featured_pos)

    def test_bootstrap_removes_legacy_category_pills(self):
        bootstrap_home_univers(self.env)
        arch = self._homepage_arch()
        self.assertNotIn('data-snippet="s_ck_category_links"', arch)

    def test_bootstrap_idempotent(self):
        bootstrap_home_univers(self.env)
        arch_before = self._homepage_arch()
        bootstrap_home_univers(self.env)
        self.assertEqual(arch_before, self._homepage_arch())

    def test_univers_before_discovery_pack(self):
        bootstrap_home_univers(self.env)
        bootstrap_home_discovery_pack(self.env)
        arch = self._homepage_arch()
        univers_pos = arch.find(UNIVERS_SECTION_MARKER)
        pack_pos = arch.find(DISCOVERY_PACK_SECTION_MARKER)
        self.assertGreater(univers_pos, 0)
        self.assertGreater(pack_pos, univers_pos)

    def test_category_links_use_bo_slugs(self):
        arch = build_home_univers_arch(self.env)
        epicerie = self.env['product.public.category'].sudo().search([
            ('name', 'in', ('Épicerie créole', 'Épicerie')),
        ], limit=1)
        self.assertTrue(epicerie)
        slug = self.env['ir.http'].sudo()._slug(epicerie)
        self.assertIn(f'/shop/category/{slug}', arch)
        self.assertNotIn('href="/shop"', arch.split('ck-univers-card--epicerie')[1].split('ck-univers-card--')[0])

    def test_bootstrap_preserves_editor_image_changes(self):
        from odoo.addons.dorevia_ck_marketone_content.home_univers import bootstrap_home_univers

        bootstrap_home_univers(self.env)
        page = self.env['website.page'].search([('url', '=', '/')], limit=1)
        arch = self._homepage_arch()
        custom = '/web/image/ir.attachment/424242/custom_epicerie.jpg'
        page.view_id.write({
            'arch_db': arch.replace('ck_univers_epicerie.jpg', 'custom_epicerie_marker.jpg', 1),
        })
        bootstrap_home_univers(self.env)
        self.assertIn('custom_epicerie_marker.jpg', self._homepage_arch())
