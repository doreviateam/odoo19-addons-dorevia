# -*- coding: utf-8 -*-

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError


class GlcBudgetLine(models.Model):
    _name = "glc.budget.line"
    _description = "Ligne budgétaire GLC"
    _inherit = ["glc.budget.mixin"]
    _order = "period_date, analytic_account_id, line_type, id"

    budget_id = fields.Many2one(
        "glc.budget",
        required=True,
        ondelete="cascade",
    )
    period_date = fields.Date(
        string="Mois",
        required=True,
        help="Premier jour du mois concerné.",
    )
    analytic_account_id = fields.Many2one(
        "account.analytic.account",
        string="Axe analytique GLC",
        required=True,
        check_company=True,
        domain=lambda self: [
            (
                "plan_id",
                "in",
                [
                    self.env.ref("dorevia_glc_analytics.analytic_plan_glc_activites").id,
                    self.env.ref("dorevia_glc_analytics.analytic_plan_glc_financements").id,
                ],
            ),
            "|",
            ("company_id", "=", False),
            ("company_id", "in", self.env.companies.ids),
        ],
    )
    line_type = fields.Selection(
        selection=[
            ("revenue", "Recette"),
            ("expense", "Charge"),
            ("funding", "Financement"),
        ],
        required=True,
    )
    amount = fields.Monetary(required=True, currency_field="currency_id")
    currency_id = fields.Many2one(related="budget_id.currency_id")
    note = fields.Char()
    company_id = fields.Many2one(related="budget_id.company_id", store=True)
    year = fields.Integer(related="budget_id.year", store=True)
    scenario = fields.Selection(related="budget_id.scenario", store=True)
    budget_state = fields.Selection(related="budget_id.state")

    _glc_budget_line_uniq = models.Constraint(
        "unique(budget_id, period_date, analytic_account_id, line_type)",
        "Cette combinaison mois / axe analytique / type existe déjà sur le budget.",
    )

    @api.onchange("line_type")
    def _onchange_line_type(self):
        if self.analytic_account_id:
            try:
                self._glc_check_analytic_account_for_line_type(
                    self.analytic_account_id, self.line_type
                )
            except ValidationError:
                self.analytic_account_id = False

    def _check_budget_editable(self):
        for line in self:
            if line.budget_id.state != "draft":
                raise UserError(_("Impossible de modifier un budget validé ou archivé."))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            budget = self.env["glc.budget"].browse(vals.get("budget_id"))
            if budget.state != "draft":
                raise UserError(_("Impossible de modifier un budget validé ou archivé."))
        return super().create(vals_list)

    def write(self, vals):
        self._check_budget_editable()
        return super().write(vals)

    def unlink(self):
        self._check_budget_editable()
        return super().unlink()

    @api.constrains("period_date")
    def _check_period_date(self):
        for line in self:
            if line.period_date and line.period_date.day != 1:
                raise ValidationError(
                    _("La date de période doit être le premier jour du mois.")
                )

    @api.constrains("amount")
    def _check_amount(self):
        for line in self:
            if line.amount is not None and line.amount < 0:
                raise ValidationError(_("Le montant prévu doit être positif ou nul."))

    @api.constrains("analytic_account_id", "line_type")
    def _check_analytic_account(self):
        for line in self:
            line._glc_check_analytic_account_for_line_type(
                line.analytic_account_id, line.line_type
            )
