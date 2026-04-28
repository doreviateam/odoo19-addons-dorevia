# -*- coding: utf-8 -*-
"""Tests automatises legers - chantier HERO-HOMEPAGE-V2 (MVP2.1 1/5).

Periimetre : hero homepage immersif. Non-regression de l'ancre
``#explorer-catalogue`` sur la section Explorer (ticket Explorer MVP2
la requiert preservee).

References :
- docs/crea/TICKET_HERO_HOMEPAGE_V2.md
- docs/mvp_02/DECISION_HERO_HOMEPAGE_V2.md
- docs/direction/SPEC_HERO_HOMEPAGE.md Section 7 (cible MVP2.1)
- docs/crea/PV_RECETTE_HERO_HOMEPAGE_V2_CK.md Section 6

Statut : non bloquants (recette MOA visuelle reste le juge final) ;
vocation = garantir l'integrite structurelle du snippet et des
contrats de lien apres toute modification ulterieure.

Execution ciblee ::

    odoo -d <base> --test-enable --stop-after-init \\
        --test-tags=dorevia_ckr_hero
"""
from odoo.tests import tagged
from odoo.tests.common import HttpCase


@tagged("post_install", "-at_install", "dorevia_ckr_hero")
class TestCkrHeroHomepageV2(HttpCase):
    """Contrats visuels et non-regression ancre Explorer sur la homepage."""

    def _get_homepage_html(self):
        """Charge la homepage publique et retourne le corps HTML."""
        resp = self.url_open("/", timeout=60)
        self.assertEqual(
            resp.status_code,
            200,
            "La homepage '/' doit repondre 200 (non-regression globale).",
        )
        return resp.text

    def test_rc_hero_section_rendered_immersive(self):
        """La section hero immersive MVP2.1 est presente sur la homepage."""
        html_body = self._get_homepage_html()
        self.assertIn(
            "ckr-hero--immersive",
            html_body,
            "La classe 'ckr-hero--immersive' (variante MVP2.1) doit etre "
            "rendue sur la homepage. Regression possible du snippet "
            "ckr_snippet_hero ou retour au split V1.",
        )
        self.assertIn(
            'class="ckr-hero__media"',
            html_body,
            "Le conteneur media du hero immersif (fond + overlay) "
            "doit etre present.",
        )
        self.assertIn(
            "hero_v2_immersive.png",
            html_body,
            "L'asset de fond 'hero_v2_immersive.png' doit etre reference "
            "dans le snippet hero (source image MVP2.1).",
        )

    def test_rc_hero_cta_primary_shop_present(self):
        """CTA primaire : 'Decouvrir la selection' vers /shop."""
        html_body = self._get_homepage_html()
        self.assertIn(
            'href="/shop"',
            html_body,
            "Le CTA primaire du hero doit pointer vers /shop "
            "(voir TICKET_HERO_HOMEPAGE_V2 Section 3).",
        )
        self.assertIn(
            "Découvrir la sélection",
            html_body,
            "Le libelle du CTA primaire 'Decouvrir la selection' "
            "doit etre rendu (gel copy MVP2.1).",
        )

    def test_rc_hero_cta_secondary_origin_alias_present(self):
        """CTA secondaire : conteneur /shop (mode origine portail)."""
        html_body = self._get_homepage_html()
        self.assertIn(
            'href="/shop?ckr_mode=origin"',
            html_body,
            "Le CTA secondaire du hero doit rester sur /shop (doctrine conteneur unique).",
        )
        self.assertIn(
            "Explorer les origines",
            html_body,
            "Le libelle du CTA secondaire 'Explorer les origines' "
            "doit etre rendu (gel copy MVP2.1).",
        )

    def test_rc_hero_title_copy_present(self):
        """Titre hero MVP2.1 : copy MOA gelee."""
        html_body = self._get_homepage_html()
        self.assertIn(
            "Retrouvez les saveurs et savoir-faire créoles.",
            html_body,
            "Le titre hero MVP2.1 doit etre rendu (gel copy - "
            "TICKET_HERO_HOMEPAGE_V2 Section 3).",
        )

    def test_rc_non_regression_explorer_anchor_preserved(self):
        """L'ancre '#explorer-catalogue' reste presente sur la section
        Explorer (exigence du ticket EXPLORER-HOMEPAGE-MVP2). Le hero V2
        ne doit pas l'avoir supprimee en reorganisant la homepage."""
        html_body = self._get_homepage_html()
        self.assertIn(
            'id="explorer-catalogue"',
            html_body,
            "L'ancre 'id=\"explorer-catalogue\"' doit rester presente "
            "sur la section Explorer. Exigence du ticket EXPLORER-HOMEPAGE-"
            "MVP2 ; tout retrait doit passer par une revision MOA.",
        )
