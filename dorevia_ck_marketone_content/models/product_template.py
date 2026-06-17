# -*- coding: utf-8 -*-
import logging

from odoo import api, fields, models, tools

_logger = logging.getLogger(__name__)


FEATURED_REFRESH_FIELDS = {
    'name',
    'public_categ_ids',
    'is_published',
    'website_published',
    'website_sequence',
    'website_ribbon_id',
    'sale_ok',
    'list_price',
    'image_1920',
    'image_512',
    'product_tag_ids',
    'ck_net_quantity',
    'ck_net_quantity_uom_id',
    'ck_reference_price_uom_id',
    'ck_show_reference_price',
}


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    ck_net_quantity = fields.Float(
        string='Quantité nette',
        default=None,
        help='Quantité nette affichée sur la card home (ex. 320 g). Laisser vide si non applicable.',
    )
    ck_net_quantity_uom_id = fields.Many2one(
        comodel_name='dorevia.ck.card.uom',
        string='Unité de quantité nette',
        domain="[('use_for_net_quantity', '=', True), ('active', '=', True)]",
        ondelete='restrict',
    )
    ck_reference_price_uom_id = fields.Many2one(
        comodel_name='dorevia.ck.card.uom',
        string='Unité du prix de référence',
        domain="[('use_for_reference_price', '=', True), ('active', '=', True)]",
        ondelete='restrict',
    )
    ck_show_reference_price = fields.Boolean(
        string='Afficher le prix au kg / litre',
        default=True,
        help='Calcule et affiche le prix de référence sur la card home lorsque la quantité nette est renseignée.',
    )

    def _ck_refresh_home_featured_products(self):
        from odoo.addons.dorevia_ck_marketone_content.home_featured import (
            refresh_home_featured_products,
        )

        refresh_home_featured_products(self.env)

    def _ck_touches_featured(self):
        """QA M1 : limite la reconstruction vedettes aux produits réellement concernés.

        En mode curation (catégorie « Coups de cœur » présente), seul un produit
        rangé dans cette catégorie justifie un rebuild de la home. En mode repli
        (pas de curation → sélection automatique), tout produit publié peut
        entrer dans le top : on conserve le comportement large d'origine.
        """
        from odoo.addons.dorevia_ck_marketone_content.home_featured import (
            FEATURED_CATEGORY_XMLID,
        )

        featured = self.env.ref(FEATURED_CATEGORY_XMLID, raise_if_not_found=False)
        # Curation active seulement si la catégorie existe ET contient des produits ;
        # sinon mode repli auto-sélection → tout produit publié peut entrer → refresh large.
        if featured and featured.product_tmpl_ids:
            return bool(self.public_categ_ids & featured)
        return True

    def write(self, vals):
        touches_featured_fields = bool(FEATURED_REFRESH_FIELDS.intersection(vals))
        # Membre des vedettes AVANT écriture (capte une sortie de curation).
        was_featured = self._ck_touches_featured() if touches_featured_fields else False
        result = super().write(vals)
        # ... ou APRÈS écriture (capte une entrée en curation).
        if touches_featured_fields and (was_featured or self._ck_touches_featured()):
            self._ck_refresh_home_featured_products()
        return result

    def _register_hook(self):
        super()._register_hook()
        if tools.config.get('test_enable') or tools.config.get('test_tags'):
            return
        self._ck_sync_home_featured_labels_on_startup()

    @api.model
    def _ck_sync_home_featured_labels_on_startup(self):
        """Reconstruit la home si des étiquettes BO manquent des cards SSR (arch périmée)."""
        from odoo.addons.dorevia_ck_marketone_content.home_featured import (
            _featured_arch_missing_cart_cta,
            _featured_arch_missing_product_labels,
            _featured_arch_stale_cards,
            bootstrap_home_featured_products,
            get_curated_featured_variants,
        )

        page = self.env['website.page'].sudo().search([('url', '=', '/')], limit=1)
        if not page or not page.view_id:
            return
        arch = page.view_id.arch_db or ''
        website = self.env['website'].search([], limit=1)
        variants = get_curated_featured_variants(self.env)
        if not _featured_arch_missing_product_labels(self.env, arch, variants) and not (
            website and _featured_arch_missing_cart_cta(self.env, website, arch, variants)
        ) and not (
            website and _featured_arch_stale_cards(self.env, website, arch, variants)
        ):
            return
        if bootstrap_home_featured_products(self.env):
            _logger.info('CK Section 3 : home reconstruite (arch vedettes périmée).')
