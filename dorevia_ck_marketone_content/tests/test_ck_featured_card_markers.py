# -*- coding: utf-8 -*-
"""Verrou de durcissement — regex de détection des cards vedettes.

Les regex de validité / péremption sont token-based, ancrées sur les classes BEM
(``ck-product-card__*``). Ce test garantit qu'elles restent fonctionnelles :
- avec le HTML dual actuel (BEM + alias legacy ``product-card-*``) ;
- avec un futur HTML BEM-only (alias retirés) ;
- avec des classes réordonnées ;
et qu'elles n'introduisent pas de faux positif entre ``card-cta`` et
``card-cart-cta``. Si quelqu'un retire les alias sans adapter le pattern, ce test
vire au rouge plutôt que de laisser la détection cron devenir silencieusement aveugle.
"""

from odoo.tests import tagged
from odoo.tests.common import TransactionCase

from odoo.addons.dorevia_ck_marketone_content.home_featured import (
    _CARD_CART_CTA_RE,
    _CARD_COVER_RE,
    _CARD_LINK_RE,
    _CARD_META_TEXT_RE,
    _CARD_PRICE_TEXT_RE,
    _CARD_TITLE_TEXT_RE,
    _FEATURED_LABELS_BLOCK_RE,
)


@tagged('post_install', '-at_install', 'dorevia_ck_marketone_card_markers')
class TestCkFeaturedCardMarkers(TransactionCase):
    def test_title_dual_bem_only_and_reordered(self):
        for html in (
            '<h3 class="ck-product-card__title product-card-title">Manio Sucré</h3>',  # dual actuel
            '<h3 class="ck-product-card__title">Manio Sucré</h3>',                     # BEM-only (futur)
            '<h3 class="product-card-title ck-product-card__title">Manio Sucré</h3>',  # réordonné
        ):
            match = _CARD_TITLE_TEXT_RE.search(html)
            self.assertTrue(match, html)
            self.assertEqual(match.group(1), 'Manio Sucré')

    def test_price_dual_and_bem_only(self):
        for html in (
            '<span class="ck-product-card__price-value price">5,00 €</span>',
            '<span class="ck-product-card__price-value">5,00 €</span>',
        ):
            match = _CARD_PRICE_TEXT_RE.search(html)
            self.assertTrue(match, html)
            self.assertEqual(match.group(1), '5,00 €')

    def test_meta_and_labels_block_dual_and_bem_only(self):
        for html in (
            '<p class="ck-product-card__meta product-card-labels">Épicerie · Guadeloupe</p>',
            '<p class="ck-product-card__meta">Épicerie · Guadeloupe</p>',
        ):
            self.assertTrue(_CARD_META_TEXT_RE.search(html), html)
            self.assertTrue(_FEATURED_LABELS_BLOCK_RE.search(html), html)

    def test_cta_and_cover_present(self):
        self.assertTrue(_CARD_LINK_RE.search('<a class="card-cta card-cta--secondary">x</a>'))
        self.assertTrue(_CARD_LINK_RE.search('<a class="card-cta">x</a>'))
        self.assertTrue(_CARD_CART_CTA_RE.search('<button class="card-cart-cta">x</button>'))
        self.assertTrue(_CARD_COVER_RE.search('<a class="ck-product-card__cover"></a>'))

    def test_no_false_positive_between_cta_tokens(self):
        # ``card-cta`` ne doit PAS matcher ``card-cart-cta``…
        self.assertFalse(_CARD_LINK_RE.search('<button class="card-cart-cta">x</button>'))
        # …ni ``card-cart-cta`` matcher la variante secondaire ``card-cta--secondary``.
        self.assertFalse(_CARD_CART_CTA_RE.search('<a class="card-cta card-cta--secondary">x</a>'))
