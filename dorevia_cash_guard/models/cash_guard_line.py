# -*- coding: utf-8 -*-

from odoo import api, fields, models
from odoo.exceptions import ValidationError


class DoreviaCashGuardLine(models.Model):
    _RECOMPUTE_TRIGGER_FIELDS = {
        "guard_id",
        "projection_date",
        "budget_post_id",
        "budget_line_id",
        "analytic_account_id",
        "direction",
        "line_type",
        "label",
        "projected_amount",
        "realized_amount",
        "partner_id",
        "source_move_id",
        "source_move_line_id",
        "bank_move_line_id",
        "certainty",
        "priority",
        "cash_state",
        "sequence",
        "note",
    }

    _name = "dorevia.cash.guard.line"
    _description = "Dorevia Cash Guard Line"
    _order = "projection_date asc, sequence asc, id asc"

    guard_id = fields.Many2one(
        "dorevia.cash.guard",
        required=True,
        ondelete="cascade",
        index=True,
    )
    projection_date = fields.Date(required=True, index=True)
    budget_post_id = fields.Many2one("account.budget.post", required=True, index=True)
    budget_line_id = fields.Many2one("budget.lines", index=True)
    analytic_account_id = fields.Many2one("account.analytic.account", index=True)
    direction = fields.Selection(
        [("inflow", "Entree"), ("outflow", "Sortie")],
        required=True,
        default="outflow",
        index=True,
    )
    line_type = fields.Selection(
        [("planned", "Prevue"), ("simulated", "Simulee")],
        required=True,
        default="planned",
        index=True,
    )
    label = fields.Char(required=True)
    projected_amount = fields.Monetary(required=True)
    realized_amount = fields.Monetary()
    signed_projected_amount = fields.Monetary(
        compute="_compute_signed_amounts",
        store=True,
    )
    signed_realized_amount = fields.Monetary(
        compute="_compute_signed_amounts",
        store=True,
    )
    variance_amount = fields.Monetary(
        compute="_compute_variance_amount",
        store=True,
    )
    balance_after_line = fields.Monetary()
    partner_id = fields.Many2one("res.partner", index=True)
    source_move_id = fields.Many2one("account.move", index=True)
    source_move_line_id = fields.Many2one("account.move.line", index=True)
    bank_move_line_id = fields.Many2one("account.move.line", index=True)
    certainty = fields.Selection(
        [
            ("certain", "Certain"),
            ("confirmed", "Confirme"),
            ("uncertain", "Incertain"),
        ],
        index=True,
    )
    priority = fields.Selection(
        [("mandatory", "Obligatoire"), ("deferrable", "Reportable")],
        index=True,
    )
    cash_state = fields.Selection(
        [
            ("planned", "Prevu"),
            ("booked", "Comptabilise"),
            ("payment_entered", "Paiement saisi"),
            ("reconciled", "Rapproche"),
            ("variance", "Ecart"),
            ("cancelled", "Annule"),
        ],
        required=True,
        default="planned",
        index=True,
    )
    sequence = fields.Integer(default=10, required=True, index=True)
    company_id = fields.Many2one(
        "res.company",
        related="guard_id.company_id",
        store=True,
        readonly=True,
        index=True,
    )
    currency_id = fields.Many2one(
        "res.currency",
        related="guard_id.currency_id",
        store=True,
        readonly=True,
    )
    note = fields.Text()

    @api.depends("direction", "projected_amount", "realized_amount")
    def _compute_signed_amounts(self):
        for line in self:
            sign = 1 if line.direction == "inflow" else -1
            line.signed_projected_amount = sign * (line.projected_amount or 0.0)
            line.signed_realized_amount = sign * (line.realized_amount or 0.0)

    @api.depends("signed_projected_amount", "signed_realized_amount")
    def _compute_variance_amount(self):
        for line in self:
            line.variance_amount = (line.signed_realized_amount or 0.0) - (
                line.signed_projected_amount or 0.0
            )

    @api.constrains("projected_amount", "realized_amount", "sequence")
    def _check_amounts_and_sequence(self):
        for line in self:
            if line.projected_amount < 0:
                raise ValidationError("Le montant previsionnel doit etre positif ou nul.")
            if line.realized_amount and line.realized_amount < 0:
                raise ValidationError("Le montant realise doit etre positif ou nul.")
            if line.sequence < 0:
                raise ValidationError("La sequence doit etre positive ou nulle.")

    @api.model_create_multi
    def create(self, vals_list):
        lines = super().create(vals_list)
        if not self.env.context.get("skip_cash_guard_recompute"):
            lines.mapped("guard_id").action_recompute_projection()
        return lines

    def write(self, vals):
        res = super().write(vals)
        if self.env.context.get("skip_cash_guard_recompute"):
            return res
        if set(vals).intersection(self._RECOMPUTE_TRIGGER_FIELDS):
            self.mapped("guard_id").action_recompute_projection()
        return res

    def unlink(self):
        guards = self.mapped("guard_id")
        res = super().unlink()
        if not self.env.context.get("skip_cash_guard_recompute"):
            guards.action_recompute_projection()
        return res
