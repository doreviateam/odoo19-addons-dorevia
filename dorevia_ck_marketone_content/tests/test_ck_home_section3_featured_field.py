# -*- coding: utf-8 -*-
"""Tests ticket En vedette — ck_is_featured (T5, T7 multi-langues, T8 migration)."""

from odoo.tests import tagged
from odoo.tests.common import TransactionCase

from odoo.addons.dorevia_ck_marketone_content.ck_product_placeholders import (
    CK_CREAM_PLACEHOLDER_PNG_B64,
)
from odoo.addons.dorevia_ck_marketone_content.home_featured import (
    FEATURED_CATEGORY_XMLID,
    FEATURED_SECTION_MARKER,
    _arch_as_string,
    _featured_target_langs,
    _ensure_featured_category,
    bootstrap_home_featured_products,
    get_curated_featured_variants,
    migrate_coups_de_coeur_category_to_ck_is_featured,
)


@tagged('post_install', '-at_install', 'dorevia_ck_marketone_home_section3_featured_field')
class TestCkHomeSection3FeaturedField(TransactionCase):
    def _make_product(self, name, **vals):
        base = {
            'name': name,
            'is_published': True,
            'website_published': True,
            'sale_ok': True,
            'list_price': 1.0,
            'image_1920': CK_CREAM_PLACEHOLDER_PNG_B64,
        }
        base.update(vals)
        return self.env['product.template'].sudo().create(base)

    def _homepage_view(self):
        website = self.env['website'].search([], limit=1)
        page = self.env['website.page'].sudo().search([
            ('url', '=', '/'),
            ('website_id', '=', website.id),
        ], limit=1)
        self.assertTrue(page and page.view_id)
        return website, page.view_id.sudo()

    def _arch_for_lang(self, view, lang):
        lang_env = self.env(context=dict(self.env.context, lang=lang))
        arch = view.with_env(lang_env).arch_db or view.with_env(lang_env).arch or ''
        return _arch_as_string(arch)

    def _ensure_website_lang(self, code):
        Lang = self.env['res.lang'].sudo()
        lang = Lang.search([('code', '=', code)], limit=1)
        if not lang:
            Lang._activate_lang(code)
            lang = Lang.search([('code', '=', code)], limit=1)
        website = self.env['website'].search([], limit=1)
        if lang not in website.language_ids:
            website.sudo().write({'language_ids': [(4, lang.id)]})
        return lang

    def test_featured_without_image_is_excluded(self):
        product = self._make_product(
            'CK Vedette Sans Image',
            ck_is_featured=True,
            image_1920=False,
        )
        product.product_variant_ids.write({'image_1920': False})
        names = [v.display_name for v in get_curated_featured_variants(self.env)]
        self.assertNotIn('CK Vedette Sans Image', names)

    def test_category_membership_does_not_feature_without_flag(self):
        category = _ensure_featured_category(self.env)
        product = self._make_product(
            'CK Vedette Cat Only',
            public_categ_ids=[(4, category.id)],
        )
        self.assertNotIn(product.product_variant_id, get_curated_featured_variants(self.env))

    def test_migration_sets_ck_is_featured_from_category(self):
        category = self.env.ref(FEATURED_CATEGORY_XMLID)
        product = self._make_product(
            'CK Vedette Migration Cat',
            ck_is_featured=False,
            public_categ_ids=[(4, category.id)],
        )
        count = migrate_coups_de_coeur_category_to_ck_is_featured(self.env)
        self.assertGreaterEqual(count, 1)
        self.assertTrue(product.ck_is_featured)
        self.assertIn(product.product_variant_id, get_curated_featured_variants(self.env))

    def test_featured_section_hidden_in_all_served_langs_when_no_featured(self):
        """T7 — masquage SSR dans chaque langue arch_db, pas seulement la source."""
        self._ensure_website_lang('fr_FR')
        website, view = self._homepage_view()

        self._make_product('CK Vedette Lang A', ck_is_featured=True)
        self._make_product('CK Vedette Lang B', ck_is_featured=True)
        bootstrap_home_featured_products(self.env)

        langs = _featured_target_langs(self.env, website)
        self.assertGreater(len(langs), 1, 'Le site doit servir au moins deux langues pour T7.')
        for lang in langs:
            arch = self._arch_for_lang(view, lang)
            self.assertIn(FEATURED_SECTION_MARKER, arch, lang)

        self.env['product.template'].sudo().search([
            ('ck_is_featured', '=', True),
        ]).write({'ck_is_featured': False})
        bootstrap_home_featured_products(self.env)
        view.invalidate_recordset(['arch_db'])

        for lang in langs:
            arch = self._arch_for_lang(view, lang)
            self.assertNotIn(
                FEATURED_SECTION_MARKER,
                arch,
                f'La section vedettes doit disparaître en {lang}',
            )
