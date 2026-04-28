# -*- coding: utf-8 -*-
"""Tests automatisés alignés sur le PV de recette « Porte Origines V1 ».

Référence : PV recette (RC-01 … RC-13), ``SPEC_IMPL_ORIGINES.md``,
``CONTRAT_URL_ORIGINES.md``.

Exécution ciblée (exemple) ::

    odoo -d <base> --test-enable --stop-after-init \\
        --test-tags=dorevia_ckr_origins

Tag ``post_install`` : dépend de ``website_sale`` + données module
(``ckr_product_attribute_origin``).
"""
import html
import uuid
import re
from urllib.parse import urlparse, parse_qs

from psycopg2 import IntegrityError

from odoo.exceptions import ValidationError
from odoo.tests import tagged
from odoo.tests.common import HttpCase, TransactionCase


def _website_sale_search_options(env, **extra):
    """Options minimales attendues par ``website_sale`` pour ``_search_get_detail``."""
    base = {
        "displayImage": True,
        "displayDescription": True,
        "displayExtraLink": True,
        "displayDetail": True,
        "display_currency": env.company.currency_id,
    }
    base.update(extra)
    return base


@tagged("post_install", "-at_install", "dorevia_ckr_origins")
class TestCkrOriginPVModel(TransactionCase):
    """RC-01, RC-02, RC-03 (partiel), logique recherche / résolution."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.website = cls.env.ref("website.default_website")
        cls.attr_origin = cls.env.ref(
            "dorevia_ckreyol_marketplace.ckr_product_attribute_origin"
        )
        cls.val_g = cls.env["product.attribute.value"].create(
            {"name": "PV Guadeloupe", "attribute_id": cls.attr_origin.id}
        )
        cls.val_m = cls.env["product.attribute.value"].create(
            {"name": "PV Martinique", "attribute_id": cls.attr_origin.id}
        )
        cls.val_empty = cls.env["product.attribute.value"].create(
            {"name": "PV Sans produit", "attribute_id": cls.attr_origin.id}
        )

    def test_pv_rc01_form_view_contains_origin_field(self):
        """RC-01 : le champ confort est présent sur la vue formulaire produit."""
        view = self.env.ref(
            "dorevia_ckreyol_marketplace.product_template_form_view_ckr_origin"
        )
        self.assertIn("ckr_origin_value_ids", view.arch)

    def test_pv_rc02_ckr_origin_value_ids_multi_inverse(self):
        """RC-02 : plusieurs valeurs d'origine persistées via le champ confort."""
        tmpl = self.env["product.template"].create(
            {
                "name": "CKR PV Produit multi-origines",
                "type": "consu",
                "sale_ok": True,
                "website_published": True,
            }
        )
        tmpl.ckr_origin_value_ids = [(6, 0, [self.val_g.id, self.val_m.id])]
        tmpl.invalidate_recordset()
        self.assertEqual(len(tmpl.ckr_origin_value_ids), 2)
        line = tmpl.attribute_line_ids.filtered(
            lambda l: l.attribute_id == self.attr_origin
        )
        self.assertEqual(len(line), 1)
        self.assertEqual(set(line.value_ids.ids), {self.val_g.id, self.val_m.id})

    def test_pv_rc03_slug_invalid(self):
        """RC-03 : contrôle du format de slug."""
        Origin = self.env["ckr.shop.origin"]
        with self.assertRaises(ValidationError):
            Origin.create(
                {
                    "attribute_value_id": self.val_g.id,
                    "slug": "MAJUSCULE",
                    "name_visitor": "X",
                    "website_id": self.website.id,
                }
            )

    def test_pv_rc03_slug_unique_per_website(self):
        """RC-03 : unicité logique slug par site (contrainte SQL)."""
        slug = "pv-uniq-slug-%s" % uuid.uuid4().hex[:12]
        Origin = self.env["ckr.shop.origin"]
        Origin.search(
            [("slug", "=", slug), ("website_id", "=", self.website.id)]
        ).unlink()
        Origin.create(
            {
                "attribute_value_id": self.val_g.id,
                "slug": slug,
                "name_visitor": "G",
                "website_id": self.website.id,
            }
        )
        with self.cr.savepoint(), self.assertRaises(IntegrityError):
            Origin.create(
                {
                    "attribute_value_id": self.val_m.id,
                    "slug": slug,
                    "name_visitor": "M",
                    "website_id": self.website.id,
                }
            )

    def test_pv_rc03_menus_and_action_exist(self):
        """RC-03 : menus back-office et action window présents."""
        self.env.ref("dorevia_ckreyol_marketplace.menu_ckreyol_configuration_origins")
        self.env.ref("dorevia_ckreyol_marketplace.menu_ckreyol_catalog_origins")
        self.env.ref("dorevia_ckreyol_marketplace.action_ckr_shop_origin")

    def test_search_detail_origin_only_no_filter_without_value_ids(self):
        """RC-05 (logique) : ``ckr_origin_only`` sans ids → pas de restriction domaine."""
        website = self.website
        tmpl = self.env["product.template"]
        detail = tmpl._search_get_detail(
            website,
            "name asc",
            _website_sale_search_options(
                self.env,
                ckr_origin_only=True,
                ckr_origin_attribute_value_ids=[],
            ),
        )
        domains = detail.get("base_domain") or []
        self.assertFalse(
            any(
                "attribute_line_ids.value_ids" in str(dom) for dom in domains
            ),
            "Aucun filtre origine attendu lorsque aucune valeur n'est ciblée.",
        )

    def test_search_detail_origin_only_with_value_ids(self):
        """RC-06 / RC-08 (logique) : filtre sur valeurs d'attribut."""
        website = self.website
        detail = self.env["product.template"]._search_get_detail(
            website,
            "name asc",
            _website_sale_search_options(
                self.env,
                ckr_origin_only=True,
                ckr_origin_attribute_value_ids=[self.val_g.id],
            ),
        )
        flat = str(detail.get("base_domain") or [])
        self.assertIn("attribute_line_ids.value_ids", flat)

    def test_search_get_detail_ckr_public_category_restricts_domain(self):
        """``ckr_public_category_ids`` : alignement grille / min-max / ``_get_shop_domain``."""
        website = self.website
        cat = self.env["product.public.category"].sudo().create(
            {"name": "CKR Test Cat facet", "website_id": website.id}
        )
        detail = self.env["product.template"]._search_get_detail(
            website,
            "name asc",
            _website_sale_search_options(
                self.env,
                ckr_public_category_ids=[cat.id],
            ),
        )
        flat = str(detail.get("base_domain") or [])
        self.assertIn("public_categ_ids", flat)
        self.assertIn(str(cat.id), flat)

    def test_search_get_detail_ckr_category_invalid_domain(self):
        """Slug catégorie inconnu → domaine vide (cohérence filtre prix / sidebar)."""
        detail = self.env["product.template"]._search_get_detail(
            self.website,
            "name asc",
            _website_sale_search_options(
                self.env,
                ckr_category_invalid=True,
            ),
        )
        domains = detail.get("base_domain") or []
        self.assertIn([("id", "=", 0)], domains)

    def test_resolve_published_slugs_order(self):
        """Ordre stable des slugs résolus (contrôleur / modèle)."""
        Origin = self.env["ckr.shop.origin"]
        Origin.create(
            {
                "attribute_value_id": self.val_g.id,
                "slug": "pv-z",
                "name_visitor": "Z",
                "website_id": self.website.id,
                "website_published": True,
            }
        )
        Origin.create(
            {
                "attribute_value_id": self.val_m.id,
                "slug": "pv-a",
                "name_visitor": "A",
                "website_id": self.website.id,
                "website_published": True,
            }
        )
        ordered = Origin._ckr_resolve_published_slugs(
            ["pv-z", "pv-a", "pv-z"], website=self.website
        )
        self.assertEqual([p.slug for p in ordered], ["pv-z", "pv-a"])


@tagged("post_install", "-at_install", "dorevia_ckr_origins")
class TestCkrOriginPVHttp(HttpCase):
    """RC-04 à RC-13 : HTTP, rendu HTML, canonical, non-régression alias."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.website = cls.env.ref("website.default_website")
        cls.attr_origin = cls.env.ref(
            "dorevia_ckreyol_marketplace.ckr_product_attribute_origin"
        )
        cls.val_g = cls.env["product.attribute.value"].create(
            {"name": "HTTP Guadeloupe", "attribute_id": cls.attr_origin.id}
        )
        cls.val_m = cls.env["product.attribute.value"].create(
            {"name": "HTTP Martinique", "attribute_id": cls.attr_origin.id}
        )
        cls.val_no_phrase = cls.env["product.attribute.value"].create(
            {"name": "HTTP Sans phrase", "attribute_id": cls.attr_origin.id}
        )
        cls.val_orphan = cls.env["product.attribute.value"].create(
            {"name": "HTTP Orpheline catalogue", "attribute_id": cls.attr_origin.id}
        )
        Origin = cls.env["ckr.shop.origin"]
        Origin.create(
            {
                "attribute_value_id": cls.val_g.id,
                "slug": "guadeloupe",
                "name_visitor": "Guadeloupe",
                "context_phrase": "Une phrase de contexte PV.",
                "website_id": cls.website.id,
                "website_published": True,
            }
        )
        Origin.create(
            {
                "attribute_value_id": cls.val_m.id,
                "slug": "martinique",
                "name_visitor": "Martinique",
                "context_phrase": "Autre phrase.",
                "website_id": cls.website.id,
                "website_published": True,
            }
        )
        Origin.create(
            {
                "attribute_value_id": cls.val_no_phrase.id,
                "slug": "sans-phrase",
                "name_visitor": "Nom visiteur sans phrase",
                "website_id": cls.website.id,
                "website_published": True,
            }
        )
        Origin.create(
            {
                "attribute_value_id": cls.val_orphan.id,
                "slug": "origine-sans-produit",
                "name_visitor": "Origine catalogue vide",
                "website_id": cls.website.id,
                "website_published": True,
            }
        )
        cls.product_g = cls.env["product.template"].create(
            {
                "name": "CKR HTTP Produit Guadeloupe",
                "type": "consu",
                "sale_ok": True,
                "website_published": True,
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
        cls.product_m = cls.env["product.template"].create(
            {
                "name": "CKR HTTP Produit Martinique",
                "type": "consu",
                "sale_ok": True,
                "website_published": True,
                "attribute_line_ids": [
                    (
                        0,
                        0,
                        {
                            "attribute_id": cls.attr_origin.id,
                            "value_ids": [(6, 0, [cls.val_m.id])],
                        },
                    )
                ],
            }
        )
        cls.product_multi = cls.env["product.template"].create(
            {
                "name": "CKR HTTP Produit bi-origine",
                "type": "consu",
                "sale_ok": True,
                "website_published": True,
                "attribute_line_ids": [
                    (
                        0,
                        0,
                        {
                            "attribute_id": cls.attr_origin.id,
                            "value_ids": [(6, 0, [cls.val_g.id, cls.val_m.id])],
                        },
                    )
                ],
            }
        )
        cls.env["product.template"].create(
            {
                "name": "CKR HTTP Produit sans phrase",
                "type": "consu",
                "sale_ok": True,
                "website_published": True,
                "attribute_line_ids": [
                    (
                        0,
                        0,
                        {
                            "attribute_id": cls.attr_origin.id,
                            "value_ids": [(6, 0, [cls.val_no_phrase.id])],
                        },
                    )
                ],
            }
        )

    def _assert_redirect(self, path, expected_code, location_substr):
        resp = self.url_open(path, allow_redirects=False)
        self.assertEqual(
            resp.status_code,
            expected_code,
            "%s → attendu %s, obtenu %s"
            % (path, expected_code, resp.status_code),
        )
        loc = resp.headers.get("Location", "")
        self.assertIn(
            location_substr,
            loc,
            "Location inattendue pour %s : %r" % (path, loc),
        )

    def _canonical_href(self, html_text):
        m = re.search(
            r'<link[^>]+rel=["\']canonical["\'][^>]+href=["\']([^"\']+)["\']',
            html_text,
            re.I,
        )
        self.assertTrue(m, "Balise canonical absente.")
        return html.unescape(m.group(1))

    def test_pv_rc04_origines_alias_301(self):
        """RC-04 : ``/origines`` → 301 vers ``/shop?ckr_mode=origin``."""
        self._assert_redirect("/origines", 301, "ckr_mode=origin")

    def test_pv_rc05_origin_mode_alone_200_and_copy(self):
        """RC-05 : mode seul, 200, copy S2 catalogue complet."""
        resp = self.url_open("/shop?ckr_mode=origin", timeout=60)
        self.assertEqual(resp.status_code, 200)
        text = resp.text
        self.assertIn("Parcourez le catalogue par origine.", text)

    def test_pv_rc06_single_origin_with_context_phrase(self):
        """RC-06 : une origine avec phrase + filtre produits."""
        resp = self.url_open(
            "/shop?ckr_mode=origin&ckr_origin=guadeloupe", timeout=60
        )
        self.assertEqual(resp.status_code, 200)
        text = resp.text
        self.assertIn("Guadeloupe", text)
        self.assertIn("Une phrase de contexte PV.", text)
        self.assertIn(self.product_g.name, text)
        self.assertNotIn(self.product_m.name, text)

    def test_pv_rc07_single_origin_without_context_phrase(self):
        """RC-07 : repli « Produits issus de {name_visitor}. »."""
        resp = self.url_open(
            "/shop?ckr_mode=origin&ckr_origin=sans-phrase", timeout=60
        )
        self.assertEqual(resp.status_code, 200)
        text = resp.text
        self.assertIn("Nom visiteur sans phrase", text)
        self.assertIn("Produits issus de", text)

    def test_pv_rc08_multi_origins_or(self):
        """RC-08 : deux slugs, titre « Origines », phrase plurielle, OU produits."""
        resp = self.url_open(
            "/shop?ckr_mode=origin&ckr_origin=guadeloupe&ckr_origin=martinique",
            timeout=60,
        )
        self.assertEqual(resp.status_code, 200)
        text = resp.text
        self.assertIn("Produits issus des origines sélectionnées.", text)
        self.assertIn(self.product_g.name, text)
        self.assertIn(self.product_m.name, text)

    def test_pv_rc09_empty_state(self):
        """RC-09 : origine valide sans produit → bandeau empty + copy."""
        resp = self.url_open(
            "/shop?ckr_mode=origin&ckr_origin=origine-sans-produit",
            timeout=60,
        )
        self.assertEqual(resp.status_code, 200)
        text = resp.text
        self.assertIn("Aucun produit pour cette sélection.", text)
        self.assertIn("pas encore de produit disponible", text)
        self.assertIn("Voir tout le catalogue", text)
        self.assertIn('href="/shop"', text)
        self.assertIn("Parcourir les origines", text)
        self.assertIn("ckr_mode=origin", text)

    def test_pv_rc10_invalid_slug_302(self):
        """RC-10 : slug inconnu → 302 ``/shop`` nu."""
        self._assert_redirect(
            "/shop?ckr_mode=origin&ckr_origin=inexistant-slug-pv",
            302,
            "/shop",
        )
        resp = self.url_open(
            "/shop?ckr_mode=origin&ckr_origin=inexistant-slug-pv",
            allow_redirects=False,
        )
        loc = resp.headers.get("Location", "")
        parsed = urlparse(loc)
        self.assertEqual(parsed.path.rstrip("/") or "/", "/shop")
        self.assertFalse(parse_qs(parsed.query).get("ckr_mode"))
        self.assertFalse(parse_qs(parsed.query).get("ckr_origin"))

    def test_pv_rc11_canonical_sorted_slugs(self):
        """RC-11 : canonical dédupliqué + tri lexicographique."""
        resp = self.url_open(
            "/shop?ckr_mode=origin&ckr_origin=martinique&ckr_origin=guadeloupe"
            "&ckr_origin=martinique",
            timeout=60,
        )
        self.assertEqual(resp.status_code, 200)
        canon = self._canonical_href(resp.text)
        self.assertIn("ckr_mode=origin", canon)
        q = urlparse(canon).query
        origins = parse_qs(q).get("ckr_origin") or []
        self.assertEqual(origins, ["guadeloupe", "martinique"])

    def test_pv_rc12_product_page_origins_links(self):
        """RC-12 : bloc origines + liens ``/shop?ckr_origin=`` (facette seule)."""
        url = self.product_multi.website_url
        self.assertTrue(url.startswith("/"))
        resp = self.url_open(url, timeout=60)
        self.assertEqual(resp.status_code, 200)
        text = resp.text
        self.assertIn("ckr-product-origins", text)
        self.assertIn("/shop?ckr_origin=guadeloupe", text)
        self.assertIn("/shop?ckr_origin=martinique", text)

    def test_pv_rc13_regression_other_gates(self):
        """RC-13 : alias Kits / Promotions / Catégories / shop nu inchangés (301/200)."""
        self._assert_redirect("/kits", 301, "ckr_mode=pack")
        self._assert_redirect("/promotions", 301, "ckr_mode=promo")
        r_cat = self.url_open("/categories", allow_redirects=False)
        self.assertEqual(r_cat.status_code, 301)
        loc_cat = r_cat.headers.get("Location", "")
        self.assertIn("/shop", loc_cat)
        self.assertNotIn(
            "/shop/category/",
            loc_cat,
            "Doctrine conteneur : /categories ne doit pas cibler /shop/category/….",
        )
        r_shop = self.url_open("/shop", timeout=60)
        self.assertEqual(r_shop.status_code, 200)
