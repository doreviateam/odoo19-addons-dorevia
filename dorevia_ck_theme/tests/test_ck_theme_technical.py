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

    def test_ck_hero_carousel_has_accessible_pause_control(self):
        """Garde-fou WCAG 2.2.2 : data-bs-pause="hover" seul ne suffit pas — un
        bouton natif clavier/tactile doit permettre de stopper le défilement auto."""
        module_path = get_module_path('dorevia_ck_theme')
        with open(
            os.path.join(module_path, 'views/snippets/ck_snippet_hero.xml'),
            encoding='utf-8',
        ) as handle:
            snippet_xml = handle.read()
        with open(os.path.join(module_path, '__manifest__.py'), encoding='utf-8') as handle:
            manifest_source = handle.read()
        self.assertIn('ck-hero__visual-pause', snippet_xml)
        self.assertIn('aria-pressed="false"', snippet_xml)
        self.assertIn('aria-label="Mettre en pause', snippet_xml)
        self.assertIn('ck_hero_carousel_pause.js', manifest_source)

    def test_ck_hero_has_theme_only_image_fallback(self):
        """Garde-fou §QA C2 : en thème seul (dorevia_ck_marketone_content non
        installé), les visuels hero ne doivent plus renvoyer 404 — repli sur un
        placeholder fourni par le thème lui-même."""
        module_path = get_module_path('dorevia_ck_theme')
        with open(
            os.path.join(module_path, 'views/snippets/ck_snippet_hero.xml'),
            encoding='utf-8',
        ) as handle:
            snippet_xml = handle.read()
        self.assertIn('ck_hero_content_ready', snippet_xml)
        self.assertIn("ir.module.module", snippet_xml)
        self.assertIn('dorevia_ck_theme/static/src/img/ck_hero_placeholder.svg', snippet_xml)
        placeholder_path = os.path.join(module_path, 'static/src/img/ck_hero_placeholder.svg')
        self.assertTrue(os.path.isfile(placeholder_path))

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
        sale_scss_path = os.path.join(module_path, 'static/src/scss/website_sale.scss')
        product_card_scss_path = os.path.join(module_path, 'static/src/scss/product_card.scss')
        card_view_path = os.path.join(module_path, 'views/website_sale_product_card.xml')
        with open(snippet_path, encoding='utf-8') as handle:
            snippet_xml = handle.read()
        with open(scss_path, encoding='utf-8') as handle:
            scss_source = handle.read()
        with open(sale_scss_path, encoding='utf-8') as handle:
            sale_scss_source = handle.read()
        with open(product_card_scss_path, encoding='utf-8') as handle:
            product_card_scss_source = handle.read()
        with open(card_view_path, encoding='utf-8') as handle:
            card_view_xml = handle.read()
        self.assertIn('Nos coups de cœur', snippet_xml)
        self.assertIn('Toute la boutique', snippet_xml)
        self.assertIn('.ck-featured-products--maquette', scss_source)
        self.assertIn('.ck-product-card', product_card_scss_source)
        self.assertIn('&--home', product_card_scss_source)
        self.assertIn('&__meta', product_card_scss_source)
        self.assertIn('ck-product-card--shop', card_view_xml)
        self.assertIn('ck-product-card__image', card_view_xml)
        self.assertIn('Ajouter au panier', card_view_xml)
        self.assertIn('.ck-product-card--shop', sale_scss_source)
        self.assertIn('ck-product-card-favorite', sale_scss_source)
        self.assertIn('actions_onhover', sale_scss_source)

    def test_ck_primary_variables_frontend_only_not_backend(self):
        """Tokens CK : frontend uniquement — BO conserve les couleurs Odoo standard."""
        module_path = get_module_path('dorevia_ck_theme')
        with open(os.path.join(module_path, '__manifest__.py'), encoding='utf-8') as handle:
            manifest_source = handle.read()
        self.assertNotIn('web._assets_primary_variables', manifest_source)
        self.assertIn('ck_tokens.scss', manifest_source)
        self.assertIn('frontend_bootstrap_variables.scss', manifest_source)
        self.assertIn(
            'website/static/src/scss/bootstrap_overridden.scss',
            manifest_source,
        )

    def test_ck_fonts_self_hosted_no_google_cdn(self):
        """QA C3 : polices Fraunces + DM Sans servies localement — pas de CDN Google."""
        module_path = get_module_path('dorevia_ck_theme')
        with open(os.path.join(module_path, 'views/website_header.xml'), encoding='utf-8') as handle:
            header_xml = handle.read()
        with open(os.path.join(module_path, '__manifest__.py'), encoding='utf-8') as handle:
            manifest_source = handle.read()
        fonts_dir = os.path.join(module_path, 'static/src/fonts')
        self.assertNotIn('fonts.googleapis.com', header_xml)
        self.assertNotIn('fonts.gstatic.com', header_xml)
        self.assertIn('website_fonts.scss', manifest_source)
        for filename in (
            'dm-sans-latin.woff2',
            'dm-sans-latin-ext.woff2',
            'fraunces-latin.woff2',
            'fraunces-latin-ext.woff2',
        ):
            self.assertTrue(os.path.isfile(os.path.join(fonts_dir, filename)), filename)
