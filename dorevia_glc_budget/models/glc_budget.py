# -*- coding: utf-8 -*-

from odoo import _, api, fields, models
from odoo.exceptions import UserError


class GlcBudget(models.Model):
    _name = "glc.budget"
    _description = "Budget prévisionnel GLC"
    _inherit = ["glc.budget.mixin"]
    _order = "year desc, scenario, id desc"

    name = fields.Char(required=True)
    year = fields.Integer(required=True, default=lambda self: fields.Date.today().year)
    company_id = fields.Many2one(
        "res.company",
        required=True,
        default=lambda self: self.env.company,
    )
    scenario = fields.Selection(
        selection=[
            ("initial", "Initial"),
            ("revised", "Révisé"),
            ("landing", "Atterrissage"),
        ],
        required=True,
        default="initial",
    )
    state = fields.Selection(
        selection=[
            ("draft", "Brouillon"),
            ("validated", "Validé"),
            ("archived", "Archivé"),
        ],
        default="draft",
        required=True,
    )
    line_ids = fields.One2many(
        "glc.budget.line",
        "budget_id",
        string="Lignes budgétaires",
    )
    note = fields.Text()
    validated_by = fields.Many2one("res.users", readonly=True)
    validated_date = fields.Datetime(readonly=True)
    currency_id = fields.Many2one(
        "res.currency",
        compute="_compute_currency_id",
        store=True,
    )

    _glc_budget_company_year_scenario_uniq = models.Constraint(
        "unique(company_id, year, scenario)",
        "Un budget existe déjà pour cette société, année et scénario.",
    )

    @api.depends("company_id")
    def _compute_currency_id(self):
        for budget in self:
            budget.currency_id = budget.company_id.currency_id

    def _check_editable(self):
        for budget in self:
            if budget.state != "draft":
                raise UserError(_("Seuls les budgets en brouillon peuvent être modifiés."))

    @api.model_create_multi
    def create(self, vals_list):
        records = super().create(vals_list)
        records._fill_default_name()
        return records

    def _fill_default_name(self):
        scenario_labels = dict(self._fields["scenario"].selection)
        for budget in self:
            if budget.name:
                continue
            budget.name = "Budget %s — %s" % (
                budget.year,
                scenario_labels.get(budget.scenario, budget.scenario),
            )

    def write(self, vals):
        if vals.keys() - {"state", "validated_by", "validated_date"}:
            self._check_editable()
        return super().write(vals)

    def unlink(self):
        self._check_editable()
        return super().unlink()

    def action_validate(self):
        self._check_editable()
        self.write(
            {
                "state": "validated",
                "validated_by": self.env.user.id,
                "validated_date": fields.Datetime.now(),
            }
        )

    def action_archive(self):
        for budget in self:
            if budget.state != "validated":
                raise UserError(_("Seuls les budgets validés peuvent être archivés."))
        self.write({"state": "archived"})

    def action_reset_to_draft(self):
        for budget in self:
            if budget.state not in ("validated",):
                raise UserError(_("Seuls les budgets validés peuvent être remis en brouillon."))
        self.write(
            {
                "state": "draft",
                "validated_by": False,
                "validated_date": False,
            }
        )
