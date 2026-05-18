# -*- coding: utf-8 -*-
"""Tests Culture v1 — page territoire ``/culture/<slug>``."""

from odoo.tests import tagged
from odoo.tests.common import HttpCase, TransactionCase


@tagged("post_install", "-at_install", "dorevia_marketone_culture_v1")
class TestMarketoneCultureV1Model(TransactionCase):
    """Résolution slug et URLs Culture / Boutique."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.website = cls.env.ref("website.default_website")
        cls.attr_origin = cls.env.ref(
            "dorevia_ckreyol_marketone.marketone_product_attribute_origin"
        )
        cls.val_g = cls.env["product.attribute.value"].create(
            {"name": "Culture Origine G", "attribute_id": cls.attr_origin.id}
        )
        cls.profile_g = cls.env["marketone.shop.origin"].create(
            {
                "attribute_value_id": cls.val_g.id,
                "slug": "guadeloupe-culture",
                "name_visitor": "Guadeloupe",
                "context_phrase": "Île aux mille saveurs.",
                "website_id": cls.website.id,
                "website_published": True,
            }
        )

    def test_resolve_published_slug(self):
        Origin = self.env["marketone.shop.origin"]
        found = Origin._marketone_resolve_published_slug(
            "guadeloupe-culture",
            website=self.website,
        )
        self.assertEqual(found, self.profile_g)
        self.assertFalse(
            Origin._marketone_resolve_published_slug(
                "inconnu",
                website=self.website,
            )
        )
        self.assertFalse(
            Origin._marketone_resolve_published_slug(
                "INVALID",
                website=self.website,
            )
        )

    def test_profile_urls(self):
        self.assertEqual(
            self.profile_g._marketone_culture_url(),
            "/culture/guadeloupe-culture",
        )
        self.assertIn(
            "marketone_mode=origin",
            self.profile_g._marketone_origin_shop_url(),
        )
        self.assertIn(
            "marketone_origin=guadeloupe-culture",
            self.profile_g._marketone_origin_shop_url(),
        )


@tagged("post_install", "-at_install", "dorevia_marketone_culture_v1")
class TestMarketoneCultureV1Http(HttpCase):
    """HTTP — page Culture, liens Boutique, non-régression portes."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.website = cls.env["website"].search([], limit=1)
        cls.attr_origin = cls.env.ref(
            "dorevia_ckreyol_marketone.marketone_product_attribute_origin"
        )
        cls.val_g = cls.env["product.attribute.value"].create(
            {"name": "Culture HTTP G", "attribute_id": cls.attr_origin.id}
        )
        cls.profile_g = cls.env["marketone.shop.origin"].create(
            {
                "attribute_value_id": cls.val_g.id,
                "slug": "guadeloupe-culture-http",
                "name_visitor": "Guadeloupe Culture",
                "context_phrase": "Entre mer et montagne.",
                "website_id": cls.website.id,
                "website_published": True,
            }
        )
        cls.product_g = cls.env["product.template"].create(
            {
                "name": "HTTP Produit Culture G",
                "type": "consu",
                "list_price": 11.0,
                "sale_ok": True,
                "is_published": True,
                "attribute_line_ids": [
                    (
                        0,
                        0,
                        {
                            "attribute_id": cls.attr_origin.id,
                            "value_ids": [(6, 0, [cls.val_g.id])],
                        },
                    )
                ],
            }
        )

    def test_culture_territory_200(self):
        response = self.url_open("/culture/guadeloupe-culture-http")
        self.assertEqual(response.status_code, 200)
        content = response.content
        self.assertIn(b"marketone-culture", content)
        self.assertIn(b"Guadeloupe Culture", content)
        self.assertIn(b"Entre mer et montagne.", content)
        self.assertIn(b"Acheter les produits de ce territoire", content)
        self.assertIn(b"marketone_mode=origin", content)
        self.assertIn(b"marketone_origin=guadeloupe-culture-http", content)

    def test_culture_unknown_slug_404(self):
        response = self.url_open("/culture/slug-inconnu-culture")
        self.assertEqual(response.status_code, 404)

    def test_culture_unpublished_404(self):
        self.profile_g.website_published = False
        response = self.url_open("/culture/guadeloupe-culture-http")
        self.assertEqual(response.status_code, 404)
        self.profile_g.website_published = True

    def test_shop_origin_facet_has_discover_link(self):
        response = self.url_open(
            "/shop?marketone_mode=origin"
            "&marketone_origin=guadeloupe-culture-http"
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"marketone-shop-origin-discover", response.content)
        self.assertIn(b"/culture/guadeloupe-culture-http", response.content)

    def test_shop_origin_mode_alone_no_discover(self):
        response = self.url_open("/shop?marketone_mode=origin")
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b"marketone-shop-origin-discover", response.content)

    def test_product_page_culture_link(self):
        response = self.url_open(self.product_g.website_url)
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"marketone-product-origins__culture-link", response.content)
        self.assertIn(b"/culture/guadeloupe-culture-http", response.content)

    def test_featured_unchanged(self):
        response = self.url_open("/shop?marketone_mode=featured")
        self.assertEqual(response.status_code, 200)
        self.assertNotIn(b"marketone-culture", response.content)
