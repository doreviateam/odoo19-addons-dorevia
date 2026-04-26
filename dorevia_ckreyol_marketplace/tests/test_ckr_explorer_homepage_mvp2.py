# -*- coding: utf-8 -*-
"""Tests - chantier EXPLORER-HOMEPAGE-MVP2 (grille asymétrique Bloc 3).

Reference :
- docs/mvp_02/DECISION_EXPLORER_HOMEPAGE_MVP2.md
- docs/crea/TICKET_EXPLORER_HOMEPAGE_MVP2.md

Execution ciblee ::

    odoo -d <base> --test-enable --stop-after-init \\
        --test-tags=dorevia_ckr_explorer
"""
from odoo.tests import tagged
from odoo.tests.common import HttpCase


@tagged("post_install", "-at_install", "dorevia_ckr_explorer")
class TestCkrExplorerHomepageMvp2(HttpCase):
    """Grille Explorer : structure, ordre des href, ancre #explorer-catalogue."""

    def _get_homepage_html(self):
        resp = self.url_open("/", timeout=60)
        self.assertEqual(resp.status_code, 200, "La homepage '/' doit repondre 200.")
        return resp.text

    def test_rc_explorer_grid_not_carousel(self):
        """Le rail V1 (carrousel + nav) est remplace par la grille MVP2."""
        html = self._get_homepage_html()
        self.assertIn('class="ckr-entries__grid"', html)
        self.assertNotIn("ckr-entries__carousel", html)
        self.assertNotIn("ckr-entries__nav--prev", html)

    def test_rc_explorer_href_order_mvp2(self):
        """Ordre des portes dans le bloc Explorer : P -> K -> C -> Co -> O."""
        html = self._get_homepage_html()
        start = html.find('id="explorer-catalogue"')
        self.assertNotEqual(start, -1, "Section Explorer presente.")
        chunk = html[start : start + 20000]
        p = chunk.find('href="/promotions"')
        k = chunk.find('href="/kits"')
        c = chunk.find('href="/categories"')
        co = chunk.find('href="/collections"')
        o = chunk.find('href="/origines"')
        for name, pos in (("promotions", p), ("kits", k), ("categories", c),
                          ("collections", co), ("origines", o)):
            self.assertNotEqual(
                pos, -1, "Lien %s manquant dans le bloc Explorer." % name
            )
        self.assertLess(p, k)
        self.assertLess(k, c)
        self.assertLess(c, co)
        self.assertLess(co, o)

    def test_rc_explorer_dominant_and_secondary_classes(self):
        """Classes de hierarchie : dominante, secondaire fort, tuiles."""
        html = self._get_homepage_html()
        self.assertIn("ckr-entries__card--promo", html)
        self.assertIn("ckr-entries__card--kits", html)
        self.assertIn("ckr-entries__card--tile", html)
        self.assertIn("ckr-entries__card__media", html)
        self.assertIn("ckr-entries__card__body", html)

    def test_rc_explorer_porte_images_static(self):
        """Cinq visuels servis depuis static (sources docs/assets mvp02)."""
        html = self._get_homepage_html()
        for fname in (
            "explorer_porte_promotions.png",
            "explorer_porte_kits.png",
            "explorer_porte_categories.png",
            "explorer_porte_collections.png",
            "explorer_porte_origines.png",
        ):
            self.assertIn(fname, html, "Image Explorer attendue : %s" % fname)
