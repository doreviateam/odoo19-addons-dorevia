# -*- coding: utf-8 -*-
"""Tests hooks Phase 3 — bootstrap catégorie · nettoyage vue shell legacy."""

from odoo.tests import tagged
from odoo.tests.common import TransactionCase

from odoo.addons.dorevia_ck_marketone_content.hooks import (
    EPICERIE_CATEGORY_DESCRIPTION,
    EPICERIE_CATEGORY_NAME,
    bootstrap_epicerie_category,
)


@tagged('post_install', '-at_install', 'dorevia_ck_theme_phase3')
class TestCkShopPhase3Hooks(TransactionCase):
    def test_bootstrap_epicerie_category_sets_display_flags(self):
        self.env['product.public.category'].search([('name', '=', EPICERIE_CATEGORY_NAME)]).unlink()
        cat = self.env['product.public.category'].create({'name': EPICERIE_CATEGORY_NAME})
        self.assertTrue(bootstrap_epicerie_category(self.env))
        cat.invalidate_recordset()
        self.assertTrue(cat.show_category_title)
        self.assertTrue(cat.show_category_description)
        self.assertIn('Savons artisanaux', cat.website_description or '')

    def test_bootstrap_skips_when_category_missing(self):
        self.env['product.public.category'].search([('name', '=', EPICERIE_CATEGORY_NAME)]).unlink()
        self.assertFalse(bootstrap_epicerie_category(self.env))

    def test_bootstrap_preserves_existing_description(self):
        self.env['product.public.category'].search([('name', '=', EPICERIE_CATEGORY_NAME)]).unlink()
        custom = '<p>Description MOA custom</p>'
        cat = self.env['product.public.category'].create({
            'name': EPICERIE_CATEGORY_NAME,
            'website_description': custom,
        })
        bootstrap_epicerie_category(self.env)
        self.assertEqual(cat.website_description, custom)

    def test_bootstrap_fills_empty_description_only(self):
        self.env['product.public.category'].search([('name', '=', EPICERIE_CATEGORY_NAME)]).unlink()
        cat = self.env['product.public.category'].create({'name': EPICERIE_CATEGORY_NAME})
        bootstrap_epicerie_category(self.env)
        cat.invalidate_recordset()
        self.assertEqual(cat.website_description, EPICERIE_CATEGORY_DESCRIPTION)
