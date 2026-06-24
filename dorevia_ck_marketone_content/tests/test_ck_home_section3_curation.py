# -*- coding: utf-8 -*-
"""Tests Section 3 — vedettes homepage pilotées par ck_is_featured (En vedette)."""

from odoo.tests import tagged
from odoo.tests.common import TransactionCase

from odoo.addons.dorevia_ck_marketone_content.home_featured import (
    FEATURED_CARD_CART_CTA,
    FEATURED_CATEGORY_NAME,
    FEATURED_CURATED_MAX,
    FEATURED_GRID_MARKER,
    FEATURED_CATEGORY_XMLID,
    _ensure_featured_category,
    _get_featured_badge_html,
    _get_featured_card_metadata_line,
    _get_featured_commercial_line,
    _get_featured_display_name,
    _get_featured_labels_line,
    _get_featured_price_label,
    _patch_homepage_featured_arch,
    bootstrap_home_featured_products,
    build_featured_product_card_html,
    build_featured_ssr_arch,
    get_curated_featured_variants,
)

from odoo.addons.dorevia_ck_marketone_content.ck_product_placeholders import (
    CK_CREAM_PLACEHOLDER_PNG_B64,
)
from odoo.addons.dorevia_ck_marketone_content.tests.ck_home_lot2_utils import (
    clear_ck_is_featured,
)


@tagged('post_install', '-at_install', 'dorevia_ck_marketone_home_section3_curation')
class TestCkHomeSection3Curation(TransactionCase):
    def setUp(self):
        super().setUp()
        # Ticket Dev — FEATURED_CURATED_MAX=4 (au lieu de 8) : les produits
        # En vedette du catalogue seed peuvent désormais à eux seuls saturer
        # le cap, masquant les produits créés par chaque test. On repart
        # d'un état propre (rollback TransactionCase en fin de test, donc
        # sans effet sur la base réelle) plutôt que de dépendre du nombre de
        # vedettes déjà présentes en seed.
        clear_ck_is_featured(self.env)

    def _make_product(self, name, **vals):
        base = {
            'name': name,
            'is_published': True,
            'website_published': True,
            'sale_ok': True,
            'list_price': 1.0,
            'image_1920': CK_CREAM_PLACEHOLDER_PNG_B64,
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

    def test_ck_is_featured_lookup_after_category_rename(self):
        category = _ensure_featured_category(self.env)
        category.write({'name': 'Sélection vitrine'})
        product = self._make_product('CK Test Vedette XMLID', ck_is_featured=True)
        self.assertIn(product.product_variant_id, get_curated_featured_variants(self.env))

    def test_only_featured_products_are_selected(self):
        inside = self._make_product('CK Test Vedette IN', ck_is_featured=True)
        outside = self._make_product('CK Test Vedette OUT')
        names = [_get_featured_display_name(v) for v in get_curated_featured_variants(self.env)]
        self.assertIn('CK Test Vedette IN', names)
        self.assertNotIn('CK Test Vedette OUT', names)
        self.assertIn(inside.product_variant_id, get_curated_featured_variants(self.env))
        self.assertNotIn(outside.product_variant_id, get_curated_featured_variants(self.env))

    def test_curated_order_follows_website_sequence(self):
        self._make_product('CK Vedette Seq A', website_sequence=30, ck_is_featured=True)
        self._make_product('CK Vedette Seq B', website_sequence=10, ck_is_featured=True)
        order = [_get_featured_display_name(v) for v in get_curated_featured_variants(self.env)]
        self.assertLess(order.index('CK Vedette Seq B'), order.index('CK Vedette Seq A'))

    def test_unpublished_featured_product_is_excluded(self):
        self._make_product(
            'CK Vedette Masquée',
            is_published=False,
            website_published=False,
            ck_is_featured=True,
        )
        names = [_get_featured_display_name(v) for v in get_curated_featured_variants(self.env)]
        self.assertNotIn('CK Vedette Masquée', names)

    def test_featured_write_refreshes_home_arch(self):
        product = self._make_product('CK Vedette Refresh')
        bootstrap_home_featured_products(self.env)
        product.write({'ck_is_featured': True})
        page = self.env['website.page'].sudo().search([('url', '=', '/')], limit=1)
        arch = page.view_id.arch_db or page.view_id.arch or ''
        self.assertIn(FEATURED_GRID_MARKER, arch)
        self.assertIn('CK Vedette Refresh', arch)

    def test_duplicate_featured_categories_are_merged(self):
        canonical = _ensure_featured_category(self.env)
        dupe = self.env['product.public.category'].sudo().create({
            'name': FEATURED_CATEGORY_NAME,
        })
        product = self._make_product(
            'CK Vedette Dupe Cat',
            ck_is_featured=True,
            public_categ_ids=[(4, dupe.id)],
        )
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
                ck_is_featured=True,
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

    def test_unfeatured_write_refreshes_home(self):
        product = self._make_product('CK Vedette Remove Featured', ck_is_featured=True)
        bootstrap_home_featured_products(self.env)
        page = self.env['website.page'].sudo().search([('url', '=', '/')], limit=1)
        self.assertIn('CK Vedette Remove Featured', page.view_id.arch_db or '')

        product.write({'ck_is_featured': False})
        arch = page.view_id.arch_db or ''
        self.assertNotIn('CK Vedette Remove Featured', arch)

    def test_category_removal_does_not_unfeature_home(self):
        category = _ensure_featured_category(self.env)
        product = self._make_product('CK Vedette Remove Prod', ck_is_featured=True, public_categ_ids=[(4, category.id)])
        bootstrap_home_featured_products(self.env)
        page = self.env['website.page'].sudo().search([('url', '=', '/')], limit=1)
        self.assertIn('CK Vedette Remove Prod', page.view_id.arch_db or '')

        product.write({'public_categ_ids': [(3, category.id)]})
        bootstrap_home_featured_products(self.env)
        arch = page.view_id.arch_db or ''
        self.assertIn('CK Vedette Remove Prod', arch)

    def test_curated_selection_is_capped(self):
        Template = self.env['product.template'].sudo()
        Template.search([('ck_is_featured', '=', True)]).write({'ck_is_featured': False})
        for i in range(10):
            self._make_product(
                f'CK Vedette Cap {i:02d}',
                website_sequence=i,
                ck_is_featured=True,
            )

        variants = get_curated_featured_variants(self.env)
        names = [_get_featured_display_name(v) for v in variants]
        self.assertEqual(len(variants), FEATURED_CURATED_MAX)
        self.assertIn('CK Vedette Cap 00', names)
        self.assertIn(f'CK Vedette Cap {FEATURED_CURATED_MAX - 1:02d}', names)
        self.assertNotIn(f'CK Vedette Cap {FEATURED_CURATED_MAX:02d}', names)
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

    def test_card_metadata_line_joins_labels_format_and_reference(self):
        guadeloupe = self.env['product.tag'].sudo().create({
            'name': 'Guadeloupe',
            'sequence': 10,
        })
        epicerie = self.env['product.tag'].sudo().create({
            'name': 'Épicerie',
            'sequence': 20,
        })
        product = self._make_product(
            'CK Vedette Metadata',
            list_price=3.6,
            product_tag_ids=[(6, 0, [guadeloupe.id, epicerie.id])],
            ck_net_quantity=100,
            ck_net_quantity_uom_id=self._card_uom('g').id,
            ck_reference_price_uom_id=self._card_uom('kg').id,
            ck_show_reference_price=True,
        )
        website = self.env['website'].search([], limit=1)
        variant = product.product_variant_id
        metadata = _get_featured_card_metadata_line(self.env, website, variant)
        self.assertEqual(metadata, 'Guadeloupe · Épicerie · 100 g · 36,00\xa0€/kg')

        card = build_featured_product_card_html(self.env, website, variant)
        self.assertIn('product-card-labels', card)
        self.assertIn('Guadeloupe · Épicerie · 100 g', card)
        self.assertIn('36,00', card)
        self.assertNotIn('reference-price', card)

    def test_card_metadata_line_skips_orphan_separators(self):
        product = self._make_product(
            'CK Vedette Metadata Labels Only',
            product_tag_ids=[(6, 0, [self.env['product.tag'].sudo().create({
                'name': 'Réunion',
                'sequence': 1,
            }).id])],
        )
        website = self.env['website'].search([], limit=1)
        variant = product.product_variant_id
        metadata = _get_featured_card_metadata_line(self.env, website, variant)
        self.assertEqual(metadata, 'Réunion')
        self.assertNotIn(' ·  · ', metadata)

    def test_card_labels_use_variant_additional_product_tags(self):
        category = _ensure_featured_category(self.env)
        martinique = self.env['product.tag'].sudo().create({
            'name': 'Martinique',
            'sequence': 15,
        })
        product = self._make_product(
            'CK Vedette Tags Variante',
            ck_is_featured=True,
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
        self.assertIn('product-card-labels', card)
        self.assertIn('320 g', card)
        self.assertIn('/kg', card)
        self.assertIn('18,13', card)
        self.assertNotIn('reference-price', card)
        pricing_start = card.index('product-card-pricing')
        pricing_end = card.index('product-card-actions', pricing_start)
        pricing_block = card[pricing_start:pricing_end]
        self.assertNotIn('/kg', pricing_block)

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

    def test_card_variant_price_without_pricelist(self):
        """Chaque card multi-variantes affiche le lst_price de la variante vendue."""
        attr = self.env['product.attribute'].sudo().create({'name': 'Goût QA Prix'})
        val_a = self.env['product.attribute.value'].sudo().create({
            'name': 'Salé QA',
            'attribute_id': attr.id,
        })
        val_b = self.env['product.attribute.value'].sudo().create({
            'name': 'Sucré QA',
            'attribute_id': attr.id,
        })
        product = self.env['product.template'].sudo().create({
            'name': 'CK Crackers QA Prix',
            'is_published': True,
            'website_published': True,
            'sale_ok': True,
            'list_price': 3.5,
            'image_1920': CK_CREAM_PLACEHOLDER_PNG_B64,
            'attribute_line_ids': [(0, 0, {
                'attribute_id': attr.id,
                'value_ids': [(6, 0, [val_a.id, val_b.id])],
            })],
        })
        sale = product.product_variant_ids.filtered(
            lambda v: 'Salé QA' in (v.display_name or '')
        )[:1]
        sweet = product.product_variant_ids.filtered(
            lambda v: 'Sucré QA' in (v.display_name or '')
        )[:1]
        self.assertTrue(sale and sweet)
        sale_ptav = sale.product_template_attribute_value_ids[:1]
        sale_ptav.write({'price_extra': 0.1})
        sale.write({'image_1920': CK_CREAM_PLACEHOLDER_PNG_B64})
        sweet.write({'image_1920': CK_CREAM_PLACEHOLDER_PNG_B64})
        self.assertAlmostEqual(sale.lst_price, 3.6)
        self.assertAlmostEqual(sweet.lst_price, 3.5)
        website = self.env['website'].search([], limit=1)
        self.assertEqual(_get_featured_price_label(self.env, website, sale), '3,60\u00a0€')
        self.assertEqual(_get_featured_price_label(self.env, website, sweet), '3,50\u00a0€')

    def test_variant_lst_price_write_refreshes_home_arch(self):
        category = _ensure_featured_category(self.env)
        product = self._make_product(
            'CK Vedette Prix Variante',
            list_price=3.5,
            ck_is_featured=True,
        )
        bootstrap_home_featured_products(self.env)
        product.product_variant_id.write({'lst_price': 4.2})
        page = self.env['website.page'].sudo().search([('url', '=', '/')], limit=1)
        arch = page.view_id.arch_db or ''
        self.assertIn('4,20', arch)

    def test_bo_variant_list_price_write_refreshes_home_arch(self):
        """Chemin BO réel Odoo 19 : write list_price (pas lst_price dans vals)."""
        category = _ensure_featured_category(self.env)
        product = self._make_product(
            'CK Vedette List Price BO',
            list_price=3.5,
            ck_is_featured=True,
        )
        variant = product.product_variant_id
        bootstrap_home_featured_products(self.env)
        variant.write({'list_price': 4.75})
        page = self.env['website.page'].sudo().search([('url', '=', '/')], limit=1)
        arch = page.view_id.arch_db or ''
        self.assertIn('4,75', arch)

    def test_card_cta_is_add_to_cart_only(self):
        """Ticket Dev — seul "Ajouter au panier" en zone basse ; image et titre
        portent la navigation fiche produit (cover plein format + lien titre)."""
        product = self._make_product('CK Vedette CTA')
        website = self.env['website'].search([], limit=1)
        variant = product.product_variant_id
        card = build_featured_product_card_html(self.env, website, variant)
        href = variant.website_url or product.website_url or '/shop'
        self.assertIn(FEATURED_CARD_CART_CTA, card)
        self.assertIn('class="card-cart-cta"', card)
        self.assertNotIn('card-cta--secondary', card)
        self.assertNotIn('>Voir le produit</a>', card)
        self.assertIn('ck-product-card__cover', card)
        self.assertIn(f'<a href="{href}" class="ck-product-card__title-link">', card)

    def test_card_hides_cart_cta_when_not_sale_ok(self):
        """Pas d'ajout rapide possible → aucun CTA en zone basse (nav via image/titre)."""
        product = self._make_product('CK Vedette Pas Vente', sale_ok=False)
        website = self.env['website'].search([], limit=1)
        card = build_featured_product_card_html(self.env, website, product.product_variant_id)
        self.assertNotIn('class="card-cart-cta"', card)
        self.assertNotIn('card-cta--secondary', card)
        self.assertNotIn('product-card-actions', card)
        self.assertIn('ck-product-card__title-link', card)

    def test_product_tags_write_refreshes_home_arch(self):
        category = _ensure_featured_category(self.env)
        tag = self.env['product.tag'].sudo().create({'name': 'Martinique'})
        product = self._make_product(
            'CK Vedette Tag Refresh',
            ck_is_featured=True,
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
            ck_is_featured=True,
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
            ck_is_featured=True,
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
