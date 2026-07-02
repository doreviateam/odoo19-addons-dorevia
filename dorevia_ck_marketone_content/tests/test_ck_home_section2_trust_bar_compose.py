# -*- coding: utf-8 -*-
"""Tests HTTP Section 2 — trust-bar réassurance post-Hero."""

from odoo.tests import tagged
from odoo.tests.common import HttpCase

from odoo.addons.dorevia_ck_marketone_content.home_dual_engage import bootstrap_home_dual_engage
from odoo.addons.dorevia_ck_marketone_content.home_editorial import bootstrap_home_editorial
from odoo.addons.dorevia_ck_marketone_content.home_hero import HERO_VARIANT_MARKER, bootstrap_home_hero
from odoo.addons.dorevia_ck_marketone_content.home_reassurance import (
    FEATURED_MARKER,
    REASSURANCE_TRUST_BAR_MARKER,
    TRUST_BAR_COPY_MARKER,
    bootstrap_home_reassurance,
)
from odoo.addons.dorevia_ck_marketone_content.hooks import (
    bootstrap_home_discovery_pack,
    bootstrap_home_featured_products,
)


@tagged('post_install', '-at_install', 'dorevia_ck_marketone_home_section2')
class TestCkHomeSection2TrustBarCompose(HttpCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        bootstrap_home_hero(cls.env)
        bootstrap_home_reassurance(cls.env)
        bootstrap_home_featured_products(cls.env)
        bootstrap_home_discovery_pack(cls.env)
        bootstrap_home_dual_engage(cls.env)
        bootstrap_home_editorial(cls.env)

    def test_home_trust_bar_present(self):
        html = self.url_open('/').text
        self.assertIn(REASSURANCE_TRUST_BAR_MARKER, html)
        self.assertIn('Livraison France', html)
        self.assertIn('Europe', html)
        self.assertIn('Paiement sécurisé', html)
        self.assertIn(TRUST_BAR_COPY_MARKER, html)
        self.assertNotIn('conditions Pro sur qualification', html)

    def test_home_trust_bar_after_hero_before_featured(self):
        html = self.url_open('/').text
        self.assertLess(html.find(HERO_VARIANT_MARKER), html.find(REASSURANCE_TRUST_BAR_MARKER))
        self.assertLess(html.find(REASSURANCE_TRUST_BAR_MARKER), html.find(FEATURED_MARKER))

    def test_home_lot1_to_lot5_non_regression(self):
        html = self.url_open('/').text
        self.assertIn('data-bs-interval="25000"', html)
        self.assertIn('ck-featured-products__grid--stable', html)
        self.assertIn('ck-discovery-pack', html)
        self.assertIn('ck-dual-engage--pro-only', html)
        self.assertIn('ck-home-editorial', html)
