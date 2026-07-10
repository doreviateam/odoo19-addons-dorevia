# -*- coding: utf-8 -*-
"""Gate seed MOA — catalogue 18079 · install fraîche code-first."""

from odoo.tests import tagged
from odoo.tests.common import TransactionCase

from odoo.addons.dorevia_ck_marketone_content.catalog_manioc_variants import (
    MANIO_CRACKERS_PARENT_NAME,
    bootstrap_catalog_vedettes_products,
)
from odoo.addons.dorevia_ck_marketone_content.catalog_seed import (
    MOA_SEED_FEATURED_TEMPLATE_COUNT,
    MOA_SEED_PRODUCT_COUNT,
    assert_catalog_seed_complete,
    ensure_catalog_seed,
    load_catalog_image_b64,
)
from odoo.addons.dorevia_ck_marketone_content.catalog_seed_guard import (
    MOA_SEED_FEATURED_TEMPLATE_NAMES,
    MOA_SEED_PUBLISHED_PRODUCT_NAMES,
    count_moa_seed_featured_templates,
    count_moa_seed_published_products,
)
from odoo.addons.dorevia_ck_marketone_content.ck_product_placeholders import is_tiny_product_image
from odoo.addons.dorevia_ck_marketone_content.home_featured import (
    bootstrap_home_featured_products,
    get_curated_featured_variants,
)
from odoo.addons.dorevia_ck_marketone_content.home_reassurance import (
    REASSURANCE_TRUST_BAR_MARKER,
    bootstrap_home_reassurance,
    reassurance_home_arch_is_valid,
)
from odoo.addons.dorevia_ck_marketone_content.hooks import (
    BRAND_NAME,
    bootstrap_website_locale_fr,
)


@tagged('post_install', '-at_install', 'ck_moa_seed')
class TestCkMoaSeed(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        ensure_catalog_seed(cls.env)

    def test_catalog_images_load_from_static(self):
        image_b64 = load_catalog_image_b64('confiture_goyave.webp')
        self.assertTrue(image_b64)
        self.assertGreater(len(image_b64), 1000)

    def test_nine_published_products_by_name(self):
        self.assertEqual(
            count_moa_seed_published_products(self.env),
            MOA_SEED_PRODUCT_COUNT,
        )
        Template = self.env['product.template'].sudo()
        for name in MOA_SEED_PUBLISHED_PRODUCT_NAMES:
            product = Template.search([('name', '=', name)], limit=1)
            self.assertTrue(product, msg=f'Produit seed absent : {name}')
            self.assertTrue(product.is_published)
            self.assertTrue(product.website_published)
            self.assertTrue(product.sale_ok)

    def test_six_featured_templates(self):
        self.assertEqual(
            count_moa_seed_featured_templates(self.env),
            MOA_SEED_FEATURED_TEMPLATE_COUNT,
        )
        Template = self.env['product.template'].sudo()
        for name in MOA_SEED_FEATURED_TEMPLATE_NAMES:
            product = Template.search([('name', '=', name)], limit=1)
            self.assertTrue(product.ck_is_featured, msg=f'Vedette manquante : {name}')

    def test_products_have_real_images(self):
        Template = self.env['product.template'].sudo()
        for name in MOA_SEED_PUBLISHED_PRODUCT_NAMES:
            product = Template.search([('name', '=', name)], limit=1)
            has_image = not is_tiny_product_image(product.image_1920)
            if product.product_variant_ids:
                has_image = has_image or any(
                    not is_tiny_product_image(variant.image_1920)
                    for variant in product.product_variant_ids
                )
            self.assertTrue(has_image, msg=f'Image placeholder ou absente : {name}')

    def test_manio_crackers_two_variants(self):
        self.assertTrue(bootstrap_catalog_vedettes_products(self.env))
        parent = self.env['product.template'].sudo().search([
            ('name', '=', MANIO_CRACKERS_PARENT_NAME),
        ], limit=1)
        self.assertEqual(len(parent.product_variant_ids), 2)
        names = parent.product_variant_ids.mapped('display_name')
        self.assertTrue(any('sal' in (n or '').lower() for n in names))
        self.assertTrue(any('sucr' in (n or '').lower() for n in names))

    def test_assert_catalog_seed_complete(self):
        assert_catalog_seed_complete(self.env)

    def test_website_locale_fr(self):
        # Reproduit la condition install fraîche --without-demo=all : fr_FR
        # présente mais INACTIVE. Sans activation, l'ancien code laissait en_US.
        Lang = self.env['res.lang'].sudo().with_context(active_test=False)
        fr = Lang.search([('code', '=', 'fr_FR')], limit=1)
        self.assertTrue(fr, 'fr_FR doit exister comme res.lang')
        website = self.env['website'].sudo().search([], limit=1)
        if fr.active and website.default_lang_id != fr:
            try:
                website.write({'default_lang_id': self.env.ref('base.lang_en').id})
                fr.write({'active': False})
            except Exception:  # noqa: BLE001 — best-effort si Odoo protège la désactivation
                pass
        self.assertTrue(bootstrap_website_locale_fr(self.env))
        website = self.env['website'].sudo().search([], limit=1)
        fr = Lang.search([('code', '=', 'fr_FR')], limit=1)
        self.assertTrue(fr.active, 'bootstrap doit ACTIVER fr_FR (pas seulement default)')
        self.assertEqual(website.default_lang_id.code, 'fr_FR')
        self.assertIn(website.name, (BRAND_NAME, 'C-Kréyòl'))

    def test_featured_variants_eligible_for_home(self):
        variants = get_curated_featured_variants(self.env)
        self.assertGreaterEqual(len(variants), 4)
        for template in variants.mapped('product_tmpl_id'):
            self.assertTrue(template._is_ck_qualified_for_public_exposure())

    def test_home_reassurance_trust_bar_present(self):
        self.assertTrue(bootstrap_home_reassurance(self.env))
        self.assertTrue(bootstrap_home_featured_products(self.env))
        website = self.env['website'].sudo().search([], limit=1)
        lang = website.default_lang_id.code if website.default_lang_id else 'fr_FR'
        page = self.env['website.page'].search([('url', '=', '/')], limit=1)
        view = page.view_id.with_context(lang=lang)
        arch = view.arch_db
        if isinstance(arch, dict):
            arch = arch.get(lang) or next(iter(arch.values()))
        self.assertIn(REASSURANCE_TRUST_BAR_MARKER, arch)
        self.assertTrue(reassurance_home_arch_is_valid(arch))

    def test_epicerie_root_category_exists(self):
        cat = self.env['product.public.category'].sudo().search([
            ('name', '=', 'Épicerie'),
            ('parent_id', '=', False),
        ], limit=1)
        self.assertTrue(cat)
