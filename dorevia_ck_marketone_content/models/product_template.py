# -*- coding: utf-8 -*-
import logging

from odoo import api, fields, models, tools

_logger = logging.getLogger(__name__)


FEATURED_REFRESH_FIELDS = {
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
    'ck_net_quantity_uom',
    'ck_reference_price_uom',
    'ck_show_reference_price',
}

CK_NET_QUANTITY_UOM_SELECTION = [
    ('g', 'g'),
    ('kg', 'kg'),
    ('ml', 'ml'),
    ('cl', 'cl'),
    ('l', 'l'),
    ('unit', 'pièce'),
]

CK_REFERENCE_PRICE_UOM_SELECTION = [
    ('kg', 'kg'),
    ('l', 'l'),
]


class ProductTemplate(models.Model):
    _inherit = 'product.template'

    ck_net_quantity = fields.Float(
        string='Quantité nette',
        default=None,
        help='Quantité nette affichée sur la card home (ex. 320 g). Laisser vide si non applicable.',
    )
    ck_net_quantity_uom = fields.Selection(
        selection=CK_NET_QUANTITY_UOM_SELECTION,
        string='Unité de quantité nette',
    )
    ck_reference_price_uom = fields.Selection(
        selection=CK_REFERENCE_PRICE_UOM_SELECTION,
        string='Unité du prix de référence',
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

    def write(self, vals):
        result = super().write(vals)
        if FEATURED_REFRESH_FIELDS.intersection(vals):
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
            _featured_arch_missing_product_labels,
            bootstrap_home_featured_products,
            get_curated_featured_variants,
        )

        page = self.env['website.page'].sudo().search([('url', '=', '/')], limit=1)
        if not page or not page.view_id:
            return
        arch = page.view_id.arch_db or ''
        variants = get_curated_featured_variants(self.env)
        if not _featured_arch_missing_product_labels(self.env, arch, variants):
            return
        if bootstrap_home_featured_products(self.env):
            _logger.info('CK Section 3 : home reconstruite (étiquettes produit manquantes).')
