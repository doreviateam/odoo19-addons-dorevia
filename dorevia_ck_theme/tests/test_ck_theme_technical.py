# -*- coding: utf-8 -*-
"""Tests maintenance technique dorevia_ck_theme (sans contenu métier)."""

import os

from odoo.modules.module import get_module_path
from odoo.tests import tagged
from odoo.tests.common import TransactionCase

from odoo.addons.dorevia_ck_theme.hooks import (
    LEGACY_PHASE3_VIEW_KEY,
    is_marketone_content_installed,
    remove_legacy_phase3_script_view,
)


@tagged('post_install', '-at_install', 'dorevia_ck_theme_technical')
class TestCkThemeTechnical(TransactionCase):
    def test_marketone_content_not_installed_by_default_on_theme_only(self):
        """Garde-fou §4bis : contenu absent si module content non installé."""
        Module = self.env['ir.module.module'].sudo()
        content = Module.search([('name', '=', 'dorevia_ck_marketone_content')], limit=1)
        if content and content.state == 'installed':
            self.skipTest('dorevia_ck_marketone_content installé — test thème seul non applicable')
        self.assertFalse(is_marketone_content_installed(self.env))

    def test_remove_legacy_phase3_script_view(self):
        products = self.env.ref('website_sale.products')
        legacy = self.env['ir.ui.view'].create({
            'name': 'Legacy Phase 3 shell view',
            'type': 'qweb',
            'mode': 'extension',
            'inherit_id': products.id,
            'arch_db': '<data/>',
            'key': LEGACY_PHASE3_VIEW_KEY,
        })
        remove_legacy_phase3_script_view(self.env)
        self.assertFalse(self.env['ir.ui.view'].search([('id', '=', legacy.id)]))

    def test_ck_hero_snippet_carousel_interval_fixed(self):
        """Garde-fou : intervalle carrousel Hero figé à 25 s — pas de réglage Builder Speed."""
        module_path = get_module_path('dorevia_ck_theme')
        with open(
            os.path.join(module_path, 'views/snippets/ck_snippet_hero.xml'),
            encoding='utf-8',
        ) as handle:
            snippet_xml = handle.read()
        with open(os.path.join(module_path, '__manifest__.py'), encoding='utf-8') as handle:
            manifest_source = handle.read()
        self.assertIn('data-bs-interval="25000"', snippet_xml)
        self.assertIn('data-bs-ride="carousel"', snippet_xml)
        self.assertIn('data-bs-pause="hover"', snippet_xml)
        self.assertIn('data-oe-protected="false"', snippet_xml)
        self.assertIn('o_editable_media', snippet_xml)
        self.assertIn('s_ck_hero_slide', snippet_xml)
        self.assertIn('ck-hero__slide-media o_editable', snippet_xml)
        self.assertNotIn('ck_hero_carousel_option', manifest_source)

    def test_ck_reassurance_trust_bar_snippet(self):
        """Garde-fou Section 2 : trust-bar maquette sur s_ck_reassurance home."""
        module_path = get_module_path('dorevia_ck_theme')
        with open(
            os.path.join(module_path, 'views/snippets/ck_snippet_reassurance.xml'),
            encoding='utf-8',
        ) as handle:
            snippet_xml = handle.read()
        scss_path = os.path.join(module_path, 'static/src/scss/website.scss')
        with open(scss_path, encoding='utf-8') as handle:
            scss_source = handle.read()
        self.assertIn('ck-reassurance--trust-bar', snippet_xml)
        self.assertIn('ck-reassurance__grid', snippet_xml)
        self.assertIn('Livraison France &amp; Europe', snippet_xml)
        self.assertIn('CK vous accompagne', snippet_xml)
        self.assertIn('Paiement en ligne simple et protégé', snippet_xml)
        self.assertNotIn('parcours checkout natif', snippet_xml)
        self.assertNotIn('conditions Pro sur qualification', snippet_xml)
        self.assertIn('.ck-reassurance--trust-bar', scss_source)

    def test_ck_featured_grid_media_visible_scss(self):
        """Garde-fou Section 3 : cartes maquette vedettes home."""
        module_path = get_module_path('dorevia_ck_theme')
        snippet_path = os.path.join(module_path, 'views/snippets/ck_snippet_featured_products.xml')
        scss_path = os.path.join(module_path, 'static/src/scss/website.scss')
        with open(snippet_path, encoding='utf-8') as handle:
            snippet_xml = handle.read()
        with open(scss_path, encoding='utf-8') as handle:
            scss_source = handle.read()
        self.assertIn('Nos coups de cœur', snippet_xml)
        self.assertIn('Toute la boutique', snippet_xml)
        self.assertIn('.ck-featured-products--maquette', scss_source)
        self.assertIn('.ck-product-card.product-card', scss_source)
        self.assertIn('.card-cta', scss_source)
