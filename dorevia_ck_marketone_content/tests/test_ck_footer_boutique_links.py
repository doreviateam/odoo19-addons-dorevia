# -*- coding: utf-8 -*-
"""CATALOG-ARCHI-001 Lot A §12.3 — bootstrap_footer_boutique_links."""

from odoo.tests import tagged
from odoo.tests.common import TransactionCase

from odoo.addons.dorevia_ck_marketone_content.footer_boutique import (
    FOOTER_BOUTIQUE_MARKER,
    bootstrap_footer_boutique_links,
)


def _arch_str(footer):
    arch = footer.arch_db or footer.arch or ''
    if isinstance(arch, dict):
        arch = next(iter(arch.values()), '')
    return arch


@tagged('post_install', '-at_install', 'dorevia_ck_footer_boutique')
class TestCkFooterBoutiqueLinks(TransactionCase):

    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.website = cls.env['website'].search([], limit=1)
        assert cls.website, 'Un website doit exister pour tester le footer'
        cls.footer = cls.env['ir.ui.view'].sudo().search([
            ('key', '=', 'website.footer_custom'),
        ], limit=1)
        assert cls.footer, 'La vue website.footer_custom doit exister'

        cls.Category = cls.env['product.public.category'].sudo()
        cls.Product = cls.env['product.template'].sudo()

    def setUp(self):
        super().setUp()
        # NB : website.footer_custom est une vue d'héritage (inherit_id sur
        # website.layout, mode extension) — un root arbitraire (ex. <div>)
        # n'est pas "localisable dans la vue parente" lors du write() et lève
        # une ValidationError. <footer> comme root fonctionne (même convention
        # que test_ck_footer_legal_links.py) : vérifié empiriquement.
        self.base_arch = (
            '<footer>'
            + FOOTER_BOUTIQUE_MARKER
            + '<ul class="list-unstyled mb-0">'
            + '<li class="mb-2"><a href="/shop">Tous les produits</a></li>'
            + '</ul></footer>'
        )
        self.footer.write({'arch': self.base_arch})

    def _make_exposable_category(self, name):
        cat = self.Category.create({'name': name, 'sequence': 960})
        for idx in range(3):
            self.Product.create({
                'name': f'{name} Produit {idx}',
                'sale_ok': True,
                'is_published': True,
                'website_published': True,
                'public_categ_ids': [(4, cat.id)],
            })
        return cat

    def test_toujours_le_lien_tous_les_produits(self):
        result = bootstrap_footer_boutique_links(self.env)
        self.assertTrue(result)
        arch = _arch_str(self.footer)
        self.assertIn('href="/shop"', arch)
        self.assertIn('Tous les produits', arch)

    def test_categorie_exposable_ajoutee(self):
        cat = self._make_exposable_category('TestCat Footer Expo Ajoutee')
        result = bootstrap_footer_boutique_links(self.env)
        self.assertTrue(result)
        arch = _arch_str(self.footer)
        self.assertIn(cat.name, arch)

    def test_categorie_non_exposable_absente(self):
        cat = self.Category.create({'name': 'TestCat Footer Non Expo', 'sequence': 961})
        self.Product.create({
            'name': 'TestCat Footer Non Expo Produit unique',
            'sale_ok': True,
            'is_published': True,
            'website_published': True,
            'public_categ_ids': [(4, cat.id)],
        })
        bootstrap_footer_boutique_links(self.env)
        arch = _arch_str(self.footer)
        self.assertNotIn(cat.name, arch)

    def test_idempotent_double_appel(self):
        cat = self._make_exposable_category('TestCat Footer Expo Idempotent')
        bootstrap_footer_boutique_links(self.env)
        arch_after_first = _arch_str(self.footer)
        bootstrap_footer_boutique_links(self.env)
        arch_after_second = _arch_str(self.footer)
        self.assertEqual(arch_after_first.count(cat.name), 1)
        self.assertEqual(arch_after_second.count(cat.name), 1)

    def test_retourne_false_sans_marqueur_boutique(self):
        self.footer.write({'arch': '<div>Pas de colonne Boutique ici.</div>'})
        result = bootstrap_footer_boutique_links(self.env)
        self.assertFalse(result)
