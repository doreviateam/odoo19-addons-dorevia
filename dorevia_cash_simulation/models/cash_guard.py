# -*- coding: utf-8 -*-

from collections import defaultdict

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class DoreviaCashGuard(models.Model):
    _inherit = "dorevia.cash.guard"

    include_simulation = fields.Boolean(
        string="Mode simulation",
        default=False,
        tracking=True,
        help=(
            "Lorsque cette option est activée, la projection inclut les devis "
            "sélectionnés ci-dessous comme hypothèses de trésorerie."
        ),
    )
    simulation_sale_order_ids = fields.Many2many(
        comodel_name="sale.order",
        string="Devis",
        help=(
            "Devis sélectionnés pour le scénario de simulation de cette "
            "projection Cash Guard."
        ),
    )
    simulation_order_count = fields.Integer(
        string="Devis en simulation",
        compute="_compute_simulation_order_count",
    )

    @api.depends("include_simulation", "simulation_sale_order_ids")
    def _compute_simulation_order_count(self):
        for guard in self:
            if guard.include_simulation:
                guard.simulation_order_count = len(
                    guard._get_eligible_sale_simulation_orders()
                )
            else:
                guard.simulation_order_count = 0

    def _get_eligible_sale_simulation_orders(self):
        """Filter selected sale orders to keep only eligible ones."""
        self.ensure_one()
        if not self.simulation_sale_order_ids:
            return self.env["sale.order"]
        today = fields.Date.today()
        return self.simulation_sale_order_ids.filtered(
            lambda o: (
                o.state in ("draft", "sent")
                and not o.invoice_ids
                and o.company_id == self.company_id
                and o.currency_id == self.currency_id
                and o.validity_date
                and o.validity_date >= self.date_from
                and o.validity_date <= self.date_to
            )
        )

    def _get_sale_simulation_buckets(self, meta, situation_date):
        """Compute simulation buckets {week_index: net_amount} from eligible quotes."""
        self.ensure_one()
        buckets = defaultdict(float)
        for order in self._get_eligible_sale_simulation_orders():
            week_idx = self._week_index_for_date(meta, order.validity_date)
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
        orders = self._get_eligible_sale_simulation_orders()
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
        if "include_simulation" in vals and not vals["include_simulation"]:
            vals["simulation_sale_order_ids"] = [(5, 0, 0)]
        res = super().write(vals)
        if self.env.context.get("skip_cash_guard_recompute"):
            return res
        sim_fields = {"include_simulation", "simulation_sale_order_ids"}
        if sim_fields & set(vals) and not (
            set(vals) & self._RECOMPUTE_GUARD_WRITE_FIELDS
        ):
            self.action_recompute_projection()
        return res

    def _has_any_simulation_document(self):
        """Return True if at least one simulation document is selected.

        Designed to be extended by dorevia_cash_simulation_purchase to also
        check simulation_purchase_order_ids.
        """
        self.ensure_one()
        return bool(self.simulation_sale_order_ids)

    @api.constrains("include_simulation", "simulation_sale_order_ids")
    def _check_simulation_has_orders(self):
        for guard in self:
            if guard.include_simulation and not guard._has_any_simulation_document():
                raise ValidationError(
                    _(
                        "Le mode simulation nécessite au moins un document "
                        "de simulation sélectionné (devis ou commande achat)."
                    )
                )
