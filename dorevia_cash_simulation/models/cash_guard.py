# -*- coding: utf-8 -*-

from collections import defaultdict

from odoo import _, api, fields, models


class DoreviaCashGuard(models.Model):
    _inherit = "dorevia.cash.guard"

    include_simulation = fields.Boolean(
        string="Inclure les simulations commerciales",
        default=False,
        tracking=True,
        help=(
            "Lorsque cette option est activée, la projection inclut les devis "
            "éligibles marqués comme simulations de trésorerie."
        ),
    )
    simulation_order_count = fields.Integer(
        string="Devis en simulation",
        compute="_compute_simulation_order_count",
    )

    @api.depends("include_simulation")
    def _compute_simulation_order_count(self):
        for guard in self:
            if guard.include_simulation:
                guard.simulation_order_count = self.env["sale.order"].search_count(
                    guard._get_simulation_order_domain()
                )
            else:
                guard.simulation_order_count = 0

    def _get_simulation_order_domain(self):
        """Domain for eligible simulation quotes (V1 rules)."""
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

    def _search_eligible_simulation_orders(self):
        """Return eligible simulation sale.orders for this projection."""
        self.ensure_one()
        return self.env["sale.order"].search(self._get_simulation_order_domain())

    def _get_sale_simulation_buckets(self, meta, situation_date):
        """Compute simulation buckets {week_index: net_amount} from eligible quotes."""
        self.ensure_one()
        buckets = defaultdict(float)
        for order in self._search_eligible_simulation_orders():
            week_idx = self._week_index_for_date(meta, order.cash_simulation_due_date)
            if week_idx is None:
                continue
            buckets[week_idx] += order.amount_total
        return buckets

    def _manual_line_net_by_week_index(self, meta, situation_date):
        buckets = super()._manual_line_net_by_week_index(meta, situation_date)
        if not self.include_simulation:
            return buckets
        sim_buckets = self._get_sale_simulation_buckets(meta, situation_date)
        for week_idx, net in sim_buckets.items():
            buckets[week_idx] = buckets.get(week_idx, 0.0) + net
        return buckets

    def action_view_simulation_orders(self):
        self.ensure_one()
        orders = self._search_eligible_simulation_orders()
        action = {
            "type": "ir.actions.act_window",
            "name": _("Devis en simulation"),
            "res_model": "sale.order",
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

    def write(self, vals):
        res = super().write(vals)
        if self.env.context.get("skip_cash_guard_recompute"):
            return res
        if "include_simulation" in vals and not (
            set(vals) & self._RECOMPUTE_GUARD_WRITE_FIELDS
        ):
            self.action_recompute_projection()
        return res
