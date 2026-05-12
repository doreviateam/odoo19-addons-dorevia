# -*- coding: utf-8 -*-

from odoo import _, fields, models


class DoreviaCashGuardPeriodMove(models.Model):
    _inherit = "dorevia.cash.guard.period.move"

    purchase_order_id = fields.Many2one(
        "purchase.order",
        string="Commande achat simulée",
        readonly=True,
        ondelete="cascade",
        index=True,
    )

    def action_open_source_document(self):
        self.ensure_one()
        if self.purchase_order_id:
            return {
                "type": "ir.actions.act_window",
                "name": self.purchase_order_id.display_name,
                "res_model": "purchase.order",
                "res_id": self.purchase_order_id.id,
                "view_mode": "form",
                "target": "new",
            }
        return super().action_open_source_document()
