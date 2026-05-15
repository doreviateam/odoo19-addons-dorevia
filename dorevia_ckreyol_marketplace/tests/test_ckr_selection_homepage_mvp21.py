# -*- coding: utf-8 -*-
"""Tests — chantier SELECTION-PRODUITS-HOMEPAGE-MVP21 (grille 4 produits)."""
import re

from odoo.tests import tagged
from odoo.tests.common import HttpCase, TransactionCase

# PNG 1×1 px (image obligatoire pour la résolution « 4 cartes avec visuel »).
_TINY_PNG_B64 = (
    "iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVR42mP8z8BQDwAEhQGAhKmMIQAAAABJRU5ErkJggg=="
)


@tagged("post_install", "-at_install", "dorevia_ckr_selection")
class TestCkrSelectionHomepageMvp21(HttpCase):
    """Catalogue publié : 4 emplacements site → homepage dynamique, sans panier."""

    def setUp(self):
        super().setUp()
        self.website = self.env.ref("website.default_website")
        Product = self.env["product.template"]
        base = {
            "type": "consu",
            "sale_ok": True,
            "website_published": True,
            "image_1920": _TINY_PNG_B64,
        }
        self.products = [
            Product.create(
                dict(base, name="CKR MVP21 Sel A", list_price=12.0)
            ),
            Product.create(
                dict(base, name="CKR MVP21 Sel B", list_price=15.5)
            ),
            Product.create(
                dict(base, name="CKR MVP21 Sel C", list_price=9.0)
            ),
            Product.create(
                dict(base, name="CKR MVP21 Sel D", list_price=7.0)
            ),
        ]
        self.website.write(
            {
                "ckr_homepage_featured_1": self.products[0].id,
                "ckr_homepage_featured_2": self.products[1].id,
                "ckr_homepage_featured_3": self.products[2].id,
                "ckr_homepage_featured_4": self.products[3].id,
            }
        )

    def _get_homepage_html(self):
        resp = self.url_open("/", timeout=60)
        self.assertEqual(resp.status_code, 200)
        return resp.text

    def test_rc_selection_grid_four_dynamic_products(self):
        """Quatre noms produits, images web, CTA fiche, pas de V1 packshot static."""
        html = self._get_homepage_html()
        start = html.find('class="ckr-section ckr-selection')
        self.assertNotEqual(start, -1, "Section Selection absente.")
        chunk = html[start : start + 50000]
        for p in self.products:
            self.assertIn(p.name, chunk, "Nom produit attendu : %s" % p.name)
        for pid in (p.id for p in self.products):
            self.assertIn(
                "/web/image/product.template/%s/image_512" % pid,
                chunk,
                "Image dynamique product.template requise.",
            )
        self.assertIn("Voir le produit", chunk)
        self.assertIn("Notre sélection du moment", chunk)
        self.assertIn("ckr-selection--band", chunk)
        # Regression V1 : plus de visuels packshot statiques sur ce bloc.
        self.assertNotIn("packshot_maniocookies.png", chunk)
        self.assertNotIn("Voir en boutique", chunk)
        # Ne pas utiliser substring : ckr-selection__card__* contient aussi « ckr-selection__card » (24 faux positifs pour 4 cartes).
        n_cards = len(re.findall(r'class\s*=\s*"ckr-selection__card"', chunk))
        self.assertEqual(n_cards, 4, "Quatre liens-carte produit attendus.")

    def test_rc_selection_not_add_to_cart_in_card(self):
        """Pas de bouton d’ajout panier dans le bloc ckr-selection (href shop produit seulement)."""
        html = self._get_homepage_html()
        # Zone minimale : entre debut section selection et CTA "Voir tous"
        start = html.find("ckr-selection__grid")
        self.assertNotEqual(start, -1)
        end = html.find("ckr-selection__cta", start)
        self.assertNotEqual(end, -1)
        zone = html[start:end]
        self.assertNotIn("a-submit", zone)
        self.assertNotIn("shop_cart", zone)


@tagged("post_install", "-at_install", "dorevia_ckr_selection")
class TestCkrSelectionHomepageMvp21Resolve(TransactionCase):
    """Règles BO + repli catalogue (sans requête HTTP)."""

    def test_resolved_featured_slot_without_listing_image_is_skipped(self):
        """Un emplacement BO sur produit sans binaire fiche/variante est ignoré ; le
        complément vient du pool catalogue (MVP2.1, docs 1_HOMEPAGE §3)."""
        website = self.env.ref("website.default_website")
        Product = self.env["product.template"]
        base = {
            "type": "consu",
            "sale_ok": True,
            "website_published": True,
        }
        bad = Product.create(dict(base, name="CKR MVP21 no img"))
        pick_a = Product.create(
            dict(base, name="CKR MVP21 pick A", image_1920=_TINY_PNG_B64)
        )
        pick_b = Product.create(
            dict(base, name="CKR MVP21 pick B", image_1920=_TINY_PNG_B64)
        )
        pick_c = Product.create(
            dict(base, name="CKR MVP21 pick C", image_1920=_TINY_PNG_B64)
        )
        # Quatrième fiche image pour alimenter le repli (si d’autres fiches
        # portent déjà l’e-commerce, le 4e slot reste un produit autorisé, pas
        # nécessairement ce record-ci).
        Product.create(
            dict(base, name="CKR MVP21 pick D pool", image_1920=_TINY_PNG_B64)
        )
        website.write(
            {
                "ckr_homepage_featured_1": bad.id,
                "ckr_homepage_featured_2": pick_a.id,
                "ckr_homepage_featured_3": pick_b.id,
                "ckr_homepage_featured_4": pick_c.id,
            }
        )
        out = website._get_ckr_homepage_resolved_featured_product_list()
        self.assertEqual(
            len(out),
            4,
            "Droit à quatre cartes avec visuel (dont 4e repli si besoin).",
        )
        out_ids = {p.id for p in out}
        self.assertNotIn(
            bad.id,
            out_ids,
            "Produit BO sans binaire visuel : ne doit pas apparaître en grille.",
        )
        for p in (pick_a, pick_b, pick_c):
            self.assertIn(
                p.id,
                out_ids,
                "Les fiches choisies en 2/3/4 doivent rester dans la sélection "
                "résolue — rec ID=%s" % p.id,
            )
        for p in out:
            self.assertTrue(
                p._ckr_has_homepage_listing_image(),
                "Chaque carte doit avoir un visuel (fiche ou variante) — rec ID=%s"
                % p.id,
            )
