# -*- coding: utf-8 -*-
from odoo import models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def _set_shop_warning_stock(self, desired_qty, new_qty, save=True):
        """CK stock warning — same structure as Odoo 19, custom i18n-ready message.

        A5 (new product without existing line) remains on the standard ``sale.order``
        path and is intentionally not overridden here (S3-B scope).
        """
        self.ensure_one()
        warning = self.env._(
            "You requested %(requested_qty)s, but only %(available_qty)s is currently available.",
            requested_qty=desired_qty,
            available_qty=new_qty,
        )
        if save:
            self.shop_warning = warning
        return warning
