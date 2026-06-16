# -*- coding: utf-8 -*-
from odoo import fields, models


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
    'ck_featured_label_ids',
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

    ck_featured_label_ids = fields.Many2many(
        'dorevia.ck.product.label',
        'product_template_ck_featured_label_rel',
        'product_tmpl_id',
        'label_id',
        string='Étiquettes card home',
    )
    ck_net_quantity = fields.Float(string='Quantité nette commerciale')
    ck_net_quantity_uom = fields.Selection(
        selection=CK_NET_QUANTITY_UOM_SELECTION,
        string='Unité quantité nette',
    )
    ck_reference_price_uom = fields.Selection(
        selection=CK_REFERENCE_PRICE_UOM_SELECTION,
        string='Unité prix de référence',
    )
    ck_show_reference_price = fields.Boolean(
        string='Afficher le prix de référence',
        default=True,
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
