# -*- coding: utf-8 -*-
"""Tests — Nom CK + drill-down tuile /shop (SPEC_CK_NOM_CK_TUILE_PRODUIT.md).

Exemple ::

    odoo -d <base> --test-enable --stop-after-init \\
        --test-tags=dorevia_ckr_tile_name
"""
from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged("post_install", "-at_install", "dorevia_ckr_tile_name")
class TestCkrProductTileName(TransactionCase):
    """Champ ``ck_product_name`` et helper ``_ckr_shop_tile_has_more_block``."""

    def test_ck_product_name_field_exists(self):
        tmpl = self.env["product.template"].create(
            {
                "name": "Nom Odoo interne",
                "type": "consu",
                "sale_ok": True,
            }
        )
        tmpl.ck_product_name = "Nom boutique CK"
        self.assertEqual(tmpl.ck_product_name, "Nom boutique CK")
        self.assertEqual(tmpl.name, "Nom Odoo interne")

    def test_form_view_contains_ck_product_name(self):
        view = self.env.ref(
            "dorevia_ckreyol_marketplace.product_template_form_view_ck_product_name"
        )
        self.assertIn("ck_product_name", view.arch)

    def test_has_more_block_when_ck_name_differs(self):
        website = self.env.ref("website.default_website")
        tmpl = self.env["product.template"].create(
            {
                "name": "Interne seulement",
                "type": "consu",
                "sale_ok": True,
                "ck_product_name": "Affichage vitrine",
            }
        )
        self.assertTrue(tmpl._ckr_shop_tile_has_more_block(website))

    def test_has_more_block_false_when_no_extra(self):
        website = self.env.ref("website.default_website")
        tmpl = self.env["product.template"].create(
            {
                "name": "Seul libellé",
                "type": "consu",
                "sale_ok": True,
            }
        )
        self.assertFalse(tmpl._ckr_shop_tile_has_more_block(website))

    def test_has_more_block_when_description_sale(self):
        website = self.env.ref("website.default_website")
        tmpl = self.env["product.template"].create(
            {
                "name": "Produit avec desc",
                "type": "consu",
                "sale_ok": True,
                "description_sale": "<p>Ligne visible dans le panneau i</p>",
            }
        )
        self.assertTrue(tmpl._ckr_shop_tile_has_more_block(website))
