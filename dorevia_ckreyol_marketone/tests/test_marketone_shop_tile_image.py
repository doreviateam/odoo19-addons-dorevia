# -*- coding: utf-8 -*-
"""Tests V1.5 — tuile /shop image_shop_tile."""

import base64

from odoo.tests import tagged
from odoo.tests.common import HttpCase, TransactionCase

PNG_1X1 = (
    b"\x89PNG\r\n\x1a\n\x00\x00\x00\rIHDR\x00\x00\x00\x01"
    b"\x00\x00\x00\x01\x08\x02\x00\x00\x00\x90wS\xde\x00\x00\x00\x0cIDATx\x9cc``\x00\x00"
    b"\x00\x02\x00\x01\xe2!\xbc3\x00\x00\x00\x00IEND\xaeB`\x82"
)


@tagged("post_install", "-at_install", "dorevia_marketone_shop_tile")
class TestMarketoneShopTileModel(TransactionCase):
    """T4, T5, T6, T7 — modèle et feature flag."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.IrConfig = cls.env["ir.config_parameter"].sudo()
        cls.Product = cls.env["product.template"]
        cls.product = cls.Product.create(
            {
                "name": "Test Shop Tile Marketone",
                "type": "consu",
                "list_price": 9.99,
                "sale_ok": True,
                "is_published": True,
                "image_1920": base64.b64encode(PNG_1X1),
            }
        )
        cls._orig_image_1920 = cls.product.image_1920

    def setUp(self):
        super().setUp()
        self.IrConfig.set_param("marketone.shop_tile_enabled", "False")

    def test_t4_feature_flag_off_ignores_shop_tile(self):
        self.product.write(
            {
                "image_shop_tile": base64.b64encode(PNG_1X1),
                "shop_tile_status": "validated",
                "shop_tile_recipe_version": "ck_shop_tile_v2_grid",
            }
        )
        self.assertFalse(self.product.marketone_use_shop_tile_on_grid())

    def test_v1_1_shop_tile_not_used_on_grid(self):
        """Doctrine : v1.1 pilote standard non affiché en grille."""
        self.IrConfig.set_param("marketone.shop_tile_enabled", "True")
        self.product.write(
            {
                "image_shop_tile": base64.b64encode(PNG_1X1),
                "shop_tile_status": "validated",
                "shop_tile_recipe_version": "ck_shop_tile_v1.1",
                "shop_tile_source_run": "pilote_20260520",
            }
        )
        self.assertFalse(self.product.marketone_use_shop_tile_on_grid())

    def test_validated_storage_not_used_on_grid(self):
        """Doctrine v2 : stockage seul, fallback master."""
        self.IrConfig.set_param("marketone.shop_tile_enabled", "True")
        self.product.write(
            {
                "image_shop_tile": base64.b64encode(PNG_1X1),
                "shop_tile_status": "validated_storage",
            }
        )
        self.assertFalse(self.product.marketone_use_shop_tile_on_grid())

    def test_validated_grid_used_on_grid(self):
        """Doctrine v2 : seul validated_grid affiche le dérivé."""
        self.IrConfig.set_param("marketone.shop_tile_enabled", "True")
        self.product.write(
            {
                "image_shop_tile": base64.b64encode(PNG_1X1),
                "shop_tile_status": "validated_grid",
            }
        )
        self.assertTrue(self.product.marketone_use_shop_tile_on_grid())

    def test_t6_apply_fields_without_touching_master(self):
        tile_b64 = base64.b64encode(PNG_1X1)
        self.product.write(
            {
                "image_shop_tile": tile_b64,
                "shop_tile_status": "validated_storage",
                "shop_tile_recipe_version": "ck_shop_tile_v1.1",
                "shop_tile_source_run": "test_run",
            }
        )
        self.assertEqual(self.product.image_1920, self._orig_image_1920)
        self.assertTrue(self.product.image_shop_tile)

    def test_t7_clear_shop_tile_disables_grid_usage(self):
        self.IrConfig.set_param("marketone.shop_tile_enabled", "True")
        self.product.write(
            {
                "image_shop_tile": base64.b64encode(PNG_1X1),
                "shop_tile_status": "validated_grid",
            }
        )
        self.assertTrue(self.product.marketone_use_shop_tile_on_grid())
        self.product.write({"image_shop_tile": False})
        self.assertFalse(self.product.marketone_use_shop_tile_on_grid())


@tagged("post_install", "-at_install", "dorevia_marketone_shop_tile")
class TestMarketoneShopTileHttp(HttpCase):
    """T1, T2, T3 — rendu /shop et fiche produit."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.IrConfig = cls.env["ir.config_parameter"].sudo()
        cls.Product = cls.env["product.template"]
        cls.product_with_tile = cls.Product.create(
            {
                "name": "Produit Tuile Shop Tile HTTP",
                "type": "consu",
                "list_price": 11.0,
                "sale_ok": True,
                "is_published": True,
                "image_1920": base64.b64encode(PNG_1X1),
                "image_shop_tile": base64.b64encode(PNG_1X1),
                "shop_tile_status": "validated",
                "shop_tile_recipe_version": "ck_shop_tile_v1.1",
            }
        )
        cls.product_without_tile = cls.Product.create(
            {
                "name": "Produit Sans Tuile Shop Tile HTTP",
                "type": "consu",
                "list_price": 12.0,
                "sale_ok": True,
                "is_published": True,
                "image_1920": base64.b64encode(PNG_1X1),
            }
        )

    def setUp(self):
        super().setUp()
        self.IrConfig.set_param("marketone.shop_tile_enabled", "False")

    def test_t2_shop_without_flag_uses_standard_image(self):
        response = self.url_open("/shop")
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(
            f"/web/image/product.template/{self.product_with_tile.id}/image_shop_tile".encode(),
            response.content,
        )

    def test_t1_shop_with_flag_uses_shop_tile_when_validated_grid(self):
        self.IrConfig.set_param("marketone.shop_tile_enabled", "True")
        self.product_with_tile.write(
            {
                "shop_tile_recipe_version": "ck_shop_tile_v1.1",
                "shop_tile_status": "validated_grid",
            }
        )
        response = self.url_open(
            "/shop?search=Produit+Tuile+Shop+Tile+HTTP"
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(
            f"/web/image/product.template/{self.product_with_tile.id}/image_shop_tile".encode(),
            response.content,
        )

    def test_t1_shop_with_flag_storage_uses_master_on_grid(self):
        """Doctrine v2 : validated_storage → fallback image_1920."""
        self.IrConfig.set_param("marketone.shop_tile_enabled", "True")
        self.product_with_tile.write(
            {
                "shop_tile_recipe_version": "ck_shop_tile_v1.1",
                "shop_tile_status": "validated_storage",
                "shop_tile_source_run": "pilote_20260520",
            }
        )
        response = self.url_open(
            "/shop?search=Produit+Tuile+Shop+Tile+HTTP"
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(
            f"/web/image/product.template/{self.product_with_tile.id}/image_shop_tile".encode(),
            response.content,
        )

    def test_t3_product_page_does_not_use_shop_tile(self):
        self.IrConfig.set_param("marketone.shop_tile_enabled", "True")
        url = self.product_with_tile.website_url
        self.assertTrue(url)
        response = self.url_open(url)
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(
            b"image_shop_tile",
            response.content,
            "La fiche produit ne doit pas exposer image_shop_tile.",
        )

    def test_t5_import_manifest_validates_offline(self):
        import importlib.util
        from pathlib import Path

        module_root = Path(__file__).resolve().parents[1]
        manifest = module_root / "docs/recette/boutique/import_pilote_43_shop_tiles.csv"
        if not manifest.is_file():
            self.skipTest("Manifest pilote 43 absent.")
        script_path = module_root / "scripts" / "import_shop_tiles.py"
        spec = importlib.util.spec_from_file_location(
            "marketone_import_shop_tiles_test", script_path
        )
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        rows = mod.load_manifest(manifest)
        errors = mod.validate_manifest_rows(rows)
        self.assertEqual(errors, [], "\n".join(errors))
        self.assertEqual(len(rows), 43)

    def test_import_normalizes_legacy_validated_to_storage(self):
        import importlib.util
        from pathlib import Path

        script_path = Path(__file__).resolve().parents[1] / "scripts" / "import_shop_tiles.py"
        spec = importlib.util.spec_from_file_location("marketone_import_shop_tiles_test2", script_path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        self.assertEqual(mod.normalize_import_status("validated"), "validated_storage")
        self.assertEqual(mod.normalize_import_status("validated_grid"), "validated_grid")
