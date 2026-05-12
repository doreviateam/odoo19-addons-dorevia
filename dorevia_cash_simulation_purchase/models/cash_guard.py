# -*- coding: utf-8 -*-

from collections import defaultdict

from odoo import _, api, fields, models


class DoreviaCashGuard(models.Model):
    _inherit = "dorevia.cash.guard"

    simulation_purchase_order_ids = fields.Many2many(
        comodel_name="purchase.order",
        string="Commandes achat",
        help=(
            "Demandes de prix / commandes achat sélectionnées pour le scénario "
            "de simulation de cette projection Cash Guard."
        ),
    )
    simulation_purchase_count = fields.Integer(
        string="Achats en simulation",
        compute="_compute_simulation_purchase_count",
    )

    @api.depends("include_simulation", "simulation_purchase_order_ids")
    def _compute_simulation_purchase_count(self):
        for guard in self:
            if guard.include_simulation:
                guard.simulation_purchase_count = len(
                    guard._get_eligible_purchase_simulation_orders()
                )
            else:
                guard.simulation_purchase_count = 0

    def _get_eligible_purchase_simulation_orders(self):
        """Filter selected purchase orders to keep only eligible ones."""
        self.ensure_one()
        if not self.simulation_purchase_order_ids:
            return self.env["purchase.order"]
        return self.simulation_purchase_order_ids.filtered(
            lambda o: (
                o.state in ("draft", "sent")
                and not o.invoice_ids
                and o.company_id == self.company_id
                and o.currency_id == self.currency_id
                and o.date_planned
                and o.date_planned.date() >= self.date_from
                and o.date_planned.date() <= self.date_to
            )
        )

    def _get_purchase_simulation_buckets(self, meta, situation_date):
        """Compute simulation buckets {week_index: net_amount} from eligible POs.

        Amounts are negative (outgoing cash flow).
        """
        self.ensure_one()
        buckets = defaultdict(float)
        for order in self._get_eligible_purchase_simulation_orders():
            week_idx = self._week_index_for_date(
                meta, order.date_planned.date()
            )
            if week_idx is None:
                continue
            buckets[week_idx] -= order.amount_total
        return buckets

    def _manual_line_net_by_week_index(self, meta, situation_date=None, **kwargs):
        if situation_date is None:
            situation_date = kwargs.get("sit")
        buckets = super()._manual_line_net_by_week_index(meta, situation_date)
        if not self.include_simulation:
            return buckets
        purchase_buckets = self._get_purchase_simulation_buckets(
            meta, situation_date
        )
        for week_idx, net in purchase_buckets.items():
            buckets[week_idx] = buckets.get(week_idx, 0.0) + net
        return buckets

    def _get_simulation_period_move_rows(self, meta, sit, weeks_by_index):
        rows = super()._get_simulation_period_move_rows(meta, sit, weeks_by_index)
        if not self.include_simulation:
            return rows
        for order in self._get_eligible_purchase_simulation_orders():
            due_date = order.date_planned.date()
            week_idx = self._week_index_for_date(meta, due_date)
            if week_idx is None:
                continue
            week = weeks_by_index.get(week_idx)
            if not week:
                continue
            rows.append(
                {
                    "guard_id": self.id,
                    "week_id": week.id,
                    "purchase_order_id": order.id,
                    "partner_id": order.partner_id.id if order.partner_id else False,
                    "move_name": order.name or "",
                    "invoice_date_due": due_date,
                    "projected_date": due_date,
                    "amount_residual": order.amount_total,
                    "signed_amount": -order.amount_total,
                    "currency_id": self.company_id.currency_id.id,
                    "company_id": self.company_id.id,
                    "explanation_type": "outflow",
                    "is_overdue": False,
                    "days_overdue": 0,
                    "is_simulation": True,
                    "document_type_label": "Commande achat simulée",
                    "display_status": "simulation",
                    "_sort": (
                        week.week_index,
                        due_date,
                        -order.amount_total,
                        200000 + order.id,
                    ),
                }
            )
        return rows

    def action_view_purchase_simulation_orders(self):
        self.ensure_one()
        orders = self._get_eligible_purchase_simulation_orders()
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

    def action_reset_period_to_defaults(self):
        self.with_context(skip_cash_guard_recompute=True).write(
            {
                "simulation_purchase_order_ids": [(5, 0, 0)],
            }
        )
        return super().action_reset_period_to_defaults()

    def _has_any_simulation_document(self):
        return super()._has_any_simulation_document() or bool(
            self.simulation_purchase_order_ids
        )

    @api.constrains("include_simulation", "simulation_purchase_order_ids")
    def _check_simulation_has_orders(self):
        super()._check_simulation_has_orders()

    def write(self, vals):
        if "include_simulation" in vals and not vals["include_simulation"]:
            vals.setdefault("simulation_purchase_order_ids", [(5, 0, 0)])
        res = super().write(vals)
        if self.env.context.get("skip_cash_guard_recompute"):
            return res
        if "simulation_purchase_order_ids" in vals and not (
            set(vals) & self._RECOMPUTE_GUARD_WRITE_FIELDS
        ):
            self.action_recompute_projection()
        return res
