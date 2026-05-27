# -*- coding: utf-8 -*-

from calendar import monthrange
from datetime import date

from odoo import _, api, fields, models
from odoo.exceptions import UserError, ValidationError

from .glc_constants import GLC_PAYROLL_ACCOUNT_PREFIXES, GLC_PERCENT_TOLERANCE


class GlcSalaryAllocation(models.Model):
    _name = "glc.salary.allocation"
    _description = "Ventilation salariale mensuelle GLC"
    _inherit = ["glc.salary.mixin"]
    _order = "period_date desc, employee_id"

    company_id = fields.Many2one(
        "res.company",
        required=True,
        default=lambda self: self.env.company,
    )
    period_date = fields.Date(
        string="Mois",
        required=True,
        default=lambda self: fields.Date.context_today(self).replace(day=1),
        help="Premier jour du mois concerné.",
    )
    employee_id = fields.Many2one(
        "hr.employee",
        string="Salarié",
        required=True,
        check_company=True,
    )
    employee_cost_line_id = fields.Many2one(
        "glc.employee.cost.line",
        string="Coût mensuel de référence",
        check_company=True,
        domain="[('employee_id', '=', employee_id), ('period_date', '=', period_date), ('company_id', '=', company_id)]",
    )
    cost_amount = fields.Monetary(
        related="employee_cost_line_id.cost_amount",
        store=True,
        currency_field="currency_id",
    )
    currency_id = fields.Many2one(
        "res.currency",
        compute="_compute_currency_id",
        store=True,
    )
    method = fields.Selection(
        selection=[
            ("percent", "Pourcentage"),
            ("hours", "Heures"),
        ],
        required=True,
        default="percent",
    )
    line_ids = fields.One2many(
        "glc.salary.allocation.line",
        "allocation_id",
        string="Lignes de ventilation",
    )
    total_percent = fields.Float(
        compute="_compute_totals",
        store=True,
        digits=(16, 2),
    )
    total_hours = fields.Float(
        compute="_compute_totals",
        store=True,
        digits=(16, 2),
    )
    allocated_amount = fields.Monetary(
        string="Montant ventilé",
        compute="_compute_totals",
        store=True,
        currency_field="currency_id",
    )
    state = fields.Selection(
        selection=[
            ("draft", "Brouillon"),
            ("to_check", "À contrôler"),
            ("validated", "Validé"),
            ("locked", "Verrouillé"),
        ],
        default="draft",
        required=True,
    )
    validated_by = fields.Many2one("res.users", readonly=True)
    validated_date = fields.Datetime(readonly=True)
    note = fields.Text()

    accounting_payroll_mass = fields.Monetary(
        string="Masse salariale comptable",
        compute="_compute_payroll_variance",
        currency_field="currency_id",
    )
    validated_allocated_total = fields.Monetary(
        string="Total ventilé validé (mois)",
        compute="_compute_payroll_variance",
        currency_field="currency_id",
    )
    payroll_variance_pct = fields.Float(
        string="Écart masse salariale (%)",
        compute="_compute_payroll_variance",
        digits=(16, 2),
    )
    payroll_variance_alert = fields.Boolean(
        compute="_compute_payroll_variance",
    )
    payroll_variance_message = fields.Char(
        compute="_compute_payroll_variance",
    )

    _glc_salary_allocation_uniq = models.Constraint(
        "unique(company_id, employee_id, period_date)",
        "Une seule ventilation par salarié et par mois.",
    )

    @api.depends("employee_cost_line_id.currency_id", "company_id")
    def _compute_currency_id(self):
        for allocation in self:
            allocation.currency_id = (
                allocation.employee_cost_line_id.currency_id
                or allocation.company_id.currency_id
            )

    @api.depends("line_ids.percent", "line_ids.hours", "line_ids.amount")
    def _compute_totals(self):
        for allocation in self:
            allocation.total_percent = sum(allocation.line_ids.mapped("percent"))
            allocation.total_hours = sum(allocation.line_ids.mapped("hours"))
            allocation.allocated_amount = sum(allocation.line_ids.mapped("amount"))

    @api.depends("company_id", "period_date", "currency_id")
    def _compute_payroll_variance(self):
        icp = self.env["ir.config_parameter"].sudo()
        threshold = float(
            icp.get_param("dorevia_glc_analytique.salary_allocation_variance_pct", "5")
        )
        for allocation in self:
            if not allocation.period_date or not allocation.company_id:
                allocation.accounting_payroll_mass = 0.0
                allocation.validated_allocated_total = 0.0
                allocation.payroll_variance_pct = 0.0
                allocation.payroll_variance_alert = False
                allocation.payroll_variance_message = False
                continue

            mass = allocation._get_accounting_payroll_mass(
                allocation.company_id, allocation.period_date
            )
            validated_total = allocation._get_validated_allocated_total(
                allocation.company_id, allocation.period_date
            )
            variance_pct = (
                abs(mass - validated_total) / mass * 100.0 if mass else 0.0
            )
            alert = bool(mass) and variance_pct >= threshold
            allocation.accounting_payroll_mass = mass
            allocation.validated_allocated_total = validated_total
            allocation.payroll_variance_pct = variance_pct
            allocation.payroll_variance_alert = alert
            allocation.payroll_variance_message = (
                _("Écart masse salariale élevé — contrôle informatif")
                if alert
                else False
            )

    @api.onchange("employee_id", "period_date", "company_id")
    def _onchange_employee_period(self):
        if not self.employee_id or not self.period_date:
            self.employee_cost_line_id = False
            return
        self.employee_cost_line_id = self.env["glc.employee.cost.line"].search(
            [
                ("employee_id", "=", self.employee_id.id),
                ("period_date", "=", self._normalize_period_date(self.period_date)),
                ("company_id", "=", self.company_id.id),
            ],
            limit=1,
        )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get("period_date"):
                vals["period_date"] = self._normalize_period_date(vals["period_date"])
        records = super().create(vals_list)
        records._sync_employee_cost_line()
        return records

    def write(self, vals):
        protected_fields = {
            "employee_id",
            "period_date",
            "method",
            "line_ids",
            "employee_cost_line_id",
            "company_id",
        }
        for allocation in self:
            if allocation.state in ("validated", "locked") and protected_fields & set(vals):
                raise UserError(_("Impossible de modifier une ventilation validée ou verrouillée."))
        if vals.get("period_date"):
            vals["period_date"] = self._normalize_period_date(vals["period_date"])
        res = super().write(vals)
        if {"employee_id", "period_date", "company_id"} & set(vals):
            self._sync_employee_cost_line()
        return res

    def _sync_employee_cost_line(self):
        CostLine = self.env["glc.employee.cost.line"]
        for allocation in self:
            if allocation.employee_cost_line_id:
                continue
            cost_line = CostLine.search(
                [
                    ("employee_id", "=", allocation.employee_id.id),
                    ("period_date", "=", allocation.period_date),
                    ("company_id", "=", allocation.company_id.id),
                ],
                limit=1,
            )
            if cost_line:
                allocation.employee_cost_line_id = cost_line

    @api.model
    def _normalize_period_date(self, period_date):
        if not period_date:
            return period_date
        date_value = fields.Date.to_date(period_date)
        return date_value.replace(day=1)

    @api.constrains("period_date")
    def _check_period_first_day(self):
        for allocation in self:
            if allocation.period_date and allocation.period_date.day != 1:
                raise ValidationError(_("La date de période doit être le premier jour du mois."))

    @api.constrains("employee_cost_line_id", "employee_id", "period_date", "company_id")
    def _check_employee_cost_line(self):
        for allocation in self:
            cost_line = allocation.employee_cost_line_id
            if not cost_line:
                continue
            if (
                cost_line.employee_id != allocation.employee_id
                or cost_line.period_date != allocation.period_date
                or cost_line.company_id != allocation.company_id
            ):
                raise ValidationError(
                    _("Le coût mensuel doit correspondre au salarié, à la société et au mois.")
                )

    def _check_validation_totals(self):
        self.ensure_one()
        if not self.employee_cost_line_id:
            raise UserError(_("Un coût mensuel chargé est requis pour valider la ventilation."))
        if not self.line_ids:
            raise UserError(_("Ajoutez au moins une ligne de ventilation."))

        if self.method == "percent":
            if not self._glc_floats_equal(self.total_percent, 100.0, GLC_PERCENT_TOLERANCE):
                raise UserError(
                    _(
                        "Validation refusée : le total des pourcentages doit être 100 %% "
                        "(actuel : %(total).2f %%).",
                        total=self.total_percent,
                    )
                )
        elif self.method == "hours":
            cost_line = self.employee_cost_line_id
            cost_line._check_reference_hours_for_hours_method()
            if not self._glc_floats_equal(
                self.total_hours, cost_line.reference_hours, GLC_PERCENT_TOLERANCE
            ):
                raise UserError(
                    _(
                        "Validation refusée : le total des heures doit être égal "
                        "aux heures de référence (%(expected).2f h, actuel : %(total).2f h).",
                        expected=cost_line.reference_hours,
                        total=self.total_hours,
                    )
                )

    def action_submit_to_check(self):
        for allocation in self:
            if allocation.state != "draft":
                raise UserError(_("Seules les ventilations en brouillon peuvent être soumises."))
            allocation.state = "to_check"

    def action_validate(self):
        move_count_before = self.env["account.move"].search_count([])
        for allocation in self:
            if allocation.state not in ("draft", "to_check"):
                raise UserError(_("Seules les ventilations en brouillon ou à contrôler peuvent être validées."))
            allocation._check_validation_totals()
            allocation.write(
                {
                    "state": "validated",
                    "validated_by": self.env.user.id,
                    "validated_date": fields.Datetime.now(),
                }
            )
        move_count_after = self.env["account.move"].search_count([])
        if move_count_after != move_count_before:
            raise UserError(_("Aucune écriture comptable ne doit être générée à la validation."))

    def action_lock(self):
        for allocation in self:
            if allocation.state != "validated":
                raise UserError(_("Seules les ventilations validées peuvent être verrouillées."))
            allocation.state = "locked"

    def action_reset_to_draft(self):
        for allocation in self:
            if allocation.state == "locked":
                raise UserError(_("Une ventilation verrouillée ne peut pas être remise en brouillon."))
            allocation.write(
                {
                    "state": "draft",
                    "validated_by": False,
                    "validated_date": False,
                }
            )

    @api.model
    def _get_accounting_payroll_mass(self, company, period_date):
        date_from = fields.Date.to_date(period_date)
        date_to = date(date_from.year, date_from.month, monthrange(date_from.year, date_from.month)[1])
        accounts = self.env["account.account"].search(
            [
                ("company_ids", "in", company.id),
                "|",
                "|",
                "|",
                ("code", "=like", "631%"),
                ("code", "=like", "633%"),
                ("code", "=like", "641%"),
                ("code", "=like", "645%"),
            ]
        )
        if not accounts:
            return 0.0
        lines = self.env["account.move.line"].search(
            [
                ("company_id", "=", company.id),
                ("account_id", "in", accounts.ids),
                ("move_id.state", "=", "posted"),
                ("date", ">=", date_from),
                ("date", "<=", date_to),
                ("display_type", "not in", ("line_section", "line_note")),
            ]
        )
        return sum(abs(line.balance) for line in lines)

    @api.model
    def _get_validated_allocated_total(self, company, period_date):
        allocations = self.search(
            [
                ("company_id", "=", company.id),
                ("period_date", "=", period_date),
                ("state", "in", ("validated", "locked")),
            ]
        )
        return sum(allocations.mapped("allocated_amount"))
