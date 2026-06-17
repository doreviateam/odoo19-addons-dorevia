# -*- coding: utf-8 -*-
"""Tests curation BO Section 3 — vedettes pilotées par la catégorie 'Coups de cœur'."""

from odoo.tests import tagged
from odoo.tests.common import TransactionCase

from odoo.addons.dorevia_ck_marketone_content.home_featured import (
    FEATURED_CARD_CART_CTA,
    FEATURED_CARD_CTA,
    FEATURED_CATEGORY_NAME,
    FEATURED_GRID_MARKER,
    FEATURED_CATEGORY_XMLID,
    _ensure_featured_category,
    _get_featured_badge_html,
    _get_featured_commercial_line,
    _get_featured_display_name,
    _get_featured_labels_line,
    _patch_homepage_featured_arch,
    bootstrap_home_featured_products,
    build_featured_product_card_html,
    build_featured_ssr_arch,
    get_curated_featured_variants,
)

_TINY_PNG = (
    b'iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAIAAACQd1PeAAAADElEQVR4nGP4z8AAAAMBAQDJ/pLvAAAAAElFTkSuQmCC'
)


@tagged('post_install', '-at_install', 'dorevia_ck_marketone_home_section3_curation')
class TestCkHomeSection3Curation(TransactionCase):
    def _make_product(self, name, **vals):
        base = {
            'name': name,
            'is_published': True,
            'website_published': True,
            'sale_ok': True,
            'list_price': 1.0,
            'image_1920': _TINY_PNG,
        }
        base.update(vals)
        return self.env['product.template'].sudo().create(base)

    def _card_uom(self, code):
        return self.env.ref(f'dorevia_ck_marketone_content.ck_card_uom_{code}')

    def test_category_is_created(self):
        category = _ensure_featured_category(self.env)
        self.assertTrue(category)
        self.assertEqual(category.name, FEATURED_CATEGORY_NAME)
        self.assertEqual(self.env.ref(FEATURED_CATEGORY_XMLID), category)

    def test_category_lookup_uses_xmlid_after_rename(self):
        category = _ensure_featured_category(self.env)
        category.write({'name': 'Sélection vitrine'})
        product = self._make_product('CK Test Vedette XMLID', public_categ_ids=[(4, category.id)])
        self.assertIn(product.product_variant_id, get_curated_featured_variants(self.env))

    def test_only_categorised_products_are_featured(self):
        category = _ensure_featured_category(self.env)
        inside = self._make_product('CK Test Vedette IN', public_categ_ids=[(4, category.id)])
        outside = self._make_product('CK Test Vedette OUT')
        names = [_get_featured_display_name(v) for v in get_curated_featured_variants(self.env)]
        self.assertIn('CK Test Vedette IN', names)
        self.assertNotIn('CK Test Vedette OUT', names)
        self.assertIn(inside.product_variant_id, get_curated_featured_variants(self.env))
        self.assertNotIn(outside.product_variant_id, get_curated_featured_variants(self.env))

    def test_curated_order_follows_website_sequence(self):
        category = _ensure_featured_category(self.env)
        self._make_product('CK Vedette Seq A', website_sequence=30, public_categ_ids=[(4, category.id)])
        self._make_product('CK Vedette Seq B', website_sequence=10, public_categ_ids=[(4, category.id)])
        order = [_get_featured_display_name(v) for v in get_curated_featured_variants(self.env)]
        self.assertLess(order.index('CK Vedette Seq B'), order.index('CK Vedette Seq A'))

    def test_unpublished_categorised_product_is_excluded(self):
        category = _ensure_featured_category(self.env)
        self._make_product(
            'CK Vedette Masquée',
            is_published=False,
            website_published=False,
            public_categ_ids=[(4, category.id)],
        )
        names = [_get_featured_display_name(v) for v in get_curated_featured_variants(self.env)]
        self.assertNotIn('CK Vedette Masquée', names)

    def test_product_curation_write_refreshes_home_arch(self):
        category = _ensure_featured_category(self.env)
        product = self._make_product('CK Vedette Refresh')
        bootstrap_home_featured_products(self.env)
        product.write({'public_categ_ids': [(4, category.id)]})
        page = self.env['website.page'].sudo().search([('url', '=', '/')], limit=1)
        arch = page.view_id.arch_db or page.view_id.arch or ''
        self.assertIn(FEATURED_GRID_MARKER, arch)
        self.assertIn('CK Vedette Refresh', arch)

    def test_duplicate_featured_categories_are_merged(self):
        canonical = _ensure_featured_category(self.env)
        dupe = self.env['product.public.category'].sudo().create({
            'name': FEATURED_CATEGORY_NAME,
        })
        product = self._make_product('CK Vedette Dupe Cat', public_categ_ids=[(4, dupe.id)])
        merged = _ensure_featured_category(self.env)
        self.assertEqual(merged, canonical)
        self.assertNotIn(dupe.id, self.env['product.public.category'].sudo().search([]).ids)
        self.assertIn(canonical, product.public_categ_ids)
        self.assertIn(product.product_variant_id, get_curated_featured_variants(self.env))

    def test_bootstrap_replaces_featured_section_without_duplicating(self):
        category = _ensure_featured_category(self.env)
        for i in range(3):
            self._make_product(
                f'CK Vedette Dup {i}',
                website_sequence=i,
                public_categ_ids=[(4, category.id)],
            )
        page = self.env['website.page'].sudo().search([('url', '=', '/')], limit=1)
        arch = page.view_id.arch_db or page.view_id.arch or ''
        stale = build_featured_ssr_arch(['<article class="ck-product-card">stale</article>'])
        patched, ok = _patch_homepage_featured_arch(arch, stale)
        self.assertTrue(ok)
        page.view_id.sudo().write({'arch_db': patched})
        bootstrap_home_featured_products(self.env)
        final = page.view_id.arch_db or ''
        self.assertEqual(final.count('data-snippet="s_ck_featured_products"'), 1)

    def test_badge_comes_from_website_ribbon_id(self):
        ribbon = self.env['product.ribbon'].sudo().create({
            'name': 'Nouveau !',
            'bg_color': '#0275d8',
            'text_color': '#FFFFFF',
            'position': 'right',
            'style': 'tag',
            'assign': 'manual',
        })
        product = self._make_product('CK Vedette Badge', website_ribbon_id=ribbon.id)
        variant = product.product_variant_id
        badge = _get_featured_badge_html(variant)
        self.assertIn('Nouveau !', badge)
        self.assertIn('badge-float', badge)
        self.assertIn('badge-new', badge)

        website = self.env['website'].search([], limit=1)
        card = build_featured_product_card_html(self.env, website, variant)
        self.assertIn('badge-new badge-float', card)
        self.assertNotIn('Coup de cœur', card)

    def test_card_without_ribbon_has_no_badge(self):
        product = self._make_product('CK Vedette Sans Badge')
        website = self.env['website'].search([], limit=1)
        card = build_featured_product_card_html(self.env, website, product.product_variant_id)
        self.assertNotIn('badge-float', card)

    def test_removing_product_from_featured_category_refreshes_home(self):
        category = _ensure_featured_category(self.env)
        product = self._make_product('CK Vedette Remove Cat', public_categ_ids=[(4, category.id)])
        bootstrap_home_featured_products(self.env)
        page = self.env['website.page'].sudo().search([('url', '=', '/')], limit=1)
        self.assertIn('CK Vedette Remove Cat', page.view_id.arch_db or '')

        category.write({'product_tmpl_ids': [(3, product.id)]})
        arch = page.view_id.arch_db or ''
        self.assertNotIn('CK Vedette Remove Cat', arch)

    def test_product_uncategorise_refreshes_home(self):
        category = _ensure_featured_category(self.env)
        product = self._make_product('CK Vedette Remove Prod', public_categ_ids=[(4, category.id)])
        bootstrap_home_featured_products(self.env)
        page = self.env['website.page'].sudo().search([('url', '=', '/')], limit=1)
        self.assertIn('CK Vedette Remove Prod', page.view_id.arch_db or '')

        product.write({'public_categ_ids': [(3, category.id)]})
        arch = page.view_id.arch_db or ''
        self.assertNotIn('CK Vedette Remove Prod', arch)

    def test_curated_selection_is_capped_to_eight_cards(self):
        category = _ensure_featured_category(self.env)
        category.product_tmpl_ids.write({'public_categ_ids': [(3, category.id)]})
        for i in range(10):
            self._make_product(
                f'CK Vedette Cap {i:02d}',
                website_sequence=i,
                public_categ_ids=[(4, category.id)],
            )

        variants = get_curated_featured_variants(self.env)
        names = [_get_featured_display_name(v) for v in variants]
        self.assertEqual(len(variants), 8)
        self.assertIn('CK Vedette Cap 00', names)
        self.assertIn('CK Vedette Cap 07', names)
        self.assertNotIn('CK Vedette Cap 08', names)
        self.assertNotIn('CK Vedette Cap 09', names)

    def test_card_labels_are_joined_and_exclude_coups_de_coeur(self):
        guadeloupe = self.env['product.tag'].sudo().create({
            'name': 'Guadeloupe',
            'sequence': 10,
        })
        epicerie = self.env['product.tag'].sudo().create({
            'name': 'Épicerie',
            'sequence': 20,
        })
        excluded = self.env['product.tag'].sudo().create({
            'name': FEATURED_CATEGORY_NAME,
            'sequence': 5,
        })
        product = self._make_product(
            'CK Vedette Labels',
            product_tag_ids=[(6, 0, [guadeloupe.id, epicerie.id, excluded.id])],
        )
        line = _get_featured_labels_line(product)
        self.assertEqual(line, 'Guadeloupe · Épicerie')

        website = self.env['website'].search([], limit=1)
        card = build_featured_product_card_html(self.env, website, product.product_variant_id)
        self.assertIn('product-card-labels', card)
        self.assertIn('Guadeloupe · Épicerie', card)
        self.assertNotIn(FEATURED_CATEGORY_NAME, card)

    def test_card_labels_use_variant_additional_product_tags(self):
        category = _ensure_featured_category(self.env)
        martinique = self.env['product.tag'].sudo().create({
            'name': 'Martinique',
            'sequence': 15,
        })
        product = self._make_product(
            'CK Vedette Tags Variante',
            public_categ_ids=[(4, category.id)],
        )
        variant = product.product_variant_id
        variant.write({'additional_product_tag_ids': [(4, martinique.id)]})
        line = _get_featured_labels_line(product, variant)
        self.assertEqual(line, 'Martinique')

        website = self.env['website'].search([], limit=1)
        card = build_featured_product_card_html(self.env, website, variant)
        self.assertIn('Martinique', card)

    def test_card_net_quantity_and_reference_price(self):
        product = self._make_product(
            'CK Vedette Prix Ref',
            list_price=5.8,
            ck_net_quantity=320,
            ck_net_quantity_uom_id=self._card_uom('g').id,
            ck_reference_price_uom_id=self._card_uom('kg').id,
            ck_show_reference_price=True,
        )
        website = self.env['website'].search([], limit=1)
        variant = product.product_variant_id
        commercial = _get_featured_commercial_line(self.env, website, variant)
        self.assertIn('320 g', commercial)
        self.assertIn('/kg', commercial)
        self.assertIn('18,13', commercial)

        card = build_featured_product_card_html(self.env, website, variant)
        self.assertIn('reference-price', card)
        self.assertIn('320 g', card)

    def test_card_reference_price_uses_configurable_uom(self):
        custom_net = self.env['dorevia.ck.card.uom'].sudo().create({
            'name': 'gramme',
            'code': 'gramme_test',
            'family': 'mass',
            'ratio': 0.001,
            'use_for_net_quantity': True,
        })
        custom_ref = self.env['dorevia.ck.card.uom'].sudo().create({
            'name': 'kilo',
            'code': 'kilo_test',
            'family': 'mass',
            'ratio': 1.0,
            'use_for_reference_price': True,
        })
        product = self._make_product(
            'CK Vedette UOM Config',
            list_price=10.0,
            ck_net_quantity=500,
            ck_net_quantity_uom_id=custom_net.id,
            ck_reference_price_uom_id=custom_ref.id,
            ck_show_reference_price=True,
        )
        website = self.env['website'].search([], limit=1)
        variant = product.product_variant_id
        commercial = _get_featured_commercial_line(self.env, website, variant)
        self.assertIn('500 gramme', commercial)
        self.assertIn('/kilo', commercial)
        self.assertIn('20,00', commercial)

    def test_card_without_net_quantity_hides_commercial_line(self):
        product = self._make_product('CK Vedette Sans Qte')
        website = self.env['website'].search([], limit=1)
        card = build_featured_product_card_html(self.env, website, product.product_variant_id)
        self.assertNotIn('reference-price', card)

    def test_card_cta_is_voir_le_produit(self):
        product = self._make_product('CK Vedette CTA')
        website = self.env['website'].search([], limit=1)
        card = build_featured_product_card_html(self.env, website, product.product_variant_id)
        self.assertIn(FEATURED_CARD_CTA, card)
        self.assertIn(FEATURED_CARD_CART_CTA, card)
        self.assertIn('class="card-cart-cta"', card)
        self.assertIn('class="card-cta card-cta--secondary"', card)
        self.assertIn('ck-product-card__cover', card)
        self.assertNotIn('>Voir</a>', card)

    def test_card_hides_cart_cta_when_not_sale_ok(self):
        product = self._make_product('CK Vedette Pas Vente', sale_ok=False)
        website = self.env['website'].search([], limit=1)
        card = build_featured_product_card_html(self.env, website, product.product_variant_id)
        self.assertIn(FEATURED_CARD_CTA, card)
        self.assertNotIn('class="card-cart-cta"', card)
        self.assertIn('product-card-actions--view-only', card)

    def test_product_tags_write_refreshes_home_arch(self):
        category = _ensure_featured_category(self.env)
        tag = self.env['product.tag'].sudo().create({'name': 'Martinique'})
        product = self._make_product(
            'CK Vedette Tag Refresh',
            public_categ_ids=[(4, category.id)],
        )
        bootstrap_home_featured_products(self.env)
        product.write({'product_tag_ids': [(4, tag.id)]})
        page = self.env['website.page'].sudo().search([('url', '=', '/')], limit=1)
        arch = page.view_id.arch_db or ''
        self.assertIn('Martinique', arch)
        self.assertIn('product-card-labels', arch)

    def test_featured_card_fields_refresh_home_arch(self):
        category = _ensure_featured_category(self.env)
        product = self._make_product(
            'CK Vedette Card Fields',
            public_categ_ids=[(4, category.id)],
        )
        bootstrap_home_featured_products(self.env)
        tag = self.env['product.tag'].sudo().create({'name': 'Martinique'})
        product.write({
            'product_tag_ids': [(4, tag.id)],
            'ck_net_quantity': 250,
            'ck_net_quantity_uom_id': self._card_uom('g').id,
        })
        page = self.env['website.page'].sudo().search([('url', '=', '/')], limit=1)
        arch = page.view_id.arch_db or ''
        self.assertIn('Martinique', arch)
        self.assertIn('250 g', arch)

    def test_bootstrap_refreshes_stale_arch_without_product_labels(self):
        category = _ensure_featured_category(self.env)
        guadeloupe = self.env['product.tag'].sudo().create({
            'name': 'Guadeloupe',
            'sequence': 10,
        })
        epicerie = self.env['product.tag'].sudo().create({
            'name': 'Épicerie',
            'sequence': 20,
        })
        product = self._make_product(
            'CK Vedette Stale Labels',
            public_categ_ids=[(4, category.id)],
            product_tag_ids=[(6, 0, [guadeloupe.id, epicerie.id])],
        )
        bootstrap_home_featured_products(self.env)
        page = self.env['website.page'].sudo().search([('url', '=', '/')], limit=1)
        view = page.view_id.sudo()
        arch = view.arch_db or ''
        self.assertIn('product-card-labels', arch)

        stale_arch = arch.replace('product-card-labels', 'product-card-labels-stale')
        view.write({'arch_db': stale_arch})
        bootstrap_home_featured_products(self.env)
        arch = view.arch_db or ''
        self.assertIn('product-card-labels', arch)
        self.assertIn('Guadeloupe · Épicerie', arch)
        self.assertNotIn('product-card-labels-stale', arch)
