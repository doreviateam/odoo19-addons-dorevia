# -*- coding: utf-8 -*-
"""CODE-004 — opt-out bootstrap Coffret / discovery-pack home."""

from lxml import etree

from odoo.tests import tagged
from odoo.tests.common import TransactionCase

from odoo.addons.dorevia_ck_marketone_content.catalog_discovery_pack import (
    DISCOVERY_PACK_PRODUCT_NAME,
    bootstrap_catalog_discovery_pack_product,
)
from odoo.addons.dorevia_ck_marketone_content.home_discovery_pack import (
    DISCOVERY_PACK_BOOTSTRAP_ICP,
    DISCOVERY_PACK_SECTION_MARKER,
    _discovery_pack_bootstrap_enabled,
    _remove_discovery_pack_sections,
    bootstrap_home_discovery_pack,
    build_discovery_pack_arch,
    discovery_pack_arch_is_valid,
)
from odoo.addons.dorevia_ck_marketone_content.hooks import bootstrap_all_marketone_content
from odoo.addons.dorevia_ck_marketone_content.home_featured import bootstrap_home_featured_products


@tagged('post_install', '-at_install', 'dorevia_ck_marketone_code_004')
class TestCkCode004DiscoveryPackOptOut(TransactionCase):
    def _icp(self):
        return self.env['ir.config_parameter'].sudo()

    def _set_icp(self, value):
        self._icp().set_param(DISCOVERY_PACK_BOOTSTRAP_ICP, value)

    def _clear_icp(self):
        self._icp().search([('key', '=', DISCOVERY_PACK_BOOTSTRAP_ICP)]).unlink()

    def _homepage_arch(self):
        page = self.env['website.page'].search([('url', '=', '/')], limit=1)
        self.assertTrue(page)
        arch = page.view_id.arch_db
        if isinstance(arch, dict):
            arch = next(iter(arch.values()))
        return arch

    def _write_homepage_arch(self, arch):
        page = self.env['website.page'].search([('url', '=', '/')], limit=1)
        page.view_id.sudo().write({'arch_db': arch})

    def _coffret_product(self):
        return self.env['product.template'].sudo().search(
            [('name', '=', DISCOVERY_PACK_PRODUCT_NAME)], limit=1)

    def test_t6_icp_string_false_not_bool_trap(self):
        """R-A — chaîne 'False' doit activer l'opt-out (pas bool(get_param))."""
        self._set_icp('False')
        self.assertFalse(_discovery_pack_bootstrap_enabled(self.env))
        self.assertTrue(bool(self._icp().get_param(DISCOVERY_PACK_BOOTSTRAP_ICP)))

    def test_t6_icp_absent_defaults_legacy_true(self):
        self._clear_icp()
        self.assertTrue(_discovery_pack_bootstrap_enabled(self.env))

    def test_t1_opt_out_does_not_republish_coffret(self):
        """T1 — ICP False : B1 ne republie pas après double bootstrap."""
        self._set_icp('False')
        product = self._coffret_product()
        if not product:
            bootstrap_catalog_discovery_pack_product(self.env)
            self._set_icp('False')
            product = self._coffret_product()
        product.write({'website_published': False, 'is_published': False})
        bootstrap_all_marketone_content(self.env)
        bootstrap_all_marketone_content(self.env)
        product.invalidate_recordset()
        self.assertFalse(product.website_published)
        self.assertFalse(product.is_published)

    def test_t4_opt_out_does_not_create_coffret(self):
        """T4 — ICP False : B1 ne crée pas le produit s'il est absent."""
        self._set_icp('False')
        existing = self._coffret_product()
        if existing:
            existing.unlink()
        bootstrap_catalog_discovery_pack_product(self.env)
        self.assertFalse(self._coffret_product())

    def test_t2_opt_out_home_stable_without_section(self):
        """T2 — section absente stable après double bootstrap."""
        self._set_icp('False')
        arch = self._homepage_arch()
        new_arch, _removed = _remove_discovery_pack_sections(arch)
        self._write_homepage_arch(new_arch)
        bootstrap_home_discovery_pack(self.env)
        arch_after = self._homepage_arch()
        bootstrap_home_discovery_pack(self.env)
        self.assertEqual(arch_after, self._homepage_arch())
        self.assertNotIn(DISCOVERY_PACK_SECTION_MARKER, self._homepage_arch())
        self.assertTrue(discovery_pack_arch_is_valid(self._homepage_arch(), env=self.env))

    def test_t3_opt_out_removes_existing_section(self):
        """T3 — retrait section coffret présente."""
        self._set_icp('True')
        bootstrap_catalog_discovery_pack_product(self.env)
        self.assertTrue(bootstrap_home_discovery_pack(self.env))
        self.assertIn(DISCOVERY_PACK_SECTION_MARKER, self._homepage_arch())
        self._set_icp('False')
        self.assertTrue(bootstrap_home_discovery_pack(self.env))
        result = self._homepage_arch()
        self.assertNotIn(DISCOVERY_PACK_SECTION_MARKER, result)
        self.assertTrue(discovery_pack_arch_is_valid(result, env=self.env))
        etree.fromstring(f'<ck-root>{result}</ck-root>')

    def test_t3d_remove_preserves_void_img_sibling_sections(self):
        """R-B — etree round-trip : ``<img/>`` sœur survivent, arch XML valide."""
        self._set_icp('True')
        sibling = (
            '<section class="ck-univers-cards">'
            '<img src="/u.jpg" alt="U" loading="lazy"/>'
            '</section>'
        )
        section = build_discovery_pack_arch(self.env)
        arch = sibling + '\n' + section
        new_arch, removed = _remove_discovery_pack_sections(arch)
        self.assertTrue(removed)
        self.assertNotIn(DISCOVERY_PACK_SECTION_MARKER, new_arch)
        self.assertIn('loading="lazy"/>', new_arch)
        etree.fromstring(f'<ck-root>{new_arch}</ck-root>')

    def test_t3b_remove_section_without_dual_engage(self):
        """T3b — helper etree retire la section sans dual-engage."""
        self._set_icp('True')
        section = build_discovery_pack_arch(self.env)
        arch = (
            '<section class="ck-univers-cards">Univers</section>\n' + section
        )
        new_arch, removed = _remove_discovery_pack_sections(arch)
        self.assertTrue(removed)
        self.assertNotIn(DISCOVERY_PACK_SECTION_MARKER, new_arch)

    def test_t3c_remove_duplicate_sections(self):
        """T3c — helper etree retire toutes les sections dupliquées."""
        self._set_icp('True')
        section = build_discovery_pack_arch(self.env)
        new_arch, removed = _remove_discovery_pack_sections(section + '\n' + section)
        self.assertTrue(removed)
        self.assertNotIn(DISCOVERY_PACK_SECTION_MARKER, new_arch)

    def test_t5_legacy_enabled_still_injects(self):
        """T5 — ICP True (legacy) : injection discovery conservée."""
        self._set_icp('True')
        from odoo.addons.dorevia_ck_marketone_content.home_univers import bootstrap_home_univers

        bootstrap_catalog_discovery_pack_product(self.env)
        bootstrap_home_univers(self.env)
        self.assertTrue(bootstrap_home_discovery_pack(self.env))
        self.assertIn(DISCOVERY_PACK_SECTION_MARKER, self._homepage_arch())
        self.assertTrue(discovery_pack_arch_is_valid(self._homepage_arch()))

    def test_home_featured_non_regression_under_opt_out(self):
        """Hero/vedettes inchangés fonctionnellement sous opt-out."""
        self._set_icp('False')
        bootstrap_home_featured_products(self.env)
        arch_before = self._homepage_arch()
        featured_marker = 'ck-featured-products__grid--stable'
        self.assertIn(featured_marker, arch_before)
        bootstrap_home_discovery_pack(self.env)
        arch_after = self._homepage_arch()
        self.assertIn(featured_marker, arch_after)
