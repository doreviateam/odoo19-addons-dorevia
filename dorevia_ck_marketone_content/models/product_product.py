# -*- coding: utf-8 -*-
from odoo import models

# Odoo 19 : l'édition « Prix de vente » sur une variante passe par l'inverse
# ``lst_price`` → ``write({'list_price': …})``, pas ``lst_price`` dans vals.
_VARIANT_PRICE_FIELDS = frozenset({
    'list_price',
    'lst_price',
})

# Image propre à la variante (édition « Image variante » en BO → image_variant_1920).
# La card affiche l'image de la variante en priorité (_get_featured_image_url).
_VARIANT_IMAGE_FIELDS = frozenset({
    'image_variant_1920',
    'image_1920',
})

_VARIANT_FEATURED_REFRESH_FIELDS = frozenset({
    'additional_product_tag_ids',
    'is_published',
    'sale_ok',
}) | _VARIANT_PRICE_FIELDS | _VARIANT_IMAGE_FIELDS


class ProductProduct(models.Model):
    _inherit = 'product.product'

    def _ck_sync_variant_fixed_pricelist_items(self):
        """Aligne les règles pricelist « fixed » variante sur le prix catalogue BO."""
        Item = self.env['product.pricelist.item'].sudo()
        for variant in self:
            items = Item.search([
                ('product_id', '=', variant.id),
                ('compute_price', '=', 'fixed'),
            ])
            target = variant.lst_price
            to_update = items.filtered(lambda item: item.fixed_price != target)
            if to_update:
                to_update.write({'fixed_price': target})

    def write(self, vals):
        result = super().write(vals)
        touches_price = bool(_VARIANT_PRICE_FIELDS.intersection(vals))
        if touches_price:
            self._ck_sync_variant_fixed_pricelist_items()
        if _VARIANT_FEATURED_REFRESH_FIELDS.intersection(vals):
            templates = self.mapped('product_tmpl_id')
            # QA D3 — cohérence avec M1 (product.template) : ne reconstruire la home
            # que si un template concerné appartient aux vedettes (curation peuplée) ;
            # sinon (mode repli auto) comportement large conservé.
            if templates and templates._ck_touches_featured():
                templates._ck_refresh_home_featured_products()
        return result
