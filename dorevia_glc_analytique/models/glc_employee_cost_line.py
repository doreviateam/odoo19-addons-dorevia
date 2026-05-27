# -*- coding: utf-8 -*-

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError

from .glc_constants import GLC_PERCENT_TOLERANCE


class GlcEmployeeCostLine(models.Model):
    _name = "glc.employee.cost.line"
    _description = "Coût salarié mensuel chargé GLC"
    _inherit = ["glc.salary.mixin"]
    _order = "period_date desc, employee_id"

    company_id = fields.Many2one(
        "res.company",
        required=True,
        default=lambda self: self.env.company,
    )
    employee_id = fields.Many2one(
        "hr.employee",
        string="Salarié",
        required=True,
        check_company=True,
    )
    period_date = fields.Date(
        string="Mois",
        required=True,
        help="Premier jour du mois concerné.",
    )
    cost_amount = fields.Monetary(
        string="Coût mensuel chargé",
        required=True,
        currency_field="currency_id",
    )
    reference_hours = fields.Float(
        string="Heures mensuelles de référence",
        digits=(16, 2),
    )
    hourly_cost = fields.Monetary(
        string="Coût horaire",
        compute="_compute_hourly_cost",
        store=True,
        currency_field="currency_id",
    )
    currency_id = fields.Many2one(
        "res.currency",
        required=True,
        default=lambda self: self.env.company.currency_id,
    )
    source = fields.Selection(
        selection=[("manual", "Manuel")],
        default="manual",
        required=True,
    )
    note = fields.Text()

    _glc_employee_cost_line_uniq = models.Constraint(
        "unique(company_id, employee_id, period_date)",
        "Un seul coût mensuel par salarié et par mois.",
    )

    @api.depends("cost_amount", "reference_hours")
    def _compute_hourly_cost(self):
        for line in self:
            if line.reference_hours and line.reference_hours > 0:
                line.hourly_cost = line.cost_amount / line.reference_hours
            else:
                line.hourly_cost = 0.0

    @api.constrains("cost_amount")
    def _check_cost_amount(self):
        for line in self:
            if line.cost_amount <= 0:
                raise ValidationError(_("Le coût mensuel chargé doit être strictement positif."))

    @api.constrains("reference_hours")
    def _check_reference_hours_non_negative(self):
        for line in self:
            if line.reference_hours is not None and line.reference_hours < 0:
                raise ValidationError(_("Les heures mensuelles de référence ne peuvent pas être négatives."))

    @api.constrains("period_date")
    def _check_period_first_day(self):
        for line in self:
            if line.period_date and line.period_date.day != 1:
                raise ValidationError(_("La date de période doit être le premier jour du mois."))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            vals["period_date"] = self._normalize_period_date(vals.get("period_date"))
        return super().create(vals_list)

    def write(self, vals):
        if vals.get("period_date"):
            vals["period_date"] = self._normalize_period_date(vals["period_date"])
        return super().write(vals)

    @api.model
    def _normalize_period_date(self, period_date):
        if not period_date:
            return period_date
        date_value = fields.Date.to_date(period_date)
        return date_value.replace(day=1)

    def _check_reference_hours_for_hours_method(self):
        self.ensure_one()
        if not self.reference_hours or self.reference_hours <= 0:
            raise ValidationError(
                _(
                    "Les heures mensuelles de référence doivent être strictement "
                    "positives pour une ventilation en heures."
                )
            )
