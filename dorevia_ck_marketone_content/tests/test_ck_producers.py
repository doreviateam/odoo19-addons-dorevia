# -*- coding: utf-8 -*-
"""Tests Sprint Producteurs CK V1 — modèle, routes, 301, 404, chips."""

from odoo.tests import tagged
from odoo.tests.common import HttpCase, TransactionCase

from odoo.addons.dorevia_ck_marketone_content.ck_product_placeholders import (
    CK_CREAM_PLACEHOLDER_PNG_B64,
)


# ---------------------------------------------------------------------------
# Helpers de fixtures partagés
# ---------------------------------------------------------------------------

def _make_producer(env, name='Distillerie Test', **kwargs):
    vals = {'name': name, 'ck_is_producer': True}
    vals.update(kwargs)
    return env['res.partner'].sudo().create(vals)


def _make_product(env, producer, name='Produit Test', published=True, sale_ok=True):
    return env['product.template'].sudo().create({
        'name': name,
        'type': 'consu',
        'list_price': 5.0,
        'sale_ok': sale_ok,
        'is_published': published,
        'ck_producer_id': producer.id,
    })


# ---------------------------------------------------------------------------
# Tests modèle (TransactionCase)
# ---------------------------------------------------------------------------

@tagged('post_install', '-at_install', 'dorevia_ck_producers_v1')
class TestCkProducersModel(TransactionCase):
    """Logique slug URL et filtrage produits publiés."""

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.producer = _make_producer(cls.env, name='SARL La Platine')

    def test_get_ck_producer_url_format(self):
        """L'URL canonique est /producteur/{slug}-{id}."""
        url = self.producer.get_ck_producer_url()
        self.assertTrue(url.startswith('/producteur/'))
        self.assertTrue(url.endswith(f'-{self.producer.id}'))
        self.assertIn('sarl-la-platine', url)

    def test_get_ck_producer_image_url(self):
        """URL image publique via route CK dédiée."""
        self.producer.ck_producer_website_image = CK_CREAM_PLACEHOLDER_PNG_B64
        url = self.producer.get_ck_producer_image_url('image_512')
        self.assertEqual(url, f'/ck/producteur/{self.producer.id}/image/image_512')

    def test_get_ck_producer_image_url_empty_without_image(self):
        """Sans ck_producer_website_image, pas d'URL image."""
        self.assertEqual(self.producer.get_ck_producer_image_url(), '')

    def test_producer_website_image_independent_from_logo(self):
        """Logo contact et photo site web sont des champs distincts."""
        self.producer.image_1920 = CK_CREAM_PLACEHOLDER_PNG_B64
        self.assertFalse(self.producer.ck_producer_website_image)
        self.assertEqual(self.producer.get_ck_producer_image_url(), '')

    def test_get_ck_producer_url_contains_id_suffix(self):
        """L'ID extrait du suffixe correspond bien au partner.id."""
        url = self.producer.get_ck_producer_url()
        extracted_id = int(url.rsplit('-', 1)[-1])
        self.assertEqual(extracted_id, self.producer.id)

    def test_get_ck_producer_products_returns_published(self):
        """Seuls les produits publiés et vendables sont retournés."""
        published = _make_product(self.env, self.producer, name='Publié', published=True)
        _make_product(self.env, self.producer, name='Non publié', published=False)
        products = self.producer.get_ck_producer_products()
        self.assertIn(published, products)

    def test_get_ck_producer_products_excludes_unpublished(self):
        """Les produits non publiés sont exclus."""
        _make_product(self.env, self.producer, name='Brouillon exclu', published=False)
        products = self.producer.get_ck_producer_products()
        for p in products:
            self.assertTrue(p.is_published)

    def test_get_ck_producer_products_excludes_not_for_sale(self):
        """Les produits avec sale_ok=False sont exclus."""
        _make_product(self.env, self.producer, name='Non vendable', published=True, sale_ok=False)
        products = self.producer.get_ck_producer_products()
        for p in products:
            self.assertTrue(p.sale_ok)

    def test_chips_producer_url_present_when_ck_is_producer(self):
        """get_ck_product_page_chips() inclut producer_url quand ck_is_producer=True."""
        product = _make_product(self.env, self.producer, name='Chips URL test')
        chips = product.get_ck_product_page_chips()
        producer_chips = [c for c in chips if c.get('name') == 'SARL La Platine']
        self.assertTrue(producer_chips, 'Chip producteur absent')
        self.assertIsNotNone(producer_chips[0].get('producer_url'))
        self.assertIn('/producteur/', producer_chips[0]['producer_url'])

    def test_chips_no_producer_url_when_not_ck_is_producer(self):
        """producer_url est None si le partenaire n'est pas marqué ck_is_producer."""
        non_producer = self.env['res.partner'].sudo().create({
            'name': 'Simple Fournisseur',
            'ck_is_producer': False,
        })
        product = self.env['product.template'].sudo().create({
            'name': 'Chips sans URL',
            'type': 'consu',
            'list_price': 5.0,
            'sale_ok': True,
            'ck_producer_id': non_producer.id,
        })
        chips = product.get_ck_product_page_chips()
        producer_chips = [c for c in chips if c.get('name') == 'Simple Fournisseur']
        self.assertTrue(producer_chips)
        self.assertIsNone(producer_chips[0].get('producer_url'))

    def test_chips_no_producer_chip_without_producer_id(self):
        """Sans ck_producer_id, aucun chip n'a producer_url."""
        product = self.env['product.template'].sudo().create({
            'name': 'Chips sans producteur',
            'type': 'consu',
            'list_price': 5.0,
            'sale_ok': True,
        })
        chips = product.get_ck_product_page_chips()
        chips_with_url = [c for c in chips if c.get('producer_url')]
        self.assertFalse(chips_with_url)


# ---------------------------------------------------------------------------
# Tests HTTP (HttpCase)
# ---------------------------------------------------------------------------

@tagged('post_install', '-at_install', 'dorevia_ck_producers_v1')
class TestCkProducersHttp(HttpCase):
    """Routes /producteurs et /producteur/<slug> — recette D/E/F."""

    FR_HEADERS = {'Accept-Language': 'fr-FR,fr;q=0.9'}

    def _get(self, url, allow_redirects=True):
        return self.url_open(url, headers=self.FR_HEADERS, allow_redirects=allow_redirects)

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.producer = cls.env['res.partner'].sudo().create({
            'name': 'SARL La Platine',
            'ck_is_producer': True,
            'ck_producer_location_label': 'Guadeloupe',
            'ck_producer_short_description': 'Rhums et sirops artisanaux.',
            'ck_producer_website_image': CK_CREAM_PLACEHOLDER_PNG_B64,
        })
        cls.product = cls.env['product.template'].sudo().create({
            'name': 'Rhum Vieux 7 ans',
            'type': 'consu',
            'list_price': 29.9,
            'sale_ok': True,
            'is_published': True,
            'ck_producer_id': cls.producer.id,
        })

    # --- A/B — Liste et fiche ------------------------------------------------

    def test_producers_list_200(self):
        """GET /producteurs → 200 pour visiteur anonyme."""
        resp = self._get('/producteurs')
        self.assertEqual(resp.status_code, 200)

    def test_producers_list_contains_producer_name(self):
        """Le nom du producteur est présent sur la page liste."""
        html = self._get('/producteurs').text
        self.assertIn('SARL La Platine', html)

    def test_producers_list_uses_ck_image_route(self):
        """La liste utilise la route image publique CK, pas /web/image/res.partner."""
        html = self._get('/producteurs').text
        self.assertIn(f'/ck/producteur/{self.producer.id}/image/image_512', html)
        self.assertNotIn(f'/web/image/res.partner/{self.producer.id}/image_512', html)

    def test_producer_image_public_route_200(self):
        """GET /ck/producteur/<id>/image/image_512 → image réelle (pas placeholder Odoo)."""
        url = self.producer.get_ck_producer_image_url('image_512')
        resp = self._get(url)
        self.assertEqual(resp.status_code, 200)
        self.assertTrue(resp.headers.get('Content-Type', '').startswith('image/'))
        self.assertNotIn('placeholder.png', resp.headers.get('Content-Disposition', ''))
        self.assertGreater(len(resp.content), 50)

    def test_producers_list_contains_location(self):
        """Le libellé géographique est présent sur la page liste."""
        html = self._get('/producteurs').text
        self.assertIn('Guadeloupe', html)

    def test_producer_detail_200(self):
        """GET /producteur/<slug> → 200 pour le producteur existant."""
        resp = self._get(self.producer.get_ck_producer_url())
        self.assertEqual(resp.status_code, 200)

    def test_producer_detail_shows_name(self):
        """Le nom du producteur est affiché sur la fiche."""
        html = self._get(self.producer.get_ck_producer_url()).text
        self.assertIn('SARL La Platine', html)

    def test_producer_detail_shows_location(self):
        """Le libellé géographique est affiché sur la fiche."""
        html = self._get(self.producer.get_ck_producer_url()).text
        self.assertIn('Guadeloupe', html)

    def test_producer_detail_shows_short_description(self):
        """L'accroche courte est affichée sur la fiche."""
        html = self._get(self.producer.get_ck_producer_url()).text
        self.assertIn('Rhums et sirops artisanaux.', html)

    def test_producer_detail_shows_product(self):
        """Le produit publié lié apparaît dans la grille produits de la fiche."""
        html = self._get(self.producer.get_ck_producer_url()).text
        self.assertIn('Rhum Vieux 7 ans', html)

    def test_producer_detail_back_link(self):
        """Le lien retour vers /producteurs est présent."""
        html = self._get(self.producer.get_ck_producer_url()).text
        self.assertIn('href="/producteurs"', html)

    # --- D — Slug et 404 -----------------------------------------------------

    def test_301_nos_producteurs_legacy_redirect(self):
        """Ancienne URL CMS /nos-producteurs → 301 vers /producteurs."""
        resp = self._get('/nos-producteurs', allow_redirects=False)
        self.assertEqual(resp.status_code, 301)
        location = resp.headers.get('Location', '')
        self.assertIn('/producteurs', location)

    def test_301_canonical_redirect_on_wrong_slug(self):
        """Un slug incorrect avec le bon ID → 301 vers le slug canonique."""
        canonical_url = self.producer.get_ck_producer_url()
        wrong_url = f'/producteur/ancien-nom-{self.producer.id}'
        resp = self._get(wrong_url, allow_redirects=False)
        self.assertEqual(resp.status_code, 301)
        location = resp.headers.get('Location', '')
        self.assertIn(canonical_url, location)

    def test_404_invalid_id(self):
        """Slug avec ID inexistant → 404."""
        resp = self._get('/producteur/producteur-fantome-999999999')
        self.assertEqual(resp.status_code, 404)

    def test_404_non_integer_id(self):
        """Slug sans ID entier au suffixe → 404."""
        resp = self._get('/producteur/slug-sans-id')
        self.assertEqual(resp.status_code, 404)

    def test_404_non_producer_partner(self):
        """Partenaire existant mais non ck_is_producer → 404."""
        non_producer = self.env['res.partner'].sudo().create({
            'name': 'Fournisseur Non Producteur',
            'ck_is_producer': False,
        })
        url = f'/producteur/fournisseur-non-producteur-{non_producer.id}'
        resp = self._get(url)
        self.assertEqual(resp.status_code, 404)

    # --- F — Régression Chips-U2 ---------------------------------------------

    def test_chip_links_to_producer_when_ck_is_producer(self):
        """Le chip producteur sur la fiche produit est un lien vers la fiche producteur."""
        html = self._get(self.product.website_url).text
        canonical_url = self.producer.get_ck_producer_url()
        self.assertIn(f'href="{canonical_url}"', html)
        self.assertIn('SARL La Platine', html)

    def test_chip_no_producer_link_without_producer(self):
        """Fiche produit sans ck_producer_id : aucun lien vers /producteur/."""
        product_no_producer = self.env['product.template'].sudo().create({
            'name': 'Produit Sans Producteur',
            'type': 'consu',
            'list_price': 3.0,
            'sale_ok': True,
            'is_published': True,
        })
        html = self._get(product_no_producer.website_url).text
        self.assertNotIn('/producteur/', html)
