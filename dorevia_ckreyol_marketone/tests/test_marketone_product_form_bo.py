# -*- coding: utf-8 -*-
"""Tests lot recadrage BO produit — vues fiche produit Marketone."""

import base64

from odoo.tests import tagged
from odoo.tests.common import TransactionCase

PNG_1X1 = (
    b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01"
    b"\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDATx\x9cc``\x00\x00"
    b"\x00\x02\x00\x01\xe2!\xbc3\x00\x00\x00\x00IEND\xaeB`\x82"
)


@tagged("post_install", "-at_install", "dorevia_marketone_bo")
class TestMarketoneProductFormBo(TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.Product = cls.env["product.template"]
        cls.bo_view = cls.env.ref(
            "dorevia_ckreyol_marketone.product_template_form_view_marketone_bo"
        )
        cls.hide_view = cls.env.ref(
            "dorevia_ckreyol_marketone.product_template_form_view_marketone_bo_hide_ecommerce_dup"
        )

    def _combined_form_arch(self):
        return self.env["product.template"].get_views([(False, "form")])["views"][
            "form"
        ]["arch"]

    def test_bo_view_no_legacy_tile_block(self):
        arch = self.bo_view.arch
        self.assertNotIn("Tuile commerce /shop", arch)
        self.assertNotIn("marketone_shop_tile_group", arch)
        combined = self._combined_form_arch()
        self.assertNotIn("Tuile commerce /shop", combined)
        self.assertNotIn("marketone_shop_tile_group", combined)

    def test_bo_view_notebook_pages_present(self):
        arch = self.bo_view.arch
        for page_name in (
            "marketone_bo_publication",
            "marketone_bo_catalogue",
            "marketone_bo_media_quality",
            "marketone_bo_technical",
        ):
            self.assertIn(f'name="{page_name}"', arch)

    def test_bo_technical_page_restricted(self):
        arch = self.bo_view.arch
        self.assertIn('name="marketone_bo_technical"', arch)
        self.assertIn('groups="base.group_no_one"', arch)

    def test_bo_technical_fields_not_on_media_page(self):
        arch = self.bo_view.arch
        media_start = arch.index('name="marketone_bo_media_quality"')
        technical_start = arch.index('name="marketone_bo_technical"')
        media_block = arch[media_start:technical_start]
        self.assertNotIn("shop_tile_recipe_version", media_block)
        self.assertNotIn("shop_tile_source_run", media_block)
        self.assertNotIn("shop_tile_processed_at", media_block)

    def test_bo_collections_on_catalogue_page(self):
        arch = self.bo_view.arch
        catalogue_start = arch.index('name="marketone_bo_catalogue"')
        media_start = arch.index('name="marketone_bo_media_quality"')
        catalogue_block = arch[catalogue_start:media_start]
        self.assertIn("marketone_collection_ids", catalogue_block)

    def test_bo_publication_site_fields(self):
        arch = self.bo_view.arch
        publication_start = arch.index('name="marketone_bo_publication"')
        catalogue_start = arch.index('name="marketone_bo_catalogue"')
        publication_block = arch[publication_start:catalogue_start]
        self.assertIn("is_published", publication_block)
        self.assertIn("public_categ_ids", publication_block)
        self.assertIn("description_ecommerce", publication_block)

    def test_bo_hide_view_masks_standard_ecommerce_fields(self):
        arch = self.hide_view.arch
        self.assertIn("extra_info", arch)
        self.assertIn("ecom_description", arch)

    def test_bo_field_labels_renamed(self):
        fields_def = self.Product.fields_get(
            [
                "image_shop_tile",
                "shop_tile_status",
                "shop_tile_moa_note",
                "shop_tile_recipe_version",
                "shop_tile_source_run",
            ]
        )
        user_facing = (
            fields_def["image_shop_tile"]["string"],
            fields_def["shop_tile_status"]["string"],
            fields_def["shop_tile_moa_note"]["string"],
        )
        for label in user_facing:
            self.assertNotIn("/shop", label.lower())
            self.assertNotIn("tuile", label.lower())
            self.assertNotIn("cli", label.lower())
        self.assertEqual(
            fields_def["image_shop_tile"]["string"],
            "Vignette catalogue normalisée",
        )
        self.assertEqual(
            fields_def["shop_tile_moa_note"]["string"],
            "Note qualité visuelle",
        )

    def test_bo_shop_tile_logic_unchanged(self):
        """Non-régression — comportement front inchangé."""
        product = self.Product.create(
            {
                "name": "BO Recadrage Test",
                "sale_ok": True,
                "is_published": True,
            }
        )
        self.env["ir.config_parameter"].sudo().set_param(
            "marketone.shop_tile_enabled", "True"
        )
        product.write(
            {
                "image_shop_tile": base64.b64encode(PNG_1X1),
                "shop_tile_status": "validated_grid",
            }
        )
        self.assertTrue(product.marketone_use_shop_tile_on_grid())
        product.write({"shop_tile_status": "validated_storage"})
        self.assertFalse(product.marketone_use_shop_tile_on_grid())
