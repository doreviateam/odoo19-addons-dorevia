# -*- coding: utf-8 -*-

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError


class GlcSalaryAllocationLine(models.Model):
    _name = "glc.salary.allocation.line"
    _description = "Ligne de ventilation salariale GLC"
    _inherit = ["glc.salary.mixin"]
    _order = "allocation_id, id"

    allocation_id = fields.Many2one(
        "glc.salary.allocation",
        required=True,
        ondelete="cascade",
    )
    activity_account_id = fields.Many2one(
        "account.analytic.account",
        string="Activité GLC",
        required=True,
        check_company=True,
        domain=lambda self: [
            ("plan_id", "=", self.env.ref("dorevia_glc_analytics.analytic_plan_glc_activites").id),
            "|",
            ("company_id", "=", False),
            ("company_id", "in", self.env.companies.ids),
        ],
    )
    percent = fields.Float(string="Pourcentage (%)", digits=(16, 2))
    hours = fields.Float(string="Heures", digits=(16, 2))
    amount = fields.Monetary(
        string="Montant ventilé",
        compute="_compute_amount",
        store=True,
        currency_field="currency_id",
    )
    currency_id = fields.Many2one(related="allocation_id.currency_id")
    note = fields.Char()

    _glc_salary_allocation_line_activity_uniq = models.Constraint(
        "unique(allocation_id, activity_account_id)",
        "Chaque activité GLC ne peut apparaître qu'une seule fois par ventilation.",
    )

    @api.depends(
        "percent",
        "hours",
        "allocation_id.method",
        "allocation_id.cost_amount",
        "allocation_id.employee_cost_line_id.hourly_cost",
    )
    def _compute_amount(self):
        for line in self:
            allocation = line.allocation_id
            if allocation.method == "percent":
                line.amount = allocation.cost_amount * (line.percent or 0.0) / 100.0
            else:
                hourly_cost = allocation.employee_cost_line_id.hourly_cost
                line.amount = (line.hours or 0.0) * hourly_cost

    def _check_allocation_editable(self):
        for line in self:
            if line.allocation_id.state in ("validated", "locked"):
                raise UserError(_("Impossible de modifier une ventilation validée ou verrouillée."))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            allocation = self.env["glc.salary.allocation"].browse(vals.get("allocation_id"))
            if allocation.state in ("validated", "locked"):
                raise UserError(_("Impossible de modifier une ventilation validée ou verrouillée."))
        return super().create(vals_list)

    def write(self, vals):
        self._check_allocation_editable()
        return super().write(vals)

    def unlink(self):
        self._check_allocation_editable()
        return super().unlink()

    @api.constrains("activity_account_id")
    def _check_activity_account(self):
        for line in self:
            line._glc_check_activity_account(line.activity_account_id)

    @api.constrains("percent", "hours")
    def _check_method_fields(self):
        for line in self:
            if line.allocation_id.method == "percent" and (line.hours or 0.0):
                raise ValidationError(_("Les heures ne sont pas utilisées en méthode pourcentage."))
            if line.allocation_id.method == "hours" and (line.percent or 0.0):
                raise ValidationError(_("Le pourcentage n'est pas utilisé en méthode heures."))
