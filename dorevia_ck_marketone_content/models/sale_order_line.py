# -*- coding: utf-8 -*-
from odoo import models


class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'

    def _set_shop_warning_stock(self, desired_qty, new_qty, save=True):
        """Message CK explicite lorsque la quantité demandée dépasse le stock."""
        self.ensure_one()
        warning = self.env._(
            "La quantité demandée n'est pas disponible. "
            "La quantité a été limitée au stock disponible : %(qty)s unité(s).",
            qty=new_qty,
        )
        if save:
            self.shop_warning = warning
        return warning
