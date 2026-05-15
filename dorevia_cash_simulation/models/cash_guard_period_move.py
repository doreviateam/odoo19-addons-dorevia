# -*- coding: utf-8 -*-

from odoo import _, fields, models


class DoreviaCashGuardPeriodMove(models.Model):
    _inherit = "dorevia.cash.guard.period.move"

    sale_order_id = fields.Many2one(
        "sale.order",
        string="Devis simulé",
        readonly=True,
        ondelete="cascade",
        index=True,
    )

    def action_open_source_document(self):
        self.ensure_one()
        if self.sale_order_id:
            return {
                "type": "ir.actions.act_window",
                "name": self.sale_order_id.display_name,
                "res_model": "sale.order",
                "res_id": self.sale_order_id.id,
                "view_mode": "form",
                "target": "new",
            }
        return super().action_open_source_document()
