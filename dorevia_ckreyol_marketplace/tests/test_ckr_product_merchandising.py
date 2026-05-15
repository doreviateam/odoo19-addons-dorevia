# -*- coding: utf-8 -*-
"""Tests — fiche produit merchandising MVP2.4 Lot 2."""

from odoo.tests import tagged
from odoo.tests.common import TransactionCase


@tagged("post_install", "-at_install", "dorevia_ckr_product_merch")
class TestCkrProductMerchandising(TransactionCase):
    """Helpers de sections basses et recommandations fiables."""

    def test_product_detail_sections_use_existing_content_only(self):
        tmpl = self.env["product.template"].create(
            {
                "name": "Produit fiche riche",
                "type": "consu",
                "sale_ok": True,
                "description_sale": "Promesse courte",
                "description_ecommerce": "<p>Description utile du produit.</p>",
            }
        )
        sections = tmpl._ckr_get_product_detail_sections()
        self.assertEqual(sections[0]["title"], "Description")
        self.assertIn("Description utile", sections[0]["body"])

    def test_product_detail_sections_do_not_duplicate_promise(self):
        tmpl = self.env["product.template"].create(
            {
                "name": "Produit promesse seule",
                "type": "consu",
                "sale_ok": True,
                "description_sale": "Même phrase courte",
            }
        )
        sections = tmpl._ckr_get_product_detail_sections()
        self.assertFalse(
            [section for section in sections if section.get("key") == "description"]
        )

    def test_product_recommendations_follow_same_public_category(self):
        category = self.env["product.public.category"].create(
            {"name": "Biscuits test"}
        )
        current = self.env["product.template"].create(
            {
                "name": "Produit courant",
                "type": "consu",
                "sale_ok": True,
                "is_published": True,
                "website_published": True,
                "public_categ_ids": [(6, 0, [category.id])],
            }
        )
        reco = self.env["product.template"].create(
            {
                "name": "Produit recommandé",
                "type": "consu",
                "sale_ok": True,
                "is_published": True,
                "website_published": True,
                "public_categ_ids": [(6, 0, [category.id])],
            }
        )
        found = current._ckr_get_product_recommendation_templates(limit=4)
        self.assertIn(reco, found)
        self.assertNotIn(current, found)

    def test_product_merchandising_templates_are_registered(self):
        view = self.env.ref(
            "dorevia_ckreyol_marketplace.ckr_product_merchandising_sections"
        )
        self.assertIn("ckr-product-info", view.arch)
        recos = self.env.ref(
            "dorevia_ckreyol_marketplace.ckr_product_recommendations"
        )
        self.assertIn("ckr-product-recos", recos.arch)
