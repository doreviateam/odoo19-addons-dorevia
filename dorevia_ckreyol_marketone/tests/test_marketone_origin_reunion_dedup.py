# -*- coding: utf-8 -*-
"""TICKET_MARKETONE_ORIGINE_REUNION_DEDUP — fusion La Réunion / Reunion."""

from odoo.tests import tagged
from odoo.tests.common import HttpCase, TransactionCase

from odoo.addons.dorevia_ckreyol_marketone.models.marketone_origin_reunion_dedup import (
    CANONICAL_REUNION_LABEL,
    _is_reunion_duplicate_label,
    marketone_dedup_reunion_origin_values,
)


@tagged("post_install", "-at_install", "dorevia_marketone_origin_reunion_dedup")
class TestMarketoneOriginReunionDedup(TransactionCase):
    """Fusion idempotente des valeurs d'attribut Origines."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.attr = cls.env.ref(
            "dorevia_ckreyol_marketone.marketone_product_attribute_origin"
        )
        cls.website = cls.env.ref("website.default_website")

    def _reunion_values(self):
        return self.env["product.attribute.value"].search(
            [("attribute_id", "=", self.attr.id)]
        ).filtered(lambda v: _is_reunion_duplicate_label(v.name))

    def test_dedup_merges_duplicate_and_keeps_products(self):
        canonical = self.env["product.attribute.value"].create(
            {"name": "La Réunion", "attribute_id": self.attr.id}
        )
        duplicate = self.env["product.attribute.value"].create(
            {"name": "Reunion", "attribute_id": self.attr.id}
        )
        product = self.env["product.template"].create(
            {
                "name": "Produit test dédup Réunion",
                "type": "consu",
                "list_price": 1.0,
                "sale_ok": True,
                "attribute_line_ids": [
                    (
                        0,
                        0,
                        {
                            "attribute_id": self.attr.id,
                            "value_ids": [(6, 0, [duplicate.id])],
                        },
                    )
                ],
            }
        )
        Origin = self.env["marketone.shop.origin"]
        profile = Origin.search([("slug", "=", "reunion")], limit=1)
        if profile:
            profile.write(
                {
                    "attribute_value_id": duplicate.id,
                    "name_visitor": "La Reunion",
                }
            )
        else:
            profile = Origin.create(
                {
                    "attribute_value_id": duplicate.id,
                    "slug": "reunion",
                    "name_visitor": "La Reunion",
                    "website_id": self.website.id,
                    "website_published": True,
                }
            )

        marketone_dedup_reunion_origin_values(self.env)

        reunion_vals = self._reunion_values()
        self.assertEqual(len(reunion_vals), 1)
        self.assertEqual(reunion_vals.name, CANONICAL_REUNION_LABEL)
        self.assertFalse(duplicate.exists())

        ptav = self.env["product.template.attribute.value"].search(
            [
                ("product_tmpl_id", "=", product.id),
                ("product_attribute_value_id", "=", reunion_vals.id),
            ]
        )
        self.assertEqual(len(ptav), 1)

        profile.invalidate_recordset()
        self.assertEqual(profile.attribute_value_id, reunion_vals)
        self.assertEqual(profile.name_visitor, CANONICAL_REUNION_LABEL)

    def test_dedup_idempotent_second_run(self):
        marketone_dedup_reunion_origin_values(self.env)
        before = self._reunion_values()
        marketone_dedup_reunion_origin_values(self.env)
        after = self._reunion_values()
        self.assertEqual(len(before), len(after))
        if after:
            self.assertEqual(after.name, CANONICAL_REUNION_LABEL)


@tagged("post_install", "-at_install", "dorevia_marketone_origin_reunion_dedup")
class TestMarketoneOriginReunionDedupHttp(HttpCase):
    """Sidebar /shop — une seule entrée La Réunion après dédup."""

    def test_shop_sidebar_single_reunion_label(self):
        marketone_dedup_reunion_origin_values(self.env)
        response = self.url_open("/shop")
        self.assertEqual(response.status_code, 200)
        html = response.text
        self.assertIn("La Réunion", html)
        self.assertNotRegex(
            html,
            r'products_attributes_filters[\s\S]{0,8000}>\s*Reunion\s*<',
        )

    def test_shop_origin_porte_reunion_still_works(self):
        marketone_dedup_reunion_origin_values(self.env)
        response = self.url_open(
            "/shop?marketone_mode=origin&marketone_origin=reunion"
        )
        self.assertEqual(response.status_code, 200)
