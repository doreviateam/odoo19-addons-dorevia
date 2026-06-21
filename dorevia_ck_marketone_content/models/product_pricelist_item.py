# -*- coding: utf-8 -*-
from odoo import api, models


class ProductPricelistItem(models.Model):
    _inherit = 'product.pricelist.item'

    def _ck_items_touch_featured(self):
        """True si une de ces règles peut influencer le prix d'une carte vedette.

        Le prix affiché sur la carte vient du prix pricelist B2C de la variante
        (cf. ``_get_featured_price_amount``). Une règle ciblant un produit/variante
        vedette — ou une règle large (globale/catégorie) — peut donc changer le
        prix rendu. On délègue ensuite à ``_ck_refresh_home_featured_if_stale`` qui
        ne reconstruit que si la carte change réellement (pas de sur-rebuild).
        """
        for item in self:
            template = item.product_tmpl_id or item.product_id.product_tmpl_id
            if template:
                if template._ck_touches_featured():
                    return True
            else:
                # Règle globale / par catégorie : peut affecter n'importe quelle vedette.
                return True
        return False

    def _ck_maybe_refresh_featured(self):
        if self._ck_items_touch_featured():
            self.env['product.template']._ck_refresh_home_featured_if_stale()

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        records._ck_maybe_refresh_featured()
        return records

    def write(self, vals):
        result = super().write(vals)
        self._ck_maybe_refresh_featured()
        return result

    def unlink(self):
        touches_featured = self._ck_items_touch_featured()
        result = super().unlink()
        if touches_featured:
            self.env['product.template']._ck_refresh_home_featured_if_stale()
        return result
