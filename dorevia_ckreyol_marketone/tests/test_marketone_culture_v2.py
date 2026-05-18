# -*- coding: utf-8 -*-
"""Tests Culture v2 légère — réplicabilité ``/culture/<slug>`` (martinique, reunion)."""

from odoo.tests import tagged
from odoo.tests.common import HttpCase


def _get_or_create_origin_profile(env, website, attr_origin, slug, name, phrase):
    """Profil origine publié — réutilise le BO recette si le slug existe déjà."""
    Origin = env["marketone.shop.origin"].sudo()
    profile = Origin.search(
        [("slug", "=", slug), ("website_id", "in", [False, website.id])],
        limit=1,
    )
    if profile:
        profile.write(
            {
                "website_id": website.id,
                "website_published": True,
            }
        )
        return profile.attribute_value_id, profile
    val = env["product.attribute.value"].create(
        {"name": f"Origine {name} v2 test", "attribute_id": attr_origin.id}
    )
    profile = Origin.create(
        {
            "attribute_value_id": val.id,
            "slug": slug,
            "name_visitor": name,
            "context_phrase": phrase,
            "website_id": website.id,
            "website_published": True,
        }
    )
    return val, profile


@tagged("post_install", "-at_install", "dorevia_marketone_culture_v2")
class TestMarketoneCultureV2Http(HttpCase):
    """HTTP — territoires martinique / reunion ; grammaire identique v1."""

    TERRITORIES = (
        {
            "slug": "martinique",
            "name": "Martinique",
            "phrase": "L'île aux fleurs, entre terroir et créolité.",
            "other_slugs": (b"/culture/reunion", b"/culture/guadeloupe"),
        },
        {
            "slug": "reunion",
            "name": "La Réunion",
            "phrase": "Un territoire volcanique aux saveurs singulières.",
            "other_slugs": (b"/culture/martinique", b"/culture/guadeloupe"),
        },
    )

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.website = cls.env["website"].search([], limit=1)
        cls.attr_origin = cls.env.ref(
            "dorevia_ckreyol_marketone.marketone_product_attribute_origin"
        )
        cls.profiles = {}
        cls.products = {}
        for spec in cls.TERRITORIES:
            val, profile = _get_or_create_origin_profile(
                cls.env,
                cls.website,
                cls.attr_origin,
                spec["slug"],
                spec["name"],
                spec["phrase"],
            )
            cls.profiles[spec["slug"]] = profile
            cls.products[spec["slug"]] = cls.env["product.template"].create(
                {
                    "name": f"Produit Culture {spec['name']}",
                    "type": "consu",
                    "list_price": 9.0,
                    "sale_ok": True,
                    "is_published": True,
                    "attribute_line_ids": [
                        (
                            0,
                            0,
                            {
                                "attribute_id": cls.attr_origin.id,
                                "value_ids": [(6, 0, [val.id])],
                            },
                        )
                    ],
                }
            )

    def _assert_culture_page_ok(self, spec):
        slug = spec["slug"]
        profile = self.profiles[slug]
        response = self.url_open(f"/culture/{slug}")
        self.assertEqual(response.status_code, 200, slug)
        content = response.content
        self.assertIn(b"marketone-culture", content)
        title = (profile.display_name_visitor or spec["name"]).encode()
        self.assertIn(title, content)
        if profile.context_phrase:
            self.assertIn(profile.context_phrase.encode(), content)
        elif spec.get("phrase"):
            self.assertIn(spec["phrase"].encode(), content)
        self.assertIn(b"marketone-culture-section", content)
        self.assertIn(b"Acheter les produits de ce territoire", content)
        self.assertIn(b"marketone_mode=origin", content)
        self.assertIn(f"marketone_origin={slug}".encode(), content)
        for other in spec["other_slugs"]:
            self.assertNotIn(other, content)

    def test_culture_martinique_200(self):
        self._assert_culture_page_ok(self.TERRITORIES[0])

    def test_culture_reunion_200(self):
        self._assert_culture_page_ok(self.TERRITORIES[1])

    def test_culture_unknown_slug_404(self):
        response = self.url_open("/culture/territoire-inconnu-v2")
        self.assertEqual(response.status_code, 404)

    def test_shop_origin_facet_discover_martinique(self):
        response = self.url_open(
            "/shop?marketone_mode=origin&marketone_origin=martinique"
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"marketone-shop-origin-discover", response.content)
        self.assertIn(b"/culture/martinique", response.content)

    def test_shop_origin_facet_discover_reunion(self):
        response = self.url_open(
            "/shop?marketone_mode=origin&marketone_origin=reunion"
        )
        self.assertEqual(response.status_code, 200)
        self.assertIn(b"/culture/reunion", response.content)

    def test_product_page_culture_links_v2(self):
        for slug in self.profiles:
            product = self.products[slug]
            response = self.url_open(product.website_url)
            self.assertEqual(response.status_code, 200)
            self.assertIn(
                b"marketone-product-origins__culture-link", response.content
            )
            self.assertIn(f"/culture/{slug}".encode(), response.content)
