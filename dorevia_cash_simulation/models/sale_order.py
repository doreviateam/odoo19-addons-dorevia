# -*- coding: utf-8 -*-

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = "sale.order"

    cash_simulation_ok = fields.Boolean(
        string="Inclure dans la simulation de trésorerie",
        default=False,
        tracking=True,
        help=(
            "Permet d'utiliser ce devis comme hypothèse d'encaissement futur "
            "dans Cash Guard lorsque le mode simulation est activé."
        ),
    )
    cash_simulation_due_date = fields.Date(
        string="Date d'échéance simulation",
        tracking=True,
        help=(
            "Date prévisionnelle d'encaissement utilisée uniquement pour la "
            "simulation de trésorerie. Indépendante de la date de validité "
            "commerciale du devis."
        ),
    )
    cash_simulation_eligible = fields.Boolean(
        string="Éligible simulation",
        compute="_compute_cash_simulation_eligible",
        store=False,
    )

    @api.depends(
        "cash_simulation_ok",
        "cash_simulation_due_date",
        "state",
        "invoice_ids",
    )
    def _compute_cash_simulation_eligible(self):
        today = fields.Date.today()
        for order in self:
            order.cash_simulation_eligible = (
                order.cash_simulation_ok
                and order.cash_simulation_due_date
                and order.cash_simulation_due_date > today
                and order.state in ("draft", "sent")
                and not order.invoice_ids
            )

    def _check_cash_simulation_fields(self):
        """Validate current simulation state after create/write.

        Called only when simulation fields were touched in the vals.
        Reads the record's *current* (post-write) values.
        """
        today = fields.Date.today()
        for order in self:
            if not order.cash_simulation_ok:
                continue
            if not order.cash_simulation_due_date:
                raise ValidationError(
                    _(
                        "Le devis « %(name)s » ne peut pas être inclus dans la simulation "
                        "sans date d'échéance de simulation.",
                        name=order.display_name,
                    )
                )
            if order.cash_simulation_due_date <= today:
                raise ValidationError(
                    _(
                        "Le devis « %(name)s » : la date d'échéance de simulation doit "
                        "être postérieure à aujourd'hui.",
                        name=order.display_name,
                    )
                )

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        sim_records = records.filtered("cash_simulation_ok")
        if sim_records:
            sim_records._check_cash_simulation_fields()
        return records

    def write(self, vals):
        res = super().write(vals)
        if "cash_simulation_ok" in vals or "cash_simulation_due_date" in vals:
            self.filtered("cash_simulation_ok")._check_cash_simulation_fields()
        return res
