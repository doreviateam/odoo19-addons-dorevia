# -*- coding: utf-8 -*-

from collections import defaultdict

from odoo import _, api, fields, models


class DoreviaCashGuard(models.Model):
    _inherit = "dorevia.cash.guard"

    simulation_purchase_count = fields.Integer(
        string="Achats en simulation",
        compute="_compute_simulation_purchase_count",
    )

    @api.depends("include_simulation")
    def _compute_simulation_purchase_count(self):
        for guard in self:
            if guard.include_simulation:
                guard.simulation_purchase_count = self.env[
                    "purchase.order"
                ].search_count(guard._get_purchase_simulation_domain())
            else:
                guard.simulation_purchase_count = 0

    def _get_purchase_simulation_domain(self):
        """Domain for eligible purchase simulation orders (V1.1 rules)."""
        self.ensure_one()
        today = fields.Date.today()
        return [
            ("cash_simulation_ok", "=", True),
            ("cash_simulation_due_date", ">", today),
            ("state", "in", ("draft", "sent")),
            ("invoice_ids", "=", False),
            ("company_id", "=", self.company_id.id),
            ("currency_id", "=", self.currency_id.id),
        ]

    def _search_eligible_purchase_simulation_orders(self):
        """Return eligible simulation purchase.orders for this projection."""
        self.ensure_one()
        return self.env["purchase.order"].search(
            self._get_purchase_simulation_domain()
        )

    def _get_purchase_simulation_buckets(self, meta, situation_date):
        """Compute simulation buckets {week_index: net_amount} from eligible POs.

        Amounts are negative (outgoing cash flow).
        """
        self.ensure_one()
        buckets = defaultdict(float)
        for order in self._search_eligible_purchase_simulation_orders():
            week_idx = self._week_index_for_date(
                meta, order.cash_simulation_due_date
            )
            if week_idx is None:
                continue
            buckets[week_idx] -= order.amount_total
        return buckets

    def _manual_line_net_by_week_index(self, meta, situation_date):
        buckets = super()._manual_line_net_by_week_index(meta, situation_date)
        if not self.include_simulation:
            return buckets
        purchase_buckets = self._get_purchase_simulation_buckets(
            meta, situation_date
        )
        for week_idx, net in purchase_buckets.items():
            buckets[week_idx] = buckets.get(week_idx, 0.0) + net
        return buckets

    def action_view_purchase_simulation_orders(self):
        self.ensure_one()
        orders = self._search_eligible_purchase_simulation_orders()
        action = {
            "type": "ir.actions.act_window",
            "name": _("Achats en simulation"),
            "res_model": "purchase.order",
            "view_mode": "list,form",
            "domain": [("id", "in", orders.ids)],
            "context": {"create": False},
        }
        if len(orders) == 1:
            action.update(
                {
                    "view_mode": "form",
                    "res_id": orders.id,
                }
            )
        return action
